from __future__ import annotations

import re
from .models import SqlAnalysis

_IDENTIFIER = r'(?:"[^"]+"|[A-Za-z][A-Za-z0-9_$#]*)(?:\.(?:"[^"]+"|[A-Za-z][A-Za-z0-9_$#]*))?'

def normalize_identifier(name: str) -> str:
    parts = name.strip().split(".")
    return ".".join(p if (p.startswith('"') and p.endswith('"')) else p.upper() for p in parts)

def _mask_literals_and_comments(sql: str) -> str:
    out: list[str] = []
    i = 0
    n = len(sql)
    state = "code"
    while i < n:
        ch = sql[i]
        nxt = sql[i + 1] if i + 1 < n else ""
        if state == "code":
            if ch == "'":
                state = "string"
                out.append(" ")
            elif ch == "-" and nxt == "-":
                state = "line_comment"
                out.extend((" ", " "))
                i += 1
            elif ch == "/" and nxt == "*":
                state = "block_comment"
                out.extend((" ", " "))
                i += 1
            else:
                out.append(ch)
        elif state == "string":
            if ch == "'" and nxt == "'":
                out.extend((" ", " "))
                i += 1
            elif ch == "'":
                state = "code"
                out.append(" ")
            else:
                out.append(" ")
        elif state == "line_comment":
            if ch == "\n":
                state = "code"
                out.append("\n")
            else:
                out.append(" ")
        else:
            if ch == "*" and nxt == "/":
                state = "code"
                out.extend((" ", " "))
                i += 1
            else:
                out.append("\n" if ch == "\n" else " ")
        i += 1
    return "".join(out)

def split_statements(sql: str) -> list[str]:
    statements: list[str] = []
    buf: list[str] = []
    i = 0
    in_string = False
    while i < len(sql):
        ch = sql[i]
        if ch == "'":
            if in_string and i + 1 < len(sql) and sql[i + 1] == "'":
                buf.extend(("'", "'"))
                i += 2
                continue
            in_string = not in_string
            buf.append(ch)
        elif ch == ";" and not in_string:
            text = "".join(buf).strip()
            if text:
                statements.append(text)
            buf = []
        else:
            buf.append(ch)
        i += 1
    tail = "".join(buf).strip()
    if tail:
        statements.append(tail)
    return statements

def _unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def analyze_sql(sql: str) -> SqlAnalysis:
    statements = split_statements(sql)
    operations: list[str] = []
    reads: list[str] = []
    writes: list[str] = []

    for raw in statements:
        text = _mask_literals_and_comments(raw)
        upper = text.lstrip().upper()
        op = "UNKNOWN"
        for candidate in ("SELECT", "INSERT", "UPDATE", "DELETE", "MERGE", "CREATE", "ALTER", "DROP", "TRUNCATE"):
            if upper.startswith(candidate):
                op = candidate
                break
        operations.append(op)

        for pattern in (
            rf'\bFROM\s+({_IDENTIFIER})',
            rf'\bJOIN\s+({_IDENTIFIER})',
            rf'\bUSING\s+({_IDENTIFIER})',
        ):
            reads.extend(normalize_identifier(m.group(1)) for m in re.finditer(pattern, text, re.IGNORECASE))

        for pattern in (
            rf'\bINSERT\s+INTO\s+({_IDENTIFIER})',
            rf'\bUPDATE\s+({_IDENTIFIER})',
            rf'\bDELETE\s+FROM\s+({_IDENTIFIER})',
            rf'\bMERGE\s+INTO\s+({_IDENTIFIER})',
            rf'\bTRUNCATE\s+TABLE\s+({_IDENTIFIER})',
        ):
            writes.extend(normalize_identifier(m.group(1)) for m in re.finditer(pattern, text, re.IGNORECASE))

    reads = _unique(reads)
    writes = _unique(writes)
    return SqlAnalysis(
        operations=operations,
        read_objects=reads,
        write_objects=writes,
        all_objects=_unique(reads + writes),
        statement_count=len(statements),
    )

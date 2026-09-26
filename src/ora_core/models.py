from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SqlAnalysis:
    operations: list[str]
    read_objects: list[str]
    write_objects: list[str]
    all_objects: list[str]
    statement_count: int

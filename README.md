# ora-core

Shared parsing and static-analysis primitives for the **Oracle Dev Tools** family.

> **Oracle compatibility**
>
> | Oracle version | Support |
> |---|---|
> | Oracle Database 19c | ✅ Supported for static SQL analysis |
> | Oracle Database 23ai | ✅ Supported for static SQL analysis |
> | Oracle AI Database 26ai | ✅ Supported for static SQL analysis |
>
> `ora-core` performs **offline static analysis** and does not connect to Oracle. Features that depend on database-specific runtime metadata must be implemented by downstream tools and documented separately.

## Why this project exists

Several small developer tools need the same foundations: comment/literal stripping, statement splitting, object reference extraction, identifier normalization and lightweight Oracle-aware token analysis. `ora-core` centralizes that logic so the companion repositories stay small and focused.

## Features

- Oracle-oriented SQL statement splitting
- Safe removal of comments and string literals for structural inspection
- Table/view reference extraction from common `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `MERGE` patterns
- Basic operation classification
- Identifier normalization while preserving quoted identifiers
- Zero runtime dependencies
- Python API designed to be reused by `ora-impact`, `ora-lineage`, `ora-lint` and later tools

## Installation

### From GitHub

```bash
python -m pip install "git+https://github.com/raoulmunet/ora-core.git"
```

### Local development

```bash
git clone https://github.com/raoulmunet/ora-core.git
cd ora-core
python -m pip install -e ".[dev]"
pytest
```

## Quick usage

```python
from ora_core import analyze_sql

sql = """
INSERT INTO dwh.customer_dim (customer_id, customer_name)
SELECT c.customer_id, c.customer_name
FROM crm.customers c
JOIN crm.customer_status s
  ON s.customer_id = c.customer_id
WHERE s.active_flag = 'Y';
"""

result = analyze_sql(sql)

print(result.operations)
print(result.read_objects)
print(result.write_objects)
```

Expected output:

```text
['INSERT']
['CRM.CUSTOMERS', 'CRM.CUSTOMER_STATUS']
['DWH.CUSTOMER_DIM']
```

## API

### `analyze_sql(sql: str) -> SqlAnalysis`

Returns a structured summary:

- `operations`
- `read_objects`
- `write_objects`
- `all_objects`
- `statement_count`

### `split_statements(sql: str) -> list[str]`

Splits a SQL script while avoiding semicolons inside string literals.

### `normalize_identifier(name: str) -> str`

Normalizes ordinary Oracle identifiers to upper case while preserving quoted identifiers.

## Scope and limitations

This is deliberately a lightweight static-analysis core, not a full Oracle SQL/PLSQL parser.

Current limitations include:

- dynamic SQL cannot be resolved without executing/interpreting the program;
- object names assembled through concatenation are not inferred;
- PL/SQL package-body semantic analysis is intentionally deferred;
- synonyms and editioning views require database metadata and therefore cannot be resolved offline;
- SQL macros and version-specific syntax may be tokenized but are not semantically expanded.

Downstream tools must surface these limitations rather than silently guessing.

## Example projects using ora-core

- [ora-impact](https://github.com/raoulmunet/ora-impact) — SQL impact analysis
- `ora-lineage` — column/table lineage
- `ora-lint` — SQL anti-pattern detection
- `ora-doc` — DDL-to-documentation generation

## Design principles

1. **Static first** — useful without database credentials.
2. **Explain uncertainty** — unresolved references are preferable to invented certainty.
3. **Version clarity** — Oracle 19c, 23ai and 26ai differences must be called out explicitly.
4. **Small API surface** — companion tools should be able to depend on the core without pulling a large framework.

## License

MIT. See [LICENSE](LICENSE).

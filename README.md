# ora-core

[![tests](https://github.com/raoulmunet/ora-core/actions/workflows/tests.yml/badge.svg)](https://github.com/raoulmunet/ora-core/actions/workflows/tests.yml) ![Python](https://img.shields.io/badge/Python-3.10--3.13-blue) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

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

## Install the complete suite locally

A single cross-platform installer is available for Windows, Linux and macOS:

```bash
python install_all.py
```

It creates an isolated environment, installs the full Oracle Dev Tools suite plus the two general companion tools, creates CLI launchers, and can optionally add them to the user's PATH.

See [INSTALL-ALL.md](INSTALL-ALL.md) for Windows/Linux/macOS instructions, verification, update and uninstall commands.

## Browser playground

All Oracle Dev Tools can be opened in the browser from the GitHub Pages hub. The shared playground runs locally in the browser and exposes a direct URL per tool, for example:

- `https://raoulmunet.github.io/ora-core/playground.html?tool=ora-impact`
- `https://raoulmunet.github.io/ora-core/playground.html?tool=ora-lint`
- `https://raoulmunet.github.io/ora-core/playground.html?tool=ora-sql-diff`

The Python CLI remains the reference implementation for each repository.

## Oracle Dev Tools landing page

The suite has a single visual landing page in [`docs/index.html`](docs/index.html), intended to be published with GitHub Pages from the `main` branch and `/docs` folder.

Expected public URL after Pages is enabled:

`https://raoulmunet.github.io/ora-core/`

## Oracle Dev Tools family

This repository is part of the **Oracle Dev Tools** suite: small, composable developer utilities designed around Oracle Database 19c, 23ai and 26ai.

| Area | Tools |
|---|---|
| Foundation | [ora-core](https://github.com/raoulmunet/ora-core) |
| SQL analysis | [ora-impact](https://github.com/raoulmunet/ora-impact) · [ora-plan](https://github.com/raoulmunet/ora-plan) · [ora-lineage](https://github.com/raoulmunet/ora-lineage) · [ora-lint](https://github.com/raoulmunet/ora-lint) · [ora-sql-diff](https://github.com/raoulmunet/ora-sql-diff) · [ora-sql-complexity](https://github.com/raoulmunet/ora-sql-complexity) · [ora-join-viz](https://github.com/raoulmunet/ora-join-viz) · [ora-bind](https://github.com/raoulmunet/ora-bind) |
| Data & operations | [ora-doc](https://github.com/raoulmunet/ora-doc) · [ora-data-quality](https://github.com/raoulmunet/ora-data-quality) · [ora-csv-loader](https://github.com/raoulmunet/ora-csv-loader) · [ora-etl-log](https://github.com/raoulmunet/ora-etl-log) · [ora-migration-check](https://github.com/raoulmunet/ora-migration-check) · [ora-errors](https://github.com/raoulmunet/ora-errors) · [ora-schema-explorer](https://github.com/raoulmunet/ora-schema-explorer) |
| PL/SQL analysis | [ora-exception-flow](https://github.com/raoulmunet/ora-exception-flow) · [ora-call-graph](https://github.com/raoulmunet/ora-call-graph) · [ora-dead-code](https://github.com/raoulmunet/ora-dead-code) |

## License

MIT. See [LICENSE](LICENSE).

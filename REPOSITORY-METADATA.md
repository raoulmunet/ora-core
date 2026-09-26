# Repository metadata guide

The GitHub connector used to maintain this suite can update repository files but does not expose write access for native repository **Description**, **Topics** or **Pages settings**. The values below are the canonical metadata to use in GitHub.

## Oracle Dev Tools

| Repository | Suggested GitHub description | Suggested topics |
|---|---|---|
| ora-core | Shared Oracle SQL static-analysis primitives for the Oracle Dev Tools family. | oracle, sql, static-analysis, parser, python |
| ora-impact | Static Oracle SQL impact analysis for read/write object dependencies. | oracle, sql, impact-analysis, dependency-analysis, python |
| ora-plan | Explain Oracle DBMS_XPLAN execution plans in plain language. | oracle, sql, execution-plan, dbms-xplan, performance, python |
| ora-lineage | Lightweight Oracle SQL table and column lineage analysis. | oracle, sql, data-lineage, etl, data-engineering, python |
| ora-lint | High-signal static checks for Oracle SQL and PL/SQL anti-patterns. | oracle, sql, plsql, linter, static-analysis, python |
| ora-doc | Generate Markdown and Mermaid documentation from common Oracle DDL. | oracle, ddl, documentation, schema, mermaid, python |
| ora-bind | Convert common Oracle SQL literals into bind variables. | oracle, sql, bind-variables, performance, python |
| ora-exception-flow | Visualize Oracle PL/SQL exception handlers and propagation paths. | oracle, plsql, exceptions, visualization, static-analysis, python |
| ora-join-viz | Visualize common Oracle ANSI JOIN relationships. | oracle, sql, joins, visualization, mermaid, python |
| ora-sql-diff | Structural diff for Oracle SQL beyond whitespace and formatting. | oracle, sql, diff, code-review, static-analysis, python |
| ora-errors | Offline explainer for common Oracle ORA errors. | oracle, ora-errors, troubleshooting, database, python |
| ora-etl-log | Analyze timestamped ETL and batch logs with Oracle error extraction. | oracle, etl, batch-processing, logs, data-engineering, python |
| ora-data-quality | Generate reviewable Oracle data-quality checks from table DDL. | oracle, data-quality, ddl, sql, data-engineering, python |
| ora-csv-loader | Generate Oracle starter DDL and SQL*Loader control files from CSV. | oracle, csv, sql-loader, data-loading, etl, python |
| ora-migration-check | Flag Oracle SQL constructs that need attention during migration. | oracle, sql, migration, postgresql, sql-server, python |
| ora-sql-complexity | Transparent structural complexity metrics for Oracle SQL. | oracle, sql, complexity, code-review, static-analysis, python |
| ora-call-graph | Generate lightweight Oracle PL/SQL procedure and package call graphs. | oracle, plsql, call-graph, static-analysis, visualization, python |
| ora-dead-code | Find conservative dead-code candidates in Oracle PL/SQL. | oracle, plsql, dead-code, static-analysis, code-quality, python |
| ora-schema-explorer | Build an offline Oracle schema overview from DDL and SQL source files. | oracle, schema, ddl, dependency-graph, documentation, python |

## General developer tools

| Repository | Suggested GitHub description | Suggested topics |
|---|---|---|
| repo-readme-architect | Generate accurate README starters from repository structure. | github, readme, documentation, developer-tools, automation, python |
| github-portfolio-generator | Generate factual Markdown developer portfolios from public GitHub metadata. | github, portfolio, markdown, developer-tools, automation, python |

## GitHub Pages candidates

The following repositories already contain a ready-to-publish `docs/index.html` and `docs/.nojekyll`:

- `ora-impact`
- `ora-plan`
- `ora-lineage`
- `ora-join-viz`
- `ora-schema-explorer`

For each repository, open **Settings → Pages**, choose **Deploy from a branch**, select **main** and **/docs**, then save.

## Suite conventions

All Oracle-focused repositories should keep:

- the Oracle 19c / 23ai / 26ai compatibility section near the top of the README;
- a GitHub Actions test badge;
- Python 3.10–3.13 support badge;
- MIT license badge;
- an **Oracle Dev Tools family** navigation section;
- explicit limitations for offline/static analysis;
- examples that can be run without guessing undocumented setup.

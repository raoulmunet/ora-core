# Install all Oracle Dev Tools locally

The suite includes a single cross-platform installer:

```text
install_all.py
```

It supports:

- Windows 10/11
- Linux
- macOS
- Python 3.10 or newer

No Git installation is required. Packages are downloaded from GitHub as ZIP archives and installed into an isolated virtual environment.

## Quick start

Download `install_all.py` from this repository, then run:

### Windows

```powershell
py install_all.py
```

If `py` is unavailable:

```powershell
python install_all.py
```

### Linux

```bash
python3 install_all.py
```

### macOS

```bash
python3 install_all.py
```

By default, the installer uses:

```text
~/.oracle-dev-tools/
```

and creates:

```text
~/.oracle-dev-tools/
├── venv/
└── bin/
```

The `bin` directory contains launchers for every command-line tool.

## Add the tools to PATH

Interactive installation asks whether the launcher directory should be added to the user's PATH.

For unattended installation:

```bash
python3 install_all.py --yes --add-to-path
```

On Windows:

```powershell
py install_all.py --yes --add-to-path
```

After PATH is updated, open a new terminal.

You can then run commands such as:

```bash
ora-impact query.sql
ora-errors ORA-01722
ora-plan plan.txt
ora-lint package.sql
ora-schema-explorer ./schema
```

## Verify installation

```bash
python3 install_all.py --check
```

or on Windows:

```powershell
py install_all.py --check
```

The check verifies all CLI entry points and runs `pip check`.

## Update the entire suite

Run the installer again:

```bash
python3 install_all.py --yes
```

The packages are reinstalled from each repository's current `main` branch.

## Uninstall

```bash
python3 install_all.py --uninstall
```

For unattended removal:

```bash
python3 install_all.py --uninstall --yes
```

The installer removes the dedicated environment and any PATH entry it created.

## Included tools

Oracle-focused tools:

- ora-core
- ora-impact
- ora-plan
- ora-lineage
- ora-lint
- ora-doc
- ora-bind
- ora-exception-flow
- ora-join-viz
- ora-sql-diff
- ora-errors
- ora-etl-log
- ora-data-quality
- ora-csv-loader
- ora-migration-check
- ora-sql-complexity
- ora-call-graph
- ora-dead-code
- ora-schema-explorer

General companion tools:

- repo-readme-architect
- github-portfolio-generator

## Why an isolated environment?

Installing the suite into `~/.oracle-dev-tools/venv` avoids modifying the operating system Python installation and works cleanly on modern Linux distributions that enforce externally-managed Python environments.

# Install all Oracle Dev Tools locally

The suite includes one cross-platform installer:

```text
install_all.py
```

It supports Windows, Linux and macOS and installs both:

- all command-line tools;
- a local browser UI for all Oracle Dev Tools.

Python 3.10 or newer is required.

No Git installation is required. Packages are downloaded from GitHub as ZIP archives.

## Quick start

### Windows

```powershell
py install_all.py
```

If `py` is unavailable:

```powershell
python install_all.py
```

### Linux / macOS

```bash
python3 install_all.py
```

The installer creates an isolated environment under:

```text
~/.oracle-dev-tools/
├── venv/
├── bin/
├── web/
├── config.json
└── serve_web.py
```

## Local browser port

During interactive installation, the installer displays a short list of allowed ports and marks which ones are available.

Current choices:

```text
8000
8080
8888
9000
9090
9876
5000
5500
7000
7777
8765
9999
```

The default is `8765` when available.

You can also choose the port non-interactively:

```bash
python3 install_all.py --yes --port 8080
```

Windows:

```powershell
py install_all.py --yes --port 8080
```

If the selected port is already in use, installation stops with a clear error instead of silently choosing another address.

## Run the tools in your local browser

After installation, start the local web UI with:

### Linux / macOS

```bash
oracle-dev-tools-web
```

### Windows

```powershell
oracle-dev-tools-web
```

If the installer directory was not added to PATH, the final installation message prints the full launcher path.

The command:

1. starts a local HTTP server bound only to `127.0.0.1`;
2. opens your default browser automatically;
3. serves the complete Oracle Dev Tools landing page and browser playground.

For the default port, the address is:

```text
http://127.0.0.1:8765/
```

For example, if you choose port `8080`:

```text
http://127.0.0.1:8080/
```

Stop the local server with:

```text
Ctrl+C
```

The server is bound to localhost only; it is not exposed to other machines on your network.

## Install and start immediately

You can ask the installer to launch the browser UI immediately after installation:

```bash
python3 install_all.py --yes --port 8765 --start-web
```

On Windows:

```powershell
py install_all.py --yes --port 8765 --start-web
```

Note: `--start-web` keeps the terminal occupied while the local server is running. Use `Ctrl+C` to stop it.

## Add all commands to PATH

Interactive installation asks whether the launcher directory should be added to the user's PATH.

For unattended installation:

```bash
python3 install_all.py --yes --add-to-path --port 8765
```

After PATH is updated, open a new terminal.

## CLI usage

The command-line tools remain available independently of the browser UI:

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

Windows:

```powershell
py install_all.py --check
```

The check verifies:

- all CLI entry points;
- Python package dependencies with `pip check`;
- local browser files;
- local web server launcher;
- configured local browser URL.

## Update the complete suite

Run the installer again:

```bash
python3 install_all.py --yes
```

It reinstalls the current `main` version of each repository and refreshes the local browser UI.

To keep a specific configured port:

```bash
python3 install_all.py --yes --port 8080
```

## Uninstall

```bash
python3 install_all.py --uninstall
```

For unattended removal:

```bash
python3 install_all.py --uninstall --yes
```

The installer removes the isolated environment, local browser UI and any PATH entry it created.

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

Installing into `~/.oracle-dev-tools/venv` avoids changing the operating system Python installation and works cleanly with modern Linux distributions that enforce externally managed Python environments.

#!/usr/bin/env python3
"""
Oracle Dev Tools - cross-platform installer.

Installs the complete Raoul Munet Oracle Dev Tools suite into an isolated
virtual environment on Windows, Linux, or macOS.

Python 3.10+ is required to run the installed tools.
"""

import argparse
import os
import platform
import shutil
import socket
import subprocess
import sys
import json
import urllib.request
from pathlib import Path

MIN_PYTHON = (3, 10)
DEFAULT_ROOT = Path.home() / ".oracle-dev-tools"
DEFAULT_PORT = 8765
PORT_CHOICES = [8000, 8080, 8888, 9000, 9090, 9876, 5000, 5500, 7000, 7777, 8765, 9999]
WEB_FILES = ["index.html", "playground.html", "playground.js", ".nojekyll"]

# Install dependency providers first. Direct GitHub ZIP URLs avoid requiring git.
REPOSITORIES = [
    "ora-core",
    "ora-doc",
    "ora-impact",
    "ora-plan",
    "ora-lineage",
    "ora-lint",
    "ora-bind",
    "ora-exception-flow",
    "ora-join-viz",
    "ora-sql-diff",
    "ora-errors",
    "ora-etl-log",
    "ora-data-quality",
    "ora-csv-loader",
    "ora-migration-check",
    "ora-sql-complexity",
    "ora-call-graph",
    "ora-dead-code",
    "ora-schema-explorer",
    "repo-readme-architect",
    "github-portfolio-generator",
]

CLI_TOOLS = [
    "ora-impact",
    "ora-plan",
    "ora-lineage",
    "ora-lint",
    "ora-doc",
    "ora-bind",
    "ora-exception-flow",
    "ora-join-viz",
    "ora-sql-diff",
    "ora-errors",
    "ora-etl-log",
    "ora-data-quality",
    "ora-csv-loader",
    "ora-migration-check",
    "ora-sql-complexity",
    "ora-call-graph",
    "ora-dead-code",
    "ora-schema-explorer",
    "repo-readme-architect",
    "github-portfolio-generator",
]

OWNER = "raoulmunet"


def die(message, code=1):
    print("ERROR:", message, file=sys.stderr)
    raise SystemExit(code)


def check_python():
    if sys.version_info < MIN_PYTHON:
        die(
            "Python 3.10 or newer is required. "
            "Current interpreter: {}.{}.{}".format(*sys.version_info[:3])
        )


def venv_python(root):
    if os.name == "nt":
        return root / "venv" / "Scripts" / "python.exe"
    return root / "venv" / "bin" / "python"


def venv_scripts(root):
    if os.name == "nt":
        return root / "venv" / "Scripts"
    return root / "venv" / "bin"


def launcher_dir(root):
    return root / "bin"


def web_root(root):
    return root / "web"


def config_path(root):
    return root / "config.json"


def port_is_available(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("127.0.0.1", port))
        return True
    except OSError:
        return False
    finally:
        sock.close()


def choose_port(requested=None, interactive=True):
    if requested is not None:
        if requested not in PORT_CHOICES:
            die(
                "Port {} is not in the allowed list: {}".format(
                    requested, ", ".join(str(x) for x in PORT_CHOICES)
                )
            )
        if not port_is_available(requested):
            die("Port {} is already in use.".format(requested))
        return requested

    available = [p for p in PORT_CHOICES if port_is_available(p)]
    if not available:
        die("None of the configured local web ports are currently available.")

    preferred = DEFAULT_PORT if DEFAULT_PORT in available else available[0]
    if not interactive:
        return preferred

    print("\nChoose the local browser port:")
    for i, port in enumerate(PORT_CHOICES, 1):
        status = "available" if port in available else "in use"
        default = " [default]" if port == preferred else ""
        print("  {:>2}. {:>5}  {}{}".format(i, port, status, default))

    while True:
        answer = input("Port number or list index [{}]: ".format(preferred)).strip()
        if not answer:
            return preferred
        try:
            value = int(answer)
        except ValueError:
            print("Please enter a port number or list index.")
            continue

        candidate = PORT_CHOICES[value - 1] if 1 <= value <= len(PORT_CHOICES) else value
        if candidate not in PORT_CHOICES:
            print("Choose one of: {}".format(", ".join(str(x) for x in PORT_CHOICES)))
            continue
        if candidate not in available:
            print("Port {} is already in use.".format(candidate))
            continue
        return candidate


def run(cmd, env=None):
    print("+", " ".join(str(x) for x in cmd))
    subprocess.run([str(x) for x in cmd], check=True, env=env)


def archive_url(repo):
    return "https://github.com/{}/{}/archive/refs/heads/main.zip".format(OWNER, repo)


def create_venv(root):
    py = venv_python(root)
    if py.exists():
        return
    print("Creating virtual environment:", root / "venv")
    run([sys.executable, "-m", "venv", str(root / "venv")])


def upgrade_packaging(root):
    py = venv_python(root)
    run([py, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])


def install_suite(root):
    py = venv_python(root)
    for repo in REPOSITORIES:
        print("\nInstalling", repo)
        # All runtime dependencies inside this suite are installed explicitly
        # in dependency order. --no-deps prevents pip from following the
        # pyproject git+ URLs, so Git itself is not required.
        run([
            py, "-m", "pip", "install",
            "--upgrade",
            "--no-deps",
            archive_url(repo),
        ])
    print("\nChecking installed package dependencies...")
    run([py, "-m", "pip", "check"])


def install_web_ui(root, port):
    target = web_root(root)
    target.mkdir(parents=True, exist_ok=True)
    base = "https://raw.githubusercontent.com/{}/ora-core/main/docs".format(OWNER)

    for name in WEB_FILES:
        url = base + "/" + name
        destination = target / name
        print("Downloading web UI:", url)
        try:
            urllib.request.urlretrieve(url, destination)
        except Exception as exc:
            die("Could not download {}: {}".format(url, exc))

    config_path(root).write_text(
        json.dumps(
            {
                "host": "127.0.0.1",
                "port": port,
                "url": "http://127.0.0.1:{}/".format(port),
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def write_web_server(root):
    server = root / "serve_web.py"
    server.write_text(
        """#!/usr/bin/env python3
import argparse
import http.server
import json
import os
import socketserver
import threading
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "config.json"
WEB = ROOT / "web"

def main():
    parser = argparse.ArgumentParser(description="Run Oracle Dev Tools in a local browser.")
    parser.add_argument("--port", type=int, help="Override configured port for this run.")
    parser.add_argument("--no-browser", action="store_true", help="Do not open the default browser.")
    args = parser.parse_args()

    cfg = json.loads(CONFIG.read_text(encoding="utf-8")) if CONFIG.exists() else {}
    port = args.port or int(cfg.get("port", 8765))
    host = "127.0.0.1"
    url = "http://{}:{}/".format(host, port)

    if not WEB.exists():
        raise SystemExit("Web UI directory not found: {}".format(WEB))

    os.chdir(WEB)

    class Server(socketserver.TCPServer):
        allow_reuse_address = True

    try:
        with Server((host, port), http.server.SimpleHTTPRequestHandler) as httpd:
            print("Oracle Dev Tools local web UI")
            print("Address: {}".format(url))
            print("Press Ctrl+C to stop.")
            if not args.no_browser:
                threading.Thread(
                    target=lambda: (time.sleep(0.6), webbrowser.open(url)),
                    daemon=True,
                ).start()
            httpd.serve_forever()
    except OSError as exc:
        raise SystemExit(
            "Cannot start local web server on port {}: {}".format(port, exc)
        )
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()
""",
        encoding="utf-8",
    )
    if os.name != "nt":
        server.chmod(0o755)


def write_launchers(root):
    target = launcher_dir(root)
    target.mkdir(parents=True, exist_ok=True)
    scripts = venv_scripts(root)

    for name in CLI_TOOLS:
        if os.name == "nt":
            source = scripts / (name + ".exe")
            wrapper = target / (name + ".cmd")
            wrapper.write_text(
                '@echo off\r\n"{}" %*\r\n'.format(source),
                encoding="utf-8",
            )
        else:
            source = scripts / name
            wrapper = target / name
            wrapper.write_text(
                '#!/bin/sh\nexec "{}" "$@"\n'.format(source),
                encoding="utf-8",
            )
            wrapper.chmod(0o755)

    if os.name == "nt":
        web_launcher = target / "oracle-dev-tools-web.cmd"
        web_launcher.write_text(
            '@echo off\r\n"{}" "{}" %*\r\n'.format(
                venv_python(root), root / "serve_web.py"
            ),
            encoding="utf-8",
        )
    else:
        web_launcher = target / "oracle-dev-tools-web"
        web_launcher.write_text(
            '#!/bin/sh\nexec "{}" "{}" "$@"\n'.format(
                venv_python(root), root / "serve_web.py"
            ),
            encoding="utf-8",
        )
        web_launcher.chmod(0o755)

    if os.name == "nt":
        activate = target / "activate-oracle-dev-tools.cmd"
        activate.write_text(
            '@echo off\r\n'
            'set "PATH={};%PATH%"\r\n'
            'echo Oracle Dev Tools enabled for this terminal.\r\n'.format(target),
            encoding="utf-8",
        )
    else:
        activate = target / "activate-oracle-dev-tools"
        activate.write_text(
            '#!/bin/sh\n'
            'export PATH="{}:$PATH"\n'
            'echo "Oracle Dev Tools enabled for this shell command context."\n'.format(target),
            encoding="utf-8",
        )
        activate.chmod(0o755)


def add_to_path_windows(path):
    try:
        import winreg
    except ImportError:
        return False, "winreg unavailable"

    key_path = r"Environment"
    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        key_path,
        0,
        winreg.KEY_READ | winreg.KEY_SET_VALUE,
    ) as key:
        try:
            current, value_type = winreg.QueryValueEx(key, "Path")
        except FileNotFoundError:
            current, value_type = "", winreg.REG_EXPAND_SZ

        entries = [x for x in current.split(";") if x]
        normalized = {os.path.normcase(os.path.normpath(x)) for x in entries}
        wanted = os.path.normcase(os.path.normpath(str(path)))
        if wanted not in normalized:
            entries.append(str(path))
            winreg.SetValueEx(key, "Path", 0, value_type, ";".join(entries))

    return True, "User PATH updated. Open a new terminal."


def add_to_path_unix(path):
    profile = Path.home() / ".profile"
    marker_start = "# >>> oracle-dev-tools >>>"
    marker_end = "# <<< oracle-dev-tools <<<"
    line = 'export PATH="{}:$PATH"'.format(path)
    block = "\n{}\n{}\n{}\n".format(marker_start, line, marker_end)

    existing = profile.read_text(encoding="utf-8") if profile.exists() else ""
    if marker_start not in existing:
        with profile.open("a", encoding="utf-8") as fh:
            fh.write(block)

    return True, "Added to ~/.profile. Open a new login terminal or run: source ~/.profile"


def add_to_path(root):
    path = launcher_dir(root)
    if os.name == "nt":
        return add_to_path_windows(path)
    return add_to_path_unix(path)


def remove_from_path_unix(path):
    profile = Path.home() / ".profile"
    if not profile.exists():
        return
    text = profile.read_text(encoding="utf-8")
    start = "# >>> oracle-dev-tools >>>"
    end = "# <<< oracle-dev-tools <<<"
    while start in text and end in text:
        a = text.index(start)
        b = text.index(end, a) + len(end)
        if b < len(text) and text[b:b+1] == "\n":
            b += 1
        text = text[:a] + text[b:]
    profile.write_text(text, encoding="utf-8")


def remove_from_path_windows(path):
    try:
        import winreg
    except ImportError:
        return
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Environment",
            0,
            winreg.KEY_READ | winreg.KEY_SET_VALUE,
        ) as key:
            current, value_type = winreg.QueryValueEx(key, "Path")
            wanted = os.path.normcase(os.path.normpath(str(path)))
            entries = [
                x for x in current.split(";")
                if x and os.path.normcase(os.path.normpath(x)) != wanted
            ]
            winreg.SetValueEx(key, "Path", 0, value_type, ";".join(entries))
    except OSError:
        pass


def uninstall(root):
    if os.name == "nt":
        remove_from_path_windows(launcher_dir(root))
    else:
        remove_from_path_unix(launcher_dir(root))

    if root.exists():
        print("Removing", root)
        shutil.rmtree(root)
    print("Oracle Dev Tools removed.")


def check_installation(root):
    py = venv_python(root)
    scripts = venv_scripts(root)

    if not py.exists():
        die("Installation not found at {}".format(root), 2)

    failed = []
    print("Python:", py)
    for name in CLI_TOOLS:
        executable = scripts / (name + (".exe" if os.name == "nt" else ""))
        ok = executable.exists()
        print("{:<28} {}".format(name, "OK" if ok else "MISSING"))
        if not ok:
            failed.append(name)

    if failed:
        die("{} CLI tool(s) are missing.".format(len(failed)), 3)

    run([py, "-m", "pip", "check"])

    web_missing = [name for name in WEB_FILES if not (web_root(root) / name).exists()]
    if web_missing:
        die("Local web UI is incomplete: {}".format(", ".join(web_missing)), 4)
    if not (root / "serve_web.py").exists():
        die("Local web server launcher is missing.", 4)

    print("\nAll {} CLI tools are installed.".format(len(CLI_TOOLS)))
    print("Local browser UI is installed.")


def print_usage(root, port):
    bin_dir = launcher_dir(root)
    print("\nInstallation complete.")
    print("Platform :", platform.system(), platform.machine())
    print("Location :", root)
    print("Launchers:", bin_dir)
    prefix = "" if str(bin_dir) in os.environ.get("PATH", "").split(os.pathsep) else str(bin_dir) + os.sep
    suffix = ".cmd" if os.name == "nt" else ""

    print("\nBrowser usage:")
    print("  Address : http://127.0.0.1:{}/".format(port))
    print("  Start   : {}oracle-dev-tools-web{}".format(prefix, suffix))
    print("  Stop    : press Ctrl+C in the terminal running the web server")

    print("\nCLI examples:")
    print("  {}ora-impact{} examples.sql".format(prefix, suffix))
    print("  {}ora-errors{} ORA-01722".format(prefix, suffix))
    print("  {}ora-plan{} plan.txt".format(prefix, suffix))

    print("\nCheck installation:")
    print("  {} --check".format(Path(sys.argv[0]).name))


def parse_args():
    parser = argparse.ArgumentParser(
        description="Install all Oracle Dev Tools on Windows, Linux, or macOS."
    )
    parser.add_argument(
        "--install-dir",
        default=str(DEFAULT_ROOT),
        help="Installation root (default: ~/.oracle-dev-tools)",
    )
    parser.add_argument(
        "--add-to-path",
        action="store_true",
        help="Persistently add the launcher directory to the current user's PATH.",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Non-interactive mode.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify an existing installation.",
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Remove the suite and installer-managed PATH entry.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List the repositories installed by this script.",
    )
    parser.add_argument(
        "--port",
        type=int,
        choices=PORT_CHOICES,
        help="Local browser port. Allowed: {}".format(
            ", ".join(str(x) for x in PORT_CHOICES)
        ),
    )
    parser.add_argument(
        "--start-web",
        action="store_true",
        help="Start the local browser UI after installation.",
    )
    return parser.parse_args()


def main():
    check_python()
    args = parse_args()
    root = Path(args.install_dir).expanduser().resolve()

    if args.list:
        for repo in REPOSITORIES:
            print(repo)
        return 0

    if args.uninstall:
        if not args.yes:
            answer = input("Remove Oracle Dev Tools from {}? [y/N] ".format(root)).strip().lower()
            if answer not in ("y", "yes"):
                print("Cancelled.")
                return 0
        uninstall(root)
        return 0

    if args.check:
        check_installation(root)
        if config_path(root).exists():
            cfg = json.loads(config_path(root).read_text(encoding="utf-8"))
            print("Local web address:", cfg.get("url", "not configured"))
        return 0

    root.mkdir(parents=True, exist_ok=True)
    port = choose_port(args.port, interactive=not args.yes)
    create_venv(root)
    upgrade_packaging(root)
    install_suite(root)
    install_web_ui(root, port)
    write_web_server(root)
    write_launchers(root)

    should_add = args.add_to_path
    if not args.yes and not args.add_to_path:
        answer = input("Add Oracle Dev Tools launchers to your user PATH? [Y/n] ").strip().lower()
        should_add = answer in ("", "y", "yes")

    if should_add:
        ok, message = add_to_path(root)
        print(message if ok else "Could not update PATH automatically: " + message)

    check_installation(root)
    print_usage(root, port)

    if args.start_web:
        print("\nStarting local browser UI...")
        run([venv_python(root), root / "serve_web.py"])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

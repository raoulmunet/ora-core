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
import subprocess
import sys
from pathlib import Path

MIN_PYTHON = (3, 10)
DEFAULT_ROOT = Path.home() / ".oracle-dev-tools"

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
    print("\nAll {} CLI tools are installed.".format(len(CLI_TOOLS)))


def print_usage(root):
    bin_dir = launcher_dir(root)
    print("\nInstallation complete.")
    print("Platform :", platform.system(), platform.machine())
    print("Location :", root)
    print("Launchers:", bin_dir)
    print("\nExamples:")
    prefix = "" if str(bin_dir) in os.environ.get("PATH", "").split(os.pathsep) else str(bin_dir) + os.sep
    suffix = ".cmd" if os.name == "nt" else ""
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
        return 0

    root.mkdir(parents=True, exist_ok=True)
    create_venv(root)
    upgrade_packaging(root)
    install_suite(root)
    write_launchers(root)

    should_add = args.add_to_path
    if not args.yes and not args.add_to_path:
        answer = input("Add Oracle Dev Tools launchers to your user PATH? [Y/n] ").strip().lower()
        should_add = answer in ("", "y", "yes")

    if should_add:
        ok, message = add_to_path(root)
        print(message if ok else "Could not update PATH automatically: " + message)

    check_installation(root)
    print_usage(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

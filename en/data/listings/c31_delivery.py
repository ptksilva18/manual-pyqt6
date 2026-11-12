# runner: ticks=9000 timeout=900
"""Delivery of the capstone project: tests with coverage, self-test, packaging and
retest."""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT = Path(__file__).resolve().parent / "c31_app"


def run(title: str, command: list[str], cwd: Path, keep=None) -> int:
    environment = dict(
        os.environ, QT_QPA_PLATFORM="offscreen", PYTHONDONTWRITEBYTECODE="1"
    )
    r = subprocess.run(
        command, cwd=cwd, env=environment, capture_output=True, text=True, timeout=600
    )
    print(f"== {title} (code {r.returncode})")
    for line in r.stdout.splitlines():
        if keep is None or keep(line):
            print("  " + line)
    if r.returncode != 0:
        print(r.stderr[-1500:])
    return r.returncode


def main() -> int:
    work = Path(tempfile.mkdtemp())
    copy = Path(shutil.copytree(PROJECT, work / "c31_app"))
    failures = run(
        "1. tests (pytest + coverage)",
        [
            sys.executable,
            "-m",
            "pytest",
            "tests",
            "-q",
            "--no-header",
            "-p",
            "no:cacheprovider",
            "--cov=leaktest",
            "--cov-report=term",
        ],
        copy,
        lambda ln: ln.startswith(("leaktest", "TOTAL")) or "passed" in ln,
    )
    output = work / "source"
    output.mkdir()
    failures += run(
        "2. self-test from the source code",
        [sys.executable, "-m", "leaktest", "--selftest", str(output)],
        copy,
    )
    failures += run(
        "3. packaging (PyInstaller, onedir)",
        [
            sys.executable,
            "-m",
            "PyInstaller",
            "--noconfirm",
            "--log-level",
            "WARN",
            "leak_test_monitor.spec",
        ],
        copy,
    )
    dist = copy / "dist" / "LeakTestMonitor"
    exe = dist / ("LeakTestMonitor.exe" if sys.platform == "win32" else "LeakTestMonitor")
    size = sum(f.stat().st_size for f in dist.rglob("*") if f.is_file()) / 1024**2
    print(f"   package: dist/LeakTestMonitor ({size:.0f} MB)")
    output_f = work / "frozen"
    output_f.mkdir()
    failures += run(
        "4. self-test of the frozen executable",
        [str(exe), "--selftest", str(output_f)],
        copy,
    )
    shutil.rmtree(work)
    print("DELIVERY", "APPROVED" if failures == 0 else "WITH FAILURES")
    return failures


if __name__ == "__main__":
    sys.exit(main())

# runner: ticks=300 timeout=180
"""Runs the suite with pytest-cov, as on a continuous integration server (no
display)."""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> int:
    environment = dict(
        os.environ, QT_QPA_PLATFORM="offscreen", PYTHONDONTWRITEBYTECODE="1"
    )
    command = [
        sys.executable,
        "-m",
        "pytest",
        "c28_test_calculator.py",
        "-q",
        "--no-header",
        "-p",
        "no:cacheprovider",
        "--cov=c28_calculator",
        "--cov-branch",
        "--cov-report=term-missing",
    ]
    print("$", " ".join(["python"] + command[1:]))
    r = subprocess.run(command, cwd=HERE, env=environment, capture_output=True, text=True)
    lines = [ln for ln in r.stdout.splitlines() if ln.strip()]
    for ln in lines:
        if (
            ln.startswith(("Name", "-", "c28_", "TOTAL"))
            or " passed" in ln
            or " failed" in ln
        ):
            print(ln)
    if os.path.exists(os.path.join(HERE, ".coverage")):
        os.remove(os.path.join(HERE, ".coverage"))
    print("pytest exit code:", r.returncode)
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())

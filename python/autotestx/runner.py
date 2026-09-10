import subprocess
from pathlib import Path
import sys

from reporter import load_results, print_report


# Project root:
# autotestx/
# ├── python/
# │   └── autotestx/
# │       └── runner.py
PROJECT_ROOT = Path(__file__).resolve().parents[2]

BUILD_DIR = PROJECT_ROOT / "cpp" / "build"
EXECUTABLE = BUILD_DIR / "Debug" / "autotestx.exe"
RESULT_FILE = PROJECT_ROOT / "results.json"


def build_project():
    print("\n[AutoTestX] Building C++ project...\n")

    result = subprocess.run(
        ["cmake", "--build", str(BUILD_DIR)],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.returncode != 0:
        print(result.stderr)
        print("[AutoTestX] Build failed.")
        return False

    print("[AutoTestX] Build successful.")
    return True


def run_tests():
    print("\n[AutoTestX] Running tests...\n")

    result = subprocess.run(
        [str(EXECUTABLE)],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.returncode != 0:
        print("[AutoTestX] Tests completed with failures.")
    else:
        print("[AutoTestX] All tests passed.")

    return True


def main():
    print("================================")
    print("        AutoTestX Runner")
    print("================================")

    if not build_project():
        sys.exit(1)

    run_tests()

    if not RESULT_FILE.exists():
        print("\n[AutoTestX] Warning: results.json not found.")
        sys.exit(1)

    print(f"\n[AutoTestX] Result file: {RESULT_FILE}")

    try:
        data = load_results(RESULT_FILE)
        print_report(data)

    except Exception as error:
        print(f"\n[AutoTestX] Failed to analyze results: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
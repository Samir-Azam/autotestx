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


# Possible CMake installation locations
CMAKE_CANDIDATES = [
    Path(
        r"C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools"
        r"\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe"
    ),
    Path(
        r"C:\Program Files\Microsoft Visual Studio\18\BuildTools"
        r"\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe"
    ),
]


def find_cmake():
    """
    Find a usable CMake executable.

    First checks known Visual Studio installation paths.
    If not found, falls back to CMake available in PATH.
    """

    for path in CMAKE_CANDIDATES:
        if path.exists():
            return str(path)

    return "cmake"


def build_project():
    print("\n[AutoTestX] Building C++ project...\n")

    cmake = find_cmake()

    result = subprocess.run(
        [cmake, "--build", str(BUILD_DIR)],
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
        return False

    print("[AutoTestX] All tests passed.")
    return True


def main():
    print("================================")
    print("        AutoTestX Runner")
    print("================================")

    # Exit code 2 = build failure
    if not build_project():
        sys.exit(2)

    # Exit code 1 = test failure
    tests_passed = run_tests()

    # Exit code 3 = missing result file
    if not RESULT_FILE.exists():
        print("\n[AutoTestX] Warning: results.json not found.")
        sys.exit(3)

    print(f"\n[AutoTestX] Result file: {RESULT_FILE}")

    try:
        data = load_results(RESULT_FILE)
        print_report(data)

    except Exception as error:
        # Exit code 3 = automation/reporting error
        print(
            f"\n[AutoTestX] Failed to analyze results: {error}"
        )
        sys.exit(3)

    # Exit code 1 = tests failed
    if not tests_passed:
        sys.exit(1)

    # Exit code 0 = everything passed
    sys.exit(0)


if __name__ == "__main__":
    main()
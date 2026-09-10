import sys
import json
from pathlib import Path


# Project root:
# C:\Users\ADMIN\OneDrive\Desktop\autotestx
PROJECT_ROOT = Path(__file__).resolve().parents[1]

PYTHON_DIR = PROJECT_ROOT / "python"

sys.path.insert(0, str(PYTHON_DIR))


from autotestx.executor import run_executable


AI_TEST_FILE = (
    PROJECT_ROOT
    / "examples"
    / "calculator_tests_ai.json"
)

BUILD_DIR = (
    PROJECT_ROOT
    / "cpp"
    / "build"
    / "Debug"
)

RESULTS_DIR = PROJECT_ROOT / "results"

RESULT_FILE = (
    RESULTS_DIR
    / "ai_test_results.json"
)


def load_ai_tests():

    if not AI_TEST_FILE.exists():
        raise FileNotFoundError(
            f"AI test file not found: {AI_TEST_FILE}"
        )

    with open(
        AI_TEST_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_results(report):

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        RESULT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4
        )


def main():

    print("================================")
    print("     AutoTestX AI Test Runner")
    print("================================")

    config = load_ai_tests()

    executable_name = config["executable"]

    executable = (
        BUILD_DIR
        / executable_name
    )

    test_cases = config["tests"]

    print(f"\nTarget: {executable_name}")
    print(f"AI Test Cases: {len(test_cases)}")
    print(f"Executable: {executable}")

    if not executable.exists():

        print(
            "\nERROR: C++ executable not found."
        )

        print(
            "Build the project before running AI tests."
        )

        sys.exit(2)

    results = []

    passed = 0
    failed = 0

    print("\nRunning AI-generated tests...")
    print("--------------------------------")

    for test in test_cases:

        print(
            f"\n[TEST] {test['name']}"
        )

        result = run_executable(
            executable=executable,
            input_data=test["input"],
            expected_output=test["expected"],
            timeout_seconds=5
        )

        test_result = {
            "name": test["name"],
            "input": test["input"],
            "expected": test["expected"],
            "actual": result.stdout,
            "passed": result.passed,
            "exit_code": result.exit_code,
            "execution_time_ms": result.execution_time_ms,
            "error": result.error
        }

        results.append(test_result)

        if result.passed:

            print("[PASS]")
            passed += 1

        else:

            print("[FAIL]")
            failed += 1

        print(
            f"  Expected: {test['expected'].strip()}"
        )

        print(
            f"  Actual:   {result.stdout}"
        )

        print(
            f"  Time:     "
            f"{result.execution_time_ms:.4f} ms"
        )

        if result.error:

            print(
                f"  Error:    {result.error}"
            )

    summary = {
        "total": len(test_cases),
        "passed": passed,
        "failed": failed
    }

    report = {
        "source": "Gemini AI-generated tests",
        "target": executable_name,
        "summary": summary,
        "tests": results
    }

    save_results(report)

    print("\n================================")
    print("          Test Summary")
    print("================================")

    print(f"Total : {summary['total']}")
    print(f"Passed: {summary['passed']}")
    print(f"Failed: {summary['failed']}")

    print(
        f"\nResult file: {RESULT_FILE}"
    )

    if failed == 0:

        print("\nRESULT: ALL AI TESTS PASSED")

        sys.exit(0)

    else:

        print("\nRESULT: AI TEST FAILURES DETECTED")

        sys.exit(1)


if __name__ == "__main__":
    main()
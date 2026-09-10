import sys
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PYTHON_DIR = PROJECT_ROOT / "python"

sys.path.insert(0, str(PYTHON_DIR))

from autotestx.executor import run_executable


TEST_CONFIG = (
    PROJECT_ROOT
    / "examples"
    / "calculator_tests.json"
)

BUILD_DIR = PROJECT_ROOT / "cpp" / "build"

RESULTS_DIR = PROJECT_ROOT / "results"

RESULT_FILE = RESULTS_DIR / "calculator_results.json"


def load_test_config():

    if not TEST_CONFIG.exists():
        raise FileNotFoundError(
            f"Test configuration not found: {TEST_CONFIG}"
        )

    with open(TEST_CONFIG, "r", encoding="utf-8") as file:
        return json.load(file)


def save_results(results):

    RESULTS_DIR.mkdir(exist_ok=True)

    with open(
        RESULT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4
        )


def main():

    print("================================")
    print("     AutoTestX Executor Suite")
    print("================================")

    config = load_test_config()

    executable_name = config["executable"]

    executable = (
        BUILD_DIR
        / "Debug"
        / executable_name
    )

    test_cases = config["tests"]

    results = []

    passed = 0
    failed = 0

    print(f"\nTarget: {executable_name}")
    print(f"Test Cases: {len(test_cases)}")

    for test in test_cases:

        print(f"\nRunning: {test['name']}")

        result = run_executable(
            executable=executable,
            input_data=test["input"] + "\n",
            expected_output=test["expected"],
            timeout_seconds=5
        )

        test_result = {
            "name": test["name"],
            "passed": result.passed,
            "input": test["input"],
            "expected": test["expected"],
            "actual": result.stdout,
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

        print(f"  Input: {test['input']}")
        print(f"  Expected: {test['expected']}")
        print(f"  Actual: {result.stdout}")
        print(f"  Exit Code: {result.exit_code}")
        print(
            f"  Execution Time: "
            f"{result.execution_time_ms:.4f} ms"
        )

        if result.error:
            print(f"  Error: {result.error}")

    summary = {
        "total": len(test_cases),
        "passed": passed,
        "failed": failed
    }

    report = {
        "target": executable_name,
        "summary": summary,
        "tests": results
    }

    save_results(report)

    print("\n================================")
    print("           Test Summary")
    print("================================")

    print(f"Total : {len(test_cases)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    print(f"\nResult file: {RESULT_FILE}")

    if failed == 0:
        print("\nRESULT: ALL TESTS PASSED")
    else:
        print("\nRESULT: TEST FAILURES DETECTED")


if __name__ == "__main__":
    main()
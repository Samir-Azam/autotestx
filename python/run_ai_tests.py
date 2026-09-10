import sys
import json
from pathlib import Path


# Project root:
# C:\Users\ADMIN\OneDrive\Desktop\autotestx
PROJECT_ROOT = Path(__file__).resolve().parents[1]

PYTHON_DIR = PROJECT_ROOT / "python"

sys.path.insert(0, str(PYTHON_DIR))


from autotestx.executor import run_executable
from autotestx.database import TestDatabase
from autotestx.failure_analyzer import AIFailureAnalyzer


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

DATABASE_FILE = (
    RESULTS_DIR
    / "test_results.db"
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

    database = TestDatabase(
        DATABASE_FILE
    )

    analyzer = AIFailureAnalyzer()

    executable_name = config["executable"]

    executable = (
        BUILD_DIR
        / executable_name
    )

    test_cases = config["tests"]

    print(
        f"\nTarget: {executable_name}"
    )

    print(
        f"AI Test Cases: {len(test_cases)}"
    )

    print(
        f"Executable: {executable}"
    )

    if not executable.exists():

        print(
            "\nERROR: C++ executable not found."
        )

        print(
            "Build the project before running AI tests."
        )

        database.close()

        sys.exit(2)

    results = []

    passed = 0
    failed = 0

    print(
        "\nRunning AI-generated tests..."
    )

    print(
        "--------------------------------"
    )

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

        if result.passed:

            print("[PASS]")

            passed += 1

        else:

            print("[FAIL]")

            failed += 1

        print(
            f"  Expected: "
            f"{test['expected'].strip()}"
        )

        print(
            f"  Actual:   "
            f"{result.stdout}"
        )

        print(
            f"  Time:     "
            f"{result.execution_time_ms:.4f} ms"
        )

        if result.error:

            print(
                f"  Error:    "
                f"{result.error}"
            )

            # -----------------------------------------
            # AI FAILURE ANALYSIS
            # -----------------------------------------

            print(
                "\n  AI Failure Analysis"
            )

            print(
                "  --------------------------------"
            )

            try:

                analysis = analyzer.analyze_failure(
                    test_result
                )

                test_result["ai_analysis"] = analysis

                print(
                    f"  Likely Cause: "
                    f"{analysis['likely_cause']}"
                )

                print(
                    f"  Severity: "
                    f"{analysis['severity']}"
                )

                print(
                    f"  Suggested Fix: "
                    f"{analysis['suggested_fix']}"
                )

            except Exception as error:

                print(
                    f"  AI analysis failed: "
                    f"{error}"
                )

                test_result["ai_analysis"] = {
                    "likely_cause": (
                        "AI analysis unavailable."
                    ),
                    "severity": "UNKNOWN",
                    "suggested_fix": (
                        "Review the test failure manually."
                    )
                }

            print(
                "  --------------------------------"
            )

        results.append(
            test_result
        )

        # -----------------------------------------
        # STORE RESULT IN SQLITE
        # -----------------------------------------

        database.insert_result(
            test_result
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

    save_results(
        report
    )

    database.close()

    print(
        "\n================================"
    )

    print(
        "          Test Summary"
    )

    print(
        "================================"
    )

    print(
        f"Total : {summary['total']}"
    )

    print(
        f"Passed: {summary['passed']}"
    )

    print(
        f"Failed: {summary['failed']}"
    )

    print(
        f"\nResult file: {RESULT_FILE}"
    )

    print(
        f"Database:    {DATABASE_FILE}"
    )

    if failed == 0:

        print(
            "\nRESULT: ALL AI TESTS PASSED"
        )

        sys.exit(0)

    else:

        print(
            "\nRESULT: AI TEST FAILURES DETECTED"
        )

        sys.exit(1)


if __name__ == "__main__":

    main()
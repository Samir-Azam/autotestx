import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PYTHON_DIR = PROJECT_ROOT / "python"

sys.path.insert(0, str(PYTHON_DIR))


from autotestx.database import TestDatabase


DATABASE_FILE = (
    PROJECT_ROOT
    / "results"
    / "test_results.db"
)


def main():

    print("================================")
    print("      AutoTestX Database")
    print("================================")

    database = TestDatabase(
        DATABASE_FILE
    )

    test_result = {
        "name": "database integration test",
        "input": "10 20",
        "expected": "30",
        "actual": "30",
        "passed": True,
        "exit_code": 0,
        "execution_time_ms": 12.45,
        "error": None
    }

    database.insert_result(
        test_result
    )

    results = database.get_results()

    print(
        f"\nStored Results: {len(results)}"
    )

    print("\nLatest Result:")
    print("--------------------------------")

    latest = results[0]

    print(f"ID: {latest[0]}")
    print(f"Test: {latest[1]}")
    print(f"Expected: {latest[3]}")
    print(f"Actual: {latest[4]}")
    print(f"Passed: {bool(latest[5])}")
    print(f"Execution Time: {latest[7]} ms")

    print("--------------------------------")

    database.close()

    print(
        f"\nDatabase created at:\n{DATABASE_FILE}"
    )


if __name__ == "__main__":
    main()
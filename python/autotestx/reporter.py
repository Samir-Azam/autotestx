import json
from pathlib import Path


def load_results(filename):
    path = Path(filename)

    if not path.exists():
        raise FileNotFoundError(
            f"Result file not found: {path}"
        )

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def print_report(data):

    summary = data["summary"]
    tests = data["tests"]

    print("\n================================")
    print("       AutoTestX Report")
    print("================================")

    print(f"Total Tests : {summary['total']}")
    print(f"Passed      : {summary['passed']}")
    print(f"Failed      : {summary['failed']}")

    print("\nTest Details:")
    print("--------------------------------")

    for test in tests:

        status = "PASS" if test["passed"] else "FAIL"

        print(
            f"[{status}] "
            f"{test['name']} "
            f"({test['execution_time_ms']:.4f} ms)"
        )

        if not test["passed"]:
            print(f"       Reason: {test['message']}")

    print("--------------------------------")

    if summary["failed"] == 0:
        print("RESULT: ALL TESTS PASSED")
    else:
        print("RESULT: TEST FAILURES DETECTED")
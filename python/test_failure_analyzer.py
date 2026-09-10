import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PYTHON_DIR = PROJECT_ROOT / "python"

sys.path.insert(0, str(PYTHON_DIR))


from autotestx.failure_analyzer import AIFailureAnalyzer


def main():

    failed_test = {
        "name": "Sum of two positive integers",
        "input": "15\n25\n",
        "expected": "40",
        "actual": "-10",
        "exit_code": 0,
        "error": (
            "Output mismatch | "
            "Expected: 40 | "
            "Actual: -10"
        )
    }

    print("================================")
    print("     AutoTestX AI Analyzer")
    print("================================")

    print("\nAnalyzing failure...")
    print("--------------------------------")

    analyzer = AIFailureAnalyzer()

    analysis = analyzer.analyze_failure(
        failed_test
    )

    print("\nAI Failure Analysis")
    print("--------------------------------")

    print(
        f"Likely Cause: "
        f"{analysis['likely_cause']}"
    )

    print(
        f"Severity: "
        f"{analysis['severity']}"
    )

    print(
        f"Suggested Fix: "
        f"{analysis['suggested_fix']}"
    )

    print("--------------------------------")


if __name__ == "__main__":
    main()
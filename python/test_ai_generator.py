import sys
from pathlib import Path


# Project root:
# C:\Users\ADMIN\OneDrive\Desktop\autotestx
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Python directory:
# C:\Users\ADMIN\OneDrive\Desktop\autotestx\python
PYTHON_DIR = PROJECT_ROOT / "python"

sys.path.insert(0, str(PYTHON_DIR))


from autotestx.ai_generator import (
    AITestGenerator,
    save_generated_tests,
)


def main():

    requirement = """
The calculator program accepts two integers through standard input
and outputs their sum.
"""

    print("================================")
    print("      AutoTestX AI Generator")
    print("================================")

    print("\nRequirement:")
    print(requirement)

    print("Generating test cases with Gemini...\n")

    generator = AITestGenerator()

    tests = generator.generate_tests(requirement)

    output_file = (
        PROJECT_ROOT
        / "examples"
        / "calculator_tests_ai.json"
    )

    save_generated_tests(
        tests,
        output_file
    )

    print("\nGenerated test cases:")
    print("--------------------------------")

    for test in tests["tests"]:

        print(
            f"[TEST] {test['name']} | "
            f"Input: {test['input'].strip()} | "
            f"Expected: {test['expected'].strip()}"
        )

    print("--------------------------------")

    print(
        f"\nTotal generated: "
        f"{len(tests['tests'])}"
    )


if __name__ == "__main__":
    main()
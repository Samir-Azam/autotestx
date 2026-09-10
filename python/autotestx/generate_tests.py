import sys
from pathlib import Path

from ai_generator import (
    AITestGenerator,
    load_source,
    save_generated_tests
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SOURCE_FILE = (
    PROJECT_ROOT
    / "examples"
    / "calculator_program.cpp"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "examples"
    / "calculator_tests_ai.json"
)


def main():

    print("================================")
    print("      AutoTestX AI Generator")
    print("================================")

    print(f"\nSource: {SOURCE_FILE}")

    source_code = load_source(SOURCE_FILE)

    generator = AITestGenerator()

    print("\n[AutoTestX] Generating test cases with AI...\n")

    result = generator.generate_tests(
        source_code=source_code,
        program_description=(
            "A C++ command-line calculator program "
            "that reads two integers from stdin and "
            "prints their sum."
        )
    )

    save_generated_tests(
        result,
        OUTPUT_FILE
    )

    print(
        f"[AutoTestX] Generated "
        f"{len(result['tests'])} test cases."
    )

    print(
        f"[AutoTestX] Saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
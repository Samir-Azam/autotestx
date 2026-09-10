import json
import os
from pathlib import Path

from google import genai


class AITestGenerator:
    """
    Generates structured test cases from a natural-language
    software requirement using Gemini.
    """

    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY environment variable is not set."
            )

        self.client = genai.Client(api_key=api_key)

    def generate_tests(self, requirement):

        prompt = f"""
You are an expert software test engineer.

Generate automated test cases for this software requirement:

{requirement}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "executable": "calculator_program.exe",
    "tests": [
        {{
            "name": "descriptive test name",
            "input": "program input",
            "expected": "expected stdout"
        }}
    ]
}}

Rules:
1. Generate 5 to 8 test cases.
2. Include normal cases.
3. Include boundary cases.
4. Include negative cases when applicable.
5. Include zero cases when applicable.
6. input and expected must be strings.
7. Return JSON only.
8. No markdown.
9. No explanations.
"""

        response = self.client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        raw_text = response.text.strip()

        # Remove accidental markdown code fences.
        if raw_text.startswith("```"):
            lines = raw_text.splitlines()

            if lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            raw_text = "\n".join(lines).strip()

        try:
            data = json.loads(raw_text)

        except json.JSONDecodeError as error:
            raise ValueError(
                f"Gemini returned invalid JSON: {error}\n\n"
                f"Response:\n{raw_text}"
            )

        self._validate(data)

        return data

    @staticmethod
    def _validate(data):

        if not isinstance(data, dict):
            raise ValueError(
                "Generated result must be a JSON object."
            )

        if "executable" not in data:
            raise ValueError(
                "Missing 'executable' field."
            )

        if "tests" not in data:
            raise ValueError(
                "Missing 'tests' field."
            )

        if not isinstance(data["tests"], list):
            raise ValueError(
                "'tests' must be a list."
            )

        if len(data["tests"]) == 0:
            raise ValueError(
                "No test cases were generated."
            )

        required_fields = {
            "name",
            "input",
            "expected"
        }

        for index, test in enumerate(
            data["tests"],
            start=1
        ):

            if not isinstance(test, dict):
                raise ValueError(
                    f"Test case {index} must be an object."
                )

            missing = required_fields - test.keys()

            if missing:
                raise ValueError(
                    f"Test case {index} is missing: "
                    f"{', '.join(sorted(missing))}"
                )

            for field in required_fields:

                if not isinstance(test[field], str):
                    raise ValueError(
                        f"Test case {index} field "
                        f"'{field}' must be a string."
                    )


def save_generated_tests(data, filename):

    path = Path(filename)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )

    print(
        f"AI-generated tests saved to: {path}"
    )
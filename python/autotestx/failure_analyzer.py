import json
import os

from google import genai


class AIFailureAnalyzer:
    """
    Uses Gemini to analyze failed automated tests.

    The analyzer provides:
    - likely cause
    - severity
    - evidence-based debugging recommendation

    It does not assume access to source code unless
    source code is explicitly provided.
    """

    VALID_SEVERITIES = {
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL"
    }

    def __init__(self):

        api_key = os.environ.get("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY environment variable is not set."
            )

        self.client = genai.Client(
            api_key=api_key
        )

    def analyze_failure(self, test_result):

        prompt = f"""
You are a senior software test engineer specializing
in automated test failure analysis.

Analyze the following automated test failure.

TEST INFORMATION
-----------------

Test Name:
{test_result["name"]}

Input:
{test_result["input"]}

Expected Output:
{test_result["expected"]}

Actual Output:
{test_result["actual"]}

Exit Code:
{test_result["exit_code"]}

Error:
{test_result["error"]}

IMPORTANT ANALYSIS RULES
------------------------

1. Base your analysis ONLY on the information provided above.

2. Do NOT claim that you inspected or saw source code.

3. Do NOT invent implementation details.

4. Clearly distinguish between:
   - observed facts
   - possible causes
   - recommended investigation

5. If source code is not provided, do NOT recommend a
   specific code change such as "replace + with -".

6. If the actual output suggests a possible implementation
   problem, describe it as a possibility rather than a fact.

7. The suggested fix should be a practical debugging or
   investigation step supported by the available evidence.

8. Severity should reflect the impact of the failure:
   LOW, MEDIUM, HIGH, or CRITICAL.

9. Keep all responses concise and useful to a software
   testing engineer.

Return ONLY valid JSON.

Use EXACTLY this structure:

{{
    "likely_cause": "brief evidence-based explanation",
    "severity": "LOW | MEDIUM | HIGH | CRITICAL",
    "suggested_fix": "specific evidence-based debugging or investigation step"
}}
"""

        response = self.client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        raw_text = response.text.strip()

        # -------------------------------------------------
        # Remove accidental Markdown code fences
        # -------------------------------------------------

        if raw_text.startswith("```"):

            lines = raw_text.splitlines()

            if lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            raw_text = "\n".join(lines).strip()

        # -------------------------------------------------
        # Parse JSON
        # -------------------------------------------------

        try:

            analysis = json.loads(raw_text)

        except json.JSONDecodeError as error:

            raise ValueError(
                f"Gemini returned invalid JSON: {error}\n\n"
                f"Response:\n{raw_text}"
            )

        # -------------------------------------------------
        # Validate response structure
        # -------------------------------------------------

        if not isinstance(analysis, dict):

            raise ValueError(
                "AI analysis must be a JSON object."
            )

        required_fields = {
            "likely_cause",
            "severity",
            "suggested_fix"
        }

        missing = required_fields - analysis.keys()

        if missing:

            raise ValueError(
                "Missing analysis fields: "
                + ", ".join(sorted(missing))
            )

        # -------------------------------------------------
        # Validate field types
        # -------------------------------------------------

        for field in required_fields:

            if not isinstance(
                analysis[field],
                str
            ):

                raise ValueError(
                    f"Analysis field '{field}' "
                    f"must be a string."
                )

        # -------------------------------------------------
        # Validate severity
        # -------------------------------------------------

        severity = analysis["severity"].upper()

        if severity not in self.VALID_SEVERITIES:

            raise ValueError(
                f"Invalid severity '{analysis['severity']}'. "
                f"Expected one of: "
                f"{', '.join(sorted(self.VALID_SEVERITIES))}"
            )

        analysis["severity"] = severity

        return analysis
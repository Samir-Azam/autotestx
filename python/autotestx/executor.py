import subprocess
import time
from pathlib import Path


class ExecutionResult:
    def __init__(
        self,
        passed,
        stdout,
        stderr,
        exit_code,
        execution_time_ms,
        error=None
    ):
        self.passed = passed
        self.stdout = stdout
        self.stderr = stderr
        self.exit_code = exit_code
        self.execution_time_ms = execution_time_ms
        self.error = error


def run_executable(
    executable,
    input_data="",
    expected_output="",
    timeout_seconds=5
):
    """
    Execute a program and validate its output.

    Parameters:
        executable: Path to the executable.
        input_data: Data sent to stdin.
        expected_output: Expected stdout.
        timeout_seconds: Maximum execution time.

    Returns:
        ExecutionResult
    """

    executable = Path(executable)

    if not executable.exists():
        return ExecutionResult(
            passed=False,
            stdout="",
            stderr="",
            exit_code=-1,
            execution_time_ms=0,
            error=f"Executable not found: {executable}"
        )

    start_time = time.perf_counter()

    try:
        result = subprocess.run(
            [str(executable)],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=timeout_seconds
        )

        end_time = time.perf_counter()

        execution_time_ms = (
            end_time - start_time
        ) * 1000

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        passed = (
            result.returncode == 0
            and stdout == expected_output.strip()
        )

        error = None

        if result.returncode != 0:
            error = (
                f"Program exited with code "
                f"{result.returncode}"
            )

        elif stdout != expected_output.strip():
            error = (
                f"Output mismatch | "
                f"Expected: {expected_output.strip()} | "
                f"Actual: {stdout}"
            )

        return ExecutionResult(
            passed=passed,
            stdout=stdout,
            stderr=stderr,
            exit_code=result.returncode,
            execution_time_ms=execution_time_ms,
            error=error
        )

    except subprocess.TimeoutExpired:
        end_time = time.perf_counter()

        execution_time_ms = (
            end_time - start_time
        ) * 1000

        return ExecutionResult(
            passed=False,
            stdout="",
            stderr="",
            exit_code=-1,
            execution_time_ms=execution_time_ms,
            error=(
                f"Test timed out after "
                f"{timeout_seconds} seconds"
            )
        )

    except Exception as error:
        end_time = time.perf_counter()

        execution_time_ms = (
            end_time - start_time
        ) * 1000

        return ExecutionResult(
            passed=False,
            stdout="",
            stderr="",
            exit_code=-1,
            execution_time_ms=execution_time_ms,
            error=str(error)
        )
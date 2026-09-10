import sqlite3
from pathlib import Path


class TestDatabase:
    """
    SQLite database for storing AutoTestX test results.
    """

    def __init__(self, database_path):

        self.database_path = Path(database_path)

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.connection = sqlite3.connect(
            self.database_path
        )

        self._create_table()

    def _create_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS test_results (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            test_name TEXT NOT NULL,

            input TEXT,

            expected TEXT,

            actual TEXT,

            passed INTEGER NOT NULL,

            exit_code INTEGER,

            execution_time_ms REAL,

            error TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        self.connection.execute(query)

        self.connection.commit()

    def insert_result(self, result):

        query = """
        INSERT INTO test_results (
            test_name,
            input,
            expected,
            actual,
            passed,
            exit_code,
            execution_time_ms,
            error
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        self.connection.execute(
            query,
            (
                result["name"],
                result["input"],
                result["expected"],
                result["actual"],
                int(result["passed"]),
                result["exit_code"],
                result["execution_time_ms"],
                result["error"]
            )
        )

        self.connection.commit()

    def get_results(self):

        query = """
        SELECT
            id,
            test_name,
            input,
            expected,
            actual,
            passed,
            exit_code,
            execution_time_ms,
            error,
            created_at
        FROM test_results
        ORDER BY id DESC
        """

        cursor = self.connection.execute(query)

        return cursor.fetchall()

    def close(self):

        self.connection.close()
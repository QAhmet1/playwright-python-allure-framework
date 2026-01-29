
import sqlite3

class DBClient:
    def __init__(self, db_path="automation_test.db"):
        self.db_path = db_path

    def execute_query(self, query, params=()):
        """Executes a SELECT query and returns all results as a list of tuples."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def execute_non_query(self, query, params=()):
        """Executes INSERT, UPDATE, or DELETE queries and commits the transaction."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

import sqlite3

class DBClient:
    def __init__(self, db_path):
        self.db_path = db_path

    def execute_non_query(self, query, params=()):
        """Executes INSERT, UPDATE, or DELETE queries and commits the transaction."""
        with sqlite3.connect(self.db_path, timeout=20) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    def execute_query(self, query, params=()):
        """Executes SELECT queries and returns results."""
        with sqlite3.connect(self.db_path, timeout=20) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
import json
import os
import mysql.connector


class MySQLConnector:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_USER_PASSWORD")
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def execute_update(self, query, params=None):
        self.cursor.execute(query, params or ())
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

import mysql.connector
from contextlib import contextmanager

class DatabaseManager:
    def __init__(self, config):
        self.config = {
            'host': config.DB_HOST,
            'user': config.DB_USER,
            'password': config.DB_PASSWORD,
            'database': config.DB_NAME
        }

    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections to ensure proper 
        connection and cursor management
        """
        connection = None
        try:
            connection = mysql.connector.connect(**self.config)
            yield connection
        except mysql.connector.Error as e:
            print(f"Database Connection Error: {e}")
            raise
        finally:
            if connection and connection.is_connected():
                connection.close()

    def execute_query(self, query, params=None):
        """
        Execute a query and return results
        """
        with self.get_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                try:
                    cursor.execute(query, params or {})
                    connection.commit()
                    return cursor.fetchall()
                except mysql.connector.Error as e:
                    print(f"Query Execution Error: {e}")
                    connection.rollback()
                    return None
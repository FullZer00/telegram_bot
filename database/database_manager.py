import sqlite3


class DatabaseManager:
    def __init__(self, db_path='test_db.sql'):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        with self._get_connection() as conn:
            conn.execute('''
                        CREATE TABLE IF NOT EXISTS users
                        (
                            id int auto_increment primary key,
                            name varchar(50),
                            password varchar(50)
                        )
                        ''')
            conn.commit()

    def add_user(self, name, password):
        with self._get_connection() as conn:
            conn.execute("""
                                INSERT INTO users (name, password) VALUES (?, ?)
                            """, (name, password))
            conn.commit()

    def get_all_users(self):
        with self._get_connection() as conn:
            users = conn.execute("SELECT * FROM users").fetchall()
            return users

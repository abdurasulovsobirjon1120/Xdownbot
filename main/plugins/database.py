import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("database.db", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("Create table if not exists users (id integer primary key, user_id integer unique)")
        self.conn.commit()

    def add_user(self, user_id):
        self.conn.execute("insert into users (user_id) values (?)", (user_id,))
        self.conn.commit()
    def get_user(self, user_id):
        return self.conn.execute("select * from users where user_id = ?", (user_id,)).fetchone()
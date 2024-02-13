import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS user_data(
                   user_name CHAR,
                   password TEXT
        );""")
        self.conn.commit()

    def insert_user_data(self, username, password):
        self.cursor.execute("INSERT INTO user_data VALUES(?,?)", [username, password])
        self.conn.commit()

    def read_user_data(self, username):
        self.cursor.execute(f"SELECT * FROM user_data WHERE user_name = '{username}' ")
        data = self.cursor.fetchall()
        if len(data) == 0:
            flag = False
            data = None
            return data, flag
        else:
            flag = True
            return flag, data[0][1]

    def __del__(self):
        self.conn.close()


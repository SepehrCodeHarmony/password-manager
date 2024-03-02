import sqlite3
import pandas as pd
from pass_manager.read_pass import read_pass_from_database
from colorama import Fore,Style
from tabulate import tabulate

class Database:
    def __init__(self, db_name):
        self.conn= sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS passwords(
                   name TEXT,
                   url TEXT,
                   username TEXT,
                   password TEXT,
                   note TEXT,
                   salt TEXT
        );""")
        self.conn.commit()

    def store_data(self, name, url, username, password, Note, salt):

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS passwords(
                       name TEXT,
                       url TEXT,
                       username TEXT,
                       password TEXT,
                       note TEXT,
                       salt TEXT
        );""")
        self.cursor.execute("INSERT INTO passwords VALUES(?,?,?,?,?,?)", [name, url, username, password, Note, salt])


        self.conn.commit()

    def get_one_data(self, name):
        try:
            conn = sqlite3.connect("database/database.db")
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM passwords WHERE website = '{name}'")
            data = cursor.fetchall()
            token = data[0][3]
            salt = data[0][4]
            username = data[0][2]
            conn.close()
            return token, salt, username
        except IndexError:
            print("\n\nwebsite did not find. you may type it wronga\n if you are sure it is right try check all data ans loo for it there\n\n")
            pass



    def get_all_data(self):

        self.cursor.execute("SELECT password, salt FROM passwords ")
        passwords_and_salts = self.cursor.fetchall()

        #decrypte the passwords
        l = []
        for i in passwords_and_salts:
            token  = i[0]
            salt = i[1]
            decrypted_password = read_pass_from_database(token.encode(), salt.encode())
            l.append(Fore.GREEN + decrypted_password + Style.RESET_ALL)

        #using pandas to print the data
        query = "SELECT * FROM passwords"
        df = pd.read_sql_query(query, self.conn)
        df = df.iloc[:, :-1]
        pd.set_option('display.max_rows', None)
        df.loc[:, 'password'] = l
        print(tabulate(df, headers = 'keys'))


    def get_data_for_csv(self):
        raw_data = []
        conn = sqlite3.connect("database/database.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM passwords")
        data = cursor.fetchall()
        for i in range(len(data)):
            name = data[i][0]
            url = data[i][1]
            username = data[i][2]
            token = data[i][3]
            note = data[i][4]
            salt = data[i][5]

            raw_data.append((name, url, username, token, note, salt))
        conn.close()
        return raw_data
    
    def __delete__(self):
        self.conn.close()

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
                   website TEXT,
                   username TEXT,
                   password TEXT,
                   salt TEXT
        );""")
        self.conn.commit()

    def store_data(self, website, username, password, salt):

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS passwords(
                       website TEXT,
                       username TEXT,
                       password TEXT,
                       salt TEXT
        );""")
        self.cursor.execute("INSERT INTO passwords VALUES(?,?,?,?)", [website, username, password, salt])


        self.conn.commit()

    def get_one_data(self, website):
        try:
            conn = sqlite3.connect("database/database.db")
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM passwords WHERE website = '{website}'")
            data = cursor.fetchall()
            token = data[0][2]
            salt = data[0][3]
            username = data[0][1]
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
        pd.set_option('display.max_rows', None)
        df.loc[:, 'password'] = l
        print(tabulate(df, headers = 'keys', tablefmt = 'psql'))

    def __delete__(self):
        self.conn.close()

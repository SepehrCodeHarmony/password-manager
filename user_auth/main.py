from user_auth.database.database_manager import Database
from user_auth.pass_manager.pass_manager import hash_with_salt, check_password
from colorama import Fore, Style
import getpass


def main(string):
    BOLD = '\033[1m'
    END = '\033[0m'
    db = Database("user_auth/database/database.db")
    if string == 'sign up':
        password = getpass.getpass(prompt='[setpas] set a password: ')
        password_repeat = getpass.getpass(prompt='[repeat] password repeat: ')
        flag, x = db.read_user_data()
        while password != password_repeat:
            print(f"{BOLD}{Fore.RED}passwords were not the same{Style.RESET_ALL}{END}\n")
            password = getpass.getpass(prompt='[setpas] set a password: ')
            password_repeat = getpass.getpass(prompt='[repeat] password repeat: ')
        if password == password_repeat:
            hashed_password = hash_with_salt(password).decode()
            db.insert_user_data(hashed_password)
            a = 1
            return a

    if string == "sign in":
        password = getpass.getpass(prompt='[passm] password for acces: ')
        confirmation, hashed_password = db.read_user_data()

        if confirmation:
            flag = check_password(password, hashed_password)

            if flag:
                auth = 1
                print('')
                return auth

            if not flag:
                print(f"{BOLD}{Fore.RED}Incorrect password{Style.RESET_ALL}{END}")
                auth = 0
                return auth

        if not confirmation:
            print(f"{BOLD}{Fore.RED}Incorrect password{Style.RESET_ALL}{END}")
            auth = 0
            return auth


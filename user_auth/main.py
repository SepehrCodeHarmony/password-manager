from user_auth.database.database_manager import Database
from user_auth.pass_manager.pass_manager import hash_with_salt, check_password
from colorama import Fore, Style
import getpass
import sys



def main(string):
    db = Database("user_auth/database/database.db")
    if string == 'sign up':
        username = input("username: ")
        password = getpass.getpass()
        password_repeat = getpass.getpass()
        flag, x = db.read_user_data(username)
        while flag:
            print(f"\n{Fore.GREEN}username already exist{Style.RESET_ALL}\n")
            username = input("username: ")
            password = getpass.getpass()
            password_repeat = getpass.getpass()
            flag, x = db.read_user_data(username)
        while password != password_repeat:
            print(f"\n{Fore.RED}passwords were not the same{Style.RESET_ALL}\n")
            password = getpass.getpass()
            password_repeat = getpass.getpass()
        if password == password_repeat:
            hashed_password = hash_with_salt(password).decode()
            db.insert_user_data(username, hashed_password)
            a = 1
            print(f"\n{Fore.GREEN}you've signed up seccessfully{Style.RESET_ALL}\n")
            return a

    if string == "sign in":
        username = input("username: ")
        password = getpass.getpass()
        confirmation, hashed_password = db.read_user_data(username)

        if confirmation:
            flag = check_password(password, hashed_password)

            if flag:
                print(f"\n{Fore.GREEN}User is verified\n{Style.RESET_ALL}")
                auth = 1
                return auth
                sys.exit()

            if not flag:
                print(f"{Fore.RED}\neither username or password is not correct\n{Style.RESET_ALL}")
                auth = 0
                return auth
                sys.exit()

        if not confirmation:
            print(f"\n{Fore.RED}either username or password is not correct\n{Style.RESET_ALL}")
            auth = 0
            return auth
            sys.exit()





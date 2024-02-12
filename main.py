from pass_manager.pass_generator import gen_password
from pass_manager.save_pass import save_pass_in_database
from pass_manager.read_pass import read_pass_from_database
from database.database_manager import Database
from data_manager.manage_data import delete_data
from bins import create_neceseries
from colorama import Fore, Style
from user_auth.main import main
import getpass


def add(user_will):
    website = input("website(topic): ")
    user_name = input("username: ")
    genpassword, gensalt = gen_password(user_name)
    if 'set' in user_will:
        genpassword = input("\nset a password:\n\t").encode()
    token = save_pass_in_database(genpassword, gensalt)
    db.store_data(website, user_name, token.decode(), gensalt.decode())
    print(Fore.WHITE + "your password is: " + Fore.GREEN + genpassword.decode())
    if "add" and "several" in string:
        BOLD = '\033[1m'
        END = '\033[0m'
        user_will = input(f"{BOLD}{Fore.LIGHTBLUE_EX}genpass {END}{Fore.GREEN}--> {Fore.MAGENTA}it will generate an strong password\n{BOLD}{Fore.LIGHTBLUE_EX}setpass {END}{Fore.GREEN}--> {Fore.MAGENTA}set your own password{Style.RESET_ALL}\n\n\t")
        add(user_will)


def find():
    a = main('sign in')
    if a:
        website = input("websitename: ")
        token, salt, username = db.get_one_data(website)
        decrypted_password = read_pass_from_database(token.encode(), salt.encode())
        print(
            Fore.WHITE + "username: " + Fore.BLUE + username + Fore.WHITE + "\npassword: " + Fore.GREEN + decrypted_password)


def see_all():
    a = main('sign in')
    if a:
        db.get_all_data()


def delete():
    string = input("Enter the number of the entry you want to delete: ")
    n = int(string.split()[0])
    delete_data(n)


if __name__ == "__main__":
    string = input(
        f"\n{Fore.GREEN}add {Style.RESET_ALL}or {Fore.GREEN}add several {Fore.WHITE}--> {Fore.MAGENTA}it will save one or several passwords {Style.RESET_ALL}\n{Fore.YELLOW}find {Fore.WHITE}--> {Fore.MAGENTA}find a password with website name{Style.RESET_ALL}\n{Fore.BLUE}see * {Fore.WHITE}--> {Fore.MAGENTA}see all the passwords{Style.RESET_ALL}\n{Fore.RED}delete {Fore.WHITE}--> {Fore.MAGENTA} delete a pasword{Style.RESET_ALL}\n{Style.RESET_ALL}\n\n\t")
    db = Database("database/database.db")
    if "add" in string:
        BOLD = '\033[1m'
        END = '\033[0m'
        user_will = input(
            f"{BOLD}{Fore.LIGHTBLUE_EX}genpass {END}{Fore.GREEN}--> {Fore.MAGENTA}it will generate a strong password\n{BOLD}{Fore.LIGHTBLUE_EX}setpass {END}{Fore.GREEN}--> {Fore.MAGENTA}set your own password{Style.RESET_ALL}\n\n\t")
        add(user_will)
    elif "find" in string:
        find()
    elif "see" in string:
        see_all()
    elif "delete" in string:
        delete()




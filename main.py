from pass_manager.pass_generator import gen_password
from pass_manager.save_pass import save_pass_in_database
from pass_manager.read_pass import read_pass_from_database
from database.database_manager import Database
from data_manager.manage_data import delete_data
from bins import create_neceseries
from colorama import Fore,Style

def add(user_will):
    website = input("website: ")
    user_name = input("username: ")
    genpassword, gensalt = gen_password(user_name)
    if user_will == 'setpass':
        genpassword = input("\nset a password:\n\t").encode()
    token = save_pass_in_database(genpassword, gensalt)
    db.store_data(website, user_name, token.decode(), gensalt.decode())
    print(Fore.WHITE + "your password is: " + Fore.GREEN+ genpassword.decode())
    if "add" and "several" in string:
        BOLD = '\033[1m'
        END = '\033[0m'
        user_will = input(f"{BOLD}{Fore.LIGHTBLUE_EX}genpass {END}{Fore.GREEN}--> {Fore.MAGENTA}it will generate an strong password\n{BOLD}{Fore.LIGHTBLUE_EX}setpass {END}{Fore.GREEN}--> {Fore.MAGENTA}set your own password{Style.RESET_ALL}\n\n\t")
        add(user_will)


def find():
    website = input("websitename: ")
    token, salt, username = db.get_one_data(website)
    decrypted_password = read_pass_from_database(token.encode(), salt.encode())
    print(Fore.WHITE + "username: " + Fore.BLUE+ username+ Fore.WHITE +"\npassword: "+ Fore.GREEN + decrypted_password)

def see_all():
    db.get_all_data()

def delete():
    string = input("Enter the number of the entry you want to delete: ")
    n = int(string.split()[0])
    delete_data(n)

if __name__ == "__main__":
    string = input(f"{Fore.GREEN }add {Fore.WHITE}or {Fore.GREEN}add several\n{Fore.YELLOW}find \n{Fore.BLUE}see * \n{Fore.RED}delete\n\n\t{Style.RESET_ALL}")
    db = Database("database/database.db")
    if "add" in string:
        BOLD = '\033[1m'
        END = '\033[0m'
        user_will = input(f"{BOLD}{Fore.LIGHTBLUE_EX}genpass {END}{Fore.GREEN}--> {Fore.MAGENTA}it will generate an strong password\n{BOLD}{Fore.LIGHTBLUE_EX}setpass {END}{Fore.GREEN}--> {Fore.MAGENTA}set your own password{Style.RESET_ALL}\n\n\t")
        add(user_will)
    elif "find" in string:
        find()
    elif "see *" in string:
        see_all()
    elif "delete" in string:
        delete()

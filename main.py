from pass_manager.pass_generator import gen_password
from pass_manager.save_pass import save_pass_in_database
from pass_manager.read_pass import read_pass_from_database
from database.database_manager import Database
from data_manager.manage_data import delete_data
from bins import create_neceseries
from colorama import Fore, Style
from user_auth.main import main
import pyperclip
from import_from_google_pass.insert import add_data_from_csv
import sys

def make_url_std(url):
        # Check if the input starts with a valid prefix
    if url.startswith(("http://www.", "https://www.", "www.", "http://", "https://")):
        # Extract the domain part (excluding the prefix)
        domain_part = url.split("://")[-1].split("/")[0]

        # Check if the domain part contains any known extensions
        valid_extensions = [".com", ".ir", ".org"]  # Add more extensions if needed
        for ext in valid_extensions:
            if domain_part.endswith(ext):
                # Remove any path or query string after the extension
                cleaned_url = f"{url.split('://')[0]}://{domain_part}{ext}"
                return cleaned_url[:50] if len(cleaned_url) > 50 else cleaned_url

    # If none of the above, assume it's a domain without any prefix or extension
    cleaned_url = f"https://www.{url}"
    return cleaned_url[:50] if len(cleaned_url) > 50 else cleaned_url

def add(user_will):
    BOLD = '\033[1m'
    END = '\033[0m'
    name = input("website name: ").strip()
    url = input("url: ").strip()
    if len(url) == 0:
        url == '---'
    if len(url) != 0:
        url = make_url_std(url)
    user_name = input("username: ")
    genpassword, gensalt = gen_password(user_name)
    if 'set' in user_will:
        genpassword = input("password: ").strip().encode()
    note = input("note: ").strip()
    if len(note) == 0:
        note = '---'
    token = save_pass_in_database(genpassword, gensalt)
    db.store_data(name, url,  user_name, token.decode(), note, gensalt.decode())
    pyperclip.copy(genpassword.decode())
    print("your password is: " + BOLD +Fore.LIGHTCYAN_EX + genpassword.decode() + END +Style.RESET_ALL)
    print(f"{BOLD}{Fore.GREEN}Password is copied. Paste it anywhere you'd like.{Style.RESET_ALL}{END}")
    if "add" and "several" in command or "add" and "several" in string:
        user_will = input(f"\n{BOLD}{Fore.LIGHTBLUE_EX}genpass {END}{Fore.GREEN}--> {Fore.MAGENTA}it will generate an strong password\n{BOLD}{Fore.LIGHTBLUE_EX}setpass {END}{Fore.GREEN}--> {Fore.MAGENTA}set your own password{Style.RESET_ALL}\n\t").strip()
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
    a = main('sign in')
    if a:
        string = input("Enter the number of the entry you want to delete: ")
        n = int(string.split()[0])
        delete_data(n)


def import_csv():
    pass_list = add_data_from_csv()
    for i in pass_list:
        name= i[0]
        url = i[1]
        if len(url) != 0:
            url = make_url_std(url)
        username = i[2]
        password = i[3]
        note = i[4]
        if len(note) == 0:
            note = '---'
        genpassword, gensalt = gen_password(username)
        genpassword = password.encode()
        token = save_pass_in_database(genpassword, gensalt)
        db.store_data(name, url,  username, token.decode(), note, gensalt.decode())

    else:
        print(f'{Fore.GREEN}your passwords has been added successfully!{Style.RESET_ALL}')

if __name__ == "__main__":

    db = Database("database/database.db")

    command = []
    string = None

    if len(sys.argv) >= 2:
        command = sys.argv[1]
        string = command

    if len(sys.argv) < 2:
        string = input(
            f"\n{Fore.GREEN}add {Style.RESET_ALL}or {Fore.GREEN}add several {Fore.WHITE}--> {Fore.MAGENTA}it will save one or several passwords {Style.RESET_ALL}\n{Fore.YELLOW}find {Fore.WHITE}--> {Fore.MAGENTA}find a password with website name{Style.RESET_ALL}\n{Fore.BLUE}see * {Fore.WHITE}--> {Fore.MAGENTA}see all the passwords{Style.RESET_ALL}\n{Fore.RED}delete {Fore.WHITE}--> {Fore.MAGENTA} delete a pasword{Style.RESET_ALL}\n{Style.RESET_ALL}import CSV{Fore.WHITE} --> {Fore.MAGENTA}import passwords from a csv file{Style.RESET_ALL}\n\t").strip()
   
    if "add" in string or "add" in command:
        BOLD = '\033[1m'
        END = '\033[0m'
        user_will = input(
            f"{BOLD}{Fore.LIGHTBLUE_EX}genpass {END}{Fore.GREEN}--> {Fore.MAGENTA}it will generate a strong password\n{BOLD}{Fore.LIGHTBLUE_EX}setpass {END}{Fore.GREEN}--> {Fore.MAGENTA}set your own password{Style.RESET_ALL}\n\t").strip()
        add(user_will)

    elif "find" in string or "find" in command:
        find()

    elif "see" in string or "see" in command:
        see_all()
        
    elif "delete" in string or "delete" in command:
        delete()

    elif "csv" or "import" in string:
        import_csv()
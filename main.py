# Import the necessary libraries
from import_from_google_pass.insert import read_cav_file
from pass_manager.pass_generator import gen_password
from pass_manager.pass_manager import decrypt_pass
from pass_manager.pass_manager import encrypt_pass
from data_manager.manage_data import delete_data
from database.database_manager import Database
from bins import create_neceseries
from colorama import Fore, Style
from user_auth.main import main
from datetime import datetime
from time import sleep
import pyperclip
import sys

# function to standardizes the user's URL input
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
                cleaned_url = f"{url.split('://')[0]}://{domain_part}"
                return cleaned_url[:50] if len(cleaned_url) > 50 else cleaned_url

    # If none of the above, assume it's a domain without any prefix or extension
    cleaned_url = f"https://www.{url}"
    return cleaned_url[:50] if len(cleaned_url) > 50 else cleaned_url


# function to add passwords to database
# user_will argument --> is used to determine if user want a generated password or not.
def add(user_will):

    # shorcut to bold the text(it will be used later)
    BOLD = '\033[1m'
    END = '\033[0m'

    # get input from user
    name = input("website name: ").strip()
    url = input("url: ").strip()
    user_name = input("username: ")

    # put "---" in url field if user left the field blank
    if len(url) == 0:
        url == '---'
    if len(url) != 0:
        url = make_url_std(url)

    # function to generate a strong password and salt(for encrypting)
    # gen_password func is in ./pass_manager/pass_generator.py 
    genpassword, gensalt = gen_password(user_name)

    # ask for a password word if user didn't want to use generated one
    if 'set' in user_will:
        genpassword = input("password: ").strip().encode()
    
    # handle the note field
    note = input("note: ").strip()
    if len(note) == 0:
        note = '---'
    
    # function to encrypt and save the passwords in database
    # encrypt_pass func is in ./pass_manager/pass_manager.py
    token = encrypt_pass(genpassword, gensalt)

    # using Databse calass store data in database 
    # Databse calass is in ./database/database_manager.py
    # using pyperclip to copyt the password in clipboear
    db.store_data(name, url,  user_name, token.decode(), note, gensalt.decode())
    pyperclip.copy(genpassword.decode())
    print("your password is: " + BOLD +Fore.LIGHTCYAN_EX + genpassword.decode() + END +Style.RESET_ALL)
    print(f"{BOLD}{Fore.GREEN}Password is copied. Paste it anywhere you'd like.{Style.RESET_ALL}{END}")
    
    # check if user wanted to added  more passwords or not
    if "add" and "several" in command or "add" and "several" in string:
        print(f"{BOLD}OPTIONS{END}")
        print("\tThe following options are understood:\n")
        print(f"\t{BOLD}genpass{END}")
        print("\t\tit will generate a strong password.")
        print(f"\n\t{BOLD}setpass{END}")
        print("\t\tset your own password.")
        user_will = input().strip()
        add(user_will)


# function to find a specific password by searching website name in databse
def find():
    # a is a bool value: if True --> user is verified if False --> user is not verified
    # main func is in ./user_auth/main.py 
    a = main('sign in')

    if a:
        website = input("websitename: ")
        # using Databse class to find a specific sign in data by website name
        token, salt, username = db.get_one_data(website)

        # decrypting the encrypted password
        # decript_pass func is in ./pass_manager/pass_manager.py
        decrypted_password = decrypt_pass(token.encode(), salt.encode())
        print(
            Fore.WHITE + "username: " + Fore.BLUE + username + Fore.WHITE + "\npassword: " + Fore.GREEN + decrypted_password)

# function to show user all data in database
def see_all():
    # a is a bool value: if True --> user is verified if False --> user is not verified
    # main func is in ./user_auth/main.py 
    a = main('sign in')
    if a:
        # using Databse class to show all data to user
        db.get_all_data()

# function for delete an intry from database
def delete():
    # a is a bool value: if True --> user is verified if False --> user is not verified
    # main func is in ./user_auth/main.py 
    a = main('sign in')
    if a:
        # using the delete_data func to delete  an entry from database
        #  delete_data func is in ./data_manager/manage_data.py
        string = input("Enter the number of the entry you want to delete: ")
        n = int(string.split()[0])
        delete_data(n)

# funceion for import data in to database using a csv file
def import_csv():
    # a is a bool value: if True --> user is verified if False --> user is not verified
    # main func is in ./user_auth/main.py 
    a = main('sign in')

    if a:
        # useing read_cav_file func to reade the csv file and orgnize the data
        pass_list = read_cav_file()
        # delte the first row of csv file data --> is gonna be the headers of our table
        del pass_list[0]

        for i in pass_list:
            # manage the data in pass_list
            name= i[0]
            url = i[1]
            if len(url) != 0:
                url = make_url_std(url)
            username = i[2]
            password = i[3]
            note = i[4]
            if len(note) == 0:
                note = '---'
            # generate a salt and encrypt the pass word
            # gen_password func is in ./pass_manager/pass_generator.py 
            genpassword, gensalt = gen_password(username)
            genpassword = password.encode()
            token = encrypt_pass(genpassword, gensalt)

            # using Databse calass store data in database 
            # Databse calass is in ./database/database_manager.py
            # using pyperclip to copyt the password in clipboear
            db.store_data(name, url,  username, token.decode(), note, gensalt.decode())

        else:
            print(f'{Fore.GREEN}your passwords has been added successfully!{Style.RESET_ALL}')


# function to create an initial list fot export all date in a csv file using export_csv function later
# passwords will be decrypted and visible in the csv file
def export_init():
    # a is a bool value: if True --> user is verified if False --> user is not verified
    # main func is in ./user_auth/main.py 
    a = main('sign in')
    csv_material = [] # a list that will go into the export_csv function later

    if a:
        raw_data = db.get_data_for_csv()
        # this is gonna be user to create a percentage bar during decrypting file
        total_records = len(raw_data)

        for i, data in enumerate(raw_data):
            name, url, username, token, note, salt = data
            decrypted_password = decrypt_pass(token.encode(), salt.encode())
            csv_material.append((name, url, username, decrypted_password, note))

            # Update the percentage bar
            progress = (i + 1) / total_records
            bar_length = 50
            filled_length = int(bar_length * progress)
            bar = f"[{'=' * filled_length}{' ' * (bar_length - filled_length)}] {progress * 100:.2f}%"
            sys.stdout.write(f"\r{bar}")
            sys.stdout.flush()

            # Simulate some work (remove this line in your actual code)
            sleep(0.01)

        print()  # Add a newline after processing

        return csv_material
    
    else:
        sys.exit()


# function create the csv file
def export_csv(data=list):
    #date time for using in the name of the csv file
    now = datetime.now()
    formatted_date_time = now.strftime("%B_%d_%Y_%H:%M:%S")
    # create the header line (start_p) and write it in csv file
    start_p = 'name,url,username,password,note\n'
    f = open(f'export/Passwords_{formatted_date_time}.csv', 'a').write(start_p)
    for i in data:
        #write the database data in to csv file
        string = f'{i[0]},{i[1]},{i[2]},{i[3]},{i[4]}\n'
        f = open(f'export/Passwords_{formatted_date_time}.csv', 'a').write(string)

        

if __name__ == "__main__":

    db = Database("database/database.db")
    BOLD = '\033[1m'
    END = '\033[0m'
    command = []
    string = None

    if len(sys.argv) >= 2:
        command = sys.argv[1]
        string = command

    if len(sys.argv) < 2:
        print(f"{BOLD}OPTIONS{END}")
        print("\tThe following options are understood:\n")
        print(f"\t{BOLD}find{END}")
        print("\t\tFind a password with the website name.")
        print(f"\n\t{BOLD}all{END}")
        print("\t\tSee all saved passwords.")
        print(f"\n\t{BOLD}delete{END}")
        print("\t\tDelete a specific password.")
        print(f"\n\t{BOLD}import CSV{END}")
        print("\t\tImport passwords from a CSV file.")
        print(f"\n\t{BOLD}export{END}")
        print("\t\tExport passwords to a CSV file (decrypted).")
        string = input().strip()

    if "add" in string or "add" in command:
        BOLD = '\033[1m'
        END = '\033[0m'
        print(f"{BOLD}OPTIONS{END}")
        print("\tThe following options are understood:\n")
        print(f"\t{BOLD}genpass{END}")
        print("\t\tit will generate a strong password.")
        print(f"\n\t{BOLD}setpass{END}")
        print("\t\tset your own password.")

        user_will = input().strip()
        add(user_will)

    if "find" in string.lower() or "find" in command:
        find()

    if "all" in string.lower() or "all" in command:
        see_all()
        
    if "delete" in string.lower() or "delete" in command:
        delete()

    if "csv" and "import" in string.lower() or "csv" and "import" in command:
        import_csv()

    if "export" in string.lower():
        csv_material = export_init()
        export_csv(csv_material)
        print("the csv file is in secure-password-manager/export directory.")
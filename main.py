from pass_manager.pass_generator import gen_password
from pass_manager.save_pass import save_pass_in_database
from pass_manager.read_pass import read_pass_from_database
from database.database_manager import Database
from data_manager.manage_data import delete_data

def add():
    website = input("website: ")
    user_name = input("username: ")
    genpassword, gensalt = gen_password(user_name)
    token = save_pass_in_database(genpassword, gensalt)
    db.store_data(website, user_name, token.decode(), gensalt.decode())
    print("your password is: ", genpassword.decode())

def find():
    website = input("websitename: ")
    token, salt, username = db.get_one_data(website)
    decrypted_password = read_pass_from_database(token.encode(), salt.encode())
    print("username: ", username, "\npassword: ", decrypted_password)

def see_all():
    db.get_all_data()

def delete():
    string = input("Enter the number of the entry you want to delete: ")
    n = int(string.split()[0])
    delete_data(n)

if __name__ == "__main__":
    string = input("add \nfind \nsee * \ndelete\n\n\t")
    db = Database("database/database.db")
    if string == "add":
        add()
    elif string =="find":
        find()
    elif string =="see *":
        see_all()
    elif "delete" in string:
        delete()

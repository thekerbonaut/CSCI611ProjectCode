#database code adapted from https://stackoverflow.com/questions/54267646/i-want-to-use-json-in-python-to-save-users-and-password/54268080
# and https://pynative.com/python-sqlite-insert-into-table/
#logging code adapted from https://realpython.com/python-logging/
#menu code adapted from https://computinglearner.com/how-to-create-a-menu-for-a-python-console-application/

#Code from Unknown Source
import rsa
import logging
import sqlite3 as sql
import hashlib
import uuid

def admin_program():
    #start logging
    logging.basicConfig(level=logging.DEBUG, filename='admin.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    logging.info("Admin program started")

    print("Welcome to the admin program")
    auth = authenticate()
    while auth == True:
        menu()
    else:
        print("Authentication failed")

def authenticate():
    #get user credentials
    user, password = get_credentials()
    #check user credentials
    dbconn = sql.connect('users.db')
    dbcur = dbconn.cursor()

    try:
        row = dbcur.execute("SELECT salt, password, admin FROM users WHERE username = '{}'".format(user)).fetchone()
        salt, hashpass, admin = row  # Unpacking the row information - btw this would fail if the username didn't exist
    except:
        print("Username not found")
        return False

    hashedIncomingPwd = hashlib.sha512((salt + password).encode("UTF-8")).hexdigest()

    if hashedIncomingPwd == hashpass:
        if admin == True:
            print("logged in")
            logging.info("Successful login, user: " + user)
            return True
        else:
            print("Insufficient privileges")
            logging.info("Insufficient privileges, user: " + user)
            return False
    else:
        print("incorrect password")
        logging.warning("Incorrect password, user: " + user)
        return False

def menu():
    #display menu
    menu_options = {
        1: 'Add user',
        2: 'Delete user',
        3: 'Exit'
    }
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

    option = int(input('Enter your choice: ')) 
    if option == 1:
        add_user()
    elif option == 2:
        delete_user()
    elif option == 3:
        print("Exiting program")
        quit()
    else:
        print('Invalid option. Please enter a number between 1 and 3.')

def get_credentials():
    user = input("Enter Username -> ")
    password = input("Enter Password -> ")
    return user, password

def add_user():
    newuser, newpassword = get_credentials()
    newadmin = ''
    print("Add to admin list?")
    admin_options = {
        0: 'No',
        1: 'Yes'
    }
    for key in admin_options.keys():
        print (key, '--', admin_options[key] )
    option = int(input('Enter your choice: ')) 
    if option == 0 or option == 1:
        newadmin = option
    else:
        print('Invalid option')
        menu()
    #connect to database
    dbconn = sql.connect('users.db')
    dbcur = dbconn.cursor()
    #hash password
    salt = uuid.uuid4().hex
    hashedpassword = hashlib.sha512((salt + newpassword).encode("UTF-8")).hexdigest()
    #add new user
    add_user_sql = "INSERT INTO users (username, salt, password, admin) VALUES (?, ?, ?, ?);"
    new_user_data = (newuser, salt, hashedpassword, newadmin)
    dbcur.execute(add_user_sql, new_user_data)
    dbconn.commit()
    print("Added new user")
    return

def delete_user():
    user = input("Enter Username -> ")
    #connect to database
    dbconn = sql.connect('users.db')
    dbcur = dbconn.cursor()
    #delete user
    delete_user_sql = "DELETE FROM users WHERE username = ?"
    dbcur.execute(delete_user_sql, (user,))
    dbconn.commit()
    print("Deleted user")
    return

if __name__ == '__main__':
    admin_program()
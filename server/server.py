#Code from Unknown Source
import socket
import rsa
from cryptography.fernet import Fernet
import logging
import sqlite3 as sql
import hashlib
import uuid
from datetime import datetime

#This class contains connection information
class Connection:
    def __init__(self):
        self.host = socket.gethostname()
        self.port = 5000

        self.server_socket = socket.socket()
        self.server_socket.bind((self.host, self.port))

        self.conn = None
        self.address = None

        self.auth = False

        #import asymmetric keys
        with open('serverprivate.pem', mode='rb') as privatefile:
            keydata = privatefile.read()
        self.serverprivkey = rsa.PrivateKey.load_pkcs1(keydata)

        with open('clientpublic.pem', mode='rb') as publicfile:
            keydata = publicfile.read()
        self.clientpubkey = rsa.PublicKey.load_pkcs1(keydata)
        
        #generate symmetric key
        self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)

def server_program():
    #start logging
    logging.basicConfig(level=logging.DEBUG, filename='logs/server.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
    logging.info(str(datetime.now()) + " Server program started")

    connection.server_socket.listen(2)
    connection.conn, connection.address = connection.server_socket.accept()
    logging.info(str(datetime.now()) + " Connection from: " + str(connection.address)) 
    print("Connection from: " + str(connection.address))
    connection.auth = authenticate(decrypt_message(connection.conn.recv(1024)))
    while connection.auth == True:
     
        data = decrypt_message(connection.conn.recv(1024))
        if not data:
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        send_message(data)

    connection.conn.close()
    auth = False
    print("connection closed")

def authenticate(creds):
    c = creds.split(',')
    user = c[0]
    password = c[1]

    #check user credentials
    dbconn = sql.connect('users.db')
    dbcur = dbconn.cursor()

    try:
        row = dbcur.execute("SELECT salt, password, admin FROM users WHERE username = '{}'".format(user)).fetchone()
        salt, hashpass, admin = row  # Unpacking the row information - btw this would fail if the username didn't exist
    except:
        print("Username not found")
        logging.info(str(datetime.now()) + " Failed login, user: " + user)
        return False

    hashedIncomingPwd = hashlib.sha512((salt + password).encode("UTF-8")).hexdigest()

    if hashedIncomingPwd == hashpass:
        #logging in as admin vs user is exactly the same right now, 
        # its just there for use in a server adminstration program that I wrote seperately
        if admin == True:
            print("logged in as admin")
            logging.info(str(datetime.now()) + " Successful login, user: " + user)
            send_message(connection.key)
            return True
        else:
            print("logged in as user")
            send_message(connection.key)
            logging.info(str(datetime.now()) + ' Successful login, user: ' + user)
            return True
    else:
        print("incorrect password")
        logging.warning(str(datetime.now()) + " Incorrect password, user: " + user)
        return False

def encrypt_message(m):
    if connection.auth == True:
        #use symmetric key
        return connection.fernet.encrypt(m.encode())
    else:
        #use asymmetric keys
        if type(m) != bytes:
            m = m.encode()
        return rsa.encrypt(m, connection.clientpubkey)
    
def decrypt_message(m):
    if connection.auth == True:
        #use symmetric key
        return connection.fernet.decrypt(m).decode()
    else:
        #use asymmetric keys
        return rsa.decrypt(m, connection.serverprivkey).decode()

def send_message(m):
    connection.conn.send(encrypt_message(m))

if __name__ == '__main__':
    #create a connection object and start the server
    connection = Connection()
    server_program()
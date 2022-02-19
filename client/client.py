#Code from Unknown Source
import socket
import rsa
from cryptography.fernet import Fernet

class Connection:
    def __init__(self):
        #hard coded options for testing purposes as well as options for getting user input

        #connection.host = input("IP -> ")
        #connection.host = '10.104.112.242'
        #connection.port = 62034
        #connection.port = int(input("Port -> "))       
        self.host = socket.gethostname()
        self.port = 5000

        self.client_socket = socket.socket()  
        self.client_socket.connect((self.host, self.port))

        #this flag is used to indicate succesful authentication after which the program switches to symmetric key encryption
        self.auth = False

        #import asymmetric keys
        with open('serverpublic.pem', mode='rb') as publicfile:
            keydata = publicfile.read()
        self.serverpubkey = rsa.PublicKey.load_pkcs1(keydata)
                            
        with open('clientprivate.pem', mode='rb') as privatefile:
            keydata = privatefile.read()
        self.clientprivkey = rsa.PrivateKey.load_pkcs1(keydata)

        #symmetric key will be stored here after it is received from server
        self.key = None
        self.fernet = None

def client_program():
    authenticate()
    #once authentication has been succesfully completed, exchange messages
    while connection.auth == True:
        message = input(" -> ") 
        send_message(message)
        data = decrypt_message(connection.client_socket.recv(1024))
        print('Received from server: ' + data)

    connection.client_socket.close()
    print("connection closed")

def authenticate():
    #get user credentials
    user = input("Enter Username -> ")
    password = input("Enter Password -> ")
    credentials = user + ',' + password
    #send credentials
    send_message(credentials)
    #recieve symmetric key from server
    connection.key = decrypt_message(connection.client_socket.recv(1024))
    connection.fernet = Fernet(connection.key)
    connection.auth = True

def encrypt_message(m):
    #choose encryption method based off of authentication state
    if connection.auth == True:
        #use symmetric key
        return connection.fernet.encrypt(m.encode())
    else:
        #use asymmetric keys
        return rsa.encrypt(m.encode(), connection.serverpubkey)

def decrypt_message(m):
    #choose decryption method based off of authentication state
    if connection.auth == True:
        #use symmetric key
        return connection.fernet.decrypt(m).decode()
    else:
        #use asymmetric keyss
        return rsa.decrypt(m, connection.clientprivkey).decode()

def send_message(m):
    #encrypt message and send
    connection.client_socket.send(encrypt_message(m))

if __name__ == '__main__':
    #create a connection object and start the client
    connection = Connection()
    client_program()

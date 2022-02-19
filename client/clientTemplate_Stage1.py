#Code from Unknown Source
import socket
import rsa
from cryptography.fernet import Fernet

def client_program():
    host = socket.gethostname()  # Running on Same PC
    #host = input("IP -> ")
    #host = '10.104.112.242'
    #port = 62034
    port = 5000
    #port = int(input("Port -> "))

    with open('public.pem', mode='rb') as publicfile:
        keydata = publicfile.read()
    pubkey = rsa.PublicKey.load_pkcs1(keydata)

    client_socket = socket.socket()  
    client_socket.connect((host, port))

    #send credentials
    user = input("Enter Username -> ")
    password = input("Enter Password -> ")
    credentials = user + ',' + password
    #encrypt credentials
    encMessage = rsa.encrypt(credentials.encode(), pubkey)
    #send credentials
    client_socket.send(encMessage)



    message = ""
    connected = True
    

    while connected == True:
        client_socket.send(message.encode())
        data = client_socket.recv(1024).decode()
        
        #print('Received from server: ' + data)
        
        if data == 'incorrect credentials':
            connected = False
            print('Connection Terminated')
            break
        else:
            key = ""

        message = input(" -> ")  

    client_socket.close()
    

#def encrypt_message(m):
    

if __name__ == '__main__':
    client_program()

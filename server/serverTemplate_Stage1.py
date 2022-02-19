#Code from Unknown Source
import socket
import rsa
from cryptography.fernet import Fernet

def server_program():
    
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket()  
    # Notice 2 arguments for the bind. Why is that?
    server_socket.bind((host, port))

    auth = False

    user = 'test'
    password = 'test'

    key = Fernet.generate_key()
    fernet = Fernet(key)

    with open('private.pem', mode='rb') as privatefile:
        keydata = privatefile.read()
    privkey = rsa.PrivateKey.load_pkcs1(keydata)
    
    server_socket.listen(2)
    conn, address = server_socket.accept()  
    print("Connection from: " + str(address))

    if auth == False:
        credentials = rsa.decrypt(conn.recv(1024), privkey).decode()
        print('Credentials = ' + credentials)
        c = credentials.split(',')

    if c[0] == user and c[1] == password:
        print('correct credentials')
        #data =  "connected"
        auth = True
        #conn.send(data.encode())
        conn.send(rsa.encrypt(key.encode()))
    else:
        print('incorrect credentials')
        data = 'incorrect credentials'
        conn.send(data.encode())
        conn.close()
        auth = False
        
    while auth == True:
     
        data = conn.recv(1024).decode()
        if not data:
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())

    conn.close()
    auth = False

if __name__ == '__main__':
    server_program()

import rsa

#keygen function has been tested
def keygen_program():
    SERVER_PUB_KEY_DST = 'client\\serverpublic.pem'
    SERVER_PRIV_KEY_DST = 'server\\serverprivate.pem'
    CLIENT_PUB_KEY_DST = 'server\\clientpublic.pem'
    CLIENT_PRIV_KEY_DST = 'client\\clientprivate.pem'
    
    (pubkey, privkey) = rsa.newkeys(2048)
    with open(SERVER_PUB_KEY_DST, 'wb+') as f:
        pk = rsa.PublicKey.save_pkcs1(pubkey, format='PEM')
        f.write(pk)
    with open(SERVER_PRIV_KEY_DST, 'wb+') as f:
        pk = rsa.PrivateKey.save_pkcs1(privkey, format='PEM')
        f.write(pk)
        
    (pubkey, privkey) = rsa.newkeys(2048)
    with open(CLIENT_PUB_KEY_DST, 'wb+') as f:
        pk = rsa.PublicKey.save_pkcs1(pubkey, format='PEM')
        f.write(pk)
    with open(CLIENT_PRIV_KEY_DST, 'wb+') as f:
        pk = rsa.PrivateKey.save_pkcs1(privkey, format='PEM')
        f.write(pk)

if __name__ == '__main__':
    #Menu code is untested
    option = input("WARNING: This action will overwrite existing keys! Proceed (Y/n): ")

    if option == 'y' or option == 'Y':
        print("Generating new keys")
        keygen_program()
    elif option == 'n' or option == 'N':
        print("Exiting program")
        quit()
    else:
        print('Invalid option.')
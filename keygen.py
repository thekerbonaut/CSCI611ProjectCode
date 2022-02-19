import rsa

def keygen_program():
    PUB_KEY_DST = '\\public.pem'
    PRIV_KEY_DST = '\\private.pem'
    
    (pubkey, privkey) = rsa.newkeys(2048)
    with open(PUB_KEY_DST, 'wb+') as f:
        pk = rsa.PublicKey.save_pkcs1(pubkey, format='PEM')
        f.write(pk)
    with open(PRIV_KEY_DST, 'wb+') as f:
        pk = rsa.PrivateKey.save_pkcs1(privkey, format='PEM')
        f.write(pk)
        
if __name__ == '__main__':
    keygen_program()

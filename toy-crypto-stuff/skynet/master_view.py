import os, sys
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

def decrypt_valuables(f, rsa_key):
    # set cipher block size
    encrypted_data = f
    block_size = 512
    # can decrypt encrypted uploads
    # can NOT decrypt signed and encrypted uploads
    # CAN verify signed and encrypted uploads
    if len(encrypted_data) % block_size != 0:
        raise RuntimeError("Decryption Failed")
    decoded_text = ''
    # spawn cipher
    z_cipher = PKCS1_OAEP.new(rsa_key)
    # iterate through blocks, decrypting each
    for i in range(int(len(encrypted_data) / block_size)):
        decoded_text += z_cipher.decrypt(encrypted_data[( block_size * i ) : ( block_size * ( i + 1 ))]).decode("utf-8")
    print(decoded_text)

if __name__ == "__main__":
    fn = input("Which file in pastebot.net does the botnet master want to view? ")
    if not os.path.exists(os.path.join("pastebot.net", fn)):
        print("The given file doesn't exist on pastebot.net")
        sys.exit(1)
    f = open(os.path.join("pastebot.net", fn), "rb").read()
    key_file = open("keys/client_private.pem", 'r')
    rsa_key = RSA.importKey(key_file.read())
    key_file.close()    
    decrypt_valuables(f, rsa_key)

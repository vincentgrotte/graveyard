import os, sys
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA

def sign_file(f, rsa_key):
    # spawns a signature and appends it to the file
    h = SHA.new()
    h.update(f)
    return f + PKCS1_PSS.new(rsa_key).sign(h)

if __name__ == "__main__":
    fn = input("Which file in pastebot.net should be signed? ")
    if not os.path.exists(os.path.join("pastebot.net", fn)):
        print("The given file doesn't exist on pastebot.net")
        sys.exit(1)
    f = open(os.path.join("pastebot.net", fn), "rb").read()
    key_file = open("keys/client_private.pem", 'r')
    rsa_key = RSA.importKey(key_file.read())
    key_file.close()
    signed_f = sign_file(f, rsa_key)
    signed_fn = os.path.join("pastebot.net", fn + ".signed")
    out = open(signed_fn, "wb")
    out.write(signed_f)
    out.close()
    print("Signed file written to", signed_fn)

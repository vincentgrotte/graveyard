import struct
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA, SHA256
from lib.helpers import read_hex

from dh import create_dh_key, calculate_dh_secret

class StealthConn(object):
    def __init__(self, conn, rsa_key, client=False, server=False, verbose=False):
        self.conn = conn
        self.cipher = None
        self.client = client
        self.server = server
        self.verbose = verbose
        self.rsa_key = rsa_key
        self.mac_size = 8
        self.initiate_session()

    def initiate_session(self):
        # spawn key material
        my_public_key, my_private_key = create_dh_key()
        # set some "magic numbers" - ie. "key material" sizes
        iv_length = AES.block_size
        key_length = 256
        sig_length = iv_length + key_length

        # if we are in "client" mode - we receive an encrypted-authentication package from the server.
        # the "client" has to extract an IV and a public key from the package, and use these materials
        # to create a "signature", which is appended to a message that is sent to the server.

        if self.client:
            # receive package
            encrypted_data = self.recv()
            # spawn the auth cipher and decrypt the package
            data = PKCS1_OAEP.new(self.rsa_key).decrypt(encrypted_data)
            # grab the iv from the start of the package
            self.iv = int.from_bytes(data[:iv_length], byteorder='big')
            # grab the public key from the back of the package
            their_public_key = int.from_bytes(data[iv_length + 1:], byteorder='big')
            # make a new message with the IV and OUR OWN public key
            message = data[:iv_length] + b' ' + my_public_key.to_bytes(key_length, byteorder='big')
            h = SHA.new()
            # hash the message
            h.update(message)
            # spawn an rsa signature and sign it with the hashed message and append the signature to the message
            # --> send message to server (send function has encryption)
            self.send(message + bytes(' ',"ascii") + PKCS1_PSS.new(self.rsa_key).sign(h))

        # if we are in "server" mode - we generate our own IV and package it with our public key material.
        # this message is encrypted and sent to the "client".
        # the IV's of the returned message and our own can be compared directly to preserve integrity

        if self.server:
            # spawn initialization vector
            self.iv = int.from_bytes(Random.new().read(iv_length), byteorder='big')
            # concatenate the iv and the server public key
            message = self.iv.to_bytes(iv_length, byteorder='big') + bytes(' ', "ascii") + my_public_key.to_bytes(key_length, byteorder='big')
            # spawn the auth cipher, encrypt the message and send
            self.send(PKCS1_OAEP.new(self.rsa_key).encrypt(message))
            # wait for response
            response = self.recv()
            # IV integrity check
            if int.from_bytes(response[:iv_length], byteorder='big') != self.iv:
                raise RuntimeError("Poisoned IV")
            # spawn hash
            h = SHA.new()
            # peel off the signature
            h.update(response[:(sig_length + 1)])
            # spawn signer
            signer = PKCS1_PSS.new(self.rsa_key)
            # signature integrity check     
            if not signer.verify(h, response[(sig_length + 2):]):
                raise RuntimeError("...This isn't the master...")
            # we extract the client's public key
            their_public_key = int.from_bytes(response[(iv_length + 1):(sig_length + 1)], byteorder='big')

        # spawn the shared secret
        shared_hash = calculate_dh_secret(their_public_key, my_private_key)
        print("Shared hash: {}".format(shared_hash))
        
        # spawn the cipher using gathered keying materials
        self.cipher = AES.new(shared_hash, AES.MODE_CFB, self.iv.to_bytes(iv_length, byteorder='big'));
        print("Authentication Successful")

    def send(self, data):
        if self.cipher:
            # grab the data, spawn an hmac, append it, encrypt the whole thing and send it down the pipe
            z_hmac = read_hex(SHA256.new(data).hexdigest()).to_bytes(32, 'big')[:self.mac_size]
            data = data + z_hmac
            encrypted_data = self.cipher.encrypt(data)
            if self.verbose:
                print("Original data: {}".format(data))
                print("Encrypted data: {}".format(repr(encrypted_data)))
                print("Sending packet of length {}".format(len(encrypted_data)))
        else:
            encrypted_data = data

        # Encode the data's length into an unsigned two byte int ('H')
        pkt_len = struct.pack('H', len(encrypted_data))
        self.conn.sendall(pkt_len)
        self.conn.sendall(encrypted_data)

    def recv(self):
        # Decode the data's length from an unsigned two byte int ('H')
        pkt_len_packed = self.conn.recv(struct.calcsize('H'))
        unpacked_contents = struct.unpack('H', pkt_len_packed)
        pkt_len = unpacked_contents[0]
        encrypted_data = self.conn.recv(pkt_len)

        if self.cipher:
            # ez decryptz
            data = self.cipher.decrypt(encrypted_data)
            if self.verbose:
                print("Receiving packet of length {}".format(pkt_len))
                print("Encrypted data: {}".format(repr(encrypted_data)))
                print("Original data: {}".format(data))
            # peel ze MAC
            z_hmac = read_hex(SHA256.new(data[:-self.mac_size]).hexdigest()).to_bytes(32, 'big')[:self.mac_size]
            # MAC integrity check
            if z_hmac != data[-self.mac_size:]:
                print('Bad Mac')
                self.close()
            data = data[:-self.mac_size]
        else:
            data = encrypted_data

        return data

    def close(self):
        self.conn.close()

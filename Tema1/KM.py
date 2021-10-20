import socket
import sys
import time
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from os import urandom

iv = '01020304050607080102030405060708'

def generate_cbc_key(given_key):
    secret_key = urandom(32)
    cipher = AES.new(given_key.encode(), AES.MODE_CBC)
    key = cipher.encrypt(secret_key)
    return str(key)

def generate_ecb_key(given_key):
    secret_key = urandom(32)
    cipher = AES.new(given_key.encode(), AES.MODE_ECB)
    key = cipher.encrypt(secret_key)
    return str(key)


def realize_connection(HOST, PORT, given_key):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    print("Conecting.. ")
    sock.connect(server_address)
    # while True:
    mode = sock.recv(1024)
    mode = mode.decode('utf-8')
    sock.send(str.encode(iv))
    if mode == 'CBC':
        key = generate_cbc_key(given_key)
    elif mode == 'ECB':
        key = generate_ecb_key(given_key)
    sock.send(str.encode(key))
        # print(data.decode('utf-8'))
        # message = input("Enter message: ")
        # sock.send(str.encode(message))
    sock.close()

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT_KM = 8000
    key = 'alabalaportocalaalabalaportocala' # de generat random cheia
    realize_connection(HOST, PORT_KM, key)
    
    
import socket
from base64 import b64encode
from os import urandom
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes

def dec_cbc(k_prim, iv, ct):
    cipher = AES.new(k_prim, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), AES.block_size)

def dec_ecb(k, message):
    cipher = AES.new(k.encode(), AES.MODE_ECB)
    return cipher.decrypt(message)

def realize_connection(HOST, PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    print("B Connected.")
    sock.connect(server_address)
    mode = sock.recv(4).decode('utf-8')
    # print("Mode: ")
    # print(mode)
    if mode == 'ECB':
        k_prim = sock.recv(16).decode('utf-8')
        en_k = sock.recv(1024)
        # print("K_prim: ")
        # print(k_prim)
        # print("Key: ")
        # print(en_k)
        print("K is:")
        pt  = dec_ecb(k_prim, en_k)
        print(pt)
    elif mode == 'CBC':
        file2 = open("iv.txt", 'rb')
        iv = file2.read()
        file2.close()
        
        k_prim = sock.recv(16)
        # print("K_prim: ")
        # print(k_prim)
        # print("iv: ")
        # print(iv)
        en_k = sock.recv(1024)
        # print("Key: ")
        # print(en_k)
        pt = dec_cbc(k_prim, iv, en_k)
        print("K is:")
        print(pt)
   
    sock.close()

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT_B = 4000
    realize_connection(HOST, PORT_B)
    
    

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
    

def realize_connection(HOST, PORT_B, PORT_KM):
    sock_km = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address_km = (HOST, PORT_KM)
    sock_km.bind(server_address_km)
    sock_km.listen(1)
    connection_km, client_address_km = sock_km.accept()
    print("Connected with KM.")
    sock_b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address_b = (HOST, PORT_B)
    sock_b.bind(server_address_b)
    sock_b.listen(1)
    connection_b, client_address_b = sock_b.accept()
    print("Connected with B.")
    
    mode = input("Choose a mode to operate: \nECB \nCBC\n")
    connection_km.send(str.encode(mode))
    connection_b.send(str.encode(mode))
    # iv = connection_km.recv(16)
    if mode == 'ECB':
        k_prim = connection_km.recv(16).decode('utf-8')
        connection_b.send(k_prim.encode())
        # print("K_prim: ")
        # print(k_prim)
        k = connection_km.recv(1024)
        # print("Key: ")
        # print(k)
        connection_b.send(k)
        
        print("K is:")
        pt = dec_ecb(k_prim, k)
        print(pt)
        
    elif mode == 'CBC':
        k_prim = connection_km.recv(16)
        # print("K_prim: ")
        # print(k_prim)
        connection_b.send(k_prim)
        en_k = connection_km.recv(1024)
        connection_b.send(en_k)
        
        file1 = open("iv.txt", 'rb')
        iv = file1.read()
        file1.close()
        # print("iv: ")
        # print(iv)
        # print("Key: ")
        # print(en_k)
        pt = dec_cbc(k_prim, iv, en_k)
        print("K is:")
        print(pt)
    
    connection_b.close()
    connection_km.close()
    

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT_B = 4000
    PORT_KM = 6000
    realize_connection(HOST, PORT_B, PORT_KM)
    
    
    

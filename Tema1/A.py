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
    
def parse_text(text):
    text_length = len(text)
    add_padd = pad(text.encode(), 16)
    return add_padd

def encrypt_cbc(block, k, iv):
    xor = bytes([a ^ b for a, b in zip(block, iv)])
    cipher = AES.new(k, AES.MODE_CBC, iv)
    ciphered_text = cipher.encrypt(xor)
    return ciphered_text

def encrypt_ecb(block, k):
    cipher = AES.new(k, AES.MODE_ECB)
    ciphered_text = cipher.encrypt(block)
    return ciphered_text


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
    
    our_key = None
    iv = None
    k = None
    if mode == 'ECB':
        k_prim = connection_km.recv(16).decode('utf-8')
        connection_b.send(k_prim.encode())
        # print("K_prim: ")
        # print(k_prim)
        k = connection_km.recv(16)
        # print("Key: ")
        # print(k)
        connection_b.send(k)
        
        print("K is:")
        our_key = dec_ecb(k_prim, k)
        print(our_key)
        
    elif mode == 'CBC':
        k_prim = connection_km.recv(16)
        # print("K_prim: ")
        # print(k_prim)
        connection_b.send(k_prim)
        en_k = connection_km.recv(54)
        connection_b.send(en_k)
        
        file1 = open("iv.txt", 'rb')
        iv = file1.read()
        file1.close()
        # print("iv: ")
        # print(iv)
        # print("Key: ")
        # print(en_k)
        our_key = dec_cbc(k_prim, iv, en_k)
        print("K is:")
        print(our_key)
    while True:
        res = connection_b.recv(2).decode('utf-8')
        if res == 'ok':
            break
    print("Got confirmation.")
    
    
    
    file = open("plaintext.txt", 'r')
    text = file.read()
    file.close()
    padded_text = parse_text(text)
    i = 0
    j = 16
    while i <= len(padded_text) - 16 and j <= len(padded_text):
        if mode == 'CBC':
            iv = encrypt_cbc(padded_text[i:j], our_key, iv)
            connection_b.send(iv)
        elif mode == 'ECB':
            iv = encrypt_ecb(padded_text[i:j], our_key)
            connection_b.send(iv)
        i += 16
        j += 16
    
    connection_b.close()
    connection_km.close()



if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT_B = 6060
    PORT_KM = 6000
    realize_connection(HOST, PORT_B, PORT_KM)

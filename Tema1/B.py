import socket
from base64 import b64encode
from os import urandom
from base64 import b64decode
from typing import TextIO
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes

count = 0

def parse_text(text):
    text_length = len(text)
    add_padd = pad(text.encode(), 16)
    return add_padd

total_count = len(parse_text("Acesta este un text random"))


def dec_cbc(k_prim, iv, ct):
    cipher = AES.new(k_prim, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), AES.block_size)

def dec_ecb(k, message):
    cipher = AES.new(k.encode(), AES.MODE_ECB)
    return cipher.decrypt(message)

def decrypt_cbc(total_count,c_text, k, iv):
    global count
    count += 1 
    ciphered_text = c_text
    decipher = AES.new(k, AES.MODE_CBC,iv)
    deciphered_text = decipher.decrypt(ciphered_text)
    xor = bytes([a ^ b for a, b in zip(deciphered_text, iv)])
    iv = ciphered_text
    txt = ''
    if count == total_count:
        txt += unpad(xor, 16).decode('latin-1')
    else:
        txt += xor.decode('latin-1')
    return txt
    

def decrypt_ebc(total_count,c_text, k):
    global count
    count += 1 
    decipher = AES.new(k, AES.MODE_ECB)
    deciphered_text = decipher.decrypt(c_text)
    # txt = ''
    # if count == total_count:
    #     txt += unpad(deciphered_text, 16).decode('latin-1')
    # else:
    #     txt += deciphered_text.decode('latin-1')
    return deciphered_text.decode('latin-1')
     

def realize_connection(HOST, PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    print("B Connected.")
    sock.connect(server_address)
    mode = sock.recv(4).decode('utf-8')
    # print("Mode: ")
    # print(mode)
    our_key = None
    iv = None
    if mode == 'ECB':
        k_prim = sock.recv(16).decode('utf-8')
        en_k = sock.recv(54)
        # print("K_prim: ")
        # print(k_prim)
        # print("Key: ")
        # print(en_k)
        print("K is:")
        our_key = dec_ecb(k_prim, en_k)
        print(our_key)
        
    elif mode == 'CBC':
        file2 = open("iv.txt", 'rb')
        iv = file2.read()
        file2.close()
        
        k_prim = sock.recv(16)
        # print("K_prim: ")
        # print(k_prim)
        # print("iv: ")
        # print(iv)
        en_k = sock.recv(54)
        # print("Key: ")
        # print(en_k)
        our_key = dec_cbc(k_prim, iv, en_k)
        print("K is:")
        print(our_key)
    sock.send("ok".encode())
    
    i = 0
    i_text = ''
    while i < int(total_count):
        if mode == 'CBC':
            i += 16
            c_text = sock.recv(16)
            result = decrypt_cbc(total_count,c_text, our_key, iv)
            i_text = i_text + result
        else:
            i += 16
            c_text = sock.recv(16)
            result = decrypt_ebc(total_count,c_text, our_key)
            i_text = i_text + result
    print("Plaintext: ")
    print(i_text)
    
    sock.close()

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT_B = 6060
    realize_connection(HOST, PORT_B)
    
    

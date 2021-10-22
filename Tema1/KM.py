import socket
from base64 import b64encode
from os import urandom
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes

def generate_cbc_key(k, k_prim):
    cipher = AES.new(k_prim, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(k, AES.block_size))
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    result = [iv, ct]
    return result

def dec_cbc(k_prim, iv, ct):
    cipher = AES.new(k_prim, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), AES.block_size)

def generate_ecb_key(k, k_prim):
    cipher = AES.new(k.encode(), AES.MODE_ECB)
    return cipher.encrypt(k_prim)

def dec_ecb(k, message):
    cipher = AES.new(k.encode(), AES.MODE_ECB)
    return cipher.decrypt(message)
    
def realize_connection(HOST, PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    sock.connect(server_address)
    print("KM Connected. ")
    
    mode = sock.recv(4)
    m = mode.decode('utf-8')
    if m == 'CBC':
        k_prim = b"alabalaportocala"
        print("K_prim: ")
        print(k_prim)
        sock.send(k_prim)
        k = get_random_bytes(16)
        result = generate_cbc_key(k, k_prim)
        iv = b64decode(result[0])
        en_k = b64decode(result[1])
        pt = dec_cbc(k_prim, iv, en_k)
        print("K is:")
        print(pt)
        file = open('iv.txt', 'wb') 
        file.write(iv)
        # print("IV:")
        # print(iv)
        file.close()
        # print("Key:")
        # print(en_k)
        sock.send(en_k)
    elif m == 'ECB':
        k_prim = 'alabalaportocala'
        # print("K_prim: ")
        # print(k_prim)
        sock.send(k_prim.encode())
        k = urandom(16)
        en_k = generate_ecb_key(k_prim, k)
        # print(en_k)
        print("K is:")
        pt  = dec_ecb(k_prim, en_k)
        print(pt)
        sock.send(en_k)
    sock.close()

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT_KM = 6000
    realize_connection(HOST, PORT_KM)
    

import socket
import sys
import time

def realize_connection(HOST, PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    print("Conecting.. ")
    sock.connect(server_address)
    m = sock.recv(1024)
    mode = m.decode('utf-8')
    print("Mode: ")
    print(mode)
    k = sock.recv(1024)
    key = k.decode('utf-8')
    print("Key: ")
    print(key)
    # while True:
        # print("Waiting for message: ")
        # data = sock.recv(1024)
        # print(data.decode('utf-8'))
        # message = input("Enter message: ")
        # sock.send(str.encode(message))
    sock.close()

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT_B = 5000
    realize_connection(HOST, PORT_B)
    
    
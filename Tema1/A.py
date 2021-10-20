import socket
import sys
import time

def realize_connection(HOST, PORT_B, PORT_KM):
    sock_km = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address_km = (HOST, PORT_KM)
    sock_km.bind(server_address_km)
    sock_km.listen(1)
    connection_km, client_address_km = sock_km.accept()
    print("Connected with A.")
    message = input("Choose a mode to operate: \nECB \nCBC\n")
    mode = str.encode(message)
    connection_km.send(mode)
    iv = connection_km.recv(32)
    k = connection_km.recv(1024)
    key = k.decode('utf-8')
    print("Key: ")
    print(key)
    
    sock_b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address_b = (HOST, PORT_B)
    sock_b.bind(server_address_b)
    sock_b.listen(1)
    connection_b, client_address_b = sock_b.accept()
    print("Connected with B.")
    connection_b.send(mode)
    connection_b.send(k)
    # while True:
        # connection_b, client_address_b = sock_b.accept()
    
            # message = input("Say smtg here: ")
            # connection_b.send(str.encode(message))
            # data = connection_b.recv(2048)
            # if data:
            #     print(data.decode('utf-8'))
            # else:
            #     print("no data")
    connection_b.close()
    connection_km.close()
    

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT_B = 5000
    PORT_KM = 8000
    realize_connection(HOST, PORT_B, PORT_KM)
    
    
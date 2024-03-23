from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM
import pickle
from Certifying_Authority import CertifyingAuthority as CA

public_keys = {}
SERVER_PORT = 8000

def auth_A(ip : str):
    global public_keys
    auth_A = CA(ip)
    socket = auth_A.socket
    
    while True:
        request, addr = socket.recvfrom(4096)
        host, request = pickle.loads(request)

        if request == "public_key":

            public_key = public_keys[host]
            socket.sendto(public_key, addr)
            print("Uma chave pública foi enviada")

        elif request == "register":
            
            password = auth_A.diffie_hellman(socket, addr)
            private_key, public_key = auth_A.generate_keys_for_node(password)
            public_keys[host] = public_key
            socket.sendto(private_key, addr)
            print(f"Chave privada de {host} gerada")

def auth_B(ip : str):
    global public_keys
    auth_B = CA(ip)
    socket = auth_B.socket
    
    while True:
        request, addr = socket.recvfrom(4096)
        host, request = pickle.loads(request)

        if request == "public_key":

            public_key = public_keys[host]
            socket.sendto(public_key, addr)
            print("Uma chave pública foi enviada")

        elif request == "register":
            
            password = auth_B.diffie_hellman(socket, addr)
            private_key, public_key = auth_B.generate_keys_for_node(password)
            public_keys[host] = public_key
            socket.sendto(private_key, addr)
            print(f"Chave privada de {host} gerada")

def auth_C(ip : str):
    global public_keys
    auth_C = CA(ip)
    socket = auth_C.socket
    
    while True:
        request, addr = socket.recvfrom(4096)
        host, request = pickle.loads(request)

        if request == "public_key":

            public_key = public_keys[host]
            socket.sendto(public_key, addr)
            print("Uma chave pública foi enviada")

        elif request == "register":
            
            password = auth_C.diffie_hellman(socket, addr)
            private_key, public_key = auth_C.generate_keys_for_node(password)
            public_keys[host] = public_key
            socket.sendto(private_key, addr)
            print(f"Chave privada de {host} gerada")

def auth_D(ip : str):
    global public_keys
    auth_D = CA(ip)
    socket = auth_D.socket
    
    while True:
        request, addr = socket.recvfrom(4096)
        host, request = pickle.loads(request)

        if request == "public_key":

            public_key = public_keys[host]
            socket.sendto(public_key, addr)
            print("Uma chave pública foi enviada")

        elif request == "register":
            
            password = auth_D.diffie_hellman(socket, addr)
            private_key, public_key = auth_D.generate_keys_for_node(password)
            public_keys[host] = public_key
            socket.sendto(private_key, addr)
            print(f"Chave privada de {host} gerada")

def auth_E(ip : str):
    global public_keys
    auth_E = CA(ip)
    socket = auth_E.socket
    
    while True:
        request, addr = socket.recvfrom(4096)
        host, request = pickle.loads(request)

        if request == "public_key":

            public_key = public_keys[host]
            socket.sendto(public_key, addr)
            print("Uma chave pública foi enviada")

        elif request == "register":
            
            password = auth_E.diffie_hellman(socket, addr)
            private_key, public_key = auth_E.generate_keys_for_node(password)
            public_keys[host] = public_key
            socket.sendto(private_key, addr)
            print(f"Chave privada de {host} gerada")

def auth_F(ip : str):
    global public_keys
    auth_F = CA(ip)
    socket = auth_F.socket
    
    while True:
        request, addr = socket.recvfrom(4096)
        host, request = pickle.loads(request)

        if request == "public_key":

            public_key = public_keys[host]
            socket.sendto(public_key, addr)
            print("Uma chave pública foi enviada")

        elif request == "register":
            
            password = auth_F.diffie_hellman(socket, addr)
            private_key, public_key = auth_F.generate_keys_for_node(password)
            public_keys[host] = public_key
            socket.sendto(private_key, addr)
            print(f"Chave privada de {host} gerada")



ips = []
for i in range (1, 7):
    ips.append(f"192.168.{i-1}.4")


A = Thread(target=auth_A, args=[ips[0]])
B = Thread(target=auth_B, args=[ips[1]])
C = Thread(target=auth_C, args=[ips[2]])
'''
D = Thread(target=auth_D, args=[ips[3]])
E = Thread(target=auth_E, args=[ips[4]])
F = Thread(target=auth_F, args=[ips[5]])
'''

A.start()
B.start()
C.start()
'''
D.start()
E.start()
F.start()
'''



from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM
import pickle
from Certifying_Authority import CertifyingAuthority as CA

SERVER_PORT = 8000

def auth_A(ip : str):
    auth_A = CA(ip)
    socket = auth_A.socket
    request, addr = socket.recvfrom(4096)
    #pickle.loads no request
    if request == "public_key":
        public_key = "bota aqui a public key"
        public_key = pickle.dumps([public_key])
        socket.sendto(public_key, (addr, SERVER_PORT))

    elif request == "register":
        #Combina a senha com o host A
        #Depois gera uma pv key usando essa senha e manda pro host A
        #Salva a pb key do host A
        print("done")   

ips = []
for i in range (1, 7):
    ips.append(f"192.168.{i-1}.4")

A = Thread(target=auth_A, args=[ips[0]])

A.start()
A.join()



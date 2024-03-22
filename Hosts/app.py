from socket import socket, AF_INET, SOCK_DGRAM
from symmetric import symmetric_key_decrypt, symmetric_key_encrypt, diffie_hellman, generate_route, direction_cost
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from typing import Dict
import pickle

SERVER_PORT = 8000

class App:
    def __init__(self, host: int , ips: tuple[str], neighbors: tuple[str], auth_addr: str):
        self.server_sockets: Dict[str, socket] = {}
        self.hosts = {1 : 'A', 2 : 'B', 3 : 'C', 4 : 'D', 5 : 'E', 6 : 'F'}
        self.host = host    
        self.route = generate_route()
        self.prev = neighbors[0]
        self.next = neighbors[1]
        self.auth_addr = auth_addr
        self.prev_interface = ips[0]
        self.next_interface = ips[1]
        
        for ip in ips:
            server_socket = socket(AF_INET, SOCK_DGRAM)
            print(f"Ip ao qual o bind está sendo feito {ip}")
            server_socket.bind((ip, SERVER_PORT))
            self.server_sockets[ip] = server_socket
        _ = input("Aperte enter para após todos os binds terem terminado")

        #Se cadastrando no CA
        request = pickle.dumps([self.hosts[self.host], "register"])
        self.socket_auth = socket(AF_INET, SOCK_DGRAM)
        self.socket_auth.sendto(request, (self.auth_addr, SERVER_PORT))
        password = diffie_hellman(self.socket_auth, (self.auth_addr, SERVER_PORT))
        self.private_key = self.socket_auth.recv(4096)
        self.private_key = serialization.load_pem_private_key(
            self.private_key,
            password=password.encode(),  
            backend=default_backend()
        )
        print("Chave privada obtida com sucesso")

    def request_public_key(self, host : int):
        host_name = self.hosts[host]
        socket = self.socket_auth
        request =  pickle.dumps([host_name, "public_key"])
        socket.sendto(request, (self.auth_addr, SERVER_PORT))
        public_key = socket.recv(4096)
        public_key = serialization.load_pem_public_key(
            public_key,
            backend=default_backend()
        )
        return public_key
    
    def encrypt(self, message : str, key_assi) -> bytes:
        data = symmetric_key_encrypt(message)
        data = pickle.dumps(data)
        data = key_assi.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return data
    
    def decrypt(self, data : bytes) -> str:
        data = self.private_key.decrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )   
        )
        cipher_text, nonce, tag, key = pickle.loads(data)
        message = symmetric_key_decrypt(cipher_text, nonce, tag, key)
        return message


    def kill_both(self):
        self.server_sockets[self.prev_interface].close()
        self.server_sockets[self.prev_interface].close()

    def send_message_to (self, message : str, receiver : int):
        my_host_name = self.hosts[self.host]
        their_host_id = receiver
        receiver_socket, cost = direction_cost(self.route, self.host, receiver)

        if receiver_socket == "prev":
            receiver = self.prev
            receiver_socket = self.prev_interface
        else:
            receiver = self.next
            receiver_socket = self.next_interface

        socket = self.server_sockets[receiver_socket]
        public_key = self.request_public_key(their_host_id)
        message = self.encrypt(message, public_key)
        message = pickle.dumps([my_host_name, cost, message])
        socket.sendto(message, (receiver, SERVER_PORT))
        
        
    def receive_message_prev(self) -> str:
        socket = self.server_sockets[self.prev_interface]
        message, addr = socket.recvfrom(4096)
        host_name, cost, message = pickle.loads(message)
        if cost == 1:
            #a mensagem é para você
            message = self.decrypt(message)
            return f"{host_name}: {message}"
        
        else:
            #se não é pra você, diminui 1 de custo, repassa e retorna dizendo que foi um fowarding
            cost -= 1
            message = pickle.dumps([host_name, cost, message]) 
            socket.sendto(message, (self.next, SERVER_PORT))
            return "FOWARDING"
        
    def receive_message_next(self) -> str:
        socket = self.server_sockets[self.next_interface]
        message, addr = socket.recvfrom(4096)
        host_name, cost, message = pickle.loads(message)

        if cost == 1:
            #a mensagem é para você
            message = self.decrypt(message)
            return f"{host_name}: {message}"
        
        else:
            #se não é pra você, diminui 1 de custo, repassa e retorna dizendo que foi um fowarding
            cost -= 1
            message = pickle.dumps([host_name, cost, message]) 
            socket.sendto(message, (self.prev, SERVER_PORT))
            return "FOWARDING"
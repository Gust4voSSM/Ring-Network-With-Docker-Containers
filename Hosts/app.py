from socket import socket, AF_INET, SOCK_DGRAM
from symmetric import symmetric_key_decrypt, symmetric_key_encrypt, diffie_hellman
from typing import Dict
import pickle

SERVER_PORT = 8000

class App:
    def __init__(self, ips: tuple[str], neighbors: tuple[str], auth_addr: str):
        self.server_sockets: Dict[str, socket] = {}
        self.shared_keys: Dict[str, bytes] = {}
        self.prev = neighbors[0]
        self.next = neighbors[1]
        self.auth_addr = auth_addr
        self.prev_interface = ips[0]
        self.next_interface = ips[1]
        
        for ip in ips:
            server_socket = socket(AF_INET, SOCK_DGRAM)
            server_socket.bind((ip, SERVER_PORT))
            self.server_sockets[ip] = server_socket
            #Antes de fazer o diffie tem que checar a autenticidade com a autoridade certificadora 
            self.shared_keys[ip] = diffie_hellman(self.server_sockets[ip], (ip, SERVER_PORT))

    def send_message(self, receiver: str, message: str):
        socket = self.server_sockets[receiver]
        shared_key = self.shared_keys[receiver]
        message = pickle.dumps(symmetric_key_encrypt(message, shared_key))
        socket.sendto(message, (receiver, SERVER_PORT))

    def receive_message(self, sender: str) -> str:
        socket = self.server_sockets[sender]
        shared_key = self.shared_keys[sender]
        message, addr = socket.recvfrom(4096)
        message = pickle.loads(symmetric_key_decrypt(message, shared_key))
        return message


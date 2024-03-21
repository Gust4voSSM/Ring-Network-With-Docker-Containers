from socket import socket, AF_INET, SOCK_DGRAM
from symmetric import symmetric_key_decrypt, symmetric_key_encrypt, diffie_hellman, generate_route, direction_cost
from typing import Dict
import pickle

SERVER_PORT = 8000

class App:
    def __init__(self, host: int , ips: tuple[str], neighbors: tuple[str], auth_addr: str):
        self.server_sockets: Dict[str, socket] = {}
        self.shared_keys: Dict[str, bytes] = {}
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
        print("Binds realizadoz com sucesso")

    def generate_shared_key_prev(self):
        self.shared_keys[self.prev_interface] = diffie_hellman(self.server_sockets[self.prev_interface], (self.prev, SERVER_PORT))
    
    def generate_shared_key_next(self):
         self.shared_keys[self.next_interface] = diffie_hellman(self.server_sockets[self.next_interface], (self.next, SERVER_PORT))
    
    def kill_both(self):
        self.server_sockets[self.prev_interface].close()
        self.server_sockets[self.prev_interface].close()

    def send_message_to (self, message : str, receiver : int):
        receiver_socket, cost = direction_cost(self.route, self.host, receiver)
        if receiver_socket == "prev":
            receiver = self.prev
            receiver_socket = self.prev_interface
        else:
            receiver = self.next
            receiver_socket = self.next_interface

        socket = self.server_sockets[receiver_socket]
        message = pickle.dumps([cost, message])
        socket.sendto(message, (receiver, SERVER_PORT))
        
    def receive_message_prev(self) -> str:
        socket = self.server_sockets[self.prev_interface]
        message, addr = socket.recvfrom(4096)
        cost, message = pickle.loads(message)
        if cost == 1:
            #a mensagem é para você
            return message
        
        else:
            #se não é pra você, diminui 1 de custo, repassa e retorna dizendo que foi um fowarding
            cost -= 1
            message = pickle.dumps([cost, message]) 
            socket.sendto(message, (self.next, SERVER_PORT))
            return "FOWARDING"
        
    def receive_message_next(self) -> str:
        socket = self.server_sockets[self.next_interface]
        message, addr = socket.recvfrom(4096)
        cost, message = pickle.loads(message)
        if cost == 1:
            #a mensagem é para você
            return message
        
        else:
            #se não é pra você, diminui 1 de custo, repassa e retorna dizendo que foi um fowarding
            cost -= 1
            message = pickle.dumps([cost, message]) 
            socket.sendto(message, (self.prev, SERVER_PORT))
            return "FOWARDING"
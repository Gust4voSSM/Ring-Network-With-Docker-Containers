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
            print(f"Ip ao qual o bind está sendo feito {ip}")
            server_socket.bind((ip, SERVER_PORT))
            self.server_sockets[ip] = server_socket
        print("Binds realizadoz com sucesso")

    def generate_shared_key_prev(self):
        self.shared_keys[self.prev_interface] = diffie_hellman(self.server_sockets[self.prev_interface], (self.prev, SERVER_PORT))
    
    def generate_shared_key_next(self):
         self.shared_keys[self.next_interface] = diffie_hellman(self.server_sockets[self.next_interface], (self.next, SERVER_PORT))
    
    def send_message_next(self, message: str):
        if self.next_interface not in self.shared_keys : self.generate_shared_key_next()
        socket = self.server_sockets[self.next_interface]
        shared_key = self.shared_keys[self.next_interface]
        cipher_text, nonce, tag = symmetric_key_encrypt(message, shared_key)
        message = pickle.dumps([cipher_text, nonce, tag])
        socket.sendto(message, (self.next, SERVER_PORT))

    def send_message_prev(self, message: str):
        if self.prev_interface not in self.shared_keys : self.generate_shared_key_prev()
        socket = self.server_sockets[self.prev_interface]
        shared_key = self.shared_keys[self.prev_interface]
        cipher_text, nonce, tag = symmetric_key_encrypt(message, shared_key)
        message = pickle.dumps([cipher_text, nonce, tag])
        socket.sendto(message, (self.prev, SERVER_PORT))

    def receive_from_next(self) -> str:
        if self.next_interface not in self.shared_keys : self.generate_shared_key_next()
        socket = self.server_sockets[self.next_interface]
        shared_key = self.shared_keys[self.next_interface]
        message, addr = socket.recvfrom(4096)
        cipher_text, nonce, tag = pickle.loads(message)
        message = symmetric_key_decrypt(cipher_text, nonce, tag, shared_key)
        return message
    
    def receive_from_prev(self) -> str:
        if self.prev_interface not in self.shared_keys : self.generate_shared_key_prev()
        socket = self.server_sockets[self.prev_interface]
        shared_key = self.shared_keys[self.prev_interface]
        message, addr = socket.recvfrom(4096)
        cipher_text, nonce, tag = pickle.loads(message)
        message = symmetric_key_decrypt(cipher_text, nonce, tag, shared_key)
        return message

    def kill_both(self):
        self.server_sockets[self.prev_interface].close()
        self.server_sockets[self.prev_interface].close()
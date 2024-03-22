from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from random import randint
from sympy import randprime
from socket import socket, AF_INET, SOCK_DGRAM

SERVER_PORT = 8000

# Simulação da Autoridade Certificadora
class CertifyingAuthority:
    def __init__(self, ip : str):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind((ip, SERVER_PORT))
        print(f"Bind com {ip} realizado com sucesso")

    def generate_keys_for_node(self, password: str):
        # Geração do par de chaves RSA
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
        public_key = private_key.public_key()

        # Exporta a chave privada
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(password.encode())  # Protege a chave privada com uma senha
        )

        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return private_key_pem, public_key_pem
    
    def diffie_hellman(self, socke, tuple) -> str:
        random_1 = randprime(1, 2000)
        socke.sendto(str(random_1).encode(), tuple)
        random_2 = int(socke.recv(2048).decode())
        if (random_1 > random_2):
            random_1, random_2 = random_2, random_1
    
        private_key = randint(1, 2000)
        public_key = random_1**private_key % random_2
        print("Troca de senhas realizada") #ver esse "bug"

        socke.sendto(str(public_key).encode(), tuple)
        other_public_key = int(socke.recv(2048).decode())
        
        shared_key = other_public_key**private_key % random_2

        return str(shared_key)


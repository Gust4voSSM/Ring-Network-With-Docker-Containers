from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.fernet import Fernet
import os

class Node:
    def __init__(self, ca, node_id):
        self.ca = ca
        self.node_id = node_id
        self.private_key = None
        self.symmetric_key = None
        self.register_with_ca()

    def register_with_ca(self):
        # O nó solicita à CA para gerar um par de chaves para ele
        private_key_pem, _ = self.ca.generate_keys_for_node(self.node_id)

        # Importa a chave privada
        self.private_key = serialization.load_pem_private_key(
            private_key_pem,
            password=None,  # Nenhuma senha foi utilizada na exportação
            backend=default_backend()
        )

        # Geração de uma chave simétrica para comunicação segura após a autenticação
        self.symmetric_key = Fernet.generate_key()
        self.fernet = Fernet(self.symmetric_key)

    def encrypt_message_with_symmetric_key(self, message):
        return self.fernet.encrypt(message.encode())

    def decrypt_message_with_symmetric_key(self, encrypted_message):
        return self.fernet.decrypt(encrypted_message).decode()

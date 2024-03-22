from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os

# Simulação da Autoridade Certificadora
class CertifyingAuthority:
    def __init__(self):
        self.nodes_public_keys = {}  # Armazena as chaves públicas dos nós

    def generate_keys_for_node(self, node_id):
        # Geração do par de chaves RSA
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()

        # Exporta a chave privada
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        # Armazena a chave pública com o identificador do nó
        self.nodes_public_keys[node_id] = public_key

        return private_key_pem, public_key

    def get_public_key(self, node_id):
        return self.nodes_public_keys.get(node_id)


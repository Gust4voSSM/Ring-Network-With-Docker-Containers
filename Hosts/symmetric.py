from Crypto.Cipher import AES
from socket import socket
from random import randint
from sympy import randprime
from Crypto.Random import get_random_bytes
from dijkstar import Graph, find_path 

def symmetric_key_encrypt(data : str):
    key = get_random_bytes(16)
    data = data.encode("utf-8")
    cipher = AES.new(key, AES.MODE_EAX)
    cipher_text, tag = cipher.encrypt_and_digest(data)
    return [cipher_text, cipher.nonce, tag, key]
    #Retorna uma lista que deve ser enviada para o outro lado

def symmetric_key_decrypt(cipher_text, nonce, tag, key):
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(cipher_text, tag)
    return data.decode("utf-8")
    #Descriptografa a lista recebida do outro lado e retorna a mensagem em texto

def diffie_hellman(socke, tuple) -> str:
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


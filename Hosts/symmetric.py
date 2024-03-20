from Crypto.Cipher import AES
from socket import socket
from random import randint
from sympy import randprime

def symmetric_key_encrypt(data, shared_key):
    data = data.encode("utf-8")
    cipher = AES.new(shared_key, AES.MODE_EAX)
    cipher_text, tag = cipher.encrypt_and_digest(data)
    return [cipher_text, cipher.nonce, tag]
    #Retorna uma lista que deve ser enviada para o outro lado

def symmetric_key_decrypt(cipher_text, nonce, tag, shared_key):
    cipher = AES.new(shared_key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(cipher_text, tag)
    return data.decode("utf-8")

    #Descriptografa a lista recebida do outro lado e retorna a mensagem em texto

def diffie_hellman(socke, tuple):
    random_1 = randprime(1, 2000)
    print("waiting for diffie")
    socke.sendto(str(random_1).encode(), tuple)
    random_2 = int(socke.recv(2048).decode())
    if (random_1 > random_2):
        random_1, random_2 = random_2, random_1
 
    private_key = randint(1, 2000)
    public_key = random_1**private_key % random_2
    print("diffie hellman realizado") #ver esse "bug"

    socke.sendto(str(public_key).encode(), tuple)
    other_public_key = int(socke.recv(2048).decode())
    
    shared_key = other_public_key**private_key % random_2
    shared_key = shared_key.to_bytes(16, 'big')

    return shared_key
    #Faz o Diffe-hellman e retorna a chave compartilhada que deve ser usada para descriptografar e criptografar mensagens



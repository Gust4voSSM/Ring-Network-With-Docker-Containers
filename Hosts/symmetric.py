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

def symmetric_key_decrypt(infos, shared_key):
    cipher = AES.new(shared_key, AES.MODE_EAX, infos[1])
    data = cipher.decrypt_and_verify(infos[0], infos[2])
    return data.decode("utf-8") 
    #Descriptografa a lista recebida do outro lado e retorna a mensagem em texto

def diffie_hellman(socke):
    random_1 = randprime(1, 2000)
    socke.send(str(random_1).encode())
    random_2 = int(socke.recv(2048).decode())
    if (random_1 > random_2):
        random_1, random_2 = random_2, random_1
 
    private_key = randint(1, 2000)
    public_key = random_1**private_key % random_2
    print("...") #ver esse "bug"

    socke.send(str(public_key).encode())
    other_public_key = int(socke.recv(2048).decode())
    
    shared_key = other_public_key**private_key % random_2
    shared_key = shared_key.to_bytes(16, 'big')

    return shared_key
    #Faz o Diffe-hellman e retorna a chave compartilhada que deve ser usada para descriptografar e criptografar mensagens



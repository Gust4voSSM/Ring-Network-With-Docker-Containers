from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def symmetric_key_encrypt(data, shared_key):
    data = data.encode("utf-8")
    cipher = AES.new(shared_key, AES.MODE_EAX)
    cipher_text, tag = cipher.encrypt_and_digest(data)
    return [cipher_text, cipher.nonce, tag]

def symmetric_key_decrypt(infos, shared_key):
    cipher = AES.new(shared_key, AES.MODE_EAX, infos[1])
    data = cipher.decrypt_and_verify(infos[0], infos[2])
    return data.decode("utf-8") 


frase = "testando se tá pegando.com jujuba carro moto 192.32.4.5.1"
key_shared = get_random_bytes(16)
inf = symmetric_key_encrypt(frase, key_shared)
print(f"Cifra: {inf[0]}, Nonce: {inf[1]} e Tag: {inf[2]}\n")
nova_frase = symmetric_key_decrypt(inf, key_shared)
print(nova_frase)

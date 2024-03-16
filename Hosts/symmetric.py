from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def symmetric_key_encrypt(data, shared_key):
    data = data.encode("utf-8")
    cipher = AES.new(shared_key, AES.MODE_EAX)
    cipher_text, tag = cipher.encrypt_and_digest(data)
    return [cipher_text, shared_key, cipher.nonce, tag]

def symmetric_key_decrypt(infos):
    cipher = AES.new(infos[1], AES.MODE_EAX, infos[2])
    data = cipher.decrypt_and_verify(infos[0], infos[3])
    return data.decode("utf-8") 

"""
frase = "testando se tá pegando.com jujuba carro moto 192.32.4.5.1"
inf = symmetric_key_encrypt(frase)
print(f"Cifra: {inf[0]}, Chave: {inf[1]}, Nonce: {inf[2]} e Tag: {inf[3]}\n")
nova_frase = symmetric_key_decrypt(inf)
print(nova_frase)
"""
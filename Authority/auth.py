import rsa

# Função para gerar as chaves necessárias para a aplicação
def generating_keys():
    key_pairs = []
    public_key, private_key = rsa.newkeys(1024)
    key_pairs.append(public_key), key_pairs.append(private_key)
    return key_pairs

# Função para criptografar a chave
def assymetric_key_encrypt(data, key_pairs):
    public_key = key_pairs[0]
    data = b'hello guys'
    ciphertext = rsa.encrypt(data, public_key)
    return ciphertext

# Função para descriptografar a chave
def assymetric_key_decryption (ciphertext, key_pairs):
    private_key = key_pairs[1]
    plain_text = rsa.decrypt(ciphertext,private_key)
    return plain_text

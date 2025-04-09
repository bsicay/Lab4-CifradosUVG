from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from Cryptodome.Cipher import PKCS1_OAEP

class CryptoService:
    def generate_key_pair():
        key = RSA.generate(2048)
        return (
            key.export_key(),
            key.publickey().export_key()
        )
    
    def encrypt_with_private_key(private_key, data):
        key = RSA.import_key(private_key)
        cipher = PKCS1_OAEP.new(key)
        return cipher.encrypt(data)
    
    def decrypt_with_public_key(public_key, encrypted_data):
        key = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(key)
        return cipher.decrypt(encrypted_data)
    
    def sign_data(private_key, hash):
        key = RSA.import_key(private_key)
        return pkcs1_15.new(key).sign(hash)
    
    def verify_signature(public_key, hash, signature):
        key = RSA.import_key(public_key)
        try:
            pkcs1_15.new(key).verify(hash, signature)
            return True
        except (ValueError, TypeError):
            return False
        
    def hash_data(data):
        hasher = SHA256.new(data)
        return hasher
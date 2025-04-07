from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from Cryptodome.Cipher import PKCS1_OAEP
import base64

class CryptoService:
    @staticmethod
    def generate_key_pair():
        key = RSA.generate(2048)
        return (
            key.export_key(),
            key.publickey().export_key()
        )
    
    @staticmethod
    def encrypt_with_public_key(public_key, data):
        key = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(key)
        return cipher.encrypt(data)
    
    @staticmethod
    def decrypt_with_private_key(private_key, encrypted_data):
        key = RSA.import_key(private_key)
        cipher = PKCS1_OAEP.new(key)
        return cipher.decrypt(encrypted_data)
    
    @staticmethod
    def sign_data(private_key, data):
        key = RSA.import_key(private_key)
        h = SHA256.new(data)
        return pkcs1_15.new(key).sign(h)
    
    @staticmethod
    def verify_signature(public_key, data, signature):
        key = RSA.import_key(public_key)
        h = SHA256.new(data)
        try:
            pkcs1_15.new(key).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False
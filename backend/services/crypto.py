from Cryptodome.PublicKey import RSA, ECC
from Cryptodome.Signature import pkcs1_15, DSS
from Cryptodome.Hash import SHA256
from Cryptodome.Cipher import PKCS1_OAEP

class CryptoService:
    def generate_key_pair(algorithm='rsa'):
        algorithm = algorithm.lower()
        
        if algorithm == 'rsa':
            key = RSA.generate(2048)
            private_key = key.export_key()
            public_key = key.publickey().export_key()
        elif algorithm == 'ecc':
            key = ECC.generate(curve='P-256')
            private_key = key.export_key(format='PEM')
            public_key = key.public_key().export_key(format='PEM')
        else:
            raise ValueError("Algoritmo no soportado. Usa 'rsa' o 'ecc'.")

        return private_key, public_key
        
    
    def encrypt_with_private_key(private_key, data):
        key = RSA.import_key(private_key)
        cipher = PKCS1_OAEP.new(key)
        return cipher.encrypt(data)
    
    def decrypt_with_public_key(public_key, encrypted_data):
        key = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(key)
        return cipher.decrypt(encrypted_data)
    
    def sign_data(private_key, hash_obj):
        """
        Firma un hash con RSA o ECC, dependiendo de la clave dada.
        """
        key = RSA.import_key(private_key) if b'RSA' in private_key else ECC.import_key(private_key)
        
        if b'RSA' in private_key:
            # Firma RSA-PKCS#1 v1.5
            return pkcs1_15.new(key).sign(hash_obj)
        else:
            # Firma ECC con ECDSA
            signer = DSS.new(key, 'fips-186-3')
            return signer.sign(hash_obj)
    
    def verify_signature(public_key, hash_obj, signature):
        """
        Verifica la firma, ya sea RSA o ECC, dependiendo de la clave dada.
        """
        key = RSA.import_key(public_key) if b'RSA' in public_key else ECC.import_key(public_key)
        
        try:
            if b'RSA' in public_key:
                pkcs1_15.new(key).verify(hash_obj, signature)
            else:
                verifier = DSS.new(key, 'fips-186-3')
                verifier.verify(hash_obj, signature)
            return True
        except (ValueError, TypeError):
            return False
        
    def hash_data(data):
        hasher = SHA256.new(data)
        return hasher
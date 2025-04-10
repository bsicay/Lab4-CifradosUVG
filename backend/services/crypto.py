from Cryptodome.PublicKey import RSA, ECC
from Cryptodome.Signature import pkcs1_15, DSS
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from Cryptodome.Hash import SHA256
from Cryptodome.Cipher import PKCS1_OAEP
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import os, base64, json


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
        
    
    # def encrypt_with_private_key(private_key, data):
    #     key = RSA.import_key(private_key)
    #     cipher = PKCS1_OAEP.new(key)
    #     return cipher.encrypt(data)
    
    # def decrypt_with_public_key(public_key, encrypted_data):
    #     key = RSA.import_key(public_key)
    #     cipher = PKCS1_OAEP.new(key)
    #     return cipher.decrypt(encrypted_data)


    # def encrypt_with_public_key(public_key, plaintext):
    #     """
    #     - Para RSA: Cifrado asimétrico con PKCS1_OAEP.
    #     - Para ECC: Emplea un cifrado híbrido estilo ECIES (ECDH + AES).
    #     Devuelve bytes (o un dict serializado en JSON) que contiene
    #     todo lo necesario para descifrar.
    #     """
    #     if b'RSA' in public_key:
    #         # === RSA ===
    #         rsa_key = RSA.import_key(public_key)
    #         cipher_rsa = PKCS1_OAEP.new(rsa_key)
    #         ciphertext = cipher_rsa.encrypt(plaintext)
    #         return ciphertext
    #     else:
    #         # === ECC (ECIES simplificado) ===
    #         ecc_pub_key = ECC.import_key(public_key)
    #         # 1) Generar clave efímera
    #         ephemeral_key = ECC.generate(curve=ecc_pub_key.curve)
    #         # 2) Intercambio ECDH
    #         shared_secret = ephemeral_key.exchange(ecc_pub_key)
    #         # 3) Derivar clave AES (usamos sha256 del shared_secret)
    #         kdf = SHA256.new(shared_secret)
    #         aes_key = kdf.digest()  # 32 bytes

    #         # 4) Cifrar con AES (modo GCM, por ejemplo)
    #         cipher_aes = AES.new(aes_key, AES.MODE_GCM)
    #         ciphertext, tag = cipher_aes.encrypt_and_digest(plaintext)

    #         # 5) Adjuntar la clave pública efímera, nonce y tag
    #         ephemeral_pub_bytes = ephemeral_key.public_key().export_key(format='DER')
    #         package = {
    #             "ephemeral_pub": base64.b64encode(ephemeral_pub_bytes).decode('utf-8'),
    #             "nonce": base64.b64encode(cipher_aes.nonce).decode('utf-8'),
    #             "tag": base64.b64encode(tag).decode('utf-8'),
    #             "ciphertext": base64.b64encode(ciphertext).decode('utf-8')
    #         }
    #         # Lo convertimos a JSON y luego a bytes
    #         return json.dumps(package).encode('utf-8')

    def encrypt_with_public_key(public_key, plaintext):
        if b'RSA' in public_key:
            rsa_key = RSA.import_key(public_key)
            cipher_rsa = PKCS1_OAEP.new(rsa_key)
            ciphertext = cipher_rsa.encrypt(plaintext)
            return ciphertext
        else:
            # ECC con cryptography
            peer_public_key = serialization.load_pem_public_key(public_key)

            # Generar clave efímera
            ephemeral_key = ec.generate_private_key(ec.SECP256R1())

            shared_key = ephemeral_key.exchange(ec.ECDH(), peer_public_key)

            # Derivar clave AES desde shared_key
            derived_key = HKDF(
                algorithm=hashes.SHA256(),
                length=32,
                salt=None,
                info=b'handshake data',
                backend=default_backend()
            ).derive(shared_key)

            # AES GCM
            nonce = os.urandom(12)
            encryptor = Cipher(
                algorithms.AES(derived_key),
                modes.GCM(nonce),
                backend=default_backend()
            ).encryptor()

            ciphertext = encryptor.update(plaintext) + encryptor.finalize()

            ephemeral_public_bytes = ephemeral_key.public_key().public_bytes(
                serialization.Encoding.PEM,
                serialization.PublicFormat.SubjectPublicKeyInfo
            )

            package = {
                "ephemeral_pub": base64.b64encode(ephemeral_public_bytes).decode(),
                "nonce": base64.b64encode(nonce).decode(),
                "tag": base64.b64encode(encryptor.tag).decode(),
                "ciphertext": base64.b64encode(ciphertext).decode()
            }

            return json.dumps(package).encode('utf-8')
 
 

    @staticmethod
    def decrypt_with_private_key(private_key, encrypted_data):
        if b'RSA' in private_key:
            rsa_key = RSA.import_key(private_key)
            cipher_rsa = PKCS1_OAEP.new(rsa_key)
            return cipher_rsa.decrypt(encrypted_data)
        else:
            package = json.loads(encrypted_data.decode('utf-8'))

            ephemeral_pub = base64.b64decode(package["ephemeral_pub"])
            nonce = base64.b64decode(package["nonce"])
            tag = base64.b64decode(package["tag"])
            ciphertext = base64.b64decode(package["ciphertext"])

            private_key_obj = serialization.load_pem_private_key(
                private_key,
                password=None,
                backend=default_backend()
            )

            ephemeral_pub_key = serialization.load_pem_public_key(ephemeral_pub)
            shared_key = private_key_obj.exchange(ec.ECDH(), ephemeral_pub_key)

            derived_key = HKDF(
                algorithm=hashes.SHA256(),
                length=32,
                salt=None,
                info=b'handshake data',
                backend=default_backend()
            ).derive(shared_key)

            decryptor = Cipher(
                algorithms.AES(derived_key),
                modes.GCM(nonce, tag),
                backend=default_backend()
            ).decryptor()

            return decryptor.update(ciphertext) + decryptor.finalize()


    def sign_data(private_key, hash_obj):
        # Asegurarnos de tener un string
        if isinstance(private_key, bytes):
            private_key_str = private_key.decode('utf-8')
        else:
            private_key_str = private_key  # asume que ya es str

        # Revisar si es RSA o ECC basándonos en la cadena resultante
        if 'RSA' in private_key_str:
            # Importar como RSA
            key = RSA.import_key(private_key_str.encode('utf-8'))
            return pkcs1_15.new(key).sign(hash_obj)
        else:
            # Importar como ECC
            key = ECC.import_key(private_key_str)
            signer = DSS.new(key, 'fips-186-3')
            return signer.sign(hash_obj)

    
    def verify_signature(public_key, hash_obj, signature):
        """
        Verifica la firma, ya sea RSA o ECC, dependiendo de la clave dada.
        """
        if isinstance(public_key, bytes):
            public_key_str = public_key.decode('utf-8')
        else:
            public_key_str = public_key  # asume que ya es str

        if 'RSA' in public_key_str:
        # Importar como RSA
            key = RSA.import_key(public_key)
            pkcs1_15.new(key).verify(hash_obj, signature)
        else:
            # Importar como ECC
            key = ECC.import_key(public_key)
            verifier = DSS.new(key, 'fips-186-3')
            verifier.verify(hash_obj, signature)
        return True
        
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
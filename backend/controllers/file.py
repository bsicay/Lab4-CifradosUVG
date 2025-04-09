from flask import jsonify, request, abort
import base64
from werkzeug.utils import secure_filename 
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import UserModel
from backend.models.file import FileModel
from backend.services.crypto import CryptoService
from datetime import datetime

class FilesController:
    @jwt_required()
    def get_files():
        try:
            archivos = FileModel.get_all_files()
            
            return jsonify([{
                "id": f['id'],
                "filename": f['filename'],
                "user_email": UserModel.get_by_id(f['user_id'])['email'],
                "uploaded_at": f['uploaded_at'].isoformat(),
                "is_signed": f['is_signed']
            } for f in archivos]), 200
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @jwt_required()
    def download_file(file_id):
        try:
            archivo = FileModel.get_file(file_id)
            if not archivo:
                return jsonify({"error": "Archivo no encontrado"}), 404
                
            return jsonify({
                "filename": archivo['filename'],
                "content": archivo['content'],
                "file_hash": archivo['file_hash'],
                "public_key": archivo['public_key'],
                "signature": archivo['signature']
            }), 200
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @jwt_required()
    def save_file(sign):
        if 'file' not in request.files:
            return jsonify({"error": "Archivo no proporcionado"}), 400
        
        archivo = request.files['file']
        private_key = request.form.get('private_key')
        
        if not private_key:
            return jsonify({"error": "Clave privada no proporcionada"}), 400
        
        try:
            private_key = private_key.replace("\\n","\n")
            
            user_email = get_jwt_identity()
            user = UserModel.get_by_email(user_email)
            
            if not user:
                return jsonify({"error": "Usuario no encontrado"}), 404

            contenido = archivo.read()

            hasher = CryptoService.hash_data(contenido)
            fileHash = hasher.hexdigest()

            signature = CryptoService.sign_data(private_key,hasher) if(sign) else None
            signature = base64.b64encode(signature).decode('utf-8') if signature else None
            
            encrypted_content = CryptoService.encrypt_with_private_key(
                private_key,
                contenido
            )
            
            contenido = base64.b64encode(encrypted_content).decode('utf-8')


            newFile = FileModel.save_file(
                user_id=user['id'],
                filename=secure_filename(archivo.filename),
                content=contenido,
                file_hash=fileHash,
                public_key=user['current_public_key'],
                signature=signature,
            )

            response = {
                "id": newFile,
                "message": "Archivo guardado",
                "filename": secure_filename(archivo.filename),
                "is_signed": sign
            }
            
            if sign:
                response["signature"] = signature.decode('utf-8') if isinstance(signature, bytes) else signature

            return jsonify(response), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @jwt_required()
    def verificar_archivo(file_id):
        try:
            archivo = FileModel.get_file(file_id)
            if not archivo:
                return jsonify({"error": "Archivo no encontrado"}), 404
                
            if not archivo['is_signed']:
                return jsonify({"error": "Archivo no está firmado"}), 400
                
            signature = request.json.get('signature')
            if not signature:
                return jsonify({"error": "Firma requerida"}), 400
                
            decrypted_content = CryptoService.decrypt_with_private_key(
                request.json.get('private_key'),
                archivo['content']
            )
            
            is_valid = CryptoService.verify_signature(
                archivo['public_key'],
                decrypted_content,
                signature
            )
            
            return jsonify({
                "is_authentic": is_valid,
                "verified_at": datetime.now(datetime.timezone.utc).isoformat()
            }), 200
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
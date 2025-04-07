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
                "content": base64.b64encode(archivo['content']).decode('utf-8'),
                "public_key": archivo['public_key'],
                "is_signed": archivo['is_signed']
            }), 200
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @jwt_required()
    def save_file():
        if 'file' not in request.files:
            return jsonify({"error": "Archivo no proporcionado"}), 400
        
        archivo = request.files['file']
        private_key = request.form.get('private_key')
        
        try:
            # Obtener usuario
            user_email = get_jwt_identity()
            user = UserModel.get_by_email(user_email)
            if not user or not user['current_public_key']:
                return jsonify({"error": "Usuario no tiene llave pública configurada"}), 400

            # Leer y cifrar archivo
            contenido = archivo.read()
            encrypted_content = CryptoService.encrypt_with_public_key(
                user['current_public_key'],
                contenido
            )

            # Firmar si se proporciona llave privada
            is_signed = False
            signature = None
            if private_key:
                signature = CryptoService.sign_data(private_key, contenido)
                is_signed = True

            # Guardar en base de datos
            FileModel.save_file(
                user_id=user['id'],
                filename=secure_filename(archivo.filename),
                content=encrypted_content,
                public_key=user['current_public_key'],
                is_signed=is_signed
            )

            response = {
                "message": "Archivo guardado",
                "filename": secure_filename(archivo.filename),
                "is_signed": is_signed
            }
            
            if signature:
                response["signature"] = base64.b64encode(signature).decode('utf-8')

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
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
                "owner": f['owner'],
                "uploaded_at": f['uploaded_at'].isoformat(),
                "is_signed": True if(f['signature'] is not None) else False,
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
                "public_key": archivo['public_key'],
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

            signature = CryptoService.sign_data(private_key,hasher) if(sign) else None
            signature = base64.b64encode(signature).decode('utf-8') if signature else None

            public_key = user['current_public_key']
            if not public_key:
                return jsonify({"error": "No se ha generado la clave pública"}), 400
    
            
            # encrypted_content = CryptoService.encrypt_with_private_key(
            #     private_key,
            #     contenido
            # )
            
            contenido = base64.b64encode(contenido).decode('utf-8')

            newFile = FileModel.save_file(
                owner=user_email,
                filename=secure_filename(archivo.filename),
                content=contenido,
                public_key=user['current_public_key'],
                signature=signature,
            )

            response = {
                "id": newFile,
                "message": "Archivo guardado",
                "filename": secure_filename(archivo.filename),
                "is_signed": sign
            }

            return jsonify(response), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @jwt_required()
    def verificar_archivo():
        if 'file' not in request.files:
            return jsonify({"error": "Archivo no proporcionado"}), 400
        
        archivo = request.files['file']
        owner = request.form.get('owner')
        
        if not owner:
            return jsonify({"error": "Correo de propietario no proporcionado"}), 400
        
        try:
            
            file = FileModel.get_file_by_owner_name(owner, secure_filename(archivo.filename))
            if not file:
                return jsonify({"error": "Archivo no encontrado en la base de datos"}), 404

            contenido = archivo.read()

            hasher = CryptoService.hash_data(contenido)

            signature = file['signature']
            
            if not signature:
                return jsonify({"error": "El archivo no tiene firma digital"}), 400
            
            signature = base64.b64decode(signature.encode('utf-8'))
            
            public_key = file['public_key']
        
            correctFile = CryptoService.verify_signature(
                public_key,
                hasher,
                signature
            )

            response = {
                "message": "Archivo correcto" if (correctFile) else "El archivo no coincide con la firma almacenada",
                "filename": secure_filename(archivo.filename),
            }

            return jsonify(response), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500
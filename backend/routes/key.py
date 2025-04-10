# backend/routes/key_routes.py
from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.services.crypto import CryptoService
from backend.models.user import UserModel

key_bp = Blueprint('keys', __name__)

@key_bp.route('/generate', methods=['GET'])
@jwt_required()
def generate_keys():
    try:
        alg = request.args.get('alg', 'rsa').lower()
        private_key, public_key = CryptoService.generate_key_pair(algorithm=alg)

        # Normalizar para que ambos (RSA/ECC) terminen como 'str'
        private_key_str = convert_to_str_if_bytes(private_key)
        public_key_str = convert_to_str_if_bytes(public_key)

        user_email = get_jwt_identity()
        UserModel.update_public_key(user_email, public_key_str)

        return jsonify({
            "private_key": private_key_str,
            "public_key": public_key_str
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def convert_to_str_if_bytes(data):
    if isinstance(data, bytes):
        return data.decode('utf-8')
    return data

from flask import jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.services.crypto import CryptoService
from backend.models.user import UserModel

key_bp = Blueprint('keys', __name__)

@key_bp.route('/generate', methods=['GET'])
@jwt_required()
def generate_keys():
    try:
        private_key, public_key = CryptoService.generate_key_pair()
        
        user_email = get_jwt_identity()
        UserModel.update_public_key(user_email, public_key)
        
        return jsonify({
            "private_key": private_key.decode('utf-8'),
            "public_key": public_key.decode('utf-8')
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
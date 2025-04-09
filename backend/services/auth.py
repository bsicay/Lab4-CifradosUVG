from flask_jwt_extended import create_access_token, create_refresh_token
from backend.models.user import UserModel
from flask_jwt_extended import decode_token, create_access_token
from jwt import ExpiredSignatureError

class AuthService:
    def login(email, password):
        user = UserModel.verify_password(email, password)
        if user:
            access_token = create_access_token(
                identity=user['email'],
                fresh=True
            )
            refresh_token = create_refresh_token(identity=user['email'])
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        return None
    
    def refresh(refresh_token):
        try:
            if UserModel.is_token_revoked(refresh_token):
                return {'error': 'Token revocado'}
            
            decoded = decode_token(refresh_token)
            user_email = decoded['sub']
            
            user = UserModel.get_by_email(user_email)
            
            UserModel.revoke_refresh_token(
                user_id=user['id'],
                token=refresh_token
                )
            
            new_access_token = create_access_token(
                identity=user_email,
                fresh=True
            )
            new_refresh_token = create_refresh_token(
                identity=user_email
            )
            
            return {
                'access_token': new_access_token,
                'refresh_token': new_refresh_token
            }
        except ExpiredSignatureError as e:
            return {'error': 'Token expirado'}
        except Exception as e:
            return {'error': 'Token no válido'}
    
    def register(email, password):
        if UserModel.get_by_email(email):
            return False
        UserModel.create(email, password)
        return True
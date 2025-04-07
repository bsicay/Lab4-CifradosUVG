from flask import jsonify, request
from backend.services.auth import AuthService
from backend.utils.validators import validate_request
from backend.utils.schemas import REGISTER_SCHEMA, LOGIN_SCHEMA, REFRESH_SCHEMA

class AuthController:
    @validate_request(LOGIN_SCHEMA)
    def login():
        data = request.get_json()
        tokens = AuthService.login(data.get('email'), data.get('password'))
        if tokens:
            return jsonify({
                "access_token": tokens['access_token'],
                "refresh_token": tokens['refresh_token']
            }), 200
        return jsonify({"result": "Credenciales inválidas"}), 401
    
    @validate_request(REFRESH_SCHEMA)
    def refresh():
        refresh_token = request.json.get('refresh_token')
        result = AuthService.refresh(refresh_token)
        if 'error' in result:
            if result['error'] == 'refresh_token_expired':
                return jsonify({
                    "error": "La sesión ha expirado"
                }), 401
            return jsonify({"error": "Token no válido"}), 401
            
        return jsonify({
            "access_token": result['access_token'],
            "refresh_token": result['refresh_token']
        }), 200
    
    @validate_request(REGISTER_SCHEMA)
    def register():
        data = request.get_json()
        if AuthService.register(data.get('email'), data.get('password')):
            tokens = AuthService.login(data.get('email'), data.get('password'))
            return jsonify({
                "access_token": tokens['access_token'],
                "refresh_token": tokens['refresh_token']
            }), 200
        return jsonify({"result": "El email ya está registrado"}), 400
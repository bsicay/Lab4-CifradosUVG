from flask import Blueprint
from backend.controllers.auth import AuthController

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    return AuthController.login()

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    return AuthController.refresh()

@auth_bp.route('/register', methods=['POST'])
def register():
    return AuthController.register()
from flask import Blueprint
from backend.controllers.auth import AuthController
from backend.utils.validators import validate_request
from backend.utils.schemas import REGISTER_SCHEMA, LOGIN_SCHEMA, REFRESH_SCHEMA

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
@validate_request(LOGIN_SCHEMA)
def login():
    return AuthController.login()

@auth_bp.route('/refresh', methods=['POST'])
@validate_request(REFRESH_SCHEMA)
def refresh():
    return AuthController.refresh()

@auth_bp.route('/register', methods=['POST'])
@validate_request(REGISTER_SCHEMA)
def register():
    return AuthController.register()
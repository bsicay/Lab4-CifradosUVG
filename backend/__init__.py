from flask import Flask, jsonify
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException
from backend.utils.BooleanConverter import BooleanConverter
from flask_cors import CORS


mysql = MySQL()
jwt = JWTManager()
app = Flask(__name__)

CORS(app, origins=["http://localhost:3000"], supports_credentials=True)


def create_app():
    from backend.routes.auth import auth_bp
    from backend.routes.file import file_bp
    from backend.routes.key import key_bp

    app.config.update({
    'MAX_CONTENT_LENGTH': 5 * 1024 * 1024,
    'ALLOWED_EXTENSIONS': {'txt', 'pdf', 'docx', 'jpg', 'png'},
    })
    app.config.from_object('backend.config.Config')
    app.url_map.converters['bool'] = BooleanConverter
    
    mysql.init_app(app)
    jwt.init_app(app)
    
    @app.route('/', methods=['GET'])
    def health_check():
        return jsonify({
            "status": "success",
            "message": "El servidor está funcionando correctamente",
            "service": "Backend Lab4"
        })
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(file_bp, url_prefix='/file')
    app.register_blueprint(key_bp, url_prefix='/key')
    
    @app.errorhandler(HTTPException)
    def handle_http_error(e):
        return jsonify({
            "error": e.name,
            "message": e.description
        }), e.code
        
    @app.errorhandler(Exception)
    def handle_exception(e):
        return jsonify({
            "error": "Error interno del servidor",
            "message": str(e)
        }), 500
    
    return app
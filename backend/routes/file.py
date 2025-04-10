from flask import Blueprint
from flask_jwt_extended import jwt_required
from backend.controllers.file import FilesController

file_bp = Blueprint('files', __name__)

@file_bp.route('/archivos', methods=['GET'])
@jwt_required()
def get_files():
    return FilesController.get_files()

@file_bp.route('/archivos/<int:file_id>/descargar', methods=['GET'])
@jwt_required()
def download_file(file_id):
    return FilesController.download_file(file_id)

@file_bp.route('/guardar/', defaults={'sign': False}, methods=['POST'])
@file_bp.route('/guardar/<bool:sign>', methods=['POST'])
@jwt_required()
def save_file(sign):
    return FilesController.save_file(sign)

@file_bp.route('/verificar', methods=['POST'])
@jwt_required()
def verificar_archivo():
    return FilesController.verificar_archivo()
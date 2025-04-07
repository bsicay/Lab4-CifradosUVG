from flask import jsonify, request
from functools import wraps
import re

def validate_request(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Verificar que el body es JSON
            if not request.is_json:
                return jsonify({"error": "Request must be JSON"}), 400
                
            data = request.get_json()
            errors = {}
            
            # Validar cada campo del esquema
            for field, config in schema.items():
                value = data.get(field)
                
                # Campo requerido
                if config.get('required') and value is None:
                    errors[field] = "Este campo es requerido"
                    continue
                    
                # Validar tipo de dato
                if value is not None and 'type' in config:
                    if not isinstance(value, config['type']):
                        errors[field] = f"Debe ser de tipo {config['type'].__name__}"
                
                # Validar formato de email
                if field == 'email' and value and not re.match(r"[^@]+@[^@]+\.[^@]+", value):
                    errors[field] = "Formato de email inválido"
                
                # Validar longitud mínima de contraseña
                if field == 'password' and value and len(value) < 8:
                    errors[field] = "La contraseña debe tener al menos 8 caracteres"
            
            if errors:
                return jsonify({"errors": errors}), 400
                
            return f(*args, **kwargs)
        return wrapper
    return decorator
from flask import jsonify, request
from functools import wraps
import re

def validate_request(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            
            if not request.is_json:
                return jsonify({"error": "El body debe ser un JSON"}), 400
                
            data = request.get_json()
            errors = {}
            
            for field, config in schema.items():
                value = data.get(field)
                
                if config.get('required') and value is None:
                    errors[field] = "Este campo es requerido"
                    continue
                    
                if value is not None and 'type' in config:
                    if not isinstance(value, config['type']):
                        errors[field] = f"Debe ser de tipo {config['type'].__name__}"
                        continue
                
                if field == 'email' and value and not re.match(r"[^@]+@[^@]+\.[^@]+", value):
                    errors[field] = "Formato de email inválido"
                    continue
                
                if field == 'password' and value and len(value) < 8:
                    errors[field] = "La contraseña debe tener al menos 8 caracteres"
                    continue
            
            if errors:
                return jsonify({"errors": errors}), 400
                
            return f(*args, **kwargs)
        return wrapper
    return decorator
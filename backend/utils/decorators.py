from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if not claims.get('is_admin', False):
            return {'result': 'Se requieren privilegios de admin'}, 403
        return fn(*args, **kwargs)
    return wrapper
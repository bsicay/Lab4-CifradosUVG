from werkzeug.security import generate_password_hash, check_password_hash
from backend.models.db import execute_query
from datetime import datetime

class UserModel:
    def create(email, password):
        hashed_pw = generate_password_hash(password)
        execute_query(
            "INSERT INTO users (email, password) VALUES (%s, %s)",
            (email, hashed_pw),
            commit=True
        )
    
    def get_by_email(email):
        cur = execute_query("SELECT * FROM users WHERE email = %s", (email,))
        if cur.description:  # Verifica si hay resultados
            columns = [col[0] for col in cur.description]  # Nombres de columnas
            user = cur.fetchone()
            return dict(zip(columns, user)) if user else None  # Conversión a diccionario
        return None
    
    def verify_password(email, password):
        user = UserModel.get_by_email(email)
        if user and check_password_hash(user['password'], password):
            return user
        return None
    
    def revoke_refresh_token(token):
        execute_query(
            "INSERT INTO revoked_tokens (token, revoked_at) VALUES (%s, %s)",
            (token, datetime.now()),
            commit=True
        )

    def is_token_revoked(token):
        cur = execute_query(
            "SELECT token FROM revoked_tokens WHERE token = %s",
            (token,)
        )
        print(f"CUR: {cur}")
        return cur.fetchone() is not None
    
    def update_public_key(email, public_key):
        execute_query(
            "UPDATE users SET current_public_key = %s WHERE email = %s",
            (public_key, email),
            commit=True
        )
        
    def get_by_id(user_id):
        cur = execute_query("SELECT * FROM users WHERE id = %s", (user_id,))
        return cur.fetchone()
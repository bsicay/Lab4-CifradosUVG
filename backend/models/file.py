from backend.models.db import execute_query
from datetime import datetime

class FileModel:
    def save_file(user_id, filename, content, file_hash, public_key, signature):
        cur = execute_query(
            """INSERT INTO files 
            (user_id, filename, content, file_hash, public_key, signature, uploaded_at) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (user_id, filename, content, file_hash, public_key, signature, datetime.now()),
            commit=True
        )
        return cur.lastrowid
    
    def get_all_files():
        cur = execute_query("""
            SELECT f.*, u.email 
            FROM files f
            JOIN users u ON f.user_id = u.id
        """)
        return cur.fetchall()
    
    def get_file(file_id):
        cur = execute_query(f"SELECT * FROM files WHERE id = {file_id}")
        if cur.description:
            columns = [col[0] for col in cur.description]
            user = cur.fetchone()
            return dict(zip(columns, user)) if user else None
        return None
    
    
    
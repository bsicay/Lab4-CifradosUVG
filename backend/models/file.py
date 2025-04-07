from backend.models.db import execute_query
from datetime import datetime

class FileModel:
    def save_file(user_id, filename, content, public_key, is_signed=False):
        execute_query(
            """INSERT INTO files 
            (user_id, filename, content, public_key, is_signed, uploaded_at) 
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (user_id, filename, content, public_key, is_signed, datetime.now()),
            commit=True
        )
    
    def get_all_files():
        cur = execute_query("""
            SELECT f.*, u.email 
            FROM files f
            JOIN users u ON f.user_id = u.id
        """)
        return cur.fetchall()
    
    def get_file(file_id):
        cur = execute_query("SELECT * FROM files WHERE id = %s", (file_id,))
        return cur.fetchone()
    
    
    
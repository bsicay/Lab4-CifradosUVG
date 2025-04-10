from backend.models.db import execute_query
from datetime import datetime

class FileModel:
    def save_file(owner, filename, content, public_key, signature):
        cur = execute_query(
            """SELECT * FROM files WHERE filename = %s AND owner = %s""",
            (filename, owner)
        )
        
        if cur.fetchone():
            execute_query(
                """DELETE FROM files WHERE filename = %s AND owner = %s""",
                (filename, owner),
                commit=True
            )
        
        cur = execute_query(
            """INSERT INTO files 
            (owner, filename, content, public_key, signature, uploaded_at) 
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (owner, filename, content, public_key, signature, datetime.now()),
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
    
    def get_file_by_owner_name(owner, filename):
        query = f"SELECT * FROM files WHERE owner = '{owner}' AND filename = '{filename}'"
        print("Query:", query)
        cur = execute_query(query)
        if cur.description:
            columns = [col[0] for col in cur.description]
            user = cur.fetchone()
            return dict(zip(columns, user)) if user else None
        return None
    
    
    
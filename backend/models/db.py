from backend import mysql

def execute_query(query, args=(), commit=False):
    cur = mysql.connection.cursor()
    cur.execute(query, args)
    if commit:
        mysql.connection.commit()
    return cur
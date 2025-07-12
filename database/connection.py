import sqlite3

def create_connection(db_file="inventory_system.db"):
    """Establece una conexión a la base de datos SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        pass
    return conn

def execute_query(conn, query, params=None):
    """Ejecuta una consulta SQL."""
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
    except sqlite3.Error as e:
        pass

def close_connection(conn):
    """Cierra la conexión a la base de datos."""
    if conn:
        conn.close()
from database.database import get_connection

def create_material(material):
    """Crea un nuevo material en la base de datos."""
    conn = get_connection()
    sql = ''' INSERT INTO materiales(nombre, descripcion, cantidad_stock, unidad_medida, costo_por_unidad, proveedor)
              VALUES(?, ?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, material)
    conn.commit()
    conn.close()
    return cur.lastrowid

def read_all_materials():
    """Obtiene todos los materiales de la base de datos."""
    conn = get_connection()
    sql = ''' SELECT * FROM materiales '''
    cur = conn.cursor()
    cur.execute(sql)
    materials = cur.fetchall()
    conn.close()
    return materials

def read_material(material_id):
    """Obtiene un material específico por su ID."""
    conn = get_connection()
    sql = ''' SELECT * FROM materiales WHERE id_material=? '''
    cur = conn.cursor()
    cur.execute(sql, (material_id,))
    material = cur.fetchone()
    conn.close()
    return material

def update_material(material_id, updated_material):
    """Actualiza un material existente en la base de datos."""
    conn = get_connection()
    sql = ''' UPDATE materiales
              SET nombre = ?,
                  descripcion = ?,
                  cantidad_stock = ?,
                  unidad_medida = ?,
                  costo_por_unidad = ?,
                  proveedor = ?
              WHERE id_material = ? '''
    cur = conn.cursor()
    cur.execute(sql, (*updated_material, material_id))
    conn.commit()
    conn.close()

def delete_material(material_id):
    """Elimina un material de la base de datos por su ID."""
    conn = get_connection()
    sql = ''' DELETE FROM materiales WHERE id_material=? '''
    cur = conn.cursor()
    cur.execute(sql, (material_id,))
    conn.commit()
    conn.close()
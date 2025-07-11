from database.database import get_connection

def create_recipe(recipe):
    """Crea una nueva receta en la base de datos."""
    conn = get_connection()
    sql = ''' INSERT INTO recetas(id_producto, version, fecha_creacion, costo_total_receta)
              VALUES(?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, recipe)
    conn.commit()
    recipe_id = cur.lastrowid
    conn.close()
    return recipe_id

def read_all_recipes():
    """Obtiene todas las recetas de la base de datos."""
    conn = get_connection()
    sql = ''' SELECT * FROM recetas '''
    cur = conn.cursor()
    cur.execute(sql)
    recipes = cur.fetchall()
    conn.close()
    return recipes

def read_recipe(recipe_id):
    """Obtiene una receta específica por su ID."""
    conn = get_connection()
    sql = ''' SELECT * FROM recetas WHERE id_receta=? '''
    cur = conn.cursor()
    cur.execute(sql, (recipe_id,))
    recipe = cur.fetchone()
    conn.close()
    return recipe

def update_recipe(recipe_id, updated_recipe):
    """Actualiza una receta existente en la base de datos."""
    conn = get_connection()
    sql = ''' UPDATE recetas
              SET id_producto = ?,
                  version = ?,
                  fecha_creacion = ?,
                  costo_total_receta = ?
              WHERE id_receta = ? '''
    cur = conn.cursor()
    cur.execute(sql, (*updated_recipe, recipe_id))
    conn.commit()
    conn.close()

def delete_recipe(recipe_id):
    """Elimina una receta de la base de datos por su ID."""
    conn = get_connection()
    sql = ''' DELETE FROM recetas WHERE id_receta=? '''
    cur = conn.cursor()
    cur.execute(sql, (recipe_id,))
    conn.commit()
    conn.close()


def add_materials_to_recipe(recipe_id, materials):
    """
    Agrega múltiples materiales a una receta en la tabla detalle_receta.
    :param recipe_id: ID de la receta a la que se agregarán los materiales.
    :param materials: Lista de tuplas (id_material, cantidad_requerida, costo_parcial).
    """
    conn = get_connection()
    sql = ''' INSERT INTO detalle_receta(id_receta, id_material, cantidad_requerida, costo_parcial)
              VALUES(?, ?, ?, ?) '''
    cur = conn.cursor()
    for material in materials:
        # material debe ser (id_material, cantidad_requerida, costo_parcial)
        cur.execute(sql, (recipe_id, material[0], material[1], material[2]))
    conn.commit()
    conn.close()


def get_recipe_cost(recipe_id):
    """
    Obtiene el costo total de una receta específica.
    
    :param recipe_id: ID de la receta.
    :return: Costo total de la receta.
    """
    conn = get_connection()
    sql = ''' SELECT SUM(costo_parcial) 
              FROM detalle_receta 
              WHERE id_receta = ? '''
    cur = conn.cursor()
    cur.execute(sql, (recipe_id,))
    cost = cur.fetchone()[0]
    conn.close()
    return cost if cost else 0.0

def get_recipe_details(recipe_id):
    """Obtiene los detalles de los materiales asociados a una receta."""
    conn = get_connection()
    sql = ''' SELECT dr.id_material, m.nombre, dr.cantidad_requerida, dr.costo_parcial
              FROM detalle_receta dr
              JOIN materiales m ON dr.id_material = m.id_material
              WHERE dr.id_receta = ? '''
    cur = conn.cursor()
    cur.execute(sql, (recipe_id,))
    details = cur.fetchall()
    conn.close()
    return details
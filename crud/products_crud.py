from database.database import get_connection
from crud.recipes_crud import get_recipe_cost

def update_product_cost_from_recipe(product_id):
    """
    Actualiza el costo de producción de un producto basado en el costo de su receta.
    
    :param product_id: ID del producto.
    """
    conn = get_connection()
    # Obtener el ID de la receta asociada al producto
    sql_recipe = ''' SELECT id_receta FROM recetas WHERE id_producto = ? '''
    cur = conn.cursor()
    cur.execute(sql_recipe, (product_id,))
    recipe = cur.fetchone()

    if recipe:
        recipe_id = recipe[0]
        # Obtener el costo total de la receta
        recipe_cost = get_recipe_cost(recipe_id)
        # Actualizar el costo de producción del producto
        sql_update = ''' UPDATE productos_terminados
                         SET costo_produccion = ?
                         WHERE id_producto = ? '''
        cur.execute(sql_update, (recipe_cost, product_id))
        conn.commit()

    conn.close()


def create_product(product):
    """Crea un nuevo producto en la base de datos."""
    conn = get_connection()
    sql = ''' INSERT INTO productos_terminados(nombre, descripcion, cantidad_stock, unidad_medida, precio_venta)
              VALUES(?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, product)
    conn.commit()
    conn.close()
    return cur.lastrowid

def read_all_products():
    """Obtiene todos los productos de la base de datos."""
    conn = get_connection()
    sql = ''' SELECT * FROM productos_terminados '''
    cur = conn.cursor()
    cur.execute(sql)
    products = cur.fetchall()
    conn.close()
    return products

def read_product(product_id):
    """Obtiene un producto específico por su ID."""
    conn = get_connection()
    sql = ''' SELECT * FROM productos_terminados WHERE id_producto=? '''
    cur = conn.cursor()
    cur.execute(sql, (product_id,))
    product = cur.fetchone()
    conn.close()
    return product

def update_product(product_id, updated_product):
    """Actualiza un producto existente en la base de datos."""
    conn = get_connection()
    sql = ''' UPDATE productos_terminados
              SET nombre = ?,
                  descripcion = ?,
                  cantidad_stock = ?,
                  unidad_medida = ?,
                  precio_venta = ?
              WHERE id_producto = ? '''
    cur = conn.cursor()
    cur.execute(sql, (*updated_product, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    """Elimina un producto de la base de datos por su ID."""
    conn = get_connection()
    sql = ''' DELETE FROM productos_terminados WHERE id_producto=? '''
    cur = conn.cursor()
    cur.execute(sql, (product_id,))
    conn.commit()
    conn.close()
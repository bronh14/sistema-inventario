from crud.materials_crud import create_material, read_material, update_material, delete_material
from crud.products_crud import create_product, read_product, update_product, delete_product
from crud.recipes_crud import create_recipe, read_recipe, update_recipe, delete_recipe, get_recipe_details
from database.database import get_connection

class InventoryService:
    def __init__(self):
        pass

    def add_material(self, name, description, quantity, unit, cost, supplier):
        return create_material((name, description, quantity, unit, cost, supplier))

    def get_material(self, material_id):
        return read_material(material_id)

    def update_material(self, material_id, name, description, quantity, unit, cost, supplier):
        return update_material(material_id, (name, description, quantity, unit, cost, supplier))

    def remove_material(self, material_id):
        return delete_material(material_id)

    def add_product(self, name, description, quantity, unit, price):
        return create_product((name, description, quantity, unit, price))

    def get_product(self, product_id):
        return read_product(product_id)

    def update_product(self, product_id, name, description, quantity, unit, price):
        return update_product(product_id, (name, description, quantity, unit, price))

    def remove_product(self, product_id):
        return delete_product(product_id)

    def add_recipe(self, product_id, version, date, cost):
        return create_recipe((product_id, version, date, cost))

    def get_recipe(self, recipe_id):
        return read_recipe(recipe_id)

    def update_recipe(self, recipe_id, product_id, version, date, cost):
        return update_recipe(recipe_id, (product_id, version, date, cost))

    def remove_recipe(self, recipe_id):
        return delete_recipe(recipe_id)


def produce_product_from_recipe(recipe_id, cantidad_a_producir):
    # 1. Obtener receta y materiales
    receta = read_recipe(recipe_id)
    if not receta:
        return False, 'Receta no encontrada.'
    id_producto = receta[1]
    materiales = get_recipe_details(recipe_id)
    # 2. Verificar stock suficiente
    for mat_id, nombre, cantidad_requerida, _ in materiales:
        mat = read_material(mat_id)
        if not mat:
            return False, f'Material {nombre} no encontrado.'
        stock_actual = mat[3]  # cantidad_stock
        total_requerido = float(cantidad_requerida) * cantidad_a_producir
        if stock_actual < total_requerido:
            return False, f'Stock insuficiente de {nombre}. Requiere {total_requerido}, hay {stock_actual}.'
    # 3. Restar materiales
    for mat_id, nombre, cantidad_requerida, _ in materiales:
        mat = read_material(mat_id)
        stock_actual = mat[3]  # cantidad_stock
        total_requerido = float(cantidad_requerida) * cantidad_a_producir
        nuevo_stock = stock_actual - total_requerido
        updated_material = (mat[1], mat[2], nuevo_stock, mat[4], mat[5], mat[6])
        update_material(mat_id, updated_material)
    # 4. Sumar cantidad al producto terminado
    prod = read_product(id_producto)
    if not prod:
        return False, 'Producto terminado no encontrado.'
    nuevo_stock_prod = prod[3] + cantidad_a_producir
    updated_product = (prod[1], prod[2], nuevo_stock_prod, prod[4], prod[5])
    update_product(id_producto, updated_product)
    return True, f'Producción exitosa. Se produjeron {cantidad_a_producir} unidades.'
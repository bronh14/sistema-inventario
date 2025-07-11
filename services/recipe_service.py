# filepath: c:\Users\Bronh14\Desktop\inventario porpuse\src\services\recipe_service.py
from crud.recipes_crud import create_recipe, read_recipe, update_recipe, delete_recipe
from models.recipes import Recipe

class RecipeService:
    def add_recipe(self, product_id, materials):
        recipe = Recipe(product_id=product_id, materials=materials)
        return create_recipe(recipe)

    def view_recipe(self, recipe_id):
        return read_recipe(recipe_id)

    def modify_recipe(self, recipe_id, materials):
        recipe = Recipe(id=recipe_id, materials=materials)
        return update_recipe(recipe)

    def remove_recipe(self, recipe_id):
        return delete_recipe(recipe_id)
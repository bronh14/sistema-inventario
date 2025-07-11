class Recipe:
    def __init__(self, id, producto_id, materiales):
        self.id = id
        self.producto_id = producto_id
        self.materiales = materiales

    def agregar_material(self, material):
        self.materiales.append(material)

    def eliminar_material(self, material):
        self.materiales.remove(material)

    def obtener_materiales(self):
        return self.materiales

    def __repr__(self):
        return f"Recipe(id={self.id}, producto_id={self.producto_id}, materiales={self.materiales})"
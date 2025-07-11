class Product:
    def __init__(self, id, nombre, precio):
        self.id = id
        self.nombre = nombre
        self.precio = precio

    def __repr__(self):
        return f"Product(id={self.id}, nombre='{self.nombre}', precio={self.precio})"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio
        }

    @staticmethod
    def from_dict(data):
        return Product(
            id=data['id'],
            nombre=data['nombre'],
            precio=data['precio']
        )
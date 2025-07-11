class Material:
    def __init__(self, id, nombre, cantidad):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad

    def __repr__(self):
        return f"Material(id={self.id}, nombre='{self.nombre}', cantidad={self.cantidad})"

    def actualizar_cantidad(self, cantidad):
        self.cantidad += cantidad

    def reducir_cantidad(self, cantidad):
        if cantidad <= self.cantidad:
            self.cantidad -= cantidad
        else:
            raise ValueError("No hay suficiente cantidad disponible.")
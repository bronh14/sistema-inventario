import sqlite3

def get_connection():
    """Establece y retorna una conexión a la base de datos."""
    return sqlite3.connect("inventory_system.db")

def initialize_database():
    """Crea las tablas necesarias si no existen."""
    conn = get_connection()
    cursor = conn.cursor()

    # Habilitar claves foráneas
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Verificar si la columna valor_total existe en pedidos
    cursor.execute("PRAGMA table_info(pedidos)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'valor_total' not in columns:
        cursor.execute("ALTER TABLE pedidos ADD COLUMN valor_total REAL;")

    # Tabla productos_terminados
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos_terminados (
        id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        descripcion TEXT,
        cantidad_stock INTEGER,
        unidad_medida TEXT,
        precio_venta REAL
    );
    """)

    # Tabla materiales
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS materiales (
        id_material INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        descripcion TEXT,
        cantidad_stock INTEGER,
        unidad_medida TEXT,
        costo_por_unidad REAL,
        proveedor TEXT
    );
    """)

    # Tabla recetas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recetas (
        id_receta INTEGER PRIMARY KEY AUTOINCREMENT,
        id_producto INTEGER,
        version TEXT,
        fecha_creacion DATE,
        costo_total_receta REAL,
        FOREIGN KEY (id_producto) REFERENCES productos_terminados(id_producto)
    );
    """)

    # Tabla detalle_receta
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detalle_receta (
        id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
        id_receta INTEGER,
        id_material INTEGER,
        cantidad_requerida REAL,
        costo_parcial REAL,
        FOREIGN KEY (id_receta) REFERENCES recetas(id_receta),
        FOREIGN KEY (id_material) REFERENCES materiales(id_material)
    );
    """)

    # Tabla movimientos_inventario
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimientos_inventario (
        id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,
        id_producto INTEGER,
        id_material INTEGER,
        cantidad REAL,
        fecha DATE,
        notas TEXT,
        costo_total REAL,
        FOREIGN KEY (id_producto) REFERENCES productos_terminados(id_producto),
        FOREIGN KEY (id_material) REFERENCES materiales(id_material)
    );
    """)
    #Tabla pedidos (sin producto_id ni cantidad)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT,
        estado TEXT,
        fecha TEXT)
    """);
    
    #Nueva tabla detalle_pedido
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detalle_pedido (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER,
        producto_id INTEGER,
        cantidad REAL,
        FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
        FOREIGN KEY (producto_id) REFERENCES productos_terminados(id_producto))
    """);

    # Tabla balance_ventas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS balance_ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        monto REAL,
        fecha DATE,
        pedido_id INTEGER
    );
    """)

    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    conn.close()
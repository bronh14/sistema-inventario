from database.database import get_connection
from crud.products_crud import read_product


def create_order_with_products(cliente, estado, fecha, productos):
    """
    Crea un pedido y asocia varios productos.
    productos: lista de tuplas (producto_id, cantidad)
    """
    conn = get_connection()
    cur = conn.cursor()
    # Calcular valor total del pedido
    valor_total = 0
    for prod_id, cantidad in productos:
        prod = read_product(prod_id)
        if prod and len(prod) > 5:
            # precio_venta está en el índice 5 (6to campo)
            precio_venta = prod[5] if prod[5] is not None else 0
        else:
            # Si el producto no existe o no tiene precio, usar 0
            precio_venta = 0
        valor_total += precio_venta * cantidad
    cur.execute("INSERT INTO pedidos (cliente, estado, fecha, valor_total) VALUES (?, ?, ?, ?)", (cliente, estado, fecha, valor_total))
    pedido_id = cur.lastrowid
    detalle = [(pedido_id, prod_id, cantidad) for prod_id, cantidad in productos]
    cur.executemany("INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad) VALUES (?, ?, ?)", detalle)
    conn.commit()
    conn.close()
    add_to_balance_if_entregado(pedido_id, estado)

def read_orders_grouped():
    """
    Devuelve un diccionario: {pedido_id: {"info": (id, cliente, estado, fecha), "productos": [(nombre, cantidad), ...]}}
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id, p.cliente, p.estado, p.fecha, pt.nombre, dp.cantidad
        FROM pedidos p
        JOIN detalle_pedido dp ON p.id = dp.pedido_id
        JOIN productos_terminados pt ON dp.producto_id = pt.id_producto
        ORDER BY p.id DESC
    """)
    rows = cur.fetchall()
    conn.close()
    pedidos = {}
    for row in rows:
        pedido_id = row[0]
        info = row[:4]
        producto = (row[4], row[5])
        if pedido_id not in pedidos:
            pedidos[pedido_id] = {"info": info, "productos": []}
        pedidos[pedido_id]["productos"].append(producto)
    return pedidos

def update_order(order_id, updated_order, productos=None):
    """
    updated_order: tupla (cliente, estado, fecha)
    productos: lista de tuplas (producto_id, cantidad) o None
    """
    print(f"[DEBUG][update_order] order_id: {order_id}, updated_order: {updated_order}")
    conn = get_connection()
    cur = conn.cursor()
    # Si se pasan productos, recalcular valor_total
    if productos is not None:
        valor_total = 0
        for prod_id, cantidad in productos:
            prod = read_product(prod_id)
            if prod and len(prod) > 5:
                # precio_venta está en el índice 5 (6to campo)
                precio_venta = prod[5] if prod[5] is not None else 0
            else:
                # Si el producto no existe o no tiene precio, usar 0
                precio_venta = 0
            valor_total += precio_venta * cantidad
        cur.execute("UPDATE pedidos SET cliente=?, estado=?, fecha=?, valor_total=? WHERE id=?", (*updated_order, valor_total, order_id))
    else:
        cur.execute("UPDATE pedidos SET cliente=?, estado=?, fecha=? WHERE id=?", (*updated_order, order_id))
    print(f"[DEBUG][update_order] Ejecutada consulta UPDATE pedidos SET cliente={updated_order[0]}, estado={updated_order[1]}, fecha={updated_order[2]} WHERE id={order_id}")
    conn.commit()
    conn.close()
    # Verificar si el estado es 'Entregado' y registrar en balance
    add_to_balance_if_entregado(order_id, updated_order[1])

def delete_order(order_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM pedidos WHERE id=?", (order_id,))
    conn.commit()
    conn.close()

def add_to_balance_if_entregado(pedido_id, estado):
    if estado.lower() == 'entregado':
        conn = get_connection()
        cur = conn.cursor()
        # Verificar si ya existe registro para este pedido
        cur.execute("SELECT COUNT(*) FROM balance_ventas WHERE pedido_id=?", (pedido_id,))
        if cur.fetchone()[0] == 0:
            cur.execute("SELECT valor_total, fecha FROM pedidos WHERE id=?", (pedido_id,))
            row = cur.fetchone()
            if row:
                monto, fecha = row
                cur.execute("INSERT INTO balance_ventas (monto, fecha, pedido_id) VALUES (?, ?, ?)", (monto, fecha, pedido_id))
                conn.commit()
        conn.close()
import tkinter as tk
from tkinter import Frame, Label, Button
from interfaces.colors import FONDO_CLARO, TABLA_HEADER, TABLA_FILA, TABLA_FILA_ALTERNA, TEXTO, BOTON_PRINCIPAL, BOTON_EXITO, BOTON_PELIGRO, TEXTO_SECUNDARIO, BORDER
from crud.products_crud import read_all_products
from crud.materials_crud import read_all_materials
from crud.recipes_crud import read_all_recipes
from crud.orders_crud import read_orders_grouped
from interfaces.view_products import add_product_form
from interfaces.view_orders import add_order_form
from interfaces.view_materials import add_material_form
from interfaces.view_recipes import add_recipe_form
from PIL import Image, ImageTk
from database.database import get_connection
from tkinter import messagebox

def show_dashboard_view(gui):
    gui.clear_main_frame()
    gui.styled_label(gui.main_frame, "Dashboard", size=22, bold=True, fg=TEXTO, bg=FONDO_CLARO, pady=4).pack(anchor="w", padx=32, pady=(24, 0))
    Label(gui.main_frame, text="Visión general del sistema de inventario", font=("Segoe UI", 13), fg=TEXTO_SECUNDARIO, bg=FONDO_CLARO).pack(anchor="w", padx=32, pady=(0, 18))

    # Cargar imágenes de tarjetas (solo una vez)
    if not hasattr(gui, 'dashboard_card_images'):
        img_files = [
            "assets/productos.png",
            "assets/pedidos.png",
            "assets/materiales.png",
            "assets/recetas.png"
        ]
        gui.dashboard_card_images = []
        for path in img_files:
            try:
                img = Image.open(path)
                img = img.resize((38, 38), Image.Resampling.LANCZOS)
                gui.dashboard_card_images.append(ImageTk.PhotoImage(img))
            except Exception:
                gui.dashboard_card_images.append(None)

    # Tarjetas resumen
    resumen_frame = Frame(gui.main_frame, bg=FONDO_CLARO)
    resumen_frame.pack(fill="x", padx=24, pady=(0, 18))
    num_cards = len(_get_summary_cards())
    for i in range(num_cards):
        resumen_frame.columnconfigure(i, weight=1)
    cards = _get_summary_cards()
    for i, card in enumerate(cards):
        card_frame = Frame(resumen_frame, bg=TABLA_FILA, bd=0, highlightbackground=BORDER, highlightthickness=1)
        card_frame.grid(row=0, column=i, padx=12, ipadx=18, ipady=12, sticky="nsew")
        top_row = Frame(card_frame, bg=TABLA_FILA)
        top_row.pack(fill="x", pady=(8,0), padx=8)
        img = gui.dashboard_card_images[i] if hasattr(gui, 'dashboard_card_images') and i < len(gui.dashboard_card_images) else None
        if img:
            Label(top_row, image=img, bg=TABLA_FILA).pack(side="left", anchor="n", padx=(0,8))
        Label(top_row, text=card['title'], font=("Segoe UI", 11), fg=card['color'], bg=TABLA_FILA).pack(side="left", anchor="n")
        Label(top_row, text=card['value'], font=("Segoe UI", 22, "bold"), fg=TEXTO, bg=TABLA_FILA, padx=12).pack(side="right", anchor="n")
        if card.get('badge'):
            Label(card_frame, text=card['badge'], font=("Segoe UI", 10), fg="white", bg=card['badge_color'], padx=8, pady=2).pack(anchor="w", pady=(0,8), padx=8)
        if card.get('subtext'):
            Label(card_frame, text=card['subtext'], font=("Segoe UI", 9), fg=card['color'], bg=TABLA_FILA).pack(anchor="w", pady=(0,8), padx=8)

    # Botón para restablecer balance
    def reset_balance():
        if messagebox.askyesno("Restablecer balance", "¿Estás seguro de restablecer el balance? Esta acción no se puede deshacer."):
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM balance_ventas")
            conn.commit()
            conn.close()
            show_dashboard_view(gui)
    balance_frame = Frame(gui.main_frame, bg=FONDO_CLARO)
    balance_frame.pack(fill="x", padx=24, pady=(0, 8))
    Button(balance_frame, text="Restablecer balance", command=reset_balance, bg=BOTON_PELIGRO, fg="white", font=("Segoe UI", 11, "bold"), padx=16, pady=6, relief="flat", cursor="hand2").pack(anchor="e", padx=8, pady=4)

    # Acciones rápidas y actividad reciente
    paneles = Frame(gui.main_frame, bg=FONDO_CLARO)
    paneles.pack(fill="x", padx=24, pady=(0, 18))
    acciones = Frame(paneles, bg=TABLA_FILA, bd=0, highlightbackground=BORDER, highlightthickness=1)
    acciones.pack(side="left", fill="both", expand=True, padx=8, ipadx=12, ipady=8)
    Label(acciones, text="Acciones Rápidas", font=("Segoe UI", 13, "bold"), fg=TEXTO, bg=TABLA_FILA).pack(anchor="w", pady=(8,0))
    for txt, cmd in _get_quick_actions(gui):
        btn = tk.Button(acciones, text=txt, font=("Segoe UI", 11), bg=FONDO_CLARO, fg=BOTON_PRINCIPAL, bd=0, relief="groove", padx=10, pady=6, highlightbackground=BORDER, highlightthickness=1, cursor="hand2")
        btn.pack(fill="x", pady=6, padx=8)
        btn.configure(command=cmd)
    actividad = Frame(paneles, bg=TABLA_FILA, bd=0, highlightbackground=BORDER, highlightthickness=1)
    actividad.pack(side="left", fill="both", expand=True, padx=8, ipadx=12, ipady=8)
    Label(actividad, text="Actividad Reciente", font=("Segoe UI", 13, "bold"), fg=TEXTO, bg=TABLA_FILA).pack(anchor="w", pady=(8,0))
    for act in _get_recent_activity():
        row = Frame(actividad, bg=TABLA_FILA)
        row.pack(fill="x", pady=4, padx=4)
        Label(row, text=act['text'], font=("Segoe UI", 10), fg=TEXTO, bg=TABLA_FILA).pack(side="left", anchor="w")
        if act.get('badge'):
            Label(row, text=act['badge'], font=("Segoe UI", 9), fg="white", bg=act['badge_color'], padx=8, pady=2).pack(side="right", anchor="e")

def _get_summary_cards():
    productos = read_all_products()
    pedidos = read_orders_grouped()
    materiales = read_all_materials()
    recetas = read_all_recipes()
    stock_bajo = sum(1 for m in materiales if m[3] is not None and m[3] < 5)
    pedidos_activos = [p for p in pedidos.values() if p['info'][2].lower().startswith('pendiente')]
    # Calcular total histórico de ventas
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT SUM(valor_total) FROM pedidos")
    total_ventas = cur.fetchone()[0] or 0
    cur.execute("SELECT SUM(monto) FROM balance_ventas")
    balance = cur.fetchone()[0] or 0
    conn.close()
    return [
        {"title": "Total Productos", "value": str(len(productos)), "color": BOTON_PRINCIPAL, "subtext": "", "badge": None},
        {"title": "Pedidos Activos", "value": str(len(pedidos_activos)), "color": BOTON_EXITO, "subtext": f"{len(pedidos_activos)} nuevos hoy", "badge": None},
        {"title": "Materiales", "value": str(len(materiales)), "color": BOTON_PELIGRO if stock_bajo else BOTON_PRINCIPAL, "subtext": f"{stock_bajo} con stock bajo" if stock_bajo else "", "badge": None, "badge_color": BOTON_PELIGRO if stock_bajo else BOTON_PRINCIPAL},
        {"title": "Recetas Activas", "value": str(len(recetas)), "color": "#7C3AED", "subtext": "", "badge": None},
        {"title": "Balance Permanente", "value": f"$ {balance:.2f}", "color": BOTON_EXITO, "subtext": "Solo aumenta con entregas", "badge": None},
    ]

def _get_quick_actions(gui):
    return [
        ("+ Nuevo Producto", lambda: add_product_form(gui)),
        ("Crear Pedido", lambda: add_order_form(gui)),
        ("Añadir Material", lambda: add_material_form(gui)),
        ("Nueva Receta", lambda: add_recipe_form(gui)),
    ]

def _get_recent_activity():
    pedidos = read_orders_grouped()
    productos = read_all_products()
    materiales = read_all_materials()
    actividad = []
    # Últimos 3 pedidos
    for p in list(pedidos.values())[:3]:
        actividad.append({
            "text": f"Pedido #{p['info'][0]} {p['info'][2]}",
            "badge": p['info'][2],
            "badge_color": BOTON_EXITO if 'entregado' in p['info'][2].lower() else BOTON_PELIGRO if 'pendiente' in p['info'][2].lower() else BOTON_PRINCIPAL
        })
    # Stock bajo
    for m in materiales:
        if m[3] is not None and m[3] < 5:
            actividad.append({
                "text": f"Stock bajo: {m[1]}",
                "badge": "Alerta", "badge_color": BOTON_PELIGRO
            })
    # Último producto añadido
    if productos:
        actividad.append({
            "text": f"Nuevo producto añadido: {productos[-1][1]}",
            "badge": "Nuevo", "badge_color": BOTON_PRINCIPAL
        })
    return actividad[:5] 
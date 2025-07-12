import tkinter as tk
from tkinter import Frame, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from crud.materials_crud import read_all_materials
from crud.products_crud import read_all_products
from crud.recipes_crud import read_all_recipes
from crud.orders_crud import read_orders_grouped
from interfaces.colors import TABLA_HEADER, TABLA_FILA_ALTERNA, TABLA_FILA, TEXTO, FONDO_CLARO, BORDER, BOTON_PRINCIPAL
import pandas as pd
import os
from tkinter import filedialog
from database.database import get_connection

def show_graphics_view(gui):
    gui.clear_main_frame()
    # Panel principal tipo tarjeta
    card = tk.Frame(gui.main_frame, bg=TABLA_FILA, bd=0, highlightbackground=BORDER, highlightthickness=1)
    card.pack(fill="both", expand=True, padx=32, pady=32)
    gui.styled_label(card, "Gráficas y Reportes", size=20, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=8).pack(anchor="w", padx=24, pady=(18, 0))
    tk.Label(card, text="Visualiza el estado del inventario en gráficos y reportes visuales", font=("Segoe UI", 12), fg=TEXTO, bg=TABLA_FILA).pack(anchor="w", padx=24, pady=(0, 18))
    tab_control = ttk.Notebook(card)
    tab1 = tk.Frame(tab_control, bg=TABLA_FILA)
    tab2 = tk.Frame(tab_control, bg=TABLA_FILA)
    tab3 = tk.Frame(tab_control, bg=TABLA_FILA)
    tab5 = tk.Frame(tab_control, bg=TABLA_FILA)
    tab_control.add(tab1, text='Stock Materiales')
    tab_control.add(tab2, text='Valor Productos')
    tab_control.add(tab3, text='Costo Recetas')
    tab_control.add(tab5, text='Pedidos Entregados')
    tab_control.pack(expand=1, fill='both', padx=24, pady=10)
    plot_materials_bar(tab1)
    plot_products_pie(tab2)
    list_recipes_cost(tab3)
    list_delivered_orders(tab5)
    # Cargar ícono de Excel si no existe
    if not hasattr(gui, 'excel_icon'):
        try:
            from PIL import Image, ImageTk
            img = Image.open('assets/excel.png')
            img = img.resize((22, 22), Image.Resampling.LANCZOS)
            gui.excel_icon = ImageTk.PhotoImage(img)
        except Exception:
            gui.excel_icon = None
    if gui.excel_icon:
        tk.Button(card, text="Exportar a Excel", command=exportar_excel, bg=BOTON_PRINCIPAL, fg="white", font=("Segoe UI", 11, "bold"), padx=16, pady=6, relief="flat", cursor="hand2", image=gui.excel_icon, compound="left").pack(anchor="e", padx=24, pady=8)
    else:
        tk.Button(card, text="Exportar a Excel", command=exportar_excel, bg=BOTON_PRINCIPAL, fg="white", font=("Segoe UI", 11, "bold"), padx=16, pady=6, relief="flat", cursor="hand2").pack(anchor="e", padx=24, pady=8)

def plot_materials_bar(parent):
    materials = read_all_materials()
    if not materials:
        label = tk.Label(parent, text="No hay materiales para mostrar.", font=("Segoe UI", 14))
        label.pack(pady=20)
        return
    nombres = [m[1] for m in materials]
    stocks = [m[3] for m in materials]
    fig, ax = plt.subplots(figsize=(6,3))
    ax.bar(nombres, stocks, color='skyblue')
    ax.set_title('Stock de Materiales')
    ax.set_ylabel('Cantidad')
    ax.set_xticks(range(len(nombres)))
    ax.set_xticklabels(nombres, rotation=45, ha='right')
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

def plot_products_pie(parent):
    products = read_all_products()
    print("[DEBUG] Productos leídos para gráfica de valor:")
    for p in products:
        print(p)
    if not products:
        label = tk.Label(parent, text="No hay productos para mostrar.", font=("Segoe UI", 14))
        label.pack(pady=20)
        return
    # Filtrar productos con precio_venta y cantidad_stock válidos (permitir precio_venta = 0)
    productos_validos = [p for p in products if p[6] is not None and p[3] is not None and p[3] > 0]
    if not productos_validos:
        label = tk.Label(parent, text="No hay productos con stock válido.", font=("Segoe UI", 14))
        label.pack(pady=20)
        return
    nombres = [f"{p[1]}\n$ {p[6]:.2f}" for p in productos_validos]  # Mostrar nombre y precio de venta
    valores = [p[6]*p[3] for p in productos_validos]  # precio_venta * cantidad_stock
    if not any(valores):
        # Si todos los valores son 0, mostrar la gráfica igual pero con advertencia
        fig, ax = plt.subplots(figsize=(5,4))
        ax.pie([1 for _ in nombres], labels=nombres, autopct=lambda pct: "0", startangle=140)
        ax.set_title('Valor Monetario de Productos en Stock (todos $0)')
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        label = tk.Label(parent, text="Todos los productos tienen precio de venta 0.", font=("Segoe UI", 12), fg="red")
        label.pack(pady=10)
        return
    fig, ax = plt.subplots(figsize=(5,4))
    ax.pie(valores, labels=nombres, autopct='%1.1f%%', startangle=140)
    ax.set_title('Valor Monetario de Productos en Stock')
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

def list_recipes_cost(parent):
    recipes = read_all_recipes()
    if not recipes:
        label = tk.Label(parent, text="No hay recetas para mostrar.", font=("Segoe UI", 14), bg=TABLA_FILA, fg=TEXTO)
        label.pack(pady=20)
        return
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background=TABLA_FILA, fieldbackground=TABLA_FILA, foreground=TEXTO, rowheight=28, font=("Segoe UI", 11), borderwidth=0)
    style.configure("Treeview.Heading", background=TABLA_HEADER, foreground=TEXTO, font=("Segoe UI", 12, "bold"), borderwidth=0)
    style.map("Treeview", background=[("selected", TABLA_FILA_ALTERNA)], foreground=[("selected", BOTON_PRINCIPAL)])
    tree_frame = tk.Frame(parent, bg=TABLA_FILA)
    tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
    tree = ttk.Treeview(tree_frame, columns=("ID", "Producto", "Costo Total"), show="headings")
    vsb = tk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    hsb = tk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tree.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")
    tree.heading("ID", text="ID Receta")
    tree.heading("Producto", text="ID Producto")
    tree.heading("Costo Total", text="Costo Total")
    for r in recipes:
        costo = r[4] if r[4] is not None else 0
        tree.insert("", "end", values=(r[0], r[1], costo))

def list_delivered_orders(parent):
    pedidos = read_orders_grouped()
    all_products = read_all_products()
    entregados = [p for p in pedidos.values() if p['info'][2].lower().startswith('entregado')]
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background=TABLA_FILA, fieldbackground=TABLA_FILA, foreground=TEXTO, rowheight=28, font=("Segoe UI", 11), borderwidth=0)
    style.configure("Treeview.Heading", background=TABLA_HEADER, foreground=TEXTO, font=("Segoe UI", 12, "bold"), borderwidth=0)
    style.map("Treeview", background=[("selected", TABLA_FILA_ALTERNA)], foreground=[("selected", BOTON_PRINCIPAL)])
    columns = ("ID Pedido", "Cliente", "Fecha", "Producto", "Cantidad", "Precio Unitario", "Total")
    tree_frame = tk.Frame(parent, bg=TABLA_FILA)
    tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    vsb = tk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    hsb = tk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tree.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    for p in entregados:
        info = p['info']
        for nombre, cantidad, precio_unitario, total in p['productos']:
            try:
                precio_unitario_str = f"${float(precio_unitario):,.2f}"
            except Exception:
                precio_unitario_str = ''
            try:
                total_str = f"${float(total):,.2f}"
            except Exception:
                total_str = ''
            tree.insert("", "end", values=(info[0], info[1], info[3], nombre, cantidad, precio_unitario_str, total_str))

def exportar_excel():
    ruta = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], title="Guardar reporte de gráficas")
    if not ruta:
        return
    # Datos de materiales
    materials = read_all_materials()
    df_materials = pd.DataFrame(materials)
    df_materials.columns = ["ID", "Nombre", "Descripción", "Cantidad", "Unidad", "Costo", "Proveedor"]
    if not df_materials.empty:
        df_materials["Costo"] = df_materials["Costo"].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else "")
    # Datos de productos
    products = read_all_products()
    df_products = pd.DataFrame(products)
    df_products.columns = ["ID", "Nombre", "Descripción", "Cantidad", "Unidad", "Costo Producción", "Precio Venta"]
    if not df_products.empty:
        df_products["Costo Producción"] = df_products["Costo Producción"].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else "")
        df_products["Precio Venta"] = df_products["Precio Venta"].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else "")
    # Datos de recetas
    recipes = read_all_recipes()
    df_recipes = pd.DataFrame(recipes)
    df_recipes.columns = ["ID", "Producto ID", "Versión", "Fecha", "Costo Total"]
    if not df_recipes.empty:
        df_recipes["Costo Total"] = df_recipes["Costo Total"].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else "")
    # Datos de pedidos
    pedidos = read_orders_grouped()
    pedidos_list = []
    for pid, data in pedidos.items():
        info = data["info"]
        for prod, cant in data["productos"]:
            pedidos_list.append([info[0], info[1], info[2], info[3], prod, cant])
        df_pedidos = pd.DataFrame(pedidos_list, columns=pd.Index(["ID Pedido", "Cliente", "Estado", "Fecha", "Producto", "Cantidad"]))
        # Datos de balance
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, monto, fecha, pedido_id FROM balance_ventas")
    balance = cur.fetchall()
    conn.close()
    df_balance = pd.DataFrame(balance)
    df_balance.columns = ["ID", "Monto", "Fecha", "Pedido ID"]
    # Guardar gráficas como imágenes temporales
    img_paths = []
    # 1. Stock Materiales
    fig1, ax1 = plt.subplots(figsize=(6,3))
    if not df_materials.empty:
        ax1.bar(df_materials["Nombre"], df_materials["Cantidad"], color='skyblue')
        ax1.set_title('Stock de Materiales')
        ax1.set_ylabel('Cantidad')
        ax1.set_xticks(range(len(df_materials["Nombre"])))
        ax1.set_xticklabels(df_materials["Nombre"], rotation=45, ha='right')
    img1 = "stock_materiales.png"
    fig1.savefig(img1, bbox_inches='tight')
    img_paths.append(img1)
    plt.close(fig1)
    # 2. Valor Productos
    fig2, ax2 = plt.subplots(figsize=(5,4))
    productos_validos = [p for p in products if (p[6] if len(p) > 6 else p[5]) is not None and p[3] is not None and p[3] > 0]
    if productos_validos:
        nombres = [f"{p[1]}\n$ {(p[6] if len(p) > 6 else p[5]):.2f}" for p in productos_validos]
        valores = [(p[6] if len(p) > 6 else p[5])*p[3] for p in productos_validos]
        ax2.pie(valores, labels=nombres, autopct='%1.1f%%', startangle=140)
        ax2.set_title('Valor Monetario de Productos en Stock')
    img2 = "valor_productos.png"
    fig2.savefig(img2, bbox_inches='tight')
    img_paths.append(img2)
    plt.close(fig2)
    # 3. Costo Recetas
    fig3, ax3 = plt.subplots(figsize=(6,3))
    if not df_recipes.empty:
        ax3.bar(df_recipes["ID"].astype(str), df_recipes["Costo Total"], color='orange')
        ax3.set_title('Costo Total por Receta')
        ax3.set_ylabel('Costo Total')
    img3 = "costo_recetas.png"
    fig3.savefig(img3, bbox_inches='tight')
    img_paths.append(img3)
    plt.close(fig3)
    # 4. Pedidos Pendientes
    fig4, ax4 = plt.subplots(figsize=(5,2))
    pendientes = [p for p in pedidos.values() if p['info'][2].lower().startswith('pendiente')]
    ax4.bar([str(p['info'][0]) for p in pendientes], [len(p['productos']) for p in pendientes], color='green')
    ax4.set_title('Pedidos Pendientes (Cantidad de productos por pedido)')
    img4 = "pedidos_pendientes.png"
    fig4.savefig(img4, bbox_inches='tight')
    img_paths.append(img4)
    plt.close(fig4)
    # Escribir a Excel
    with pd.ExcelWriter(ruta, engine="xlsxwriter") as writer:
        df_materials.to_excel(writer, sheet_name="Materiales", index=False)
        df_products.to_excel(writer, sheet_name="Productos", index=False)
        df_recipes.to_excel(writer, sheet_name="Recetas", index=False)
        df_pedidos.to_excel(writer, sheet_name="Pedidos", index=False)
        df_balance.to_excel(writer, sheet_name="Balance", index=False)
        # Insertar imágenes en hoja "Graficas"
        workbook = writer.book
        worksheet = workbook.add_worksheet("Graficas")
        writer.sheets["Graficas"] = worksheet
        for i, img_path in enumerate(img_paths):
            worksheet.insert_image(i*22, 1, img_path)
    # Borrar imágenes temporales
    for img_path in img_paths:
        if os.path.exists(img_path):
            os.remove(img_path) 
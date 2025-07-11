from tkinter import Frame, Entry, messagebox, ttk, Tk, Label, StringVar, Toplevel
from crud.products_crud import create_product, read_all_products, update_product, delete_product
from crud.recipes_crud import get_recipe_cost, read_all_recipes
from interfaces.colors import NEGRO, AZUL_MARINO, AZUL_PETROLEO, PURPURA_NOCHE, AZUL_CIELO, AZUL_HIELO, TABLA_HEADER, TABLA_FILA, TABLA_FILA_ALTERNA, TEXTO, FONDO_CLARO, BORDER, BOTON_PRINCIPAL, BOTON_PRINCIPAL_HOVER, BOTON_PELIGRO
from PIL import Image, ImageTk
import tkinter as tk
import pandas as pd
import os
from tkinter import filedialog

def show_products_view(gui):
    gui.clear_main_frame()
    # Cargar imágenes de acción si no existen
    if not hasattr(gui, 'action_images'):
        img_files = [
            'assets/agregar.png',
            'assets/editar.png',
            'assets/eliminar.png'
        ]
        gui.action_images = []
        for path in img_files:
            try:
                img = Image.open(path)
                img = img.resize((22, 22), Image.Resampling.LANCZOS)
                gui.action_images.append(ImageTk.PhotoImage(img))
            except Exception:
                gui.action_images.append(None)
    # Cargar ícono de Excel si no existe
    if not hasattr(gui, 'excel_icon'):
        try:
            img = Image.open('assets/excel.png')
            img = img.resize((22, 22), Image.Resampling.LANCZOS)
            gui.excel_icon = ImageTk.PhotoImage(img)
        except Exception:
            gui.excel_icon = None
    # Panel principal tipo tarjeta
    card = Frame(gui.main_frame, bg=TABLA_FILA, bd=0, highlightbackground=BORDER, highlightthickness=1)
    card.pack(fill="both", expand=True, padx=32, pady=32)
    gui.styled_label(card, "Gestión de Productos", size=20, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=8).pack(anchor="w", padx=24, pady=(18, 0))
    Label(card, text="Visualiza, crea, edita y elimina productos del sistema", font=("Segoe UI", 12), fg=TEXTO, bg=TABLA_FILA).pack(anchor="w", padx=24, pady=(0, 18))
    # Botones alineados
    frame_botones = Frame(card, bg=TABLA_FILA)
    frame_botones.pack(pady=10, padx=24, anchor="w")
    Button = gui.styled_button
    Button(frame_botones, "Agregar Producto", lambda: add_product_form(gui), bg=BOTON_PRINCIPAL, fg="white", image=gui.action_images[0], compound="left").pack(side="left", padx=5)
    Button(frame_botones, "Editar Producto", lambda: edit_product_form(gui), bg=BOTON_PRINCIPAL, fg="white", image=gui.action_images[1], compound="left").pack(side="left", padx=5)
    Button(frame_botones, "Eliminar Producto", lambda: delete_product_form(gui), bg=BOTON_PRINCIPAL, fg="white", image=gui.action_images[2], compound="left").pack(side="left", padx=5)
    Button(frame_botones, "Exportar a Excel", lambda: exportar_excel(), bg=BOTON_PRINCIPAL, fg="white", image=gui.excel_icon, compound="left").pack(anchor="e", padx=24, pady=8)
    # Tabla de productos
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background=TABLA_FILA, fieldbackground=TABLA_FILA, foreground=TEXTO, rowheight=28, font=("Segoe UI", 11), borderwidth=0)
    style.configure("Treeview.Heading", background=TABLA_HEADER, foreground=TEXTO, font=("Segoe UI", 12, "bold"), borderwidth=0)
    style.map("Treeview", background=[("selected", TABLA_FILA_ALTERNA)], foreground=[("selected", BOTON_PRINCIPAL)])
    columns = ("ID", "Nombre", "Descripción", "Cantidad", "Unidad", "Costo Producción", "Precio Venta", "Alerta")
    gui.products_table = ttk.Treeview(card, columns=columns, show="headings")
    gui._products_sort_state = {col: False for col in columns}  # False: asc, True: desc
    def sort_products_table(col):
        data = [(gui.products_table.set(k, col), k) for k in gui.products_table.get_children("")]
        try:
            data = [(float(v.replace('$','').replace(',','')) if v.replace('$','').replace(',','').replace('.','',1).isdigit() else v, k) for v, k in data]
            data.sort(reverse=gui._products_sort_state[col])
        except Exception:
            # Si hay mezcla de tipos, ordenar como string
            data = [(str(v), k) for v, k in data]
            data.sort(reverse=gui._products_sort_state[col])
        for index, (val, k) in enumerate(data):
            gui.products_table.move(k, '', index)
        gui._products_sort_state[col] = not gui._products_sort_state[col]
    for col in columns:
        gui.products_table.heading(col, text=col, command=lambda c=col: sort_products_table(c))
        gui.products_table.column(col, anchor="center")
    gui.products_table.pack(fill="both", expand=True, padx=24, pady=10)
    view_products(gui)

def view_products(gui):
    for row in gui.products_table.get_children():
        gui.products_table.delete(row)
    products = read_all_products()
    recipes = read_all_recipes()
    for p in products:
        # Costo de producción calculado por receta
        recetas_producto = [r for r in recipes if str(r[1]) == str(p[0])]
        if recetas_producto:
            receta = max(recetas_producto, key=lambda r: int(r[2]) if str(r[2]).isdigit() else 0)
            costo_produccion = get_recipe_cost(receta[0])
            costo_produccion_str = f"${costo_produccion:,.2f}"
        else:
            costo_produccion_str = ''
        # Precio de venta directo de la base de datos (columna 7, índice 6)
        precio_venta = p[6] if len(p) > 6 else ''
        if precio_venta is None or precio_venta == '' or str(precio_venta).lower() == 'none':
            precio_venta_str = ''
        else:
            try:
                precio_venta_float = float(precio_venta)
                precio_venta_str = f"${precio_venta_float:,.2f}"
            except Exception:
                precio_venta_str = ''
        alerta = "Stock bajo" if p[3] is not None and p[3] < 5 else ""
        gui.products_table.insert("", "end", values=(
            p[0], p[1], p[2], p[3], p[4], costo_produccion_str, precio_venta_str, alerta
        ))

def get_recipe_id_by_product(product_id):
    recipes = read_all_recipes()
    recetas_producto = [r for r in recipes if str(r[1]) == str(product_id)]
    if not recetas_producto:
        return None
    receta = max(recetas_producto, key=lambda r: int(r[2]) if str(r[2]).isdigit() else 0)
    return receta[0]

def add_product_form(gui):
    form = Toplevel(gui.master)
    form.title("Agregar Producto")
    form.configure(bg=TABLA_FILA)
    form.geometry("420x420")
    form.resizable(True, True)
    # Scrollbars
    canvas = tk.Canvas(form, bg=TABLA_FILA, highlightthickness=0)
    vscrollbar = tk.Scrollbar(form, orient="vertical", command=canvas.yview)
    hscrollbar = tk.Scrollbar(form, orient="horizontal", command=canvas.xview)
    scroll_frame = Frame(canvas, bg=TABLA_FILA)
    scroll_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    vscrollbar.pack(side="right", fill="y")
    hscrollbar.pack(side="bottom", fill="x")
    gui.styled_label(scroll_frame, "Nombre", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=0, column=0, sticky="w", padx=18, pady=8)
    nombre_entry = Entry(scroll_frame, font=gui.font, bg=FONDO_CLARO, fg=TEXTO, relief="flat", bd=2, highlightbackground=BORDER, highlightthickness=1)
    nombre_entry.grid(row=0, column=1, padx=10, pady=8)
    gui.styled_label(scroll_frame, "Descripción", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=1, column=0, sticky="w", padx=18, pady=8)
    descripcion_entry = Entry(scroll_frame, font=gui.font, bg=FONDO_CLARO, fg=TEXTO, relief="flat", bd=2, highlightbackground=BORDER, highlightthickness=1)
    descripcion_entry.grid(row=1, column=1, padx=10, pady=8)
    gui.styled_label(scroll_frame, "Cantidad", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=2, column=0, sticky="w", padx=18, pady=8)
    cantidad_entry = Entry(scroll_frame, font=gui.font, bg=FONDO_CLARO, fg=TEXTO, relief="flat", bd=2, highlightbackground=BORDER, highlightthickness=1)
    cantidad_entry.grid(row=2, column=1, padx=10, pady=8)
    gui.styled_label(scroll_frame, "Unidad", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=3, column=0, sticky="w", padx=18, pady=8)
    unidad_entry = Entry(scroll_frame, font=gui.font, bg=FONDO_CLARO, fg=TEXTO, relief="flat", bd=2, highlightbackground=BORDER, highlightthickness=1)
    unidad_entry.grid(row=3, column=1, padx=10, pady=8)
    gui.styled_label(scroll_frame, "Precio Venta", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=4, column=0, sticky="w", padx=18, pady=8)
    precio_entry = Entry(scroll_frame, font=gui.font, bg=FONDO_CLARO, fg=TEXTO, relief="flat", bd=2, highlightbackground=BORDER, highlightthickness=1)
    precio_entry.grid(row=4, column=1, padx=10, pady=8)
    def guardar_producto():
        nombre = nombre_entry.get()
        descripcion = descripcion_entry.get()
        cantidad = cantidad_entry.get()
        unidad = unidad_entry.get()
        precio = precio_entry.get().replace('$','').replace(',','').strip()
        print(f"[DEBUG] Guardar producto: nombre={nombre}, descripcion={descripcion}, cantidad={cantidad}, unidad={unidad}, precio={precio}")
        if not (nombre and cantidad and unidad and precio):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        if precio.lower() == 'none' or precio == '':
            messagebox.showerror("Error", "El precio de venta no puede estar vacío.")
            return
        try:
            cantidad = float(cantidad)
            precio = float(precio)
        except ValueError:
            messagebox.showerror("Error", "Cantidad y precio deben ser numéricos.")
            return
        print(f"[DEBUG] Llamando a create_product con: ({nombre}, {descripcion}, {cantidad}, {unidad}, {precio})")
        res = create_product((nombre, descripcion, cantidad, unidad, precio))
        print(f"[DEBUG] Resultado create_product: {res}")
        messagebox.showinfo("Éxito", "Producto agregado correctamente.")
        form.destroy()
        view_products(gui)
    gui.styled_button(scroll_frame, "Guardar Producto", guardar_producto, bg=BOTON_PRINCIPAL, fg="white").grid(row=5, column=0, columnspan=2, pady=12)

def edit_product_form(gui):
    selected = gui.products_table.selection()
    if not selected:
        messagebox.showwarning("Advertencia", "Seleccione un producto de la tabla para editar")
        return
    product_values = gui.products_table.item(selected[0])["values"]
    product_id = product_values[0]
    form = Toplevel(gui.master)
    form.title("Editar Producto")
    form.configure(bg=TABLA_FILA)
    form.geometry("420x420")
    form.resizable(True, True)
    # Scrollbars
    canvas = tk.Canvas(form, bg=TABLA_FILA, highlightthickness=0)
    vscrollbar = tk.Scrollbar(form, orient="vertical", command=canvas.yview)
    hscrollbar = tk.Scrollbar(form, orient="horizontal", command=canvas.xview)
    scroll_frame = Frame(canvas, bg=TABLA_FILA)
    scroll_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    vscrollbar.pack(side="right", fill="y")
    hscrollbar.pack(side="bottom", fill="x")
    gui.styled_label(scroll_frame, "Nombre", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=0, column=0, sticky="w", padx=18, pady=8)
    nombre_entry = Entry(scroll_frame, font=gui.font, bg=FONDO_CLARO, fg=TEXTO, relief="flat", bd=2, highlightbackground=BORDER, highlightthickness=1)
    nombre_entry.insert(0, product_values[1])
    nombre_entry.grid(row=0, column=1, padx=10, pady=8)
    gui.styled_label(scroll_frame, "Descripción", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=1, column=0, sticky="w", padx=18, pady=8)
    descripcion_entry = Entry(scroll_frame, font=gui.font, bg=FONDO_CLARO, fg=TEXTO, relief="flat", bd=2, highlightbackground=BORDER, highlightthickness=1)
    descripcion_entry.insert(0, product_values[2])
    descripcion_entry.grid(row=1, column=1, padx=10, pady=8)
    gui.styled_label(scroll_frame, "Cantidad", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=2, column=0, sticky="w", padx=18, pady=8)
    cantidad_entry = Entry(scroll_frame, font=gui.font, bg=FONDO_CLARO, fg=TEXTO, relief="flat", bd=2, highlightbackground=BORDER, highlightthickness=1)
    cantidad_entry.insert(0, product_values[3])
    cantidad_entry.grid(row=2, column=1, padx=10, pady=8)
    gui.styled_label(scroll_frame, "Unidad", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=3, column=0, sticky="w", padx=18, pady=8)
    unidad_entry = Entry(scroll_frame, font=gui.font, bg=FONDO_CLARO, fg=TEXTO, relief="flat", bd=2, highlightbackground=BORDER, highlightthickness=1)
    unidad_entry.insert(0, product_values[4])
    unidad_entry.grid(row=3, column=1, padx=10, pady=8)
    gui.styled_label(scroll_frame, "Precio Venta", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=4, column=0, sticky="w", padx=18, pady=8)
    precio_entry = Entry(scroll_frame, font=gui.font, bg=FONDO_CLARO, fg=TEXTO, relief="flat", bd=2, highlightbackground=BORDER, highlightthickness=1)
    precio_valor = product_values[6] if len(product_values) > 6 else product_values[5]
    if isinstance(precio_valor, str) and precio_valor.startswith('$'):
        precio_entry.insert(0, precio_valor)
    elif isinstance(precio_valor, (int, float)):
        precio_entry.insert(0, f"${precio_valor:,.2f}")
    else:
        precio_entry.insert(0, precio_valor)
    precio_entry.grid(row=4, column=1, padx=10, pady=8)
    def guardar_edicion():
        nombre = nombre_entry.get()
        descripcion = descripcion_entry.get()
        cantidad = cantidad_entry.get()
        unidad = unidad_entry.get()
        precio = precio_entry.get().replace('$','').replace(',','').strip()
        print(f"[DEBUG] Editar producto: id={product_id}, nombre={nombre}, descripcion={descripcion}, cantidad={cantidad}, unidad={unidad}, precio={precio}")
        if not (nombre and cantidad and unidad and precio):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        if precio.lower() == 'none' or precio == '':
            messagebox.showerror("Error", "El precio de venta no puede estar vacío.")
            return
        try:
            cantidad = float(cantidad)
            precio = float(precio)
        except ValueError:
            messagebox.showerror("Error", "Cantidad y precio deben ser numéricos.")
            return
        print(f"[DEBUG] Llamando a update_product con: id={product_id}, ({nombre}, {descripcion}, {cantidad}, {unidad}, {precio})")
        update_product(product_id, (nombre, descripcion, cantidad, unidad, precio))
        print(f"[DEBUG] Producto actualizado correctamente.")
        messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
        form.destroy()
        view_products(gui)
    gui.styled_button(scroll_frame, "Guardar Cambios", guardar_edicion, bg=BOTON_PRINCIPAL, fg="white").grid(row=5, column=0, columnspan=2, pady=12)

def delete_product_form(gui):
    selected = gui.products_table.selection()
    if not selected:
        messagebox.showwarning("Advertencia", "Seleccione un producto de la tabla para eliminar")
        return
    product_values = gui.products_table.item(selected[0])["values"]
    product_id = product_values[0]
    confirm = messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el producto ID {product_id}?")
    if confirm:
        delete_product(product_id)
        messagebox.showinfo("Éxito", "Producto eliminado correctamente")
        view_products(gui)

def exportar_excel():
    ruta = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], title="Guardar productos")
    if not ruta:
        return
    products = read_all_products()
    recipes = read_all_recipes()
    data = []
    for p in products:
        recetas_producto = [r for r in recipes if str(r[1]) == str(p[0])]
        if recetas_producto:
            receta = max(recetas_producto, key=lambda r: int(r[2]) if str(r[2]).isdigit() else 0)
            costo_produccion = get_recipe_cost(receta[0])
        else:
            costo_produccion = ''
        precio_venta = p[6] if len(p) > 6 else ''
        data.append([
            p[0], p[1], p[2], p[3], p[4],
            f"${costo_produccion:,.2f}" if costo_produccion != '' else '',
            f"${precio_venta:,.2f}" if precio_venta != '' else ''
        ])
    df = pd.DataFrame(data, columns=pd.Index(["ID", "Nombre", "Descripción", "Cantidad", "Unidad", "Costo Producción", "Precio Venta"]))
    df.to_excel(ruta, index=False)
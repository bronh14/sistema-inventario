from tkinter import Frame, Entry, messagebox, ttk, Tk, Label, StringVar, Toplevel
import datetime
from crud.recipes_crud import (
    get_recipe_details, create_recipe, read_all_recipes, update_recipe, delete_recipe,
    add_materials_to_recipe, get_connection
)
from crud.materials_crud import read_all_materials
from crud.products_crud import  read_all_products
from interfaces.colors import NEGRO, AZUL_MARINO, AZUL_PETROLEO, PURPURA_NOCHE, AZUL_CIELO, AZUL_HIELO, TABLA_HEADER, TABLA_FILA, TABLA_FILA_ALTERNA, TEXTO, FONDO_CLARO, BORDER, BOTON_PRINCIPAL, BOTON_PRINCIPAL_HOVER
from services.inventory_service import produce_product_from_recipe
from tkinter.simpledialog import askinteger
from PIL import Image, ImageTk
import tkinter as tk
import pandas as pd
import os
from tkinter import filedialog

def get_products_list():
    products = read_all_products()
    return [(str(p[0]), p[1]) for p in products]

def get_materials_list():
    materials = read_all_materials()
    return [(str(m[0]), m[1], float(m[5])) for m in materials]

def show_recipes_view(gui):
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
    gui.styled_label(card, "Gestión de Recetas", size=20, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=8).pack(anchor="w", padx=24, pady=(18, 0))
    Label(card, text="Visualiza, crea, edita y elimina recetas del sistema", font=("Segoe UI", 12), fg=TEXTO, bg=TABLA_FILA).pack(anchor="w", padx=24, pady=(0, 18))
    # Botones alineados
    frame_botones = Frame(card, bg=TABLA_FILA)
    frame_botones.pack(pady=10, padx=24, anchor="w", fill="x")
    Button = gui.styled_button
    Button(frame_botones, "Agregar Receta", lambda: add_recipe_form(gui), bg=BOTON_PRINCIPAL, fg="white", image=gui.action_images[0], compound="left").pack(side="left", padx=5)
    Button(frame_botones, "Editar Receta", lambda: edit_recipe_form(gui), bg=BOTON_PRINCIPAL, fg="white", image=gui.action_images[1], compound="left").pack(side="left", padx=5)
    Button(frame_botones, "Eliminar Receta", lambda: delete_recipe_form(gui), bg=BOTON_PRINCIPAL, fg="white", image=gui.action_images[2], compound="left").pack(side="left", padx=5)
    Button(frame_botones, "Exportar a Excel", lambda: exportar_excel(gui), bg=BOTON_PRINCIPAL, fg="white", image=gui.excel_icon, compound="left").pack(side="left", padx=5)
    def crear_producto_desde_receta():
        selected = gui.recipes_table.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una receta para producir el producto.")
            return
        recipe_id = gui.recipes_table.item(selected[0])["values"][0]
        cantidad = askinteger("Cantidad a producir", "¿Cuántas unidades desea producir?", minvalue=1)
        if cantidad is None:
            return
        ok, msg = produce_product_from_recipe(recipe_id, cantidad)
        if ok:
            messagebox.showinfo("Éxito", msg)
        else:
            messagebox.showerror("Error", msg)
    Button(frame_botones, "Crear Producto", crear_producto_desde_receta, bg=BOTON_PRINCIPAL, fg="white").pack(side="right", padx=5)
    # Tabla de recetas
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background=TABLA_FILA, fieldbackground=TABLA_FILA, foreground=TEXTO, rowheight=28, font=("Segoe UI", 11), borderwidth=0)
    style.configure("Treeview.Heading", background=TABLA_HEADER, foreground=TEXTO, font=("Segoe UI", 12, "bold"), borderwidth=0)
    style.map("Treeview", background=[("selected", TABLA_FILA_ALTERNA)], foreground=[("selected", BOTON_PRINCIPAL)])
    columns = ("ID", "Producto ID", "Versión", "Fecha", "Costo Total")
    frame_tabla = Frame(card, bg=TABLA_FILA)
    frame_tabla.pack(fill="both", expand=True, padx=24, pady=10)
    gui.recipes_table = ttk.Treeview(frame_tabla, columns=columns, show="headings")
    vsb = tk.Scrollbar(frame_tabla, orient="vertical", command=gui.recipes_table.yview)
    hsb = tk.Scrollbar(frame_tabla, orient="horizontal", command=gui.recipes_table.xview)
    gui.recipes_table.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    gui.recipes_table.pack(side="left", fill="both", expand=True, anchor="n")
    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")
    for col in columns:
        gui.recipes_table.heading(col, text=col)
        gui.recipes_table.column(col, anchor="center", stretch=True, width=150)
    # Tabla de materiales de la receta
    frame_tabla2 = Frame(card, bg=TABLA_FILA)
    frame_tabla2.pack(fill="both", expand=True, padx=24, pady=10)
    gui.recipe_materials_table = ttk.Treeview(frame_tabla2, columns=("ID Material", "Nombre", "Cantidad", "Costo Parcial"), show="headings")
    vsb2 = tk.Scrollbar(frame_tabla2, orient="vertical", command=gui.recipe_materials_table.yview)
    hsb2 = tk.Scrollbar(frame_tabla2, orient="horizontal", command=gui.recipe_materials_table.xview)
    gui.recipe_materials_table.configure(yscrollcommand=vsb2.set, xscrollcommand=hsb2.set)
    gui.recipe_materials_table.pack(side="left", fill="both", expand=True, anchor="n")
    vsb2.pack(side="right", fill="y")
    hsb2.pack(side="bottom", fill="x")
    for col in ("ID Material", "Nombre", "Cantidad", "Costo Parcial"):
        gui.recipe_materials_table.heading(col, text=col)
        gui.recipe_materials_table.column(col, anchor="center", stretch=True, width=150)
    gui.recipes_table.bind("<<TreeviewSelect>>", lambda event: on_recipe_select(gui, event))
    view_recipes(gui)

def on_recipe_select(gui, event):
    selected = gui.recipes_table.selection()
    if not selected:
        return
    recipe_id = gui.recipes_table.item(selected[0])["values"][0]
    materials = get_recipe_details(recipe_id)
    for row in gui.recipe_materials_table.get_children():
        gui.recipe_materials_table.delete(row)
    for mat in materials:
        costo_parcial_str = f"${mat[3]:,.2f}" if mat[3] is not None else ''
        gui.recipe_materials_table.insert("", "end", values=(mat[0], mat[1], mat[2], costo_parcial_str))

def view_recipes(gui):
    for row in gui.recipes_table.get_children():
        gui.recipes_table.delete(row)
    recipes = read_all_recipes()
    for recipe in recipes:
        # Formatear costo total
        costo_total = recipe[4]
        costo_total_str = f"${costo_total:,.2f}" if costo_total is not None else ''
        gui.recipes_table.insert("", "end", values=(recipe[0], recipe[1], recipe[2], recipe[3], costo_total_str))

def add_recipe_form(gui):
    form = Toplevel(gui.master)
    form.title("Agregar Receta")
    form.configure(bg=TABLA_FILA)
    form.geometry("650x750")
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
    for i in range(2):
        scroll_frame.columnconfigure(i, weight=1)
    products = get_products_list()
    materials = get_materials_list()
    selected_product = StringVar()
    selected_material = StringVar()
    gui.styled_label(scroll_frame, "Producto", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=0, column=0, sticky="w", padx=18, pady=8)
    product_combo = ttk.Combobox(scroll_frame, textvariable=selected_product, state="readonly", values=[f"{pid} - {name}" for pid, name in products], font=gui.font)
    product_combo.grid(row=0, column=1, padx=10, pady=8, sticky="ew")
    if products:
        product_combo.current(0)
    version = 1
    gui.styled_label(scroll_frame, "Versión", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=1, column=0, sticky="w", padx=18, pady=8)
    version_label = Label(scroll_frame, text=str(version), bg=TABLA_FILA, fg=BOTON_PRINCIPAL, font=gui.font)
    version_label.grid(row=1, column=1, padx=10, pady=8, sticky="ew")
    fecha_actual = datetime.datetime.now().strftime("%y-%m-%d")
    gui.styled_label(scroll_frame, "Fecha de Creación", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=2, column=0, sticky="w", padx=18, pady=8)
    date_label = Label(scroll_frame, text=fecha_actual, bg=TABLA_FILA, fg=BOTON_PRINCIPAL, font=gui.font)
    date_label.grid(row=2, column=1, padx=10, pady=8, sticky="ew")
    gui.styled_label(scroll_frame, "Costo Total", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=3, column=0, sticky="w", padx=18, pady=8)
    cost_var = StringVar(value="0.0")
    cost_label = Label(scroll_frame, textvariable=cost_var, bg=TABLA_FILA, fg=BOTON_PRINCIPAL, font=gui.font)
    cost_label.grid(row=3, column=1, padx=10, pady=8, sticky="ew")
    gui.styled_label(scroll_frame, "Materiales", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=4, column=0, columnspan=2, padx=18, pady=8, sticky="w")
    materials_table = ttk.Treeview(scroll_frame, columns=("ID", "Nombre", "Cantidad", "Costo Unitario", "Costo Parcial"), show="headings", height=5)
    for col in ("ID", "Nombre", "Cantidad", "Costo Unitario", "Costo Parcial"):
        materials_table.heading(col, text=col)
        materials_table.column(col, anchor="center")
    materials_table.grid(row=5, column=0, columnspan=2, pady=8, padx=18, sticky="ew")
    gui.styled_label(scroll_frame, "Material", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=6, column=0, sticky="w", padx=18, pady=8)
    material_combo = ttk.Combobox(scroll_frame, textvariable=selected_material, state="readonly", values=[f"{mid} - {name}" for mid, name, _ in materials], font=gui.font)
    material_combo.grid(row=6, column=1, padx=10, pady=8, sticky="ew")
    if materials:
        material_combo.current(0)
    gui.styled_label(scroll_frame, "Cantidad", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=7, column=0, sticky="w", padx=18, pady=8)
    quantity_entry = Entry(scroll_frame, font=gui.font, bg=FONDO_CLARO, fg=TEXTO, relief="flat", bd=2, highlightbackground=BORDER, highlightthickness=1)
    quantity_entry.grid(row=7, column=1, padx=10, pady=8, sticky="ew")
    def add_material_to_table():
        mat_index = material_combo.current()
        if mat_index == -1:
            messagebox.showwarning("Advertencia", "Seleccione un material")
            return
        mat_id, mat_name, mat_cost = materials[mat_index]
        cantidad = quantity_entry.get()
        try:
            cantidad = float(cantidad)
        except ValueError:
            messagebox.showwarning("Advertencia", "Cantidad inválida")
            return
        costo_parcial = cantidad * mat_cost
        mat_cost_str = f"${mat_cost:,.2f}"
        costo_parcial_str = f"${costo_parcial:,.2f}"
        materials_table.insert("", "end", values=(mat_id, mat_name, cantidad, mat_cost_str, costo_parcial_str))
        quantity_entry.delete(0, "end")
        update_total_cost()
    def update_total_cost():
        total = 0.0
        for row in materials_table.get_children():
            costo_parcial = float(materials_table.item(row)["values"][4])
            total += costo_parcial
        cost_var.set(str(round(total, 2)))
    gui.styled_button(scroll_frame, "Agregar Material", add_material_to_table, bg=BOTON_PRINCIPAL, fg="white").grid(row=8, column=0, columnspan=2, pady=4, sticky="ew")
    def save_recipe():
        prod_index = product_combo.current()
        if prod_index == -1:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return
        product_id = products[prod_index][0]
        costo_total = cost_var.get().replace('$','').replace(',','').strip()
        materials_data = []
        for row in materials_table.get_children():
            mat_id = materials_table.item(row)["values"][0]
            cantidad = materials_table.item(row)["values"][2]
            costo_parcial = materials_table.item(row)["values"][4]
            costo_parcial = str(costo_parcial).replace('$','').replace(',','').strip()
            materials_data.append((mat_id, cantidad, costo_parcial))
        if not (product_id and materials_data):
            messagebox.showwarning("Advertencia", "Todos los campos y al menos un material son obligatorios")
            return
        recipe_id = create_recipe((product_id, version, fecha_actual, costo_total))
        add_materials_to_recipe(recipe_id, materials_data)
        messagebox.showinfo("Éxito", "Receta y materiales agregados correctamente")
        form.destroy()
        view_recipes(gui)
    gui.styled_button(scroll_frame, "Guardar Receta", save_recipe, bg=BOTON_PRINCIPAL, fg="white").grid(row=9, column=0, columnspan=2, pady=12, sticky="ew")

def edit_recipe_form(gui):
    selected = gui.recipes_table.selection()
    if not selected:
        messagebox.showwarning("Advertencia", "Seleccione una receta de la tabla para editar")
        return
    recipe_values = gui.recipes_table.item(selected[0])["values"]
    recipe_id = recipe_values[0]
    old_version = int(recipe_values[2]) if str(recipe_values[2]).isdigit() else 1
    new_version = old_version + 1
    fecha_actual = datetime.datetime.now().strftime("%y-%m-%d")
    form = Toplevel(gui.master)
    form.title("Editar Receta")
    form.configure(bg=TABLA_FILA)
    form.geometry("650x750")
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
    for i in range(2):
        scroll_frame.columnconfigure(i, weight=1)
    gui.styled_label(scroll_frame, "Nuevo ID del Producto", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=0, column=0, sticky="w", padx=18, pady=8)
    product_id_entry = Entry(scroll_frame, font=gui.font, bg=FONDO_CLARO, fg=TEXTO, relief="flat", bd=2, highlightbackground=BORDER, highlightthickness=1)
    product_id_entry.insert(0, recipe_values[1])
    product_id_entry.grid(row=0, column=1, padx=10, pady=8, sticky="ew")
    gui.styled_label(scroll_frame, "Nueva Versión", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=1, column=0, sticky="w", padx=18, pady=8)
    version_label = Label(scroll_frame, text=str(new_version), bg=TABLA_FILA, fg=BOTON_PRINCIPAL, font=gui.font)
    version_label.grid(row=1, column=1, padx=10, pady=8, sticky="ew")
    gui.styled_label(scroll_frame, "Nueva Fecha de Creación", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=2, column=0, sticky="w", padx=18, pady=8)
    date_label = Label(scroll_frame, text=fecha_actual, bg=TABLA_FILA, fg=BOTON_PRINCIPAL, font=gui.font)
    date_label.grid(row=2, column=1, padx=10, pady=8, sticky="ew")
    gui.styled_label(scroll_frame, "Nuevo Costo Total", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=3, column=0, sticky="w", padx=18, pady=8)
    cost_var = StringVar(value=str(recipe_values[4]))
    cost_label = Label(scroll_frame, textvariable=cost_var, bg=TABLA_FILA, fg=BOTON_PRINCIPAL, font=gui.font)
    cost_label.grid(row=3, column=1, padx=10, pady=8, sticky="ew")
    gui.styled_label(scroll_frame, "Materiales", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=4, column=0, columnspan=2, padx=18, pady=8, sticky="w")
    materials_table = ttk.Treeview(scroll_frame, columns=("ID", "Nombre", "Cantidad", "Costo Unitario", "Costo Parcial"), show="headings", height=5)
    for col in ("ID", "Nombre", "Cantidad", "Costo Unitario", "Costo Parcial"):
        materials_table.heading(col, text=col)
        materials_table.column(col, anchor="center")
    materials_table.grid(row=5, column=0, columnspan=2, pady=8, padx=18, sticky="ew")
    materials_actuales = get_recipe_details(recipe_id)
    for mat in materials_actuales:
        mat_cost_str = f"${mat[3]:,.2f}" if mat[3] is not None else ''
        costo_parcial_str = f"${float(mat[2])*float(mat[3]):,.2f}" if mat[3] is not None and mat[2] is not None else ''
        materials_table.insert("", "end", values=(mat[0], mat[1], mat[2], mat_cost_str, costo_parcial_str))
    materials = get_materials_list()
    selected_material = StringVar()
    gui.styled_label(scroll_frame, "Material", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=6, column=0, sticky="w", padx=18, pady=8)
    material_combo = ttk.Combobox(scroll_frame, textvariable=selected_material, state="readonly", values=[f"{mid} - {name}" for mid, name, _ in materials], font=gui.font)
    material_combo.grid(row=6, column=1, padx=10, pady=8, sticky="ew")
    if materials:
        material_combo.current(0)
    gui.styled_label(scroll_frame, "Cantidad", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=7, column=0, sticky="w", padx=18, pady=8)
    quantity_entry = Entry(scroll_frame, font=gui.font, bg=FONDO_CLARO, fg=TEXTO, relief="flat", bd=2, highlightbackground=BORDER, highlightthickness=1)
    quantity_entry.grid(row=7, column=1, padx=10, pady=8, sticky="ew")
    def add_material_to_table():
        mat_index = material_combo.current()
        if mat_index == -1:
            messagebox.showwarning("Advertencia", "Seleccione un material")
            return
        mat_id, mat_name, mat_cost = materials[mat_index]
        cantidad = quantity_entry.get()
        try:
            cantidad = float(cantidad)
        except ValueError:
            messagebox.showwarning("Advertencia", "Cantidad inválida")
            return
        costo_parcial = cantidad * mat_cost
        mat_cost_str = f"${mat_cost:,.2f}"
        costo_parcial_str = f"${costo_parcial:,.2f}"
        materials_table.insert("", "end", values=(mat_id, mat_name, cantidad, mat_cost_str, costo_parcial_str))
        quantity_entry.delete(0, "end")
        update_total_cost()
    def update_total_cost():
        total = 0.0
        for row in materials_table.get_children():
            costo_parcial = float(materials_table.item(row)["values"][4])
            try:
                total += float(costo_parcial)
            except Exception:
                pass
        cost_var.set(str(round(total, 2)))
    gui.styled_button(scroll_frame, "Agregar Material", add_material_to_table, bg=BOTON_PRINCIPAL, fg="white").grid(row=8, column=0, columnspan=2, pady=4, sticky="ew")
    def save_edit_recipe():
        product_id = product_id_entry.get()
        costo_total = cost_var.get().replace('$','').replace(',','').strip()
        materials_data = []
        for row in materials_table.get_children():
            mat_id = materials_table.item(row)["values"][0]
            cantidad = materials_table.item(row)["values"][2]
            costo_parcial = materials_table.item(row)["values"][4]
            costo_parcial = str(costo_parcial).replace('$','').replace(',','').strip()
            materials_data.append((mat_id, cantidad, costo_parcial))
        if not (product_id and materials_data):
            messagebox.showwarning("Advertencia", "Todos los campos y al menos un material son obligatorios")
            return
        update_recipe(recipe_id, (product_id, new_version, fecha_actual, costo_total))
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM detalle_receta WHERE id_receta = ?", (recipe_id,))
        conn.commit()
        conn.close()
        add_materials_to_recipe(recipe_id, materials_data)
        messagebox.showinfo("Éxito", "Receta actualizada correctamente")
        form.destroy()
        view_recipes(gui)
    gui.styled_button(scroll_frame, "Guardar Cambios", save_edit_recipe, bg=BOTON_PRINCIPAL, fg="white").grid(row=9, column=0, columnspan=2, pady=12, sticky="ew")

def delete_recipe_form(gui):
    selected = gui.recipes_table.selection()
    if not selected:
        messagebox.showwarning("Advertencia", "Seleccione una receta de la tabla para eliminar")
        return
    recipe_values = gui.recipes_table.item(selected[0])["values"]
    recipe_id = recipe_values[0]
    confirm = messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar la receta ID {recipe_id}?")
    if confirm:
        delete_recipe(recipe_id)
        messagebox.showinfo("Éxito", "Receta eliminada correctamente")
        view_recipes(gui)

def exportar_excel(gui):
    ruta = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], title="Guardar recetas")
    if not ruta:
        return
    recipes = read_all_recipes()
    df_recetas = pd.DataFrame(recipes, columns=pd.Index(["ID", "Producto ID", "Versión", "Fecha", "Costo Total"]))
    # Detalle de materiales por receta
    detalles = []
    for r in recipes:
        mats = get_recipe_details(r[0])
        for mat in mats:
            detalles.append([r[0], mat[0], mat[1], mat[2], mat[3]])
        df_detalle = pd.DataFrame(detalles, columns=pd.Index(["ID Receta", "ID Material", "Nombre Material", "Cantidad", "Costo Parcial"]))
        with pd.ExcelWriter(ruta) as writer:
            df_recetas.to_excel(writer, sheet_name="Recetas", index=False)
            df_detalle.to_excel(writer, sheet_name="Detalle Materiales", index=False)
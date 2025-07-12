from tkinter import Frame, Entry, messagebox, ttk, Tk, Label, StringVar, Toplevel
from crud.materials_crud import create_material, read_all_materials, update_material, delete_material
from interfaces.colors import NEGRO, AZUL_MARINO, AZUL_PETROLEO, PURPURA_NOCHE, AZUL_CIELO, AZUL_HIELO, TABLA_HEADER, TABLA_FILA, TABLA_FILA_ALTERNA, TEXTO, FONDO_CLARO, BORDER, BOTON_PRINCIPAL, BOTON_PRINCIPAL_HOVER, BOTON_PELIGRO
from PIL import Image, ImageTk
import tkinter as tk
import pandas as pd
import os
from tkinter import filedialog

def show_materials_view(gui):
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
    gui.styled_label(card, "Gestión de Materiales", size=20, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=8).pack(anchor="w", padx=24, pady=(18, 0))
    Label(card, text="Visualiza, crea, edita y elimina materiales del sistema", font=("Segoe UI", 12), fg=TEXTO, bg=TABLA_FILA).pack(anchor="w", padx=24, pady=(0, 18))
    # Botones alineados
    frame_botones = Frame(card, bg=TABLA_FILA)
    frame_botones.pack(pady=10, padx=24, anchor="w")
    Button = gui.styled_button
    Button(frame_botones, "Agregar Material", lambda: add_material_form(gui), bg=BOTON_PRINCIPAL, fg="white", image=gui.action_images[0], compound="left").pack(side="left", padx=5)
    Button(frame_botones, "Editar Material", lambda: edit_material_form(gui), bg=BOTON_PRINCIPAL, fg="white", image=gui.action_images[1], compound="left").pack(side="left", padx=5)
    Button(frame_botones, "Eliminar Material", lambda: delete_material_form(gui), bg=BOTON_PRINCIPAL, fg="white", image=gui.action_images[2], compound="left").pack(side="left", padx=5)
    Button(frame_botones, "Exportar a Excel", lambda: exportar_excel(gui), bg=BOTON_PRINCIPAL, fg="white", image=gui.excel_icon, compound="left").pack(anchor="e", padx=24, pady=8)
    # Tabla de materiales
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background=TABLA_FILA, fieldbackground=TABLA_FILA, foreground=TEXTO, rowheight=28, font=("Segoe UI", 11), borderwidth=0)
    style.configure("Treeview.Heading", background=TABLA_HEADER, foreground=TEXTO, font=("Segoe UI", 12, "bold"), borderwidth=0)
    style.map("Treeview", background=[("selected", TABLA_FILA_ALTERNA)], foreground=[("selected", BOTON_PRINCIPAL)])
    columns = ("ID", "Nombre", "Descripción", "Cantidad", "Unidad", "Costo", "Proveedor", "Alerta")
    frame_tabla = Frame(card, bg=TABLA_FILA)
    frame_tabla.pack(fill="both", expand=True, padx=24, pady=10)
    gui.materials_table = ttk.Treeview(frame_tabla, columns=columns, show="headings")
    vsb = tk.Scrollbar(frame_tabla, orient="vertical", command=gui.materials_table.yview)
    hsb = tk.Scrollbar(frame_tabla, orient="horizontal", command=gui.materials_table.xview)
    gui.materials_table.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    gui.materials_table.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")
    gui._materials_sort_state = {col: False for col in columns}
    def sort_materials_table(col):
        data = [(gui.materials_table.set(k, col), k) for k in gui.materials_table.get_children("")]
        try:
            data = [(float(v.replace('$','').replace(',','')) if v.replace('$','').replace(',','').replace('.','',1).isdigit() else v, k) for v, k in data]
        except Exception:
            pass
        data.sort(reverse=gui._materials_sort_state[col])
        for index, (val, k) in enumerate(data):
            gui.materials_table.move(k, '', index)
        gui._materials_sort_state[col] = not gui._materials_sort_state[col]
    for col in columns:
        gui.materials_table.heading(col, text=col, command=lambda c=col: sort_materials_table(c))
        gui.materials_table.column(col, anchor="center")
    view_materials(gui)

def view_materials(gui):
    for row in gui.materials_table.get_children():
        gui.materials_table.delete(row)
    materials = read_all_materials()
    for m in materials:
        alerta = "Stock bajo" if m[3] is not None and m[3] < 5 else ""
        costo_str = f"${m[5]:,.2f}" if m[5] is not None else ''
        gui.materials_table.insert("", "end", values=(m[0], m[1], m[2], m[3], m[4], costo_str, m[6], alerta))

def add_material_form(gui):
    form = Toplevel(gui.master)
    form.title("Agregar Material")
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
    gui.styled_label(scroll_frame, "Costo por Unidad", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=4, column=0, sticky="w", padx=18, pady=8)
    costo_entry = Entry(scroll_frame, font=gui.font, bg=FONDO_CLARO, fg=TEXTO, relief="flat", bd=2, highlightbackground=BORDER, highlightthickness=1)
    costo_entry.grid(row=4, column=1, padx=10, pady=8)
    gui.styled_label(scroll_frame, "Proveedor", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=5, column=0, sticky="w", padx=18, pady=8)
    proveedor_entry = Entry(scroll_frame, font=gui.font, bg=FONDO_CLARO, fg=TEXTO, relief="flat", bd=2, highlightbackground=BORDER, highlightthickness=1)
    proveedor_entry.grid(row=5, column=1, padx=10, pady=8)
    def guardar_material():
        nombre = nombre_entry.get()
        descripcion = descripcion_entry.get()
        cantidad = cantidad_entry.get()
        unidad = unidad_entry.get()
        costo = costo_entry.get().replace('$','').replace(',','').strip()
        proveedor = proveedor_entry.get()
        if not (nombre and cantidad and unidad and costo and proveedor):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        if costo.lower() == 'none' or costo == '':
            messagebox.showerror("Error", "El costo por unidad no puede estar vacío.")
            return
        try:
            cantidad = float(cantidad)
            costo = float(costo)
        except ValueError:
            messagebox.showerror("Error", "Cantidad y costo deben ser numéricos.")
            return
        create_material((nombre, descripcion, cantidad, unidad, costo, proveedor))
        messagebox.showinfo("Éxito", "Material agregado correctamente.")
        form.destroy()
        view_materials(gui)
    gui.styled_button(scroll_frame, "Guardar Material", guardar_material, bg=BOTON_PRINCIPAL, fg="white").grid(row=6, column=0, columnspan=2, pady=12)

def edit_material_form(gui):
    selected = gui.materials_table.selection()
    if not selected:
        messagebox.showwarning("Advertencia", "Seleccione un material de la tabla para editar")
        return
    material_values = gui.materials_table.item(selected[0])["values"]
    material_id = material_values[0]
    form = Toplevel(gui.master)
    form.title("Editar Material")
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
    nombre_entry.insert(0, material_values[1])
    nombre_entry.grid(row=0, column=1, padx=10, pady=8)
    gui.styled_label(scroll_frame, "Descripción", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=1, column=0, sticky="w", padx=18, pady=8)
    descripcion_entry = Entry(scroll_frame, font=gui.font, bg=FONDO_CLARO, fg=TEXTO, relief="flat", bd=2, highlightbackground=BORDER, highlightthickness=1)
    descripcion_entry.insert(0, material_values[2])
    descripcion_entry.grid(row=1, column=1, padx=10, pady=8)
    gui.styled_label(scroll_frame, "Cantidad", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=2, column=0, sticky="w", padx=18, pady=8)
    cantidad_entry = Entry(scroll_frame, font=gui.font, bg=FONDO_CLARO, fg=TEXTO, relief="flat", bd=2, highlightbackground=BORDER, highlightthickness=1)
    cantidad_entry.insert(0, material_values[3])
    cantidad_entry.grid(row=2, column=1, padx=10, pady=8)
    gui.styled_label(scroll_frame, "Unidad", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=3, column=0, sticky="w", padx=18, pady=8)
    unidad_entry = Entry(scroll_frame, font=gui.font, bg=FONDO_CLARO, fg=TEXTO, relief="flat", bd=2, highlightbackground=BORDER, highlightthickness=1)
    unidad_entry.insert(0, material_values[4])
    unidad_entry.grid(row=3, column=1, padx=10, pady=8)
    gui.styled_label(scroll_frame, "Costo por Unidad", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=4, column=0, sticky="w", padx=18, pady=8)
    costo_entry = Entry(scroll_frame, font=gui.font, bg=FONDO_CLARO, fg=TEXTO, relief="flat", bd=2, highlightbackground=BORDER, highlightthickness=1)
    costo_valor = material_values[5]
    if isinstance(costo_valor, str) and costo_valor.startswith('$'):
        costo_entry.insert(0, costo_valor)
    elif isinstance(costo_valor, (int, float)):
        costo_entry.insert(0, f"${costo_valor:,.2f}")
    else:
        costo_entry.insert(0, costo_valor)
    costo_entry.grid(row=4, column=1, padx=10, pady=8)
    gui.styled_label(scroll_frame, "Proveedor", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=5, column=0, sticky="w", padx=18, pady=8)
    proveedor_entry = Entry(scroll_frame, font=gui.font, bg=FONDO_CLARO, fg=TEXTO, relief="flat", bd=2, highlightbackground=BORDER, highlightthickness=1)
    proveedor_entry.insert(0, material_values[6])
    proveedor_entry.grid(row=5, column=1, padx=10, pady=8)
    def guardar_edicion():
        nombre = nombre_entry.get()
        descripcion = descripcion_entry.get()
        cantidad = cantidad_entry.get()
        unidad = unidad_entry.get()
        costo = costo_entry.get().replace('$','').replace(',','').strip()
        proveedor = proveedor_entry.get()
        if not (nombre and cantidad and unidad and costo and proveedor):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        if costo.lower() == 'none' or costo == '':
            messagebox.showerror("Error", "El costo por unidad no puede estar vacío.")
            return
        try:
            cantidad = float(cantidad)
            costo = float(costo)
        except ValueError:
            messagebox.showerror("Error", "Cantidad y costo deben ser numéricos.")
            return
        update_material(material_id, (nombre, descripcion, cantidad, unidad, costo, proveedor))
        messagebox.showinfo("Éxito", "Material actualizado correctamente.")
        form.destroy()
        view_materials(gui)
    gui.styled_button(scroll_frame, "Guardar Cambios", guardar_edicion, bg=BOTON_PRINCIPAL, fg="white").grid(row=6, column=0, columnspan=2, pady=12)

def delete_material_form(gui):
    selected = gui.materials_table.selection()
    if not selected:
        messagebox.showwarning("Advertencia", "Seleccione un material de la tabla para eliminar")
        return
    material_values = gui.materials_table.item(selected[0])["values"]
    material_id = material_values[0]
    confirm = messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el material ID {material_id}?")
    if confirm:
        delete_material(material_id)
        messagebox.showinfo("Éxito", "Material eliminado correctamente")
        view_materials(gui)

def exportar_excel(gui):
    ruta = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], title="Guardar materiales")
    if not ruta:
        return
    materials = read_all_materials()
    df = pd.DataFrame(materials, columns=pd.Index(["ID", "Nombre", "Descripción", "Cantidad", "Unidad", "Costo", "Proveedor"]))
    df.to_excel(ruta, index=False)
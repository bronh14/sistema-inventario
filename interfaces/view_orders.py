from tkinter import Frame, Entry, messagebox, ttk, Tk, Label, StringVar, Toplevel
import datetime
from crud.orders_crud import create_order_with_products, read_orders_grouped, update_order, delete_order
from interfaces.colors import NEGRO, AZUL_MARINO, AZUL_PETROLEO, PURPURA_NOCHE, AZUL_CIELO, AZUL_HIELO, TABLA_HEADER, TABLA_FILA, TABLA_FILA_ALTERNA, TEXTO, FONDO_CLARO, BORDER, BOTON_PRINCIPAL, BOTON_PRINCIPAL_HOVER
from crud.products_crud import  read_all_products
from PIL import Image, ImageTk
import tkinter as tk
import pandas as pd
import os
from tkinter import filedialog
try:
    from tkcalendar import DateEntry
except ImportError:
    # Fallback si tkcalendar no está disponible
    DateEntry = None

def get_products_list():
    products = read_all_products()
    return [(str(p[0]), p[1]) for p in products]

def create_date_entry(parent, font, bg_color, fg_color, border_color, default_date=None):
    """
    Crea un campo de fecha con calendario desplegable.
    Si tkcalendar no está disponible, crea un Entry normal.
    """
    if DateEntry is not None:
        # Usar DateEntry con calendario
        date_entry = DateEntry(
            parent,
            width=20,
            background=bg_color,
            foreground=fg_color,
            borderwidth=1,
            highlightbackground=border_color,
            highlightthickness=1,
            font=font,
            date_pattern='yyyy-mm-dd',
            locale='es_ES' if hasattr(DateEntry, 'locale') else None
        )
        if default_date:
            try:
                # Convertir string a fecha si es necesario
                if isinstance(default_date, str):
                    if default_date != "YYYY-MM-DD":
                        date_entry.set_date(default_date)
            except:
                pass
        return date_entry
    else:
        # Fallback: Entry normal
        date_entry = Entry(parent, font=font, bg=bg_color, fg=fg_color, 
                          relief="flat", bd=2, highlightbackground=border_color, 
                          highlightthickness=1)
        if default_date:
            date_entry.insert(0, default_date)
        else:
            date_entry.insert(0, "YYYY-MM-DD")
        return date_entry

ESTADOS_PEDIDO = [
    "Pendiente",
    "Entregado"
]

def show_orders_view(gui):
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
    gui.styled_label(card, "Gestión de Pedidos", size=20, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=8).pack(anchor="w", padx=24, pady=(18, 0))
    Label(card, text="Visualiza, crea, edita y elimina pedidos del sistema", font=("Segoe UI", 12), fg=TEXTO, bg=TABLA_FILA).pack(anchor="w", padx=24, pady=(0, 18))
    # Botones alineados
    frame_botones = Frame(card, bg=TABLA_FILA)
    frame_botones.pack(pady=10, padx=24, anchor="w")
    Button = gui.styled_button
    Button(frame_botones, "Agregar Pedido", lambda: add_order_form(gui), bg=BOTON_PRINCIPAL, fg="white", image=gui.action_images[0], compound="left").pack(side="left", padx=5)
    Button(frame_botones, "Editar Pedido", lambda: edit_order_form(gui), bg=BOTON_PRINCIPAL, fg="white", image=gui.action_images[1], compound="left").pack(side="left", padx=5)
    Button(frame_botones, "Eliminar Pedido", lambda: delete_order_form(gui), bg=BOTON_PRINCIPAL, fg="white", image=gui.action_images[2], compound="left").pack(side="left", padx=5)
    Button(frame_botones, "Exportar a Excel", exportar_excel, bg=BOTON_PRINCIPAL, fg="white", image=gui.excel_icon, compound="left").pack(anchor="e", padx=24, pady=8)
    # Tabla de pedidos
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background=TABLA_FILA, fieldbackground=TABLA_FILA, foreground=TEXTO, rowheight=28, font=("Segoe UI", 11), borderwidth=0)
    style.configure("Treeview.Heading", background=TABLA_HEADER, foreground=TEXTO, font=("Segoe UI", 12, "bold"), borderwidth=0)
    style.map("Treeview", background=[("selected", TABLA_FILA_ALTERNA)], foreground=[("selected", BOTON_PRINCIPAL)])
    columns = ("ID", "Cliente", "Estado", "Fecha", "Fecha Entrega")
    frame_tabla = Frame(card, bg=TABLA_FILA)
    frame_tabla.pack(fill="both", expand=True, padx=24, pady=10)
    gui.orders_table = ttk.Treeview(frame_tabla, columns=columns, show="headings")
    vsb = tk.Scrollbar(frame_tabla, orient="vertical", command=gui.orders_table.yview)
    hsb = tk.Scrollbar(frame_tabla, orient="horizontal", command=gui.orders_table.xview)
    gui.orders_table.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    gui.orders_table.pack(side="left", fill="both", expand=True, anchor="n")
    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")
    for col in columns:
        gui.orders_table.heading(col, text=col)
        gui.orders_table.column(col, anchor="center", stretch=True, width=150)
    # Subtabla de productos del pedido seleccionado
    frame_tabla2 = Frame(card, bg=TABLA_FILA)
    frame_tabla2.pack(fill="both", expand=True, padx=24, pady=10)
    gui.order_products_table = ttk.Treeview(frame_tabla2, columns=("Nombre", "Cantidad", "Precio Unitario", "Total"), show="headings")
    vsb2 = tk.Scrollbar(frame_tabla2, orient="vertical", command=gui.order_products_table.yview)
    hsb2 = tk.Scrollbar(frame_tabla2, orient="horizontal", command=gui.order_products_table.xview)
    gui.order_products_table.configure(yscrollcommand=vsb2.set, xscrollcommand=hsb2.set)
    gui.order_products_table.pack(side="left", fill="both", expand=True, anchor="n")
    vsb2.pack(side="right", fill="y")
    hsb2.pack(side="bottom", fill="x")
    for col in ("Nombre", "Cantidad", "Precio Unitario", "Total"):
        gui.order_products_table.heading(col, text=col)
        gui.order_products_table.column(col, anchor="center", stretch=True, width=150)
    gui.orders_table.bind("<<TreeviewSelect>>", lambda event: on_order_select(gui, event))
    view_orders(gui)

def view_orders(gui):
    for row in gui.orders_table.get_children():
        gui.orders_table.delete(row)
    pedidos = read_orders_grouped()
    for pedido_id, data in pedidos.items():
        info = data["info"]
        productos = data["productos"]
        # Badge de estado
        estado = info[2]
        badge = f"[{estado}]" if estado else ""
        fecha_entrega = info[4] if info[4] else ""
        parent = gui.orders_table.insert("", "end", values=(info[0], info[1], badge, info[3], fecha_entrega))
        for nombre, cantidad, precio_unitario, total in productos:
            gui.orders_table.insert(parent, "end", values=("", f"Producto: {nombre}", f"Cantidad: {cantidad}", "", ""))

def on_order_select(gui, event):
    selected = gui.orders_table.selection()
    if not selected:
        return
    pedido_id = gui.orders_table.item(selected[0])["values"][0]
    pedidos = read_orders_grouped()
    if pedido_id not in pedidos:
        return
    productos = pedidos[pedido_id]["productos"]
    for row in gui.order_products_table.get_children():
        gui.order_products_table.delete(row)
    for nombre, cantidad, precio_unitario, total in productos:
        try:
            precio_venta_str = f"${float(precio_unitario):,.2f}"
        except Exception:
            precio_venta_str = ''
        try:
            total_str = f"${float(total):,.2f}"
        except Exception:
            total_str = ''
        gui.order_products_table.insert("", "end", values=(nombre, cantidad, precio_venta_str, total_str))

def add_order_form(gui):
    productos_seleccionados = []
    form = Toplevel(gui.master)
    form.title("Agregar Pedido")
    form.configure(bg=TABLA_FILA)
    form.geometry("520x600")
    form.resizable(True, True)
    # Frame con canvas y scrollbars
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
    # Usar scroll_frame en vez de form para los widgets
    gui.styled_label(scroll_frame, "Cliente", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=0, column=0, sticky="w", padx=18, pady=8)
    cliente_entry = Entry(scroll_frame, font=gui.font, bg=FONDO_CLARO, fg=TEXTO, relief="flat", bd=2, highlightbackground=BORDER, highlightthickness=1)
    cliente_entry.grid(row=0, column=1, padx=10, pady=8)
    gui.styled_label(scroll_frame, "Estado", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=1, column=0, sticky="w", padx=18, pady=8)
    estado_var = StringVar(value=ESTADOS_PEDIDO[0])
    estado_combo = ttk.Combobox(scroll_frame, textvariable=estado_var, state="readonly", values=ESTADOS_PEDIDO, font=gui.font)
    estado_combo.grid(row=1, column=1, padx=10, pady=8)
    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
    gui.styled_label(scroll_frame, "Fecha", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=2, column=0, sticky="w", padx=18, pady=8)
    fecha_label = Label(scroll_frame, text=fecha, bg=TABLA_FILA, fg=BOTON_PRINCIPAL, font=gui.font)
    fecha_label.grid(row=2, column=1, padx=10, pady=8)
    
    gui.styled_label(scroll_frame, "Fecha de Entrega", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=3, column=0, sticky="w", padx=18, pady=8)
    fecha_entrega_entry = create_date_entry(scroll_frame, gui.font, FONDO_CLARO, TEXTO, BORDER)
    fecha_entrega_entry.grid(row=3, column=1, padx=10, pady=8)
    
    gui.styled_label(scroll_frame, "Producto", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=4, column=0, sticky="w", padx=18, pady=8)
    productos = get_products_list()
    producto_var = StringVar()
    producto_combo = ttk.Combobox(scroll_frame, textvariable=producto_var, state="readonly", values=[f"{pid} - {name}" for pid, name in productos], font=gui.font)
    producto_combo.grid(row=4, column=1, padx=10, pady=8)
    if productos:
        producto_combo.current(0)
    gui.styled_label(scroll_frame, "Cantidad", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=5, column=0, sticky="w", padx=18, pady=8)
    cantidad_entry = Entry(scroll_frame, font=gui.font, bg=FONDO_CLARO, fg=TEXTO, relief="flat", bd=2, highlightbackground=BORDER, highlightthickness=1)
    cantidad_entry.grid(row=5, column=1, padx=10, pady=8)
    productos_listbox = ttk.Treeview(scroll_frame, columns=("Producto", "Cantidad"), show="headings", height=5)
    productos_listbox.heading("Producto", text="Producto")
    productos_listbox.heading("Cantidad", text="Cantidad")
    productos_listbox.grid(row=6, column=0, columnspan=2, pady=8, padx=18)
    def agregar_producto():
        prod_index = producto_combo.current()
        cantidad = cantidad_entry.get()
        if prod_index == -1 or not cantidad:
            messagebox.showerror("Error", "Seleccione producto y cantidad.")
            return
        try:
            cantidad = float(cantidad)
        except ValueError:
            messagebox.showerror("Error", "Cantidad inválida.")
            return
        producto_id = productos[prod_index][0]
        producto_nombre = productos[prod_index][1]
        productos_seleccionados.append((producto_id, cantidad))
        productos_listbox.insert("", "end", values=(producto_nombre, cantidad))
        cantidad_entry.delete(0, "end")
    gui.styled_button(scroll_frame, "Agregar Producto", agregar_producto, bg=BOTON_PRINCIPAL, fg="white").grid(row=7, column=0, columnspan=2, pady=4)
    def guardar_pedido():
        cliente = cliente_entry.get()
        estado = estado_var.get().strip()
        estado = next((e for e in ESTADOS_PEDIDO if e.lower().strip() == estado.lower().strip()), estado)
        
        # Obtener fecha de entrega del calendario
        if DateEntry is not None and hasattr(fecha_entrega_entry, 'get_date'):
            try:
                fecha_entrega = fecha_entrega_entry.get_date().strftime("%Y-%m-%d")
            except:
                fecha_entrega = None
        else:
            fecha_entrega = fecha_entrega_entry.get().strip()
            if fecha_entrega == "YYYY-MM-DD":
                fecha_entrega = None
        
        if not cliente or not productos_seleccionados or not estado:
            messagebox.showerror("Error", "Debe ingresar cliente, estado y al menos un producto.")
            return
        create_order_with_products(cliente, estado, fecha, productos_seleccionados, fecha_entrega)
        messagebox.showinfo("Éxito", "Pedido creado correctamente.")
        form.destroy()
        view_orders(gui)
    gui.styled_button(scroll_frame, "Guardar Pedido", guardar_pedido, bg=BOTON_PRINCIPAL, fg="white").grid(row=8, column=0, columnspan=2, pady=12)


def edit_order_form(gui):
    selected = gui.orders_table.selection()
    if not selected:
        messagebox.showwarning("Advertencia", "Seleccione un pedido de la tabla para editar")
        return
    parent = gui.orders_table.parent(selected[0])
    if parent:  
        messagebox.showwarning("Advertencia", "Seleccione la fila del pedido, no de un producto.")
        return
    order_values = gui.orders_table.item(selected[0])["values"]
    order_id = order_values[0]
    form = Toplevel(gui.master)
    form.title("Editar Pedido")
    form.configure(bg=TABLA_FILA)
    form.geometry("420x320")
    form.resizable(True, True)
    gui.styled_label(form, "Cliente", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=0, column=0, sticky="w", padx=18, pady=8)
    cliente_entry = Entry(form, font=gui.font, bg=FONDO_CLARO, fg=TEXTO, relief="flat", bd=2, highlightbackground=BORDER, highlightthickness=1)
    cliente_entry.insert(0, order_values[1])
    cliente_entry.grid(row=0, column=1, padx=10, pady=8)
    gui.styled_label(form, "Estado", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=1, column=0, sticky="w", padx=18, pady=8)
    estado_var = StringVar()
    estado_combo = ttk.Combobox(form, textvariable=estado_var, state="readonly", values=ESTADOS_PEDIDO, font=gui.font)
    estado_combo.grid(row=1, column=1, padx=10, pady=8)
    estado_actual = str(order_values[2]).strip()
    estado_match = next((e for e in ESTADOS_PEDIDO if e.lower().strip() == estado_actual.lower()), ESTADOS_PEDIDO[0])
    estado_var.set(estado_match)
    fecha = order_values[3]
    fecha_entrega = order_values[4] if len(order_values) > 4 else ""
    gui.styled_label(form, "Fecha", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=2, column=0, sticky="w", padx=18, pady=8)
    fecha_label = Label(form, text=fecha, bg=TABLA_FILA, fg=BOTON_PRINCIPAL, font=gui.font)
    fecha_label.grid(row=2, column=1, padx=10, pady=8)
    
    gui.styled_label(form, "Fecha de Entrega", size=13, fg=BOTON_PRINCIPAL, bg=TABLA_FILA, pady=2).grid(row=3, column=0, sticky="w", padx=18, pady=8)
    fecha_entrega_entry = create_date_entry(form, gui.font, FONDO_CLARO, TEXTO, BORDER, fecha_entrega)
    fecha_entrega_entry.grid(row=3, column=1, padx=10, pady=8)
    
    def save_edit_order():
        form.focus()
        form.update_idletasks()
        cliente = cliente_entry.get()
        estado = estado_var.get().strip()
        estado = next((e for e in ESTADOS_PEDIDO if e.lower().strip() == estado.lower().strip()), estado)
        
        # Obtener fecha de entrega del calendario
        if DateEntry is not None and hasattr(fecha_entrega_entry, 'get_date'):
            try:
                fecha_entrega = fecha_entrega_entry.get_date().strftime("%Y-%m-%d")
            except:
                fecha_entrega = ""
        else:
            fecha_entrega = fecha_entrega_entry.get().strip()
        
        if not (cliente and estado):
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
            return
        update_order(order_id, (cliente, estado, fecha, fecha_entrega))
        messagebox.showinfo("Éxito", "Pedido actualizado correctamente")
        form.destroy()
        view_orders(gui)
    gui.styled_button(form, "Guardar Cambios", save_edit_order, bg=BOTON_PRINCIPAL, fg="white").grid(row=4, column=0, columnspan=2, pady=12)

def delete_order_form(gui):
    selected = gui.orders_table.selection()
    if not selected:
        messagebox.showwarning("Advertencia", "Seleccione un pedido de la tabla para eliminar")
        return
    parent = gui.orders_table.parent(selected[0])
    if parent:
        messagebox.showwarning("Advertencia", "Seleccione la fila del pedido, no de un producto.")
        return
    order_values = gui.orders_table.item(selected[0])["values"]
    order_id = order_values[0]
    confirm = messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el pedido ID {order_id}?")
    if confirm:
        delete_order(order_id)
        messagebox.showinfo("Éxito", "Pedido eliminado correctamente")
        view_orders(gui)

def exportar_excel():
    ruta = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], title="Guardar pedidos")
    if not ruta:
        return
    pedidos = read_orders_grouped()
    pedidos_list = []
    for pid, data in pedidos.items():
        info = data["info"]
        for prod, cant, precio_unitario, total in data["productos"]:
            pedidos_list.append([info[0], info[1], info[2], info[3], info[4] if len(info) > 4 else "", prod, cant, precio_unitario, total])
    df_pedidos = pd.DataFrame(pedidos_list, columns=pd.Index(["ID Pedido", "Cliente", "Estado", "Fecha", "Fecha Entrega", "Producto", "Cantidad", "Precio Unitario", "Total"]))
    df_pedidos.to_excel(ruta, index=False)
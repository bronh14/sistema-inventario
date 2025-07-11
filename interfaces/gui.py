from tkinter import Tk, Frame, Label, Button
import tkinter.font as tkFont
from interfaces.view_materials import show_materials_view
from interfaces.view_products import show_products_view
from interfaces.view_recipes import show_recipes_view
from interfaces.view_orders import show_orders_view
from interfaces.colors import NEGRO, AZUL_MARINO, AZUL_PETROLEO, PURPURA_NOCHE, AZUL_CIELO, AZUL_HIELO, FONDO_CLARO, SIDEBAR, SIDEBAR_HOVER, BOTON_PRINCIPAL, BOTON_PRINCIPAL_HOVER, BOTON_EXITO, BOTON_EXITO_HOVER, BOTON_PELIGRO, BOTON_PELIGRO_HOVER, TEXTO, TEXTO_SECUNDARIO, BORDER, TABLA_HEADER, TABLA_FILA_ALTERNA, TABLA_FILA, ICONO
from interfaces.graphics import show_graphics_view
from interfaces.dashboard import show_dashboard_view
from PIL import Image, ImageTk


class InventoryGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sistema de Inventario")
        master.geometry("1300x900")
        master.configure(bg=FONDO_CLARO)
        self.font = tkFont.Font(family="Segoe UI", size=11)

        # Cargar imágenes del sidebar
        self.sidebar_images = {}
        image_files = {
            "Dashboard": "assets/dashborad.png",
            "Pedidos": "assets/pedidos.png",
            "Materiales": "assets/materiales.png",
            "Productos": "assets/productos.png",
            "Recetas": "assets/recetas.png",
            "Gráficas": "assets/graficas.png"
        }
        for key, path in image_files.items():
            try:
                img = Image.open(path)
                img = img.resize((28, 28), Image.Resampling.LANCZOS)
                self.sidebar_images[key] = ImageTk.PhotoImage(img)
            except Exception:
                self.sidebar_images[key] = None

        # Sidebar
        self.sidebar = Frame(master, width=220, bg=SIDEBAR, bd=0, highlightthickness=0)
        self.sidebar.pack(side="left", fill="y")

        self.main_frame = Frame(master, bg=FONDO_CLARO)
        self.main_frame.pack(side="right", fill="both", expand=True)

        self.add_sidebar_button("Dashboard", show_dashboard_view)
        self.add_sidebar_button("Pedidos", show_orders_view)
        self.add_sidebar_button("Materiales", show_materials_view)
        self.add_sidebar_button("Productos", show_products_view)
        self.add_sidebar_button("Recetas", show_recipes_view)
        self.add_sidebar_button("Gráficas", show_graphics_view)
        self.main_frame.pack(side="right", fill="both", expand=True)

        # Mostrar dashboard al iniciar
        show_dashboard_view(self)

    def add_sidebar_button(self, text, command):
        img = self.sidebar_images.get(text)
        if img:
            btn = Button(self.sidebar, text=text, font=self.font, fg="white", bg=SIDEBAR, activebackground=SIDEBAR_HOVER, bd=0, highlightthickness=0, command=lambda: command(self), padx=18, pady=12, relief="flat", cursor="hand2", image=img, compound="left")
        else:
            btn = Button(self.sidebar, text=text, font=self.font, fg="white", bg=SIDEBAR, activebackground=SIDEBAR_HOVER, bd=0, highlightthickness=0, command=lambda: command(self), padx=18, pady=12, relief="flat", cursor="hand2")
        btn.pack(fill="x", pady=8, padx=18)
        btn.configure(borderwidth=0, highlightbackground=SIDEBAR)
        btn.bind("<Enter>", lambda e: btn.config(bg=SIDEBAR_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=SIDEBAR))

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def styled_label(self, parent, text, size=14, bold=True, fg=TEXTO, bg=FONDO_CLARO, pady=10):
        font = tkFont.Font(family="Segoe UI", size=size, weight="bold" if bold else "normal")
        return Label(parent, text=text, font=font, fg=fg, bg=bg, pady=pady)

    def styled_button(self, parent, text, command, bg=BOTON_PRINCIPAL, fg="white", **kwargs):
        btn = Button(parent, text=text, font=self.font, bg=bg, fg=fg, activebackground=BOTON_PRINCIPAL_HOVER, activeforeground="white", bd=0, highlightthickness=0, command=command, padx=16, pady=8, relief="flat", cursor="hand2", **kwargs)
        btn.configure(borderwidth=0, highlightbackground=bg)
        btn.bind("<Enter>", lambda e: btn.config(bg=BOTON_PRINCIPAL_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        btn.configure(relief="flat")
        btn.configure(highlightthickness=0)
        btn.configure(borderwidth=0)
        btn.configure(overrelief="flat")
        btn.configure(cursor="hand2")
        btn.configure(font=self.font)
        return btn

def main_gui():
    root = Tk()
    inventory_gui = InventoryGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main_gui()
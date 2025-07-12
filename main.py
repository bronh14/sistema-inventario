from database.database import initialize_database
from interfaces.gui import main_gui

def main():
    # Inicializar la base de datos
    initialize_database()
    
    main_gui()  # Interfaz gráfica de usuario

if __name__ == "__main__":
    main()
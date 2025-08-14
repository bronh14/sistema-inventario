#!/usr/bin/env python3
"""
Script para instalar tkcalendar si no está disponible.
Ejecutar este script si se tienen problemas con los calendarios desplegables.
"""

import subprocess
import sys

def install_tkcalendar():
    """Instala tkcalendar usando pip"""
    try:
        print("Instalando tkcalendar...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tkcalendar>=1.6.1"])
        print("✅ tkcalendar instalado correctamente!")
        print("Ahora puedes usar los calendarios desplegables en los formularios de pedidos.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar tkcalendar: {e}")
        print("Intenta ejecutar manualmente: pip install tkcalendar>=1.6.1")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def check_tkcalendar():
    """Verifica si tkcalendar está instalado"""
    try:
        import tkcalendar
        print("✅ tkcalendar ya está instalado!")
        return True
    except ImportError:
        print("❌ tkcalendar no está instalado.")
        return False

if __name__ == "__main__":
    print("=== Verificador de tkcalendar ===")
    if not check_tkcalendar():
        print("\n¿Deseas instalar tkcalendar ahora? (s/n): ", end="")
        response = input().lower().strip()
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            install_tkcalendar()
        else:
            print("Instalación cancelada. Los calendarios desplegables no estarán disponibles.")
    else:
        print("No es necesario instalar tkcalendar.") 
#!/usr/bin/env python3
"""
Script para generar un ejecutable del Sistema de Inventario usando PyInstaller
Incluye Python embebido para sistemas sin Python instalado
"""

import os
import sys
import subprocess
import shutil
import urllib.request
import zipfile

def install_pyinstaller():
    """Instala PyInstaller si no está disponible"""
    try:
        import PyInstaller
        print("PyInstaller ya está instalado.")
    except ImportError:
        print("Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def download_python_embedded():
    """Descarga Python embebido para incluir en el ejecutable"""
    print("Descargando Python embebido...")
    
    # URL de Python embebido para Windows
    python_url = "https://www.python.org/ftp/python/3.11.8/python-3.11.8-embed-amd64.zip"
    embedded_dir = "python_embedded"
    
    if not os.path.exists(embedded_dir):
        os.makedirs(embedded_dir)
    
    zip_path = os.path.join(embedded_dir, "python_embedded.zip")
    
    try:
        # Descargar Python embebido
        urllib.request.urlretrieve(python_url, zip_path)
        
        # Extraer
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(embedded_dir)
        
        # Limpiar archivo zip
        os.remove(zip_path)
        
        print("Python embebido descargado exitosamente.")
        return embedded_dir
    except Exception as e:
        print(f"Error al descargar Python embebido: {e}")
        return None

def build_executable():
    """Construye el ejecutable"""
    print("Construyendo ejecutable del Sistema de Inventario...")
    
    # Comando de PyInstaller con Python embebido
    cmd = [
        "pyinstaller",
        "--onefile",                    # Un solo archivo ejecutable
        "--windowed",                   # Sin consola (para GUI)
        "--name=SistemaInventario",     # Nombre del ejecutable
        "--icon=assets/productos.png",  # Icono (si existe)
        "--add-data=assets;assets",     # Incluir carpeta de assets
        "--hidden-import=PIL._tkinter_finder",  # Importación oculta necesaria
        "--hidden-import=matplotlib.backends.backend_tkagg",
        "--hidden-import=pandas",
        "--hidden-import=xlsxwriter",
        "--hidden-import=sqlite3",
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=tkinter.messagebox",
        "--hidden-import=tkinter.filedialog",
        "--hidden-import=tkinter.simpledialog",
        "--collect-all=pandas",
        "--collect-all=matplotlib",
        "--collect-all=PIL",
        "--collect-all=xlsxwriter",
        "main.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("¡Ejecutable creado exitosamente!")
        print("El archivo se encuentra en: dist/SistemaInventario.exe")
        
        # Crear instalador mejorado
        create_installer()
        
    except subprocess.CalledProcessError as e:
        print(f"Error al crear el ejecutable: {e}")
        return False
    
    return True

def create_installer():
    """Crea un instalador mejorado"""
    print("Creando instalador...")
    
    installer_content = '''@echo off
setlocal enabledelayedexpansion

echo ========================================
echo    INSTALADOR SISTEMA DE INVENTARIO
echo ========================================
echo.

set INSTALL_DIR=%PROGRAMFILES%\\SistemaInventario
set DESKTOP_SHORTCUT=%USERPROFILE%\\Desktop\\Sistema de Inventario.lnk

echo Instalando en: %INSTALL_DIR%

:: Crear directorio de instalación
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
if not exist "%INSTALL_DIR%\\assets" mkdir "%INSTALL_DIR%\\assets"

echo Copiando archivos...
copy "SistemaInventario.exe" "%INSTALL_DIR%\\"
xcopy "assets\\*" "%INSTALL_DIR%\\assets\\" /E /I /Y

:: Crear acceso directo en el escritorio
echo Creando acceso directo en el escritorio...
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP_SHORTCUT%'); $Shortcut.TargetPath = '%INSTALL_DIR%\\SistemaInventario.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'Sistema de Gestión de Inventario'; $Shortcut.Save()}"

:: Crear entrada en el menú inicio
echo Creando entrada en el menú inicio...
set START_MENU=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\SistemaInventario
if not exist "%START_MENU%" mkdir "%START_MENU%"
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%START_MENU%\\Sistema de Inventario.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\SistemaInventario.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'Sistema de Gestión de Inventario'; $Shortcut.Save()}"

:: Crear desinstalador
echo Creando desinstalador...
copy "uninstall.bat" "%INSTALL_DIR%\\"

:: Crear archivo de registro para desinstalación
echo Creando registro de instalación...
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\SistemaInventario" /v "DisplayName" /t REG_SZ /d "Sistema de Inventario" /f
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\SistemaInventario" /v "UninstallString" /t REG_SZ /d "%INSTALL_DIR%\\uninstall.bat" /f
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\SistemaInventario" /v "DisplayIcon" /t REG_SZ /d "%INSTALL_DIR%\\SistemaInventario.exe" /f
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\SistemaInventario" /v "Publisher" /t REG_SZ /d "Sistema de Inventario" /f
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\SistemaInventario" /v "DisplayVersion" /t REG_SZ /d "1.0.0" /f

echo.
echo ========================================
echo    INSTALACION COMPLETADA
echo ========================================
echo.
echo El sistema se ha instalado en: %INSTALL_DIR%
echo Se ha creado un acceso directo en el escritorio.
echo Se ha agregado al menú inicio.
echo.
echo Para desinstalar, ejecuta: %INSTALL_DIR%\\uninstall.bat
echo.

read /p "¿Deseas ejecutar el sistema ahora? (s/n): " -n 1 -r
echo
if /i "%REPLY%"=="S" (
    echo.
    echo Iniciando Sistema de Inventario...
    start "" "%INSTALL_DIR%\\SistemaInventario.exe"
)

pause
'''
    
    with open("dist/Instalar_Sistema_Inventario.bat", "w", encoding="utf-8") as f:
        f.write(installer_content)
    
    print("Instalador creado: dist/Instalar_Sistema_Inventario.bat")

def create_portable_version():
    """Crea una versión portable"""
    print("Creando versión portable...")
    
    portable_dir = "dist/SistemaInventario_Portable"
    if os.path.exists(portable_dir):
        shutil.rmtree(portable_dir)
    
    os.makedirs(portable_dir)
    
    # Copiar archivos
    shutil.copy("dist/SistemaInventario.exe", portable_dir)
    shutil.copytree("assets", os.path.join(portable_dir, "assets"))
    
    # Crear script de inicio
    with open(os.path.join(portable_dir, "Iniciar_Sistema.bat"), "w", encoding="utf-8") as f:
        f.write('''@echo off
echo Iniciando Sistema de Inventario...
SistemaInventario.exe
pause
''')
    
    print(f"Versión portable creada en: {portable_dir}")

def main():
    """Función principal"""
    print("=== GENERADOR DE EJECUTABLE ===")
    print("Sistema de Inventario")
    print()
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("main.py"):
        print("ERROR: No se encontró main.py")
        print("Ejecuta este script desde el directorio raíz del proyecto")
        return
    
    # Instalar PyInstaller si es necesario
    install_pyinstaller()
    
    # Construir ejecutable
    if build_executable():
        print("\n=== CREANDO VERSIONES ===")
        
        # Crear versión portable
        create_portable_version()
        
        print("\n=== RESUMEN ===")
        print("Archivos generados:")
        print("- dist/SistemaInventario.exe (ejecutable principal)")
        print("- dist/Instalar_Sistema_Inventario.bat (instalador completo)")
        print("- dist/SistemaInventario_Portable/ (versión portable)")
        print("\nPara distribuir:")
        print("1. Copia la carpeta 'dist' completa")
        print("2. Para instalación: ejecuta 'Instalar_Sistema_Inventario.bat'")
        print("3. Para uso portable: copia 'SistemaInventario_Portable'")
    else:
        print("Error en la generación del ejecutable")

if __name__ == "__main__":
    main() 
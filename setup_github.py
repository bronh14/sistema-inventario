#!/usr/bin/env python3
"""
Script para configurar y subir el proyecto a GitHub
"""

import os
import subprocess
import sys
import json
import urllib.request
import urllib.parse

def check_git_installed():
    """Verifica si Git está instalado"""
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def init_git_repo():
    """Inicializa el repositorio Git"""
    print("Inicializando repositorio Git...")
    
    # Inicializar Git
    subprocess.run(["git", "init"], check=True)
    
    # Configurar usuario (si no está configurado)
    try:
        subprocess.run(["git", "config", "user.name"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("Configurando usuario Git...")
        name = input("Ingresa tu nombre para Git: ")
        subprocess.run(["git", "config", "user.name", name], check=True)
    
    try:
        subprocess.run(["git", "config", "user.email"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("Configurando email Git...")
        email = input("Ingresa tu email para Git: ")
        subprocess.run(["git", "config", "user.email", email], check=True)

def create_github_repo():
    """Crea el repositorio en GitHub usando la API"""
    print("Creando repositorio en GitHub...")
    
    # Solicitar token de GitHub
    token = input("Ingresa tu token de GitHub (o presiona Enter para crear manualmente): ").strip()
    
    if not token:
        print("\nPara crear el repositorio manualmente:")
        print("1. Ve a https://github.com/new")
        print("2. Nombre del repositorio: sistema-inventario")
        print("3. Descripción: Sistema de gestión de inventario con interfaz gráfica")
        print("4. Marca como público")
        print("5. NO inicialices con README (ya tenemos uno)")
        print("6. Haz clic en 'Create repository'")
        return None
    
    # Configuración del repositorio
    repo_name = "sistema-inventario"
    repo_description = "Sistema de gestión de inventario con interfaz gráfica desarrollado en Python"
    
    # Crear repositorio via API
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": repo_name,
        "description": repo_description,
        "private": False,
        "auto_init": False
    }
    
    try:
        req = urllib.request.Request(url, headers=headers, data=json.dumps(data).encode())
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            print(f"Repositorio creado: {result['html_url']}")
            return result['clone_url']
    except Exception as e:
        print(f"Error al crear repositorio: {e}")
        return None

def add_files_to_git():
    """Agrega archivos al repositorio Git"""
    print("Agregando archivos al repositorio...")
    
    # Agregar todos los archivos
    subprocess.run(["git", "add", "."], check=True)
    
    # Commit inicial
    subprocess.run(["git", "commit", "-m", "Initial commit: Sistema de Inventario"], check=True)

def push_to_github(remote_url):
    """Sube el código a GitHub"""
    print("Subiendo código a GitHub...")
    
    # Agregar remote
    subprocess.run(["git", "remote", "add", "origin", remote_url], check=True)
    
    # Cambiar nombre de la rama principal
    subprocess.run(["git", "branch", "-M", "main"], check=True)
    
    # Push
    subprocess.run(["git", "push", "-u", "origin", "main"], check=True)

def create_release_script():
    """Crea script para hacer releases"""
    print("Creando script de release...")
    
    release_script = '''#!/bin/bash
# Script para crear un release en GitHub

VERSION=$1
if [ -z "$VERSION" ]; then
    echo "Uso: ./release.sh <version>"
    echo "Ejemplo: ./release.sh 1.0.0"
    exit 1
fi

echo "Creando release v$VERSION..."

# Actualizar versión en archivos
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/g" setup.py
sed -i "s/version = \"[^\"]*\"/version = \"$VERSION\"/g" pyproject.toml

# Commit cambios
git add .
git commit -m "Bump version to $VERSION"
git push origin main

# Crear tag
git tag -a "v$VERSION" -m "Release v$VERSION"
git push origin "v$VERSION"

# Crear release en GitHub
gh release create "v$VERSION" \\
    --title "Sistema de Inventario v$VERSION" \\
    --notes "Release v$VERSION del Sistema de Inventario" \\
    --latest

echo "Release v$VERSION creado exitosamente!"
'''
    
    with open("release.sh", "w") as f:
        f.write(release_script)
    
    # Hacer ejecutable (en sistemas Unix)
    if os.name != 'nt':
        os.chmod("release.sh", 0o755)

def main():
    """Función principal"""
    print("=== CONFIGURADOR DE REPOSITORIO GITHUB ===")
    print("Sistema de Inventario")
    print()
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("main.py"):
        print("ERROR: No se encontró main.py")
        print("Ejecuta este script desde el directorio raíz del proyecto")
        return
    
    # Verificar Git
    if not check_git_installed():
        print("ERROR: Git no está instalado")
        print("Por favor instala Git desde https://git-scm.com")
        return
    
    try:
        # Inicializar repositorio Git
        init_git_repo()
        
        # Crear repositorio en GitHub
        remote_url = create_github_repo()
        
        # Agregar archivos
        add_files_to_git()
        
        if remote_url:
            # Subir a GitHub
            push_to_github(remote_url)
            print("\n✅ Repositorio creado y subido exitosamente!")
            print(f"URL: {remote_url.replace('.git', '')}")
        else:
            print("\n⚠️  Repositorio local creado")
            print("Crea el repositorio en GitHub manualmente y luego ejecuta:")
            print("git remote add origin https://github.com/TU_USUARIO/sistema-inventario.git")
            print("git push -u origin main")
        
        # Crear script de release
        create_release_script()
        
        print("\n=== PRÓXIMOS PASOS ===")
        print("1. Ve a tu repositorio en GitHub")
        print("2. Copia la URL del repositorio")
        print("3. Actualiza la URL en install_from_github.bat y install_from_github.sh")
        print("4. Para hacer releases, usa: ./release.sh <version>")
        
    except subprocess.CalledProcessError as e:
        print(f"Error en el proceso: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main() 
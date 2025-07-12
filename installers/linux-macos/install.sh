#!/bin/bash

echo "========================================"
echo "   INSTALADOR SISTEMA DE INVENTARIO"
echo "========================================"
echo

# Función para detectar el sistema operativo
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    else
        echo "unknown"
    fi
}

# Función para instalar Python en Linux
install_python_linux() {
    echo "Instalando Python en Linux..."
    
    # Detectar distribución
    if command -v apt-get &> /dev/null; then
        # Ubuntu/Debian
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip python3-venv
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL/Fedora
        sudo yum install -y python3 python3-pip
    elif command -v dnf &> /dev/null; then
        # Fedora (nuevo)
        sudo dnf install -y python3 python3-pip
    elif command -v pacman &> /dev/null; then
        # Arch Linux
        sudo pacman -S --noconfirm python python-pip
    else
        echo "ERROR: No se pudo detectar el gestor de paquetes"
        echo "Por favor instala Python 3.8+ manualmente"
        exit 1
    fi
}

# Función para instalar Python en macOS
install_python_macos() {
    echo "Instalando Python en macOS..."
    
    # Verificar si Homebrew está instalado
    if ! command -v brew &> /dev/null; then
        echo "Instalando Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    # Instalar Python
    brew install python@3.11
    
    # Agregar al PATH si es necesario
    if ! command -v python3 &> /dev/null; then
        echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
        source ~/.zshrc
    fi
}

# Verificar Python
echo "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "Python3 no está instalado. Instalando automáticamente..."
    
    OS=$(detect_os)
    case $OS in
        "linux")
            install_python_linux
            ;;
        "macos")
            install_python_macos
            ;;
        *)
            echo "ERROR: Sistema operativo no soportado"
            echo "Por favor instala Python 3.8+ manualmente desde https://python.org"
            exit 1
            ;;
    esac
    
    # Verificar instalación
    if ! command -v python3 &> /dev/null; then
        echo "ERROR: La instalación de Python falló"
        exit 1
    fi
    
    echo "Python instalado exitosamente."
else
    echo "Python3 encontrado."
fi

# Verificar versión de Python
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "ERROR: Se requiere Python 3.8 o superior. Versión actual: $python_version"
    echo "Actualizando Python..."
    
    OS=$(detect_os)
    case $OS in
        "linux")
            install_python_linux
            ;;
        "macos")
            install_python_macos
            ;;
    esac
fi

# Verificar pip
echo "Verificando pip..."
if ! command -v pip3 &> /dev/null; then
    echo "Instalando pip..."
    python3 -m ensurepip --upgrade
fi

echo
echo "Instalando dependencias..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Error al instalar dependencias"
    echo "Intentando con --user..."
    python3 -m pip install -r requirements.txt --user
    if [ $? -ne 0 ]; then
        echo "ERROR: No se pudieron instalar las dependencias"
        exit 1
    fi
fi

echo
echo "Instalando el sistema como paquete..."
python3 -m pip install -e .

if [ $? -ne 0 ]; then
    echo "ERROR: Error al instalar el paquete"
    echo "Intentando con --user..."
    python3 -m pip install -e . --user
    if [ $? -ne 0 ]; then
        echo "ERROR: No se pudo instalar el paquete"
        exit 1
    fi
fi

# Crear script de ejecución
echo "Creando script de ejecución..."
cat > sistema-inventario.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
python3 main.py
EOF

chmod +x sistema-inventario.sh

# Crear acceso directo en el escritorio (Linux)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Creando acceso directo en el escritorio..."
    cat > ~/Desktop/Sistema\ de\ Inventario.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Sistema de Inventario
Comment=Sistema de gestión de inventario
Exec=$(pwd)/sistema-inventario.sh
Icon=$(pwd)/assets/productos.png
Terminal=false
Categories=Office;
EOF
    chmod +x ~/Desktop/Sistema\ de\ Inventario.desktop
fi

echo
echo "========================================"
echo "   INSTALACION COMPLETADA EXITOSAMENTE"
echo "========================================"
echo
echo "Para ejecutar el sistema:"
echo "  - Opcion 1: ./sistema-inventario.sh"
echo "  - Opcion 2: python3 main.py"
echo "  - Opcion 3: sistema-inventario (si está en PATH)"
echo

read -p "¿Deseas ejecutar el sistema ahora? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo
    echo "Iniciando Sistema de Inventario..."
    python3 main.py
fi 
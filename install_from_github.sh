#!/bin/bash

echo "========================================"
echo "   INSTALADOR DESDE GITHUB"
echo "   Sistema de Inventario"
echo "========================================"
echo

GITHUB_REPO="https://github.com/Bronh14/sistema-inventario.git"
INSTALL_DIR="$HOME/Desktop/SistemaInventario"

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

# Función para instalar Git en Linux
install_git_linux() {
    echo "Instalando Git en Linux..."
    
    if command -v apt-get &> /dev/null; then
        # Ubuntu/Debian
        sudo apt-get update
        sudo apt-get install -y git
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL/Fedora
        sudo yum install -y git
    elif command -v dnf &> /dev/null; then
        # Fedora (nuevo)
        sudo dnf install -y git
    elif command -v pacman &> /dev/null; then
        # Arch Linux
        sudo pacman -S --noconfirm git
    else
        echo "ERROR: No se pudo detectar el gestor de paquetes"
        echo "Por favor instala Git manualmente"
        exit 1
    fi
}

# Función para instalar Git en macOS
install_git_macos() {
    echo "Instalando Git en macOS..."
    
    if ! command -v brew &> /dev/null; then
        echo "Instalando Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    brew install git
}

# Verificar Git
echo "Verificando Git..."
if ! command -v git &> /dev/null; then
    echo "Git no está instalado. Instalando automáticamente..."
    
    OS=$(detect_os)
    case $OS in
        "linux")
            install_git_linux
            ;;
        "macos")
            install_git_macos
            ;;
        *)
            echo "ERROR: Sistema operativo no soportado"
            echo "Por favor instala Git manualmente desde https://git-scm.com"
            exit 1
            ;;
    esac
    
    # Verificar instalación
    if ! command -v git &> /dev/null; then
        echo "ERROR: La instalación de Git falló"
        exit 1
    fi
    
    echo "Git instalado exitosamente."
else
    echo "Git encontrado."
fi

echo
echo "Descargando proyecto desde GitHub..."

# Crear directorio de instalación
mkdir -p "$(dirname "$INSTALL_DIR")"

if [ -d "$INSTALL_DIR" ]; then
    echo "El directorio ya existe. Actualizando..."
    cd "$INSTALL_DIR"
    git pull origin main
else
    echo "Clonando repositorio..."
    git clone "$GITHUB_REPO" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

if [ $? -ne 0 ]; then
    echo "ERROR: No se pudo descargar el proyecto"
    echo "Verifica tu conexión a internet y el nombre del repositorio"
    exit 1
fi

echo
echo "Proyecto descargado exitosamente en: $INSTALL_DIR"
echo
echo "Ejecutando instalador..."
cd "$INSTALL_DIR"
chmod +x install.sh
./install.sh

echo
echo "========================================"
echo "   INSTALACION DESDE GITHUB COMPLETADA"
echo "========================================"
echo
echo "El sistema se ha instalado desde GitHub."
echo "Ubicación: $INSTALL_DIR"
echo 
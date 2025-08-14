#!/bin/bash

echo "========================================"
echo "   Activando Entorno Virtual"
echo "========================================"
echo

# Verificar si el entorno virtual existe
if [ ! -f "venv/bin/activate" ]; then
    echo "Error: El entorno virtual no existe."
    echo "Ejecuta: python3 -m venv venv"
    exit 1
fi

# Activar el entorno virtual
source venv/bin/activate

echo
echo "✅ Entorno virtual activado correctamente!"
echo
echo "Para ejecutar la aplicación:"
echo "  python main.py"
echo
echo "Para instalar nuevas dependencias:"
echo "  pip install nombre_paquete"
echo
echo "Para desactivar el entorno virtual:"
echo "  deactivate"
echo

# Mantener la sesión activa
exec $SHELL 
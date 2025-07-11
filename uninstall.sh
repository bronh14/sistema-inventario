#!/bin/bash

echo "========================================"
echo "   DESINSTALADOR SISTEMA DE INVENTARIO"
echo "========================================"
echo

read -p "¿Estás seguro de que deseas desinstalar el Sistema de Inventario? (s/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo "Desinstalación cancelada."
    exit 0
fi

echo
echo "Desinstalando paquete..."
pip3 uninstall sistema-inventario -y

echo
echo "Eliminando archivos de configuración..."
rm -rf ~/.sistema_inventario 2>/dev/null

echo
echo "Eliminando base de datos local..."
rm -f inventory_system.db 2>/dev/null
rm -f inventory.db 2>/dev/null

echo
echo "========================================"
echo "   DESINSTALACION COMPLETADA"
echo "========================================"
echo
echo "El Sistema de Inventario ha sido desinstalado."
echo 
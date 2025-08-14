# Entorno Virtual - Sistema de Inventario

## 📋 Resumen

Este proyecto utiliza un entorno virtual de Python para aislar las dependencias y evitar conflictos con otros proyectos.

## 🚀 Configuración Rápida

### Windows
```bash
# Activar entorno virtual
activate_venv.bat

# O manualmente:
venv\Scripts\activate
```

### Linux/macOS
```bash
# Activar entorno virtual
./activate_venv.sh

# O manualmente:
source venv/bin/activate
```

## 📦 Dependencias Instaladas

El entorno virtual incluye las siguientes dependencias:

- **pandas>=1.5.0** - Manipulación y análisis de datos
- **matplotlib>=3.5.0** - Creación de gráficos y visualizaciones
- **Pillow>=9.0.0** - Procesamiento de imágenes
- **xlsxwriter>=3.0.0** - Generación de archivos Excel
- **tkcalendar>=1.6.1** - Calendarios desplegables en la interfaz

## 🔧 Comandos Útiles

### Activar el entorno virtual
```bash
# Windows
activate_venv.bat

# Linux/macOS
./activate_venv.sh
```

### Ejecutar la aplicación
```bash
python main.py
```

### Instalar nuevas dependencias
```bash
pip install nombre_paquete
```

### Ver dependencias instaladas
```bash
pip list
```

### Actualizar dependencias
```bash
pip install -r requirements.txt --upgrade
```

### Desactivar el entorno virtual
```bash
deactivate
```

## 🛠️ Gestión del Entorno Virtual

### Crear un nuevo entorno virtual
```bash
# Windows
python -m venv venv

# Linux/macOS
python3 -m venv venv
```

### Eliminar el entorno virtual
```bash
# Windows
rmdir /s venv

# Linux/macOS
rm -rf venv
```

### Recrear el entorno virtual
```bash
# 1. Eliminar el entorno actual
rm -rf venv  # Linux/macOS
# rmdir /s venv  # Windows

# 2. Crear nuevo entorno
python -m venv venv

# 3. Activar
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# 4. Instalar dependencias
pip install -r requirements.txt
```

## 📁 Estructura del Entorno Virtual

```
proyecto/
├── venv/                    # Entorno virtual
│   ├── Scripts/            # Scripts de activación (Windows)
│   ├── bin/                # Scripts de activación (Linux/macOS)
│   ├── Lib/                # Librerías de Python
│   └── pyvenv.cfg          # Configuración del entorno
├── activate_venv.bat       # Script de activación (Windows)
├── activate_venv.sh        # Script de activación (Linux/macOS)
├── requirements.txt        # Dependencias del proyecto
└── main.py                 # Aplicación principal
```

## ⚠️ Notas Importantes

1. **Siempre activa el entorno virtual** antes de trabajar en el proyecto
2. **No incluyas la carpeta `venv/`** en el control de versiones
3. **Usa `pip freeze > requirements.txt`** para actualizar las dependencias
4. **El entorno virtual es específico** para cada instalación

## 🔍 Solución de Problemas

### Error: "No module named 'tkcalendar'"
```bash
pip install tkcalendar>=1.6.1
```

### Error: "venv no se reconoce como comando"
```bash
# Instalar venv si no está disponible
python -m pip install virtualenv
```

### Error: "Permission denied" en Linux/macOS
```bash
chmod +x activate_venv.sh
```

### Problemas con dependencias
```bash
# Reinstalar todas las dependencias
pip install -r requirements.txt --force-reinstall
```

## 📚 Recursos Adicionales

- [Documentación de venv](https://docs.python.org/3/library/venv.html)
- [Guía de pip](https://pip.pypa.io/en/stable/)
- [Documentación del proyecto](docs/README.md) 
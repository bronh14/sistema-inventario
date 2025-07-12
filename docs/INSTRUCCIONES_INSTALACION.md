# Instrucciones de Instalación - Sistema de Inventario

## 🚀 Instalación Automática (Recomendada)

### Windows
1. Descarga todos los archivos del proyecto
2. **Ejecuta `install.bat` como administrador**
3. El instalador verificará si Python está instalado
4. **Si Python no está instalado, lo descargará e instalará automáticamente**
5. Instalará todas las dependencias del proyecto
6. Creará un acceso directo en el escritorio
7. El sistema se ejecutará automáticamente al finalizar

### Linux/macOS
1. Descarga todos los archivos del proyecto
2. Abre una terminal en el directorio del proyecto
3. Ejecuta: `./install.sh`
4. El instalador verificará si Python está instalado
5. **Si Python no está instalado, lo instalará automáticamente usando el gestor de paquetes del sistema**
6. Instalará todas las dependencias del proyecto
7. Creará un script de ejecución local
8. Sigue las instrucciones en pantalla

## 📦 Instalación Manual

### Prerrequisitos
- Python 3.8 o superior
- pip (incluido con Python)

### Pasos
1. Abre una terminal en el directorio del proyecto
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Instala el paquete:
   ```bash
   pip install -e .
   ```
4. Ejecuta el sistema:
   ```bash
   sistema-inventario
   ```

## 🎯 Generación de Ejecutable (Windows)

Para crear un archivo .exe completamente independiente:

1. Ejecuta el script de generación:
   ```bash
   python build_exe.py
   ```
2. El ejecutable se creará en la carpeta `dist/`
3. Se generarán tres versiones:
   - **Ejecutable principal**: `SistemaInventario.exe`
   - **Instalador completo**: `Instalar_Sistema_Inventario.bat`
   - **Versión portable**: `SistemaInventario_Portable/`
4. Copia la carpeta `dist` completa al equipo destino
5. Ejecuta `Instalar_Sistema_Inventario.bat` en el equipo destino

## Verificación de la Instalación

### Verificar Dependencias
```bash
python -c "import pandas, matplotlib, PIL, xlsxwriter; print('Todas las dependencias están instaladas')"
```

### Verificar el Sistema
```bash
sistema-inventario
```

## Desinstalación

### Windows
Ejecuta `uninstall.bat` como administrador

### Linux/macOS
Ejecuta `./uninstall.sh`

### Manual
```bash
pip uninstall sistema-inventario
```

## Solución de Problemas

### Error: "Python no está en el PATH"
- **Con instalador automático**: El instalador descargará e instalará Python automáticamente
- **Manual**: Instala Python desde https://python.org y asegúrate de marcar "Add Python to PATH"

### Error: "pip no está instalado"
```bash
python -m ensurepip --upgrade
```

### Error: "Permisos denegados"
- **Windows**: Ejecuta como administrador
- **Linux/macOS**: Usa `sudo`

### Error: "Dependencias faltantes"
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Error: "Base de datos corrupta"
1. Cierra el programa
2. Elimina `inventory_system.db`
3. Reinicia el programa

### Error: "Instalación de Python falló"
1. **Windows**: 
   - Verifica la conexión a internet
   - Descarga Python manualmente desde https://python.org
   - Reinicia el sistema e intenta nuevamente
2. **Linux**: 
   - Usa el gestor de paquetes de tu distribución
   - `sudo apt-get install python3 python3-pip` (Ubuntu/Debian)
   - `sudo yum install python3 python3-pip` (CentOS/RHEL)
3. **macOS**: 
   - Instala Homebrew: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
   - Instala Python: `brew install python@3.11`

### Error: "No se pudo detectar el gestor de paquetes" (Linux)
- **Ubuntu/Debian**: `sudo apt-get update && sudo apt-get install python3 python3-pip`
- **CentOS/RHEL**: `sudo yum install python3 python3-pip`
- **Fedora**: `sudo dnf install python3 python3-pip`
- **Arch Linux**: `sudo pacman -S python python-pip`

## Estructura de Archivos Después de la Instalación

### Instalación Automática
```
Sistema de Inventario/
├── SistemaInventario.exe          # Ejecutable principal
├── assets/                         # Imágenes e iconos
├── inventory_system.db            # Base de datos
├── uninstall.bat                  # Desinstalador
└── Instalar_Sistema_Inventario.bat # Instalador
```

### Versión Portable
```
SistemaInventario_Portable/
├── SistemaInventario.exe          # Ejecutable principal
├── assets/                         # Imágenes e iconos
└── Iniciar_Sistema.bat            # Script de inicio
```

## Configuración Post-Instalación

1. **Primera ejecución**: El sistema creará automáticamente la base de datos
2. **Acceso directo**: Se creará en el escritorio automáticamente
3. **Menú inicio**: Se agregará al menú inicio (Windows)
4. **Configuración**: Los archivos de configuración se guardan en el directorio del usuario

## Soporte Técnico

Si encuentras problemas durante la instalación:

1. Verifica que tienes conexión a internet (para descargar Python)
2. Asegúrate de tener permisos de administrador
3. Revisa los logs de error en la consola
4. Contacta soporte técnico con el mensaje de error completo

## Actualizaciones

Para actualizar el sistema:

1. Descarga la nueva versión
2. Desinstala la versión anterior usando el desinstalador
3. Instala la nueva versión siguiendo las instrucciones anteriores

## Notas Importantes

- **El sistema requiere conexión a internet solo para la instalación inicial**
- **Python se instala automáticamente si no está presente**
- **La base de datos se almacena localmente**
- **Los reportes se guardan en el directorio seleccionado por el usuario**
- **El sistema es compatible con Windows 10/11, macOS 10.14+ y Linux**
- **La versión portable no requiere instalación**

## Características de la Instalación Automática

### Windows
- ✅ Descarga automática de Python 3.11.8
- ✅ Instalación silenciosa con PATH configurado
- ✅ Instalación de todas las dependencias
- ✅ Creación de acceso directo en escritorio
- ✅ Registro en el menú inicio
- ✅ Desinstalador completo

### Linux/macOS
- ✅ Detección automática del gestor de paquetes
- ✅ Instalación de Python usando el gestor del sistema
- ✅ Instalación de todas las dependencias
- ✅ Creación de script de ejecución local
- ✅ Acceso directo en escritorio (Linux)
- ✅ Desinstalador completo

### Ejecutable Independiente
- ✅ Python embebido en el ejecutable
- ✅ No requiere Python instalado en el sistema
- ✅ Versión portable disponible
- ✅ Instalador completo con registro de Windows 
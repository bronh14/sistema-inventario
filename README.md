# Sistema de Inventario

Un sistema completo de gestión de inventario con interfaz gráfica desarrollado en Python usando Tkinter.

## Características

- **Gestión de Materiales**: Control de stock, costos y proveedores
- **Gestión de Productos**: Productos terminados con precios de venta
- **Recetas de Producción**: Definición de recetas con materiales y costos
- **Gestión de Pedidos**: Creación y seguimiento de pedidos de clientes
- **Dashboard**: Vista general del sistema con estadísticas
- **Gráficas y Reportes**: Visualización de datos con matplotlib
- **Exportación a Excel**: Generación de reportes en formato Excel
- **Base de Datos SQLite**: Almacenamiento local de datos
- **Instalación Automática**: Incluye Python automáticamente si no está instalado
- **Instalación desde GitHub**: Descarga e instalación directa desde el repositorio

## Requisitos del Sistema

- **Windows 10/11**: Instalación automática de Python incluida
- **Linux**: Ubuntu 18.04+, CentOS 7+, Fedora 28+
- **macOS**: 10.14+ (Mojave o superior)
- **4GB RAM mínimo**
- **500MB espacio en disco**
- **Conexión a internet** (solo para la instalación inicial)

## 🚀 Instalación Rápida desde GitHub

### Windows
```bash
# Descargar e instalar automáticamente
curl -L https://raw.githubusercontent.com/Bronh14/sistema-inventario/main/install_from_github.bat -o install.bat
install.bat
```

### Linux/macOS
```bash
# Descargar e instalar automáticamente
curl -L https://raw.githubusercontent.com/Bronh14/sistema-inventario/main/install_from_github.sh | bash
```

## 📦 Instalación Manual

### 🚀 Instalación Automática (Recomendada)

#### Windows
1. Descarga todos los archivos del proyecto
2. **Ejecuta `install.bat` como administrador**
3. El instalador descargará e instalará Python automáticamente si es necesario
4. Sigue las instrucciones en pantalla
5. El sistema se ejecutará automáticamente al finalizar

#### Linux/macOS
1. Descarga todos los archivos del proyecto
2. Abre una terminal en el directorio del proyecto
3. Ejecuta: `./install.sh`
4. El instalador instalará Python automáticamente si es necesario
5. Sigue las instrucciones en pantalla

### 📦 Instalación Manual

#### Prerrequisitos
- Python 3.8 o superior
- pip (incluido con Python)

#### Pasos
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

### 🎯 Generación de Ejecutable (Windows)

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

## Uso

### Inicio Rápido

1. Ejecuta el programa
2. El sistema creará automáticamente la base de datos si no existe
3. Comienza agregando materiales en la sección "Materiales"
4. Crea productos en la sección "Productos"
5. Define recetas en la sección "Recetas"
6. Gestiona pedidos en la sección "Pedidos"

### Funcionalidades Principales

#### Dashboard
- Vista general del inventario
- Acceso rápido a funciones principales
- Estadísticas en tiempo real

#### Materiales
- Agregar, editar y eliminar materiales
- Control de stock y costos
- Información de proveedores
- Exportación a Excel

#### Productos
- Gestión de productos terminados
- Control de precios de venta
- Cálculo automático de costos de producción
- Exportación a Excel

#### Recetas
- Definición de recetas de producción
- Asociación de materiales con cantidades
- Cálculo automático de costos
- Producción de productos desde recetas

#### Pedidos
- Creación de pedidos de clientes
- Seguimiento de estado (Pendiente/Entregado)
- Cálculo automático de valores totales
- Exportación a Excel

#### Gráficas y Reportes
- Gráficas de stock de materiales
- Valor monetario de productos
- Costos de recetas
- Pedidos entregados
- Exportación completa a Excel con gráficas

## Estructura del Proyecto

```
src/
├── main.py                 # Punto de entrada principal
├── requirements.txt        # Dependencias del proyecto
├── requirements-dev.txt    # Dependencias para desarrollo
├── setup.py               # Configuración del instalador
├── pyproject.toml         # Configuración moderna de Python
├── README.md              # Documentación
├── install.bat            # Instalador Windows
├── install.sh             # Instalador Linux/macOS
├── install_from_github.bat # Instalador desde GitHub (Windows)
├── install_from_github.sh  # Instalador desde GitHub (Linux/macOS)
├── uninstall.bat          # Desinstalador Windows
├── uninstall.sh           # Desinstalador Linux/macOS
├── build_exe.py           # Generador de ejecutables
├── setup_github.py        # Configurador de repositorio GitHub
├── assets/                # Imágenes e iconos
├── crud/                  # Operaciones de base de datos
├── database/              # Configuración de base de datos
├── interfaces/            # Interfaz gráfica
├── models/                # Modelos de datos
├── services/              # Lógica de negocio
└── utils/                 # Utilidades
```

## Base de Datos

El sistema utiliza SQLite como base de datos local. Los archivos de base de datos se crean automáticamente:

- `inventory_system.db`: Base de datos principal
- `inventory.db`: Base de datos de respaldo (opcional)

### Tablas Principales

- **productos_terminados**: Productos finales
- **materiales**: Materias primas e insumos
- **recetas**: Definiciones de recetas
- **detalle_receta**: Materiales por receta
- **pedidos**: Órdenes de clientes
- **detalle_pedido**: Productos por pedido
- **balance_ventas**: Registro de ventas

## Personalización

### Colores y Estilo

El sistema utiliza una paleta de colores inspirada en Odoo. Puedes modificar los colores editando `interfaces/colors.py`.

### Configuración

- Los valores monetarios se muestran con formato de dólar ($)
- Las fechas usan formato YY-MM-DD
- Las exportaciones a Excel incluyen gráficas automáticamente

## Solución de Problemas

### Error de Dependencias

Si encuentras errores de dependencias faltantes:

```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Error de Base de Datos

Si hay problemas con la base de datos:

1. Cierra el programa
2. Elimina el archivo `inventory_system.db`
3. Reinicia el programa (se creará una nueva base de datos)

### Error de Gráficas

Si las gráficas no se muestran correctamente:

```bash
pip install matplotlib --upgrade
```

### Error de Instalación de Python

Si la instalación automática de Python falla:

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

## Desinstalación

### Windows
Ejecuta `uninstall.bat` como administrador

### Linux/macOS
Ejecuta `./uninstall.sh`

### Manual
```bash
pip uninstall sistema-inventario
```

## Distribución

### Para Usuarios Finales

1. **Instalación automática**: Usa los scripts `install.bat` o `install.sh`
2. **Instalación desde GitHub**: Usa `install_from_github.bat` o `install_from_github.sh`
3. **Ejecutable independiente**: Usa `build_exe.py` para crear un .exe
4. **Versión portable**: Copia la carpeta `SistemaInventario_Portable`

### Para Desarrolladores

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar tests
pytest

# Formatear código
black .

# Verificar tipos
mypy .
```

### Configurar Repositorio GitHub

```bash
# Configurar y subir a GitHub
python setup_github.py

# Crear release
./release.sh 1.0.0
```

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Soporte

Para soporte técnico o reportar bugs, por favor contacta:

- Email: soporte@ejemplo.com
- GitHub Issues: [Reportar un problema](https://github.com/Bronh14/sistema-inventario/issues)

## Changelog

### v1.0.0
- Lanzamiento inicial
- Gestión completa de inventario
- Interfaz gráfica moderna
- Exportación a Excel
- Gráficas y reportes
- **Instalación automática de Python**
- **Ejecutables independientes**
- **Versión portable**
- **Instalación desde GitHub** 
# Sistema de Inventario

Un sistema completo de gestión de inventario con interfaz gráfica desarrollado en Python usando Tkinter.

## 🚀 Instalación Rápida

### Windows
```bash
# Descargar e instalar automáticamente
curl -L https://raw.githubusercontent.com/Bronh14/sistema-inventario/main/installers/windows/instalar.bat -o instalar.bat
instalar.bat
```

### Linux/macOS
```bash
# Descargar e instalar automáticamente
curl -L https://raw.githubusercontent.com/Bronh14/sistema-inventario/main/installers/linux-macos/install.sh | bash
```

## 📚 Documentación

- **[Guía Completa](docs/README.md)** - Documentación completa del proyecto
- **[Instrucciones de Instalación](docs/INSTRUCCIONES_INSTALACION.md)** - Guía detallada de instalación
- **[Guía de Distribución](docs/COMO_DISTRIBUIR.md)** - Cómo distribuir el sistema

## 🛠️ Instaladores

### Windows
- `installers/windows/instalar.bat` - Instalador ultra simple (1KB)
- `installers/windows/instalar_sistema_inventario.bat` - Instalador completo
- `installers/windows/install.bat` - Instalador manual
- `installers/windows/install_from_github.bat` - Instalación desde GitHub
- `installers/windows/uninstall.bat` - Desinstalador

### Linux/macOS
- `installers/linux-macos/install.sh` - Instalador automático
- `installers/linux-macos/install_from_github.sh` - Instalación desde GitHub
- `installers/linux-macos/uninstall.sh` - Desinstalador

## 🎯 Características

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

## 🔧 Requisitos del Sistema

- **Windows 10/11**: Instalación automática de Python incluida
- **Linux**: Ubuntu 18.04+, CentOS 7+, Fedora 28+
- **macOS**: 10.14+ (Mojave o superior)
- **4GB RAM mínimo**
- **500MB espacio en disco**
- **Conexión a internet** (solo para la instalación inicial)

## 📦 Estructura del Proyecto

```
sistema-inventario/
├── main.py                 # Punto de entrada principal
├── requirements.txt        # Dependencias del proyecto
├── requirements-dev.txt    # Dependencias para desarrollo
├── setup.py               # Configuración del instalador
├── pyproject.toml         # Configuración moderna de Python
├── build_exe.py           # Generador de ejecutables
├── setup_github.py        # Configurador de repositorio GitHub
├── installers/            # Instaladores por sistema operativo
│   ├── windows/           # Instaladores para Windows
│   └── linux-macos/       # Instaladores para Linux/macOS
├── docs/                  # Documentación
├── assets/                # Imágenes e iconos
├── crud/                  # Operaciones de base de datos
├── database/              # Configuración de base de datos
├── interfaces/            # Interfaz gráfica
├── models/                # Modelos de datos
├── services/              # Lógica de negocio
└── utils/                 # Utilidades
```

## 🚀 Uso Rápido

1. Ejecuta el instalador correspondiente a tu sistema operativo
2. El sistema creará automáticamente la base de datos
3. Comienza agregando materiales en la sección "Materiales"
4. Crea productos en la sección "Productos"
5. Define recetas en la sección "Recetas"
6. Gestiona pedidos en la sección "Pedidos"

## 🔄 Actualizaciones

Para actualizar el sistema, simplemente ejecuta el instalador nuevamente. Se descargará automáticamente la versión más reciente sin perder tus datos.

## 🛠️ Desarrollo

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar tests
pytest

# Formatear código
black .

# Verificar tipos
mypy .

# Configurar repositorio GitHub
python setup_github.py
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Para soporte técnico o reportar bugs:

- Email: soporte@ejemplo.com
- GitHub Issues: [Reportar un problema](https://github.com/Bronh14/sistema-inventario/issues)

---

**⭐ Si este proyecto te es útil, ¡dale una estrella en GitHub!** 
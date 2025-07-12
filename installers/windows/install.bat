@echo off
setlocal enabledelayedexpansion

echo ========================================
echo    INSTALADOR SISTEMA DE INVENTARIO
echo ========================================
echo.

:: Verificar si Python está instalado
echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python no está instalado. Descargando e instalando Python...
    
    :: Crear directorio temporal
    if not exist "%TEMP%\python_install" mkdir "%TEMP%\python_install"
    cd /d "%TEMP%\python_install"
    
    :: Descargar Python 3.11 (versión estable)
    echo Descargando Python 3.11...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe' -OutFile 'python-installer.exe'}"
    
    if not exist "python-installer.exe" (
        echo ERROR: No se pudo descargar Python
        echo Por favor instala Python manualmente desde https://python.org
        pause
        exit /b 1
    )
    
    :: Instalar Python silenciosamente con PATH
    echo Instalando Python...
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    
    :: Esperar a que termine la instalación
    timeout /t 30 /nobreak >nul
    
    :: Limpiar archivos temporales
    cd /d "%~dp0"
    rmdir /s /q "%TEMP%\python_install"
    
    :: Refrescar variables de entorno
    call refreshenv >nul 2>&1
    
    :: Verificar instalación
    python --version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: La instalación de Python falló
        echo Por favor reinicia el sistema e intenta nuevamente
        pause
        exit /b 1
    )
    
    echo Python instalado exitosamente.
) else (
    echo Python encontrado.
)

:: Verificar versión de Python
echo Verificando versión de Python...
python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"
if errorlevel 1 (
    echo ERROR: Se requiere Python 3.8 o superior
    echo Versión actual:
    python --version
    pause
    exit /b 1
)

:: Verificar pip
echo Verificando pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo Instalando pip...
    python -m ensurepip --upgrade
)

echo.
echo Instalando dependencias...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Error al instalar dependencias
    echo Intentando con --user...
    python -m pip install -r requirements.txt --user
    if errorlevel 1 (
        echo ERROR: No se pudieron instalar las dependencias
        pause
        exit /b 1
    )
)

echo.
echo Instalando el sistema como paquete...
python -m pip install -e .

if errorlevel 1 (
    echo ERROR: Error al instalar el paquete
    echo Intentando con --user...
    python -m pip install -e . --user
    if errorlevel 1 (
        echo ERROR: No se pudo instalar el paquete
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo    INSTALACION COMPLETADA EXITOSAMENTE
echo ========================================
echo.
echo Para ejecutar el sistema:
echo   - Opcion 1: sistema-inventario
echo   - Opcion 2: python main.py
echo.

:: Crear acceso directo en el escritorio
echo Creando acceso directo en el escritorio...
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Sistema de Inventario.lnk'); $Shortcut.TargetPath = 'python'; $Shortcut.Arguments = 'main.py'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Save()}"

echo Acceso directo creado en el escritorio.
echo.
echo Presiona cualquier tecla para ejecutar el sistema ahora...
pause >nul

echo.
echo Iniciando Sistema de Inventario...
python main.py

pause 
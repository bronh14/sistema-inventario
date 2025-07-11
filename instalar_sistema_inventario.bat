@echo off
setlocal enabledelayedexpansion

:: Configuración del repositorio
set GITHUB_REPO=https://github.com/Bronh14/sistema-inventario.git
set GITHUB_RAW=https://raw.githubusercontent.com/Bronh14/sistema-inventario/main
set INSTALL_DIR=%USERPROFILE%\Desktop\SistemaInventario
set TEMP_DIR=%TEMP%\sistema_inventario_install

echo ========================================
echo    INSTALADOR SISTEMA DE INVENTARIO
echo    Descarga e Instalacion Automatica
echo ========================================
echo.

:: Crear directorio temporal
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"
cd /d "%TEMP_DIR%"

:: Verificar conexión a internet
echo Verificando conexion a internet...
ping -n 1 github.com >nul 2>&1
if errorlevel 1 (
    echo ERROR: No hay conexion a internet
    echo Por favor verifica tu conexion e intenta nuevamente
    pause
    exit /b 1
)

:: Verificar si Git está instalado
echo Verificando Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo Git no esta instalado. Descargando Git...
    
    :: Descargar Git
    echo Descargando Git...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.48.1.windows.1/Git-2.48.1-64-bit.exe' -OutFile 'git-installer.exe'}"
    
    if not exist "git-installer.exe" (
        echo ERROR: No se pudo descargar Git
        echo Descargando version alternativa...
        powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/latest/download/Git-2.48.1-64-bit.exe' -OutFile 'git-installer.exe'}"
        
        if not exist "git-installer.exe" (
            echo ERROR: No se pudo descargar Git
            echo Por favor instala Git manualmente desde https://git-scm.com
            pause
            exit /b 1
        )
    )
    
    :: Instalar Git silenciosamente
    echo Instalando Git...
    git-installer.exe /VERYSILENT /NORESTART /COMPONENTS="icons,ext\reg\shellhere,assoc,assoc_sh"
    
    :: Esperar a que termine la instalación
    timeout /t 30 /nobreak >nul
    
    :: Refrescar variables de entorno
    call refreshenv >nul 2>&1
    
    :: Verificar instalación
    git --version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: La instalacion de Git fallo
        echo Por favor reinicia el sistema e intenta nuevamente
        pause
        exit /b 1
    )
    
    echo Git instalado exitosamente.
) else (
    echo Git encontrado.
)

:: Verificar Python
echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python no esta instalado. Descargando Python...
    
    :: Descargar Python
    echo Descargando Python 3.11...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe' -OutFile 'python-installer.exe'}"
    
    if not exist "python-installer.exe" (
        echo ERROR: No se pudo descargar Python
        echo Descargando version alternativa...
        powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe' -OutFile 'python-installer.exe'}"
        
        if not exist "python-installer.exe" (
            echo ERROR: No se pudo descargar Python
            echo Por favor instala Python manualmente desde https://python.org
            pause
            exit /b 1
        )
    )
    
    :: Instalar Python silenciosamente con PATH
    echo Instalando Python...
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    
    :: Esperar a que termine la instalación
    timeout /t 45 /nobreak >nul
    
    :: Refrescar variables de entorno
    call refreshenv >nul 2>&1
    
    :: Verificar instalación
    python --version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: La instalacion de Python fallo
        echo Por favor reinicia el sistema e intenta nuevamente
        pause
        exit /b 1
    )
    
    echo Python instalado exitosamente.
) else (
    echo Python encontrado.
)

:: Verificar versión de Python
echo Verificando version de Python...
python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"
if errorlevel 1 (
    echo ERROR: Se requiere Python 3.8 o superior
    echo Version actual:
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
echo Descargando proyecto desde GitHub...

:: Crear directorio de instalación
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: Clonar o actualizar repositorio
if exist "%INSTALL_DIR%\.git" (
    echo El directorio ya existe. Actualizando...
    cd /d "%INSTALL_DIR%"
    git pull origin main
) else (
    echo Clonando repositorio...
    git clone %GITHUB_REPO% "%INSTALL_DIR%"
    cd /d "%INSTALL_DIR%"
)

if errorlevel 1 (
    echo ERROR: No se pudo descargar el proyecto
    echo Intentando metodo alternativo...
    
    :: Método alternativo: descargar archivos individuales
    echo Descargando archivos principales...
    powershell -Command "& {Invoke-WebRequest -Uri '%GITHUB_RAW%/main.py' -OutFile '%INSTALL_DIR%\main.py'}"
    powershell -Command "& {Invoke-WebRequest -Uri '%GITHUB_RAW%/requirements.txt' -OutFile '%INSTALL_DIR%\requirements.txt'}"
    powershell -Command "& {Invoke-WebRequest -Uri '%GITHUB_RAW%/install.bat' -OutFile '%INSTALL_DIR%\install.bat'}"
    
    if not exist "%INSTALL_DIR%\main.py" (
        echo ERROR: No se pudo descargar el proyecto
        echo Verifica tu conexion a internet y el nombre del repositorio
        pause
        exit /b 1
    )
    
    echo Archivos principales descargados.
    cd /d "%INSTALL_DIR%"
)

echo.
echo Proyecto descargado exitosamente en: %INSTALL_DIR%
echo.

:: Ejecutar instalador del proyecto
if exist "install.bat" (
    echo Ejecutando instalador del proyecto...
    call install.bat
) else (
    echo Instalador no encontrado. Instalando dependencias manualmente...
    
    echo Instalando dependencias...
    python -m pip install --upgrade pip
    python -m pip install pandas matplotlib Pillow xlsxwriter
    
    echo.
    echo ========================================
    echo    INSTALACION COMPLETADA
    echo ========================================
    echo.
    echo Para ejecutar el sistema:
    echo   python main.py
    echo.
    
    :: Crear acceso directo en el escritorio
    echo Creando acceso directo en el escritorio...
    powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Sistema de Inventario.lnk'); $Shortcut.TargetPath = 'python'; $Shortcut.Arguments = 'main.py'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Save()}"
    
    echo Acceso directo creado en el escritorio.
    echo.
    
    read /p "¿Deseas ejecutar el sistema ahora? (s/n): " -n 1 -r
    echo
    if /i "%REPLY%"=="S" (
        echo.
        echo Iniciando Sistema de Inventario...
        python main.py
    )
)

:: Limpiar archivos temporales
echo.
echo Limpiando archivos temporales...
cd /d "%~dp0"
rmdir /s /q "%TEMP_DIR%" 2>nul

echo.
echo ========================================
echo    INSTALACION DESDE GITHUB COMPLETADA
echo ========================================
echo.
echo El sistema se ha instalado desde GitHub.
echo Ubicacion: %INSTALL_DIR%
echo.
echo Caracteristicas instaladas:
echo - Python (si no estaba instalado)
echo - Git (si no estaba instalado)
echo - Todas las dependencias del proyecto
echo - Acceso directo en el escritorio
echo.
pause 
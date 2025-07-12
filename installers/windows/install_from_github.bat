@echo off
setlocal enabledelayedexpansion

echo ========================================
echo    INSTALADOR DESDE GITHUB
echo    Sistema de Inventario
echo ========================================
echo.

set GITHUB_REPO=https://github.com/Bronh14/sistema-inventario.git
set INSTALL_DIR=%USERPROFILE%\Desktop\SistemaInventario

echo Verificando Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo Git no está instalado. Descargando Git...
    
    :: Crear directorio temporal
    if not exist "%TEMP%\git_install" mkdir "%TEMP%\git_install"
    cd /d "%TEMP%\git_install"
    
    :: Descargar Git
    echo Descargando Git...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.48.1.windows.1/Git-2.48.1-64-bit.exe' -OutFile 'git-installer.exe'}"
    
    if not exist "git-installer.exe" (
        echo ERROR: No se pudo descargar Git
        echo Por favor instala Git manualmente desde https://git-scm.com
        pause
        exit /b 1
    )
    
    :: Instalar Git silenciosamente
    echo Instalando Git...
    git-installer.exe /VERYSILENT /NORESTART
    
    :: Esperar a que termine la instalación
    timeout /t 30 /nobreak >nul
    
    :: Limpiar archivos temporales
    cd /d "%~dp0"
    rmdir /s /q "%TEMP%\git_install"
    
    :: Refrescar variables de entorno
    call refreshenv >nul 2>&1
    
    :: Verificar instalación
    git --version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: La instalación de Git falló
        echo Por favor reinicia el sistema e intenta nuevamente
        pause
        exit /b 1
    )
    
    echo Git instalado exitosamente.
) else (
    echo Git encontrado.
)

echo.
echo Descargando proyecto desde GitHub...
if exist "%INSTALL_DIR%" (
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
    echo Verifica tu conexión a internet y el nombre del repositorio
    pause
    exit /b 1
)

echo.
echo Proyecto descargado exitosamente en: %INSTALL_DIR%
echo.
echo Ejecutando instalador...
cd /d "%INSTALL_DIR%"
call install.bat

echo.
echo ========================================
echo    INSTALACION DESDE GITHUB COMPLETADA
echo ========================================
echo.
echo El sistema se ha instalado desde GitHub.
echo Ubicación: %INSTALL_DIR%
echo.
pause 
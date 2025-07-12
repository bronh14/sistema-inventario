@echo off
setlocal enabledelayedexpansion

echo ========================================
echo    DESINSTALADOR SISTEMA DE INVENTARIO
echo ========================================
echo.

set INSTALL_DIR=%PROGRAMFILES%\SistemaInventario
set DESKTOP_SHORTCUT=%USERPROFILE%\Desktop\Sistema de Inventario.lnk
set START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs\SistemaInventario

echo ¿Estás seguro de que deseas desinstalar el Sistema de Inventario?
set /p confirm="Escribe 'SI' para confirmar: "

if /i not "%confirm%"=="SI" (
    echo Desinstalación cancelada.
    pause
    exit /b 0
)

echo.
echo Desinstalando paquete Python...
python -m pip uninstall sistema-inventario -y 2>nul

echo.
echo Eliminando acceso directo del escritorio...
if exist "%DESKTOP_SHORTCUT%" (
    del "%DESKTOP_SHORTCUT%"
    echo Acceso directo del escritorio eliminado.
)

echo.
echo Eliminando entrada del menú inicio...
if exist "%START_MENU%" (
    rmdir /s /q "%START_MENU%"
    echo Entrada del menú inicio eliminada.
)

echo.
echo Eliminando archivos de instalación...
if exist "%INSTALL_DIR%" (
    rmdir /s /q "%INSTALL_DIR%"
    echo Archivos de instalación eliminados.
)

echo.
echo Limpiando registro de Windows...
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\SistemaInventario" /f 2>nul
echo Registro de Windows limpiado.

echo.
echo Eliminando archivos de configuración...
if exist "%USERPROFILE%\.sistema_inventario" (
    rmdir /s /q "%USERPROFILE%\.sistema_inventario"
)

echo.
echo Eliminando base de datos local (si existe)...
if exist "inventory_system.db" (
    del "inventory_system.db"
    echo Base de datos local eliminada.
)
if exist "inventory.db" (
    del "inventory.db"
    echo Base de datos de respaldo eliminada.
)

echo.
echo ========================================
echo    DESINSTALACION COMPLETADA
echo ========================================
echo.
echo El Sistema de Inventario ha sido completamente desinstalado.
echo.
echo Archivos eliminados:
echo - Acceso directo del escritorio
echo - Entrada del menú inicio
echo - Archivos de instalación
echo - Registro de Windows
echo - Configuraciones locales
echo.
pause 
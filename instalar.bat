@echo off
echo ========================================
echo    INSTALADOR SISTEMA DE INVENTARIO
echo    Descarga e Instalacion Automatica
echo ========================================
echo.

:: Descargar el instalador completo desde GitHub
echo Descargando instalador completo...
powershell -Command "& {Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/Bronh14/sistema-inventario/main/instalar_sistema_inventario.bat' -OutFile '%TEMP%\instalar_completo.bat'}"

if exist "%TEMP%\instalar_completo.bat" (
    echo Instalador descargado. Ejecutando...
    call "%TEMP%\instalar_completo.bat"
) else (
    echo ERROR: No se pudo descargar el instalador
    echo Verifica tu conexion a internet
    pause
) 
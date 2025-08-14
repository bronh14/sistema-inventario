@echo off
echo ========================================
echo   Activando Entorno Virtual
echo ========================================
echo.

REM Verificar si el entorno virtual existe
if not exist "venv\Scripts\activate.bat" (
    echo Error: El entorno virtual no existe.
    echo Ejecuta: python -m venv venv
    pause
    exit /b 1
)

REM Activar el entorno virtual
call venv\Scripts\activate.bat

echo.
echo ✅ Entorno virtual activado correctamente!
echo.
echo Para ejecutar la aplicación:
echo   python main.py
echo.
echo Para instalar nuevas dependencias:
echo   pip install nombre_paquete
echo.
echo Para desactivar el entorno virtual:
echo   deactivate
echo.

REM Mantener la ventana abierta
cmd /k 
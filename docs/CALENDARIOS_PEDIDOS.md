# Calendarios Desplegables en Pedidos

## Descripción

El sistema de pedidos ahora incluye calendarios desplegables para seleccionar la fecha de entrega de manera más intuitiva y fácil.

## Características

- **Calendario visual**: Selecciona fechas haciendo clic en el calendario desplegable
- **Formato consistente**: Las fechas se guardan en formato YYYY-MM-DD
- **Campo opcional**: La fecha de entrega es opcional, se puede dejar vacía
- **Compatibilidad**: Si `tkcalendar` no está disponible, se usa un campo de texto normal

## Instalación

### Requisito: tkcalendar

Para usar los calendarios desplegables, necesitas instalar la librería `tkcalendar`:

```bash
pip install tkcalendar>=1.6.1
```

### Instalación automática

Ejecuta el script de instalación incluido:

```bash
python install_tkcalendar.py
```

## Uso

### En formularios de pedidos

1. **Crear pedido**: Al crear un nuevo pedido, verás un campo "Fecha de Entrega" con un ícono de calendario
2. **Hacer clic**: Haz clic en el campo para abrir el calendario desplegable
3. **Seleccionar fecha**: Navega por los meses y selecciona la fecha deseada
4. **Confirmar**: La fecha seleccionada aparecerá en el campo

### En edición de pedidos

1. **Editar pedido**: Al editar un pedido existente, el campo mostrará la fecha actual
2. **Cambiar fecha**: Haz clic para abrir el calendario y seleccionar una nueva fecha
3. **Guardar**: Los cambios se guardan al hacer clic en "Guardar Cambios"

## Fallback

Si `tkcalendar` no está instalado, el sistema automáticamente usa un campo de texto normal donde puedes escribir la fecha manualmente en formato YYYY-MM-DD.

## Solución de problemas

### Error: "No module named 'tkcalendar'"

Ejecuta:
```bash
pip install tkcalendar>=1.6.1
```

### El calendario no se abre

1. Verifica que `tkcalendar` esté instalado correctamente
2. Reinicia la aplicación
3. Si persiste el problema, usa el campo de texto manual

### Fecha no se guarda correctamente

1. Asegúrate de que la fecha esté en formato YYYY-MM-DD
2. Verifica que la fecha sea válida
3. Revisa los logs de la aplicación para más detalles

## Compatibilidad

- **Windows**: ✅ Compatible
- **macOS**: ✅ Compatible  
- **Linux**: ✅ Compatible

## Notas técnicas

- El calendario usa el locale español cuando está disponible
- Las fechas se validan antes de guardar
- El formato de fecha es consistente en toda la aplicación 
# TODO - Implementación Cotizaciones con Datos de Receta

## Objetivo
Actualizar cotizaciones para que:
1. Mantenga: nombre, telefono, cantidad, seleccionar receta
2. Calcule total automático: cantidad * precio_venta de la receta
3. Muestre todos los datos de la receta al cliente

## Tareas

### 1. Backend - Modificar API de cotizaciones
- [x] Editar `app/main.py` - Endpoint GET /cotizaciones para incluir datos de la receta

### 2. Frontend - Actualizar Cotizaciones.jsx
- [x] Quitar input manual de total
- [x] Agregar cálculo automático: total = cantidad * precio_venta
- [x] Mostrar datos de receta en la tabla (nombre, precio unitario, costo producción)
- [x] Ajustar formulario para calcular total al seleccionar receta y cantidad
- [x] Agregar toggle para ver ingredientes de la receta

## Archivos editados
1. app/main.py - Modificado GET /cotizaciones
2. ../frontend/src/pages/Cotizaciones.jsx - Formulario y tabla actualizados
3. ../frontend/src/index.css - Estilos para expand-btn, details-row, ingredientes-list

## Estado: COMPLETADO ✅

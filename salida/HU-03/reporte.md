# Reporte · HU-03

**Estado:** LISTA
**Costo de agentes:** 1.03 USD
**Ciclos de corrección:** 0

## Bitácora
- Filtro de historia: OK
- Criterios escritos en criterios.feature
- Preguntas abiertas: la persona respondió 'si'
- Casos de prueba escritos en casos_prueba.json
- Plan rechazado: No modifiques el comportamiento de HU-01 y HU-02: POST /api/empleados, GET /api/empleados (buscar, departamento), el formulario de alta y los data-testid del directorio quedan iguales. Nunca debe haber dos elementos visibles con el mismo data-testid: al pulsar editar-empleado-{id}, el formulario de alta existente pasa a modo edición con los datos del empleado (correo deshabilitado) y se guarda con el mismo botón empleado-guardar; no crees un segundo formulario con los mismos data-testid. Oculta baja-empleado-{id} si el empleado ya está de baja.
- Plan aprobado por una persona
- Construcción 1
- Verificación: OK
- Pruebas automatizadas: OK (12 casos)
- Despliegue: OK
- Despliegue y pruebas listos
- Pruebas E2E: 19 passed, 3 skipped, 1 warning in 1.75s

## Última ejecución de pruebas
```
19 passed, 3 skipped, 1 warning in 1.75s

```
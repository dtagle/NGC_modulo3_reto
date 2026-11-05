# Notas · Sesión 3 · HU-02 Consultar el directorio de empleados

## Ejecución de la fábrica (`python -m flujos.flujo_s3 historias/HU-02-consultar-directorio.md`)

- **Preguntas abiertas:** el analista dejó 4 (texto exacto de «sin resultados», si búsqueda y filtro se combinan, orden y paginación). Respondí `si`.
- **Plan rechazado una vez** con este comentario: «Indica explícitamente que extiendes el código de HU-01 sin romperlo: no cambies POST /api/empleados ni el formulario de alta. Los data-testid por fila deben seguir CLAUDE.md al pie de la letra: `fila-empleado-{id}`, `numero-empleado-{id}` y `estado-empleado-{id}` usando el id numérico del empleado (no `numero_empleado`). Búsqueda y filtro deben poder combinarse.»
- **El segundo plan sí lo incorporó:** agregó una sección «No tocar (HU-01)» y cambió los `data-testid` al id numérico. Lo aprobé.
- **Bitácora final:** Construcción 1 → Verificación: OK → Pruebas automatizadas: OK (10 casos) y Despliegue: OK, en paralelo → «app LISTA» · 1.15 USD.

## `docker compose ps`

```text
NAME             IMAGE          COMMAND                  SERVICE    STATUS                   PORTS
app-backend-1    app-backend    "uvicorn main:app --…"   backend    Up 7 minutes (healthy)   0.0.0.0:8000->8000/tcp
app-frontend-1   app-frontend   "/docker-entrypoint.…"   frontend   Up 7 minutes             0.0.0.0:8080->80/tcp
```

El backend está *healthy* (healthcheck a `/api/salud`) y el frontend *running*; http://localhost:8080 muestra el directorio.

## `python -m pytest tests -q`

**Primera ejecución, justo después del flujo: 4 de 5 pruebas de API fallaron**, y las E2E también. El flujo dijo «OK» porque `verificar_pruebas_escritas` solo comprueba que las pruebas se recolectan y que cada caso tiene un test, no que pasen. Causas, todas del automatizador y no de la app:

| Fallo | Causa | Corrección (al agente, no al resultado) |
| --- | --- | --- |
| Búsqueda devolvía todos los empleados | El test usaba `?busqueda=` y la API expone `?buscar=` | Documenté los parámetros de `GET /api/empleados` en `contexto/convenciones_app.md` |
| E2E no encontraba `fila-empleado-EMP-0020` | Copió los casos en vez de `CLAUDE.md`, que usa el `{id}` numérico | Aclaré en las convenciones que `{id}` es el id numérico, y agregué al automatizador la regla «si un caso contradice CLAUDE.md, gana CLAUDE.md» |
| Estado «baja» no se veía | `tests/apoyo_baja.py` escribía directo en SQLite y la escritura se perdía con el volumen de Docker | Regla nueva: solo API pública y navegador; si falta una precondición, `pytest.skip("motivo")` |

Borré las pruebas generadas y volví a correr `python -m agentes.automatizador HU-02`: **8 passed, 2 skipped**. Las dos omitidas necesitaban un empleado de baja, y esa operación todavía no existía.

Resultado actual, con HU-02 y HU-03 juntas después del Lab 4:

```text
21 passed, 1 skipped, 1 warning in 1.58s
```

La omitida es CP-07 de HU-03 en E2E (un departamento inválido no se puede elegir en un `<select>`); ese caso se cubre por API.

**Comparación con la tabla manual de `notas_s2.md`:** no hay `notas_s2.md` en `salida/HU-01/`, así que no se pudo comparar. Queda pendiente.

## Intento fuera de rol (`python buscar_denegados.py`)

```text
desarrollador  Write     /tmp/run_build.py
               su rol solo permite: backend/*, frontend/*
```

El desarrollador intentó escribir un script auxiliar en `/tmp` para correr `npm run build`, en una ejecución anterior en la que no encontraba `npm` en su `PATH`. Lo detuvo el hook de rol `confinar_escritura`: la ruta queda fuera de `app/` y su lista `ESCRITURA` solo permite `backend/*` y `frontend/*`. En esta ejecución de HU-02 ningún agente intentó escribir fuera de su rol.

Llamadas registradas en `auditoria.jsonl` (acumulado): desarrollador 130, automatizador 79, desarrollador-plan 48, despliegue 32.

## Para pensar al cierre

- **Arquitectura:** es un flujo LangGraph con un orquestador central. Las aristas en código deciden el siguiente paso (`despues_de_verificar`); la persona decide solo en `aprobar_plan` y en las preguntas abiertas.
- **Por qué hay paralelo:** el automatizador solo necesita los casos y el código, y el despliegue solo necesita el código. Ninguno depende de lo que produce el otro. El desarrollador va antes porque los dos dependen de su código.
- **Lección:** «Pruebas automatizadas: OK» no significaba que las pruebas pasaran. Las verificaciones deterministas solo prueban lo que miden.

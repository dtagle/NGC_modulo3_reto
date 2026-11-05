"""Pruebas de API para HU-02: ver el directorio de empleados, buscar y filtrar."""

import uuid
from datetime import date

import httpx


def _crear_empleado(url_api: str, nombre: str, correo: str, puesto: str, departamento: str) -> dict:
    respuesta = httpx.post(
        f"{url_api}/api/empleados",
        json={
            "nombre": nombre,
            "correo": correo,
            "puesto": puesto,
            "departamento": departamento,
            "fecha_ingreso": str(date.today()),
        },
    )
    assert respuesta.status_code == 201, respuesta.text
    return respuesta.json()


def _dar_de_baja(url_api: str, empleado_id: int, fecha_baja: str) -> dict:
    respuesta = httpx.put(
        f"{url_api}/api/empleados/{empleado_id}/baja", json={"fecha_baja": fecha_baja}
    )
    assert respuesta.status_code == 200, respuesta.text
    return respuesta.json()


def test_cp_01_directorio_completo_con_empleado_activo_y_baja(url_api: str) -> None:
    """CP-01: ver el directorio completo con un empleado activo y uno en baja."""
    sufijo = uuid.uuid4().hex[:8]
    activo = _crear_empleado(
        url_api, f"Ana Pérez {sufijo}", f"ana.perez.{sufijo}@empresa.com", "Analista", "Tecnología"
    )
    de_baja = _crear_empleado(
        url_api, f"Luis Gómez {sufijo}", f"luis.gomez.{sufijo}@empresa.com", "Vendedor", "Ventas"
    )
    _dar_de_baja(url_api, de_baja["id"], de_baja["fecha_ingreso"])

    respuesta = httpx.get(f"{url_api}/api/empleados", params={"buscar": sufijo})

    assert respuesta.status_code == 200
    resultados = respuesta.json()
    assert len(resultados) == 2
    por_id = {empleado["id"]: empleado for empleado in resultados}
    assert por_id[activo["id"]]["nombre"] == f"Ana Pérez {sufijo}"
    assert por_id[activo["id"]]["puesto"] == "Analista"
    assert por_id[activo["id"]]["departamento"] == "Tecnología"
    assert por_id[activo["id"]]["estado"] == "activo"
    assert por_id[de_baja["id"]]["nombre"] == f"Luis Gómez {sufijo}"
    assert por_id[de_baja["id"]]["puesto"] == "Vendedor"
    assert por_id[de_baja["id"]]["departamento"] == "Ventas"
    assert por_id[de_baja["id"]]["estado"] == "baja"


def test_cp_03_buscar_por_nombre_sin_distinguir_mayusculas(url_api: str) -> None:
    """CP-03: buscar por nombre sin distinguir mayúsculas de minúsculas."""
    sufijo = uuid.uuid4().hex[:8]
    nombre = f"Ana Pérez {sufijo}"
    correo = f"ana.perez.{sufijo}@empresa.com"
    creado = _crear_empleado(url_api, nombre, correo, "Analista", "Tecnología")

    respuesta = httpx.get(f"{url_api}/api/empleados", params={"buscar": nombre.upper()})

    assert respuesta.status_code == 200
    resultados = respuesta.json()
    assert len(resultados) == 1
    assert resultados[0]["id"] == creado["id"]
    assert resultados[0]["numero_empleado"] == creado["numero_empleado"]
    assert resultados[0]["nombre"] == nombre
    assert resultados[0]["puesto"] == "Analista"
    assert resultados[0]["departamento"] == "Tecnología"
    assert resultados[0]["estado"] == "activo"


def test_cp_05_buscar_por_correo_sin_distinguir_mayusculas(url_api: str) -> None:
    """CP-05: buscar por correo sin distinguir mayúsculas de minúsculas."""
    sufijo = uuid.uuid4().hex[:8]
    nombre = f"Marta Ruiz {sufijo}"
    correo = f"marta.ruiz.{sufijo}@empresa.com"
    creado = _crear_empleado(url_api, nombre, correo, "Vendedor", "Ventas")

    respuesta = httpx.get(f"{url_api}/api/empleados", params={"buscar": correo.upper()})

    assert respuesta.status_code == 200
    resultados = respuesta.json()
    assert len(resultados) == 1
    assert resultados[0]["id"] == creado["id"]
    assert resultados[0]["numero_empleado"] == creado["numero_empleado"]
    assert resultados[0]["correo"] == correo


def test_cp_07_filtrar_directorio_por_departamento(url_api: str) -> None:
    """CP-07: filtrar el directorio por departamento."""
    sufijo = uuid.uuid4().hex[:8]
    tecnologia_1 = _crear_empleado(
        url_api, f"Ana Pérez {sufijo}", f"ana.perez.{sufijo}@empresa.com", "Analista", "Tecnología"
    )
    tecnologia_2 = _crear_empleado(
        url_api, f"Pedro Ortiz {sufijo}", f"pedro.ortiz.{sufijo}@empresa.com", "Analista", "Tecnología"
    )
    ventas = _crear_empleado(
        url_api, f"Luis Gómez {sufijo}", f"luis.gomez.{sufijo}@empresa.com", "Vendedor", "Ventas"
    )

    respuesta = httpx.get(f"{url_api}/api/empleados", params={"departamento": "Tecnología"})

    assert respuesta.status_code == 200
    resultados = respuesta.json()
    ids_resultado = {empleado["id"] for empleado in resultados}
    assert tecnologia_1["id"] in ids_resultado
    assert tecnologia_2["id"] in ids_resultado
    assert ventas["id"] not in ids_resultado
    assert all(empleado["departamento"] == "Tecnología" for empleado in resultados)


def test_cp_09_busqueda_sin_coincidencias(url_api: str) -> None:
    """CP-09: una búsqueda sin coincidencias devuelve un arreglo vacío."""
    sufijo = uuid.uuid4().hex[:8]
    _crear_empleado(
        url_api, f"Ana Pérez {sufijo}", f"ana.perez.{sufijo}@empresa.com", "Analista", "Tecnología"
    )
    texto_busqueda_sin_coincidencias = f"Carlos Sánchez {uuid.uuid4().hex}"

    respuesta = httpx.get(f"{url_api}/api/empleados", params={"buscar": texto_busqueda_sin_coincidencias})

    assert respuesta.status_code == 200
    assert respuesta.json() == []

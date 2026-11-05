"""Pruebas de API para HU-03: editar empleados y darlos de baja."""

import uuid
from datetime import date

import httpx


def _crear_empleado(
    url_api: str,
    nombre: str,
    correo: str,
    puesto: str,
    departamento: str,
    fecha_ingreso: str,
) -> dict:
    respuesta = httpx.post(
        f"{url_api}/api/empleados",
        json={
            "nombre": nombre,
            "correo": correo,
            "puesto": puesto,
            "departamento": departamento,
            "fecha_ingreso": fecha_ingreso,
        },
    )
    assert respuesta.status_code == 201, respuesta.text
    return respuesta.json()


def test_cp_01_editar_puesto_y_departamento_de_empleado_activo(url_api: str) -> None:
    """CP-01: editar puesto y departamento de un empleado activo."""
    sufijo = uuid.uuid4().hex[:8]
    creado = _crear_empleado(
        url_api,
        f"Laura Pérez {sufijo}",
        f"laura.perez.{sufijo}@empresa.com",
        "Analista",
        "Finanzas",
        str(date.today()),
    )

    respuesta = httpx.put(
        f"{url_api}/api/empleados/{creado['id']}",
        json={"puesto": "Analista Senior", "departamento": "Tecnología"},
    )

    assert respuesta.status_code == 200, respuesta.text
    cuerpo = respuesta.json()
    assert cuerpo["puesto"] == "Analista Senior"
    assert cuerpo["departamento"] == "Tecnología"


def test_cp_03_numero_empleado_y_correo_no_se_modifican_al_editar(url_api: str) -> None:
    """CP-03: el número de empleado y el correo no se modifican aunque se envíen en la edición."""
    sufijo = uuid.uuid4().hex[:8]
    correo_original = f"laura.perez.{sufijo}@empresa.com"
    creado = _crear_empleado(
        url_api,
        f"Laura Pérez {sufijo}",
        correo_original,
        "Analista",
        "Finanzas",
        str(date.today()),
    )

    respuesta = httpx.put(
        f"{url_api}/api/empleados/{creado['id']}",
        json={"numero_empleado": "EMP-9999", "correo": "otro@empresa.com"},
    )

    assert respuesta.status_code == 200, respuesta.text
    cuerpo = respuesta.json()
    assert cuerpo["numero_empleado"] == creado["numero_empleado"]
    assert cuerpo["correo"] == correo_original


def test_cp_04_error_al_editar_con_puesto_demasiado_corto(url_api: str) -> None:
    """CP-04: error al editar con un puesto demasiado corto."""
    sufijo = uuid.uuid4().hex[:8]
    creado = _crear_empleado(
        url_api,
        f"Laura Pérez {sufijo}",
        f"laura.perez.{sufijo}@empresa.com",
        "Analista",
        "Finanzas",
        str(date.today()),
    )

    respuesta = httpx.put(f"{url_api}/api/empleados/{creado['id']}", json={"puesto": "A"})

    assert respuesta.status_code == 422, respuesta.text
    assert "puesto" in respuesta.json()["detail"]


def test_cp_06_error_al_editar_con_departamento_no_permitido(url_api: str) -> None:
    """CP-06: error al editar con un departamento no permitido."""
    sufijo = uuid.uuid4().hex[:8]
    creado = _crear_empleado(
        url_api,
        f"Laura Pérez {sufijo}",
        f"laura.perez.{sufijo}@empresa.com",
        "Analista",
        "Finanzas",
        str(date.today()),
    )

    respuesta = httpx.put(
        f"{url_api}/api/empleados/{creado['id']}", json={"departamento": "Marketing"}
    )

    assert respuesta.status_code == 422, respuesta.text
    assert "departamento" in respuesta.json()["detail"]


def test_cp_08_error_al_editar_a_un_empleado_dado_de_baja(url_api: str) -> None:
    """CP-08: error al intentar editar a un empleado dado de baja."""
    sufijo = uuid.uuid4().hex[:8]
    creado = _crear_empleado(
        url_api,
        f"Carlos Ruiz {sufijo}",
        f"carlos.ruiz.{sufijo}@empresa.com",
        "Analista",
        "Finanzas",
        str(date.today()),
    )
    respuesta_baja = httpx.put(
        f"{url_api}/api/empleados/{creado['id']}/baja", json={"fecha_baja": str(date.today())}
    )
    assert respuesta_baja.status_code == 200, respuesta_baja.text

    respuesta = httpx.put(
        f"{url_api}/api/empleados/{creado['id']}", json={"puesto": "Gerente"}
    )

    assert respuesta.status_code == 409, respuesta.text
    assert respuesta.json()["detail"] == "No se puede editar a un empleado dado de baja"


def test_cp_09_dar_de_baja_a_un_empleado_activo(url_api: str) -> None:
    """CP-09: dar de baja a un empleado activo."""
    sufijo = uuid.uuid4().hex[:8]
    correo = f"laura.perez.{sufijo}@empresa.com"
    creado = _crear_empleado(
        url_api,
        f"Laura Pérez {sufijo}",
        correo,
        "Analista",
        "Finanzas",
        "2022-03-01",
    )

    respuesta = httpx.put(
        f"{url_api}/api/empleados/{creado['id']}/baja", json={"fecha_baja": "2024-06-15"}
    )

    assert respuesta.status_code == 200, respuesta.text
    cuerpo = respuesta.json()
    assert cuerpo["estado"] == "baja"
    assert cuerpo["fecha_baja"] == "2024-06-15"

    respuesta_directorio = httpx.get(f"{url_api}/api/empleados", params={"buscar": correo})
    assert respuesta_directorio.status_code == 200
    ids_resultado = {empleado["id"] for empleado in respuesta_directorio.json()}
    assert creado["id"] in ids_resultado


def test_cp_11_error_al_dar_de_baja_con_fecha_anterior_a_ingreso(url_api: str) -> None:
    """CP-11: error al dar de baja con una fecha de baja anterior a la fecha de ingreso."""
    sufijo = uuid.uuid4().hex[:8]
    creado = _crear_empleado(
        url_api,
        f"Marcos Díaz {sufijo}",
        f"marcos.diaz.{sufijo}@empresa.com",
        "Analista",
        "Finanzas",
        "2023-01-10",
    )

    respuesta = httpx.put(
        f"{url_api}/api/empleados/{creado['id']}/baja", json={"fecha_baja": "2022-12-01"}
    )

    assert respuesta.status_code == 422, respuesta.text
    assert "fecha de baja" in respuesta.json()["detail"].lower()

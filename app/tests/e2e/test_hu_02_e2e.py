"""Pruebas E2E para HU-02: ver el directorio de empleados, buscar y filtrar."""

import uuid
from datetime import date

import httpx
from playwright.sync_api import Page, expect


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


def test_cp_02_directorio_completo_con_empleado_activo_y_baja(page: Page, url_web: str, url_api: str) -> None:
    """CP-02: ver el directorio completo con un empleado activo y uno en baja."""
    sufijo = uuid.uuid4().hex[:8]
    activo = _crear_empleado(
        url_api, f"Ana Pérez {sufijo}", f"ana.perez.{sufijo}@empresa.com", "Analista", "Tecnología"
    )
    de_baja = _crear_empleado(
        url_api, f"Luis Gómez {sufijo}", f"luis.gomez.{sufijo}@empresa.com", "Vendedor", "Ventas"
    )
    _dar_de_baja(url_api, de_baja["id"], de_baja["fecha_ingreso"])

    page.goto(url_web)

    fila_activo = page.get_by_test_id(f"fila-empleado-{activo['id']}")
    expect(fila_activo).to_be_visible()
    expect(page.get_by_test_id(f"numero-empleado-{activo['id']}")).to_have_text(
        activo["numero_empleado"]
    )
    expect(page.get_by_test_id(f"estado-empleado-{activo['id']}")).to_have_text("Activo")

    fila_baja = page.get_by_test_id(f"fila-empleado-{de_baja['id']}")
    expect(fila_baja).to_be_visible()
    expect(page.get_by_test_id(f"numero-empleado-{de_baja['id']}")).to_have_text(
        de_baja["numero_empleado"]
    )
    expect(page.get_by_test_id(f"estado-empleado-{de_baja['id']}")).to_have_text("Baja")


def test_cp_04_buscar_por_nombre_sin_distinguir_mayusculas(page: Page, url_web: str, url_api: str) -> None:
    """CP-04: buscar por nombre sin distinguir mayúsculas de minúsculas."""
    sufijo = uuid.uuid4().hex[:8]
    nombre = f"Ana Pérez {sufijo}"
    correo = f"ana.perez.{sufijo}@empresa.com"
    creado = _crear_empleado(url_api, nombre, correo, "Analista", "Tecnología")

    page.goto(url_web)
    page.get_by_test_id("buscar-empleados").fill(nombre.upper())

    filas = page.locator('[data-testid="tabla-empleados"] tbody tr')
    expect(filas).to_have_count(1)
    expect(page.get_by_test_id(f"fila-empleado-{creado['id']}")).to_be_visible()


def test_cp_06_buscar_por_correo_sin_distinguir_mayusculas(page: Page, url_web: str, url_api: str) -> None:
    """CP-06: buscar por correo sin distinguir mayúsculas de minúsculas."""
    sufijo = uuid.uuid4().hex[:8]
    nombre = f"Marta Ruiz {sufijo}"
    correo = f"marta.ruiz.{sufijo}@empresa.com"
    creado = _crear_empleado(url_api, nombre, correo, "Vendedor", "Ventas")

    page.goto(url_web)
    page.get_by_test_id("buscar-empleados").fill(correo.upper())

    filas = page.locator('[data-testid="tabla-empleados"] tbody tr')
    expect(filas).to_have_count(1)
    expect(page.get_by_test_id(f"fila-empleado-{creado['id']}")).to_be_visible()


def test_cp_08_filtrar_directorio_por_departamento(page: Page, url_web: str, url_api: str) -> None:
    """CP-08: filtrar el directorio por departamento."""
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

    page.goto(url_web)
    page.get_by_test_id("filtro-departamento").select_option("Tecnología")

    expect(page.get_by_test_id(f"fila-empleado-{tecnologia_1['id']}")).to_be_visible()
    expect(page.get_by_test_id(f"fila-empleado-{tecnologia_2['id']}")).to_be_visible()
    expect(page.get_by_test_id(f"fila-empleado-{ventas['id']}")).not_to_be_visible()


def test_cp_10_busqueda_sin_coincidencias(page: Page, url_web: str, url_api: str) -> None:
    """CP-10: una búsqueda sin coincidencias muestra el mensaje de sin resultados."""
    sufijo = uuid.uuid4().hex[:8]
    _crear_empleado(
        url_api, f"Ana Pérez {sufijo}", f"ana.perez.{sufijo}@empresa.com", "Analista", "Tecnología"
    )
    texto_busqueda_sin_coincidencias = f"Carlos Sánchez {uuid.uuid4().hex}"

    page.goto(url_web)
    page.get_by_test_id("buscar-empleados").fill(texto_busqueda_sin_coincidencias)

    sin_resultados = page.get_by_test_id("sin-resultados")
    expect(sin_resultados).to_be_visible()
    expect(sin_resultados).to_have_text("No se encontraron empleados con ese criterio de búsqueda")
    filas = page.locator('[data-testid="tabla-empleados"] tbody tr')
    expect(filas).to_have_count(0)

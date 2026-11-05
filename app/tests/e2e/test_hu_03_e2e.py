"""Pruebas E2E para HU-03: editar empleados y darlos de baja."""

import uuid
from datetime import date

import httpx
import pytest
from playwright.sync_api import Page, expect


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


def test_cp_02_editar_puesto_y_departamento_de_empleado_activo(
    page: Page, url_web: str, url_api: str
) -> None:
    """CP-02: editar puesto y departamento de un empleado activo."""
    sufijo = uuid.uuid4().hex[:8]
    creado = _crear_empleado(
        url_api,
        f"Laura Pérez {sufijo}",
        f"laura.perez.{sufijo}@empresa.com",
        "Analista",
        "Finanzas",
        str(date.today()),
    )

    page.goto(url_web)
    fila = page.get_by_test_id(f"fila-empleado-{creado['id']}")
    expect(fila).to_be_visible()
    page.get_by_test_id(f"editar-empleado-{creado['id']}").click()
    page.get_by_test_id("empleado-puesto").fill("Analista Senior")
    page.get_by_test_id("empleado-departamento").select_option("Tecnología")
    page.get_by_test_id("empleado-guardar").click()

    expect(page.get_by_test_id("mensaje-exito")).to_be_visible()
    expect(fila).to_contain_text("Analista Senior")
    expect(fila).to_contain_text("Tecnología")


def test_cp_05_error_al_editar_con_puesto_demasiado_corto(
    page: Page, url_web: str, url_api: str
) -> None:
    """CP-05: error al editar con un puesto demasiado corto."""
    sufijo = uuid.uuid4().hex[:8]
    creado = _crear_empleado(
        url_api,
        f"Laura Pérez {sufijo}",
        f"laura.perez.{sufijo}@empresa.com",
        "Analista",
        "Finanzas",
        str(date.today()),
    )

    page.goto(url_web)
    page.get_by_test_id(f"editar-empleado-{creado['id']}").click()
    page.get_by_test_id("empleado-puesto").fill("A")
    page.get_by_test_id("empleado-guardar").click()

    mensaje_error = page.get_by_test_id("mensaje-error")
    expect(mensaje_error).to_be_visible()
    expect(mensaje_error).to_contain_text("puesto")


def test_cp_07_error_al_editar_con_departamento_no_permitido(
    page: Page, url_web: str, url_api: str
) -> None:
    """CP-07: error al editar con un departamento no permitido."""
    pytest.skip(
        "data-testid='empleado-departamento' es un <select> "
        "(frontend/src/components/FormularioEmpleado.jsx) cuyas únicas opciones "
        "son los departamentos de CLAUDE.md/DEPARTAMENTOS_VALIDOS; no ofrece "
        "'Marketing' como opción, así que no se puede seleccionar ni escribir ese "
        "valor desde la UI. Este caso solo es verificable a nivel API (ver CP-06)."
    )


def test_cp_10_dar_de_baja_a_un_empleado_activo(page: Page, url_web: str, url_api: str) -> None:
    """CP-10: dar de baja a un empleado activo."""
    sufijo = uuid.uuid4().hex[:8]
    creado = _crear_empleado(
        url_api,
        f"Laura Pérez {sufijo}",
        f"laura.perez.{sufijo}@empresa.com",
        "Analista",
        "Finanzas",
        "2022-03-01",
    )

    page.goto(url_web)
    fila = page.get_by_test_id(f"fila-empleado-{creado['id']}")
    expect(fila).to_be_visible()
    page.get_by_test_id(f"baja-empleado-{creado['id']}").click()
    page.get_by_test_id("empleado-fecha-baja").fill("2024-06-15")
    page.get_by_test_id("confirmar-baja").click()

    expect(page.get_by_test_id("mensaje-exito")).to_be_visible()
    expect(page.get_by_test_id(f"estado-empleado-{creado['id']}")).to_have_text("Baja")
    expect(page.get_by_test_id(f"fila-empleado-{creado['id']}")).to_be_visible()


def test_cp_12_error_al_dar_de_baja_con_fecha_anterior_a_ingreso(
    page: Page, url_web: str, url_api: str
) -> None:
    """CP-12: error al dar de baja con una fecha de baja anterior a la fecha de ingreso."""
    sufijo = uuid.uuid4().hex[:8]
    creado = _crear_empleado(
        url_api,
        f"Marcos Díaz {sufijo}",
        f"marcos.diaz.{sufijo}@empresa.com",
        "Analista",
        "Finanzas",
        "2023-01-10",
    )

    page.goto(url_web)
    page.get_by_test_id(f"baja-empleado-{creado['id']}").click()
    page.get_by_test_id("empleado-fecha-baja").fill("2022-12-01")
    page.get_by_test_id("confirmar-baja").click()

    mensaje_error = page.get_by_test_id("mensaje-error")
    expect(mensaje_error).to_be_visible()
    expect(mensaje_error).to_contain_text("fecha de baja")

"""API de gestión de empleados."""

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import func, select
from sqlalchemy.orm import Session

import modelos
from database import Base, engine, obtener_db
from esquemas import (
    DEPARTAMENTOS_VALIDOS,
    EmpleadoActualizar,
    EmpleadoBaja,
    EmpleadoCrear,
    EmpleadoSalida,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gestión de empleados")


@app.exception_handler(RequestValidationError)
async def manejar_error_validacion(request: Request, exc: RequestValidationError) -> JSONResponse:
    primer_error = exc.errors()[0]
    mensaje = primer_error["msg"]
    prefijo = "Value error, "
    if mensaje.startswith(prefijo):
        mensaje = mensaje[len(prefijo):]
    else:
        campo = primer_error["loc"][-1] if primer_error["loc"] else "datos"
        mensaje = f"El campo {campo} debe corregirse"
    return JSONResponse(status_code=422, content={"detail": mensaje})


@app.get("/api/salud")
def salud() -> dict[str, str]:
    return {"estado": "ok"}


@app.get("/api/departamentos")
def departamentos() -> list[str]:
    return DEPARTAMENTOS_VALIDOS


@app.post("/api/empleados", response_model=EmpleadoSalida, status_code=201)
def crear_empleado(datos: EmpleadoCrear, db: Session = Depends(obtener_db)) -> modelos.Empleado:
    ya_existe = db.scalar(
        select(modelos.Empleado).where(func.lower(modelos.Empleado.correo) == datos.correo)
    )
    if ya_existe is not None:
        raise HTTPException(status_code=409, detail="El correo ya está registrado")

    total_empleados = db.scalar(select(func.count(modelos.Empleado.id))) or 0
    numero_empleado = f"EMP-{total_empleados + 1:04d}"

    empleado = modelos.Empleado(
        numero_empleado=numero_empleado,
        nombre=datos.nombre,
        correo=datos.correo,
        puesto=datos.puesto,
        departamento=datos.departamento,
        fecha_ingreso=datos.fecha_ingreso,
        estado="activo",
    )
    db.add(empleado)
    db.commit()
    db.refresh(empleado)
    return empleado


@app.get("/api/empleados", response_model=list[EmpleadoSalida])
def listar_empleados(
    buscar: str | None = None,
    departamento: str | None = None,
    db: Session = Depends(obtener_db),
) -> list[modelos.Empleado]:
    consulta = select(modelos.Empleado)
    if buscar:
        texto = f"%{buscar.strip().lower()}%"
        consulta = consulta.where(
            func.lower(modelos.Empleado.nombre).like(texto)
            | func.lower(modelos.Empleado.correo).like(texto)
        )
    if departamento:
        consulta = consulta.where(modelos.Empleado.departamento == departamento)
    return list(db.scalars(consulta).all())


@app.get("/api/empleados/{empleado_id}", response_model=EmpleadoSalida)
def obtener_empleado(empleado_id: int, db: Session = Depends(obtener_db)) -> modelos.Empleado:
    empleado = db.get(modelos.Empleado, empleado_id)
    if empleado is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado


@app.put("/api/empleados/{empleado_id}", response_model=EmpleadoSalida)
def actualizar_empleado(
    empleado_id: int, datos: EmpleadoActualizar, db: Session = Depends(obtener_db)
) -> modelos.Empleado:
    empleado = db.get(modelos.Empleado, empleado_id)
    if empleado is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    if empleado.estado == "baja":
        raise HTTPException(
            status_code=409, detail="No se puede editar a un empleado dado de baja"
        )

    if datos.puesto is not None:
        empleado.puesto = datos.puesto
    if datos.departamento is not None:
        empleado.departamento = datos.departamento

    db.commit()
    db.refresh(empleado)
    return empleado


@app.put("/api/empleados/{empleado_id}/baja", response_model=EmpleadoSalida)
def dar_de_baja_empleado(
    empleado_id: int, datos: EmpleadoBaja, db: Session = Depends(obtener_db)
) -> modelos.Empleado:
    empleado = db.get(modelos.Empleado, empleado_id)
    if empleado is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    if datos.fecha_baja < empleado.fecha_ingreso:
        raise HTTPException(
            status_code=422,
            detail="La fecha de baja no puede ser anterior a la fecha de ingreso",
        )

    empleado.estado = "baja"
    empleado.fecha_baja = datos.fecha_baja

    db.commit()
    db.refresh(empleado)
    return empleado

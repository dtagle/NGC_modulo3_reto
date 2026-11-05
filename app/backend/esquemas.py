"""Esquemas Pydantic de la app de empleados."""

from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator

DEPARTAMENTOS_VALIDOS = [
    "Tecnología",
    "Ventas",
    "Finanzas",
    "Recursos Humanos",
    "Operaciones",
]


class EmpleadoCrear(BaseModel):
    nombre: str = Field(min_length=2, max_length=80)
    correo: str = Field(min_length=1)
    puesto: str = Field(min_length=2, max_length=60)
    departamento: str
    fecha_ingreso: date

    @field_validator("correo")
    @classmethod
    def validar_dominio_corporativo(cls, valor: str) -> str:
        correo = valor.strip().lower()
        if not correo.endswith("@empresa.com"):
            raise ValueError("Usa el correo corporativo @empresa.com")
        return correo

    @field_validator("departamento")
    @classmethod
    def validar_departamento(cls, valor: str) -> str:
        if valor not in DEPARTAMENTOS_VALIDOS:
            raise ValueError("El campo departamento debe corregirse")
        return valor

    @field_validator("fecha_ingreso")
    @classmethod
    def validar_fecha_no_futura(cls, valor: date) -> date:
        if valor > date.today():
            raise ValueError("La fecha de ingreso no puede ser futura")
        return valor


class EmpleadoActualizar(BaseModel):
    puesto: str | None = Field(default=None, min_length=2, max_length=60)
    departamento: str | None = None

    @field_validator("departamento")
    @classmethod
    def validar_departamento(cls, valor: str | None) -> str | None:
        if valor is not None and valor not in DEPARTAMENTOS_VALIDOS:
            raise ValueError("El campo departamento debe corregirse")
        return valor


class EmpleadoBaja(BaseModel):
    fecha_baja: date


class EmpleadoSalida(BaseModel):
    id: int
    numero_empleado: str
    nombre: str
    correo: str
    puesto: str
    departamento: str
    fecha_ingreso: date
    estado: str
    fecha_baja: date | None
    creado_en: datetime

    model_config = {"from_attributes": True}

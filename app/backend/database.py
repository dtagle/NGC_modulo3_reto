"""Configuración de la base de datos SQLite para la app de empleados."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

CARPETA_DATOS = os.path.join(os.path.dirname(__file__), "datos")
os.makedirs(CARPETA_DATOS, exist_ok=True)

RUTA_BD = os.path.join(CARPETA_DATOS, "empleados.db")
URL_BD = f"sqlite:///{RUTA_BD}"

engine = create_engine(URL_BD, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def obtener_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

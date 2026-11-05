import { useEffect, useState } from "react";
import { actualizarEmpleado, crearEmpleado, obtenerDepartamentos } from "../api/empleados.js";

const DATOS_INICIALES = {
  nombre: "",
  correo: "",
  puesto: "",
  departamento: "",
  fecha_ingreso: "",
};

export default function FormularioEmpleado({ empleadoEnEdicion, onTerminarEdicion, onGuardado }) {
  const [datos, setDatos] = useState(DATOS_INICIALES);
  const [departamentos, setDepartamentos] = useState([]);
  const [mensajeExito, setMensajeExito] = useState("");
  const [mensajeError, setMensajeError] = useState("");

  const editando = Boolean(empleadoEnEdicion);

  useEffect(() => {
    obtenerDepartamentos()
      .then(setDepartamentos)
      .catch(() => setDepartamentos([]));
  }, []);

  useEffect(() => {
    if (empleadoEnEdicion) {
      setDatos({
        nombre: empleadoEnEdicion.nombre,
        correo: empleadoEnEdicion.correo,
        puesto: empleadoEnEdicion.puesto,
        departamento: empleadoEnEdicion.departamento,
        fecha_ingreso: empleadoEnEdicion.fecha_ingreso,
      });
      setMensajeExito("");
      setMensajeError("");
    } else {
      setDatos(DATOS_INICIALES);
    }
  }, [empleadoEnEdicion]);

  function actualizarCampo(campo, valor) {
    setDatos((anteriores) => ({ ...anteriores, [campo]: valor }));
  }

  async function manejarGuardar(evento) {
    evento.preventDefault();
    setMensajeExito("");
    setMensajeError("");
    try {
      if (editando) {
        await actualizarEmpleado(empleadoEnEdicion.id, {
          puesto: datos.puesto,
          departamento: datos.departamento,
        });
        setMensajeExito("Empleado actualizado con éxito");
        onGuardado?.();
        onTerminarEdicion?.();
      } else {
        const empleado = await crearEmpleado(datos);
        setMensajeExito(`Empleado ${empleado.numero_empleado} registrado con éxito`);
        setDatos(DATOS_INICIALES);
        onGuardado?.();
      }
    } catch (error) {
      setMensajeError(error.message);
    }
  }

  function manejarCancelar() {
    onTerminarEdicion?.();
    setMensajeExito("");
    setMensajeError("");
  }

  return (
    <form onSubmit={manejarGuardar}>
      <h1>{editando ? "Editar empleado" : "Registrar empleado"}</h1>

      <label htmlFor="nombre">Nombre</label>
      <input
        id="nombre"
        data-testid="empleado-nombre"
        type="text"
        value={datos.nombre}
        disabled={editando}
        onChange={(e) => actualizarCampo("nombre", e.target.value)}
      />

      <label htmlFor="correo">Correo</label>
      <input
        id="correo"
        data-testid="empleado-correo"
        type="text"
        value={datos.correo}
        disabled={editando}
        onChange={(e) => actualizarCampo("correo", e.target.value)}
      />

      <label htmlFor="puesto">Puesto</label>
      <input
        id="puesto"
        data-testid="empleado-puesto"
        type="text"
        value={datos.puesto}
        onChange={(e) => actualizarCampo("puesto", e.target.value)}
      />

      <label htmlFor="departamento">Departamento</label>
      <select
        id="departamento"
        data-testid="empleado-departamento"
        value={datos.departamento}
        onChange={(e) => actualizarCampo("departamento", e.target.value)}
      >
        <option value="">Selecciona un departamento</option>
        {departamentos.map((departamento) => (
          <option key={departamento} value={departamento}>
            {departamento}
          </option>
        ))}
      </select>

      <label htmlFor="fecha_ingreso">Fecha de ingreso</label>
      <input
        id="fecha_ingreso"
        data-testid="empleado-fecha-ingreso"
        type="date"
        value={datos.fecha_ingreso}
        disabled={editando}
        onChange={(e) => actualizarCampo("fecha_ingreso", e.target.value)}
      />

      <button type="submit" data-testid="empleado-guardar">
        Guardar
      </button>

      {editando && (
        <button type="button" onClick={manejarCancelar}>
          Cancelar
        </button>
      )}

      {mensajeExito && <p data-testid="mensaje-exito">{mensajeExito}</p>}
      {mensajeError && <p data-testid="mensaje-error">{mensajeError}</p>}
    </form>
  );
}

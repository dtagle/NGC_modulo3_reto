import { useEffect, useState } from "react";
import { darDeBajaEmpleado, obtenerDepartamentos, obtenerEmpleados } from "../api/empleados.js";

function capitalizar(texto) {
  return texto.charAt(0).toUpperCase() + texto.slice(1);
}

export default function DirectorioEmpleados({ version, onEditar, onCambio }) {
  const [empleados, setEmpleados] = useState([]);
  const [departamentos, setDepartamentos] = useState([]);
  const [buscar, setBuscar] = useState("");
  const [departamento, setDepartamento] = useState("");
  const [error, setError] = useState("");
  const [cargado, setCargado] = useState(false);
  const [empleadoEnBaja, setEmpleadoEnBaja] = useState(null);
  const [fechaBaja, setFechaBaja] = useState("");
  const [mensajeExitoAccion, setMensajeExitoAccion] = useState("");
  const [mensajeErrorAccion, setMensajeErrorAccion] = useState("");

  useEffect(() => {
    obtenerDepartamentos()
      .then(setDepartamentos)
      .catch(() => setDepartamentos([]));
  }, []);

  useEffect(() => {
    obtenerEmpleados({ buscar, departamento })
      .then((resultado) => {
        setEmpleados(resultado);
        setError("");
        setCargado(true);
      })
      .catch((err) => setError(err.message));
  }, [buscar, departamento, version]);

  function iniciarBaja(id) {
    setEmpleadoEnBaja(id);
    setFechaBaja("");
    setMensajeExitoAccion("");
    setMensajeErrorAccion("");
  }

  function cancelarBaja() {
    setEmpleadoEnBaja(null);
    setFechaBaja("");
  }

  async function confirmarBaja() {
    setMensajeExitoAccion("");
    setMensajeErrorAccion("");
    try {
      await darDeBajaEmpleado(empleadoEnBaja, fechaBaja);
      setMensajeExitoAccion("Empleado dado de baja con éxito");
      setEmpleadoEnBaja(null);
      setFechaBaja("");
      onCambio?.();
    } catch (err) {
      setMensajeErrorAccion(err.message);
    }
  }

  return (
    <section>
      <h1>Directorio de empleados</h1>

      <input
        data-testid="buscar-empleados"
        type="text"
        placeholder="Buscar por nombre o correo"
        value={buscar}
        onChange={(e) => setBuscar(e.target.value)}
      />

      <select
        data-testid="filtro-departamento"
        value={departamento}
        onChange={(e) => setDepartamento(e.target.value)}
      >
        <option value="">Todos los departamentos</option>
        {departamentos.map((d) => (
          <option key={d} value={d}>
            {d}
          </option>
        ))}
      </select>

      {error && <p data-testid="mensaje-error">{error}</p>}
      {mensajeExitoAccion && <p data-testid="mensaje-exito">{mensajeExitoAccion}</p>}
      {mensajeErrorAccion && <p data-testid="mensaje-error">{mensajeErrorAccion}</p>}

      {cargado && empleados.length === 0 && (
        <p data-testid="sin-resultados">
          No se encontraron empleados con ese criterio de búsqueda
        </p>
      )}

      <table data-testid="tabla-empleados">
        <thead>
          <tr>
            <th>Número</th>
            <th>Nombre</th>
            <th>Puesto</th>
            <th>Departamento</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {empleados.map((empleado) => (
            <tr key={empleado.id} data-testid={`fila-empleado-${empleado.id}`}>
              <td data-testid={`numero-empleado-${empleado.id}`}>{empleado.numero_empleado}</td>
              <td>{empleado.nombre}</td>
              <td>{empleado.puesto}</td>
              <td>{empleado.departamento}</td>
              <td data-testid={`estado-empleado-${empleado.id}`}>
                {capitalizar(empleado.estado)}
              </td>
              <td>
                <button
                  type="button"
                  data-testid={`editar-empleado-${empleado.id}`}
                  onClick={() => onEditar?.(empleado)}
                >
                  Editar
                </button>
                {empleado.estado !== "baja" && (
                  <button
                    type="button"
                    data-testid={`baja-empleado-${empleado.id}`}
                    onClick={() => iniciarBaja(empleado.id)}
                  >
                    Dar de baja
                  </button>
                )}
                {empleadoEnBaja === empleado.id && (
                  <div>
                    <label htmlFor="empleado-fecha-baja">Fecha de baja</label>
                    <input
                      id="empleado-fecha-baja"
                      data-testid="empleado-fecha-baja"
                      type="date"
                      value={fechaBaja}
                      onChange={(e) => setFechaBaja(e.target.value)}
                    />
                    <button type="button" data-testid="confirmar-baja" onClick={confirmarBaja}>
                      Confirmar baja
                    </button>
                    <button type="button" onClick={cancelarBaja}>
                      Cancelar
                    </button>
                  </div>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}

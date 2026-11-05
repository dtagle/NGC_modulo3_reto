export async function crearEmpleado(datos) {
  const respuesta = await fetch("/api/empleados", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
  });
  const cuerpo = await respuesta.json();
  if (!respuesta.ok) {
    throw new Error(cuerpo.detail || "Ocurrió un error al registrar al empleado");
  }
  return cuerpo;
}

export async function actualizarEmpleado(id, datos) {
  const respuesta = await fetch(`/api/empleados/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
  });
  const cuerpo = await respuesta.json();
  if (!respuesta.ok) {
    throw new Error(cuerpo.detail || "Ocurrió un error al editar al empleado");
  }
  return cuerpo;
}

export async function darDeBajaEmpleado(id, fecha_baja) {
  const respuesta = await fetch(`/api/empleados/${id}/baja`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ fecha_baja }),
  });
  const cuerpo = await respuesta.json();
  if (!respuesta.ok) {
    throw new Error(cuerpo.detail || "Ocurrió un error al dar de baja al empleado");
  }
  return cuerpo;
}

export async function obtenerEmpleados({ buscar, departamento } = {}) {
  const parametros = new URLSearchParams();
  if (buscar) parametros.set("buscar", buscar);
  if (departamento) parametros.set("departamento", departamento);
  const query = parametros.toString();
  const respuesta = await fetch(`/api/empleados${query ? `?${query}` : ""}`);
  if (!respuesta.ok) {
    throw new Error("No se pudo cargar el directorio de empleados");
  }
  return respuesta.json();
}

export async function obtenerDepartamentos() {
  const respuesta = await fetch("/api/departamentos");
  if (!respuesta.ok) {
    throw new Error("No se pudieron cargar los departamentos");
  }
  return respuesta.json();
}

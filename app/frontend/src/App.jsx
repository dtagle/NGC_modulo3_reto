import { useState } from "react";
import DirectorioEmpleados from "./components/DirectorioEmpleados.jsx";
import FormularioEmpleado from "./components/FormularioEmpleado.jsx";

export default function App() {
  const [empleadoEnEdicion, setEmpleadoEnEdicion] = useState(null);
  const [version, setVersion] = useState(0);

  function refrescarDirectorio() {
    setVersion((anterior) => anterior + 1);
  }

  return (
    <main>
      <FormularioEmpleado
        empleadoEnEdicion={empleadoEnEdicion}
        onTerminarEdicion={() => setEmpleadoEnEdicion(null)}
        onGuardado={refrescarDirectorio}
      />
      <DirectorioEmpleados
        version={version}
        onEditar={setEmpleadoEnEdicion}
        onCambio={refrescarDirectorio}
      />
    </main>
  );
}

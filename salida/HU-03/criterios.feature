# language: es

Característica: Editar y dar de baja a un empleado
  Como persona del área de Recursos Humanos
  quiero cambiar el puesto y el departamento de un empleado, y poder darlo de baja
  para mantener el directorio al día sin perder el historial

  Escenario: Editar puesto y departamento de un empleado activo
    Dado que existe el empleado "EMP-0015" con puesto "Analista", departamento "Finanzas" y estado "activo"
    Cuando edito al empleado "EMP-0015" con puesto "Analista Senior" y departamento "Tecnología"
    Entonces el sistema responde 200
    Y el empleado "EMP-0015" muestra puesto "Analista Senior" y departamento "Tecnología"

  Escenario: El número de empleado y el correo no se modifican aunque se envíen en la edición
    Dado que existe el empleado "EMP-0015" con numero_empleado "EMP-0015" y correo "laura.perez@empresa.com"
    Cuando edito al empleado "EMP-0015" enviando numero_empleado "EMP-9999" y correo "otro@empresa.com"
    Entonces el sistema responde 200
    Y el empleado "EMP-0015" conserva numero_empleado "EMP-0015" y correo "laura.perez@empresa.com"

  Escenario: Error al editar con un puesto demasiado corto
    Dado que existe el empleado "EMP-0015" con estado "activo"
    Cuando edito al empleado "EMP-0015" con puesto "A"
    Entonces el sistema responde 422
    Y el mensaje indica que corrija el campo "puesto"

  Escenario: Error al editar con un departamento no permitido
    Dado que existe el empleado "EMP-0015" con estado "activo"
    Cuando edito al empleado "EMP-0015" con departamento "Marketing"
    Entonces el sistema responde 422
    Y el mensaje indica que corrija el campo "departamento"

  Escenario: Error al intentar editar a un empleado dado de baja
    Dado que existe el empleado "EMP-0020" con estado "baja"
    Cuando edito al empleado "EMP-0020" con puesto "Gerente"
    Entonces el sistema responde 409
    Y el mensaje es "No se puede editar a un empleado dado de baja"

  Escenario: Dar de baja a un empleado activo
    Dado que existe el empleado "EMP-0015" con estado "activo" y fecha_ingreso "2022-03-01"
    Cuando doy de baja al empleado "EMP-0015" con fecha_baja "2024-06-15"
    Entonces el sistema responde 200
    Y el empleado "EMP-0015" tiene estado "baja" y fecha_baja "2024-06-15"
    Y el empleado "EMP-0015" sigue apareciendo en el directorio

  Escenario: Error al dar de baja con una fecha de baja anterior a la fecha de ingreso
    Dado que existe el empleado "EMP-0021" con estado "activo" y fecha_ingreso "2023-01-10"
    Cuando doy de baja al empleado "EMP-0021" con fecha_baja "2022-12-01"
    Entonces el sistema responde 422
    Y el mensaje indica que corrija el campo "fecha_baja"

# Preguntas abiertas
# - No se especifica el texto exacto del mensaje de error cuando la fecha de baja es anterior
#   a la fecha de ingreso; la regla 3 solo indica que debe señalar el campo a corregir.
# - No se define si al editar se debe rechazar la petición (422/400) cuando se envían
#   numero_empleado o correo, o si el sistema simplemente los ignora y conserva el valor original;
#   se asumió esta última opción.
# - No se especifica qué ocurre si se intenta dar de baja a un empleado que ya está en estado "baja".

# language: es
Característica: Registrar empleado
  Como persona del área de Recursos Humanos
  quiero registrar a un empleado con su nombre, correo corporativo, puesto, departamento y fecha de ingreso
  para darlo de alta en la empresa

  Escenario: Registro exitoso de un empleado con datos válidos
    Dado que no existe ningún empleado con correo "ana.martinez@empresa.com"
    Y que el último número de empleado asignado es "EMP-0003"
    Cuando registro un empleado con nombre "Ana Martínez", correo "Ana.Martinez@empresa.com", puesto "Desarrolladora", departamento "Tecnología" y fecha de ingreso "2024-01-15"
    Entonces el sistema responde con código 201
    Y el empleado queda registrado con correo "ana.martinez@empresa.com" en minúsculas
    Y el empleado queda registrado con número de empleado "EMP-0004"
    Y el empleado queda registrado con estado "activo"
    Y la pantalla muestra el mensaje de confirmación "Empleado EMP-0004 registrado con éxito"

  Escenario: Intento de registro con correo ya existente (sin importar mayúsculas)
    Dado que ya existe un empleado con correo "carlos.ruiz@empresa.com"
    Cuando registro un empleado con nombre "Carlos Ruiz", correo "Carlos.Ruiz@EMPRESA.com", puesto "Analista", departamento "Finanzas" y fecha de ingreso "2024-02-01"
    Entonces el sistema responde con código 409
    Y la pantalla muestra el mensaje "El correo ya está registrado"
    Y no se crea ningún empleado nuevo

  Escenario: Intento de registro con correo que no es corporativo
    Dado que no existe ningún empleado con correo "laura.gomez@gmail.com"
    Cuando registro un empleado con nombre "Laura Gómez", correo "laura.gomez@gmail.com", puesto "Contadora", departamento "Finanzas" y fecha de ingreso "2024-03-10"
    Entonces el sistema responde con código 422
    Y la pantalla muestra el mensaje "Usa el correo corporativo @empresa.com"
    Y no se crea ningún empleado nuevo

  Escenario: Intento de registro con fecha de ingreso futura
    Dado que la fecha actual es "2024-06-01"
    Cuando registro un empleado con nombre "Mario Torres", correo "mario.torres@empresa.com", puesto "Supervisor", departamento "Operaciones" y fecha de ingreso "2024-12-25"
    Entonces el sistema responde con código 422
    Y la pantalla muestra el mensaje "La fecha de ingreso no puede ser futura"
    Y no se crea ningún empleado nuevo

  Esquema del escenario: Intento de registro con otros datos inválidos
    Dado que no existe ningún empleado con correo "<correo>"
    Cuando registro un empleado con nombre "<nombre>", correo "<correo>", puesto "<puesto>", departamento "<departamento>" y fecha de ingreso "<fecha_ingreso>"
    Entonces el sistema responde con código 422
    Y la pantalla indica que el campo "<campo_invalido>" debe corregirse
    Y no se crea ningún empleado nuevo

    Ejemplos:
      | nombre | correo                  | puesto       | departamento    | fecha_ingreso | campo_invalido |
      | A      | nombre.valido@empresa.com | Analista   | Tecnología      | 2024-01-01    | nombre         |
      | Nombre con más de ochenta caracteres que sobrepasa claramente el límite permitido para este campo de prueba | otro.valido@empresa.com | Analista | Tecnología | 2024-01-01 | nombre |
      | Pedro López | pedro.lopez@empresa.com | A           | Tecnología      | 2024-01-01    | puesto         |
      | Sofía Díaz  | sofia.diaz@empresa.com  | Diseñadora  | Marketing       | 2024-01-01    | departamento   |

  # Preguntas abiertas
  # - Las reglas de negocio indican que, ante datos inválidos (regla 3), "la pantalla muestra qué campo corregir",
  #   pero no se especifica el texto exacto del mensaje para cada campo (nombre, puesto, departamento).
  #   Se usó una redacción genérica de ejemplo; falta confirmar el mensaje exacto esperado por campo.

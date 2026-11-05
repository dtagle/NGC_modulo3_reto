# language: es
Característica: Consultar el directorio de empleados
  Como persona del área de Recursos Humanos
  Quiero ver el directorio de empleados, buscarlos por nombre o correo y filtrarlos por departamento
  Para encontrar rápido a una persona

  Escenario: Camino feliz - ver el directorio completo con sus datos
    Dado que el directorio tiene registrados a los siguientes empleados:
      | numero_empleado | nombre      | puesto    | departamento | estado |
      | EMP-0001        | Ana Pérez   | Analista  | Tecnología   | activo |
      | EMP-0002        | Luis Gómez  | Vendedor  | Ventas       | baja   |
    Cuando abro el directorio de empleados
    Entonces veo 2 empleados en la lista
    Y veo que el empleado "EMP-0001" tiene nombre "Ana Pérez", puesto "Analista", departamento "Tecnología" y estado "activo"
    Y veo que el empleado "EMP-0002" tiene nombre "Luis Gómez", puesto "Vendedor", departamento "Ventas" y estado "baja"

  Escenario: Buscar por nombre sin distinguir mayúsculas de minúsculas
    Dado que el directorio tiene registrado al empleado "EMP-0001" con nombre "Ana Pérez" y correo "ana.perez@empresa.com"
    Cuando busco "ANA PÉREZ" en el directorio
    Entonces veo 1 resultado
    Y el resultado corresponde al empleado "EMP-0001"

  Escenario: Buscar por correo sin distinguir mayúsculas de minúsculas
    Dado que el directorio tiene registrado al empleado "EMP-0003" con nombre "Marta Ruiz" y correo "marta.ruiz@empresa.com"
    Cuando busco "MARTA.RUIZ@EMPRESA.COM" en el directorio
    Entonces veo 1 resultado
    Y el resultado corresponde al empleado "EMP-0003"

  Escenario: Filtrar el directorio por departamento
    Dado que el directorio tiene registrados a los siguientes empleados:
      | numero_empleado | nombre       | departamento |
      | EMP-0001        | Ana Pérez    | Tecnología   |
      | EMP-0002        | Luis Gómez   | Ventas       |
      | EMP-0004        | Pedro Ortiz  | Tecnología   |
    Cuando filtro el directorio por el departamento "Tecnología"
    Entonces veo 2 resultados
    Y los resultados son los empleados "EMP-0001" y "EMP-0004"

  Escenario: Error - búsqueda sin coincidencias muestra mensaje de resultados vacíos
    Dado que el directorio tiene registrado al empleado "EMP-0001" con nombre "Ana Pérez" y correo "ana.perez@empresa.com"
    Cuando busco "Carlos Sánchez" en el directorio
    Entonces veo el mensaje "No se encontraron empleados con ese criterio de búsqueda"
    Y la lista de resultados está vacía

# Preguntas abiertas
# - No se especifica el texto exacto del mensaje para "sin resultados"; se usó un texto razonable como suposición.
# - No se especifica si la búsqueda combina nombre y correo en un solo campo o si son campos separados.
# - No se especifica si el filtro por departamento se puede combinar con la búsqueda por nombre/correo al mismo tiempo.
# - No se especifica el orden en que se listan los empleados (alfabético, por número de empleado, etc.) ni si hay paginación.

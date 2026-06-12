# 📐 Diseño y Especificaciones del Proyecto (AGENDA_PAOLA)

Este documento sirve como cuaderno de diseño. Antes de escribir código, debemos definir con precisión cómo funcionará el sistema a nivel de base de datos, reglas de negocio y diseño de pantallas.

---

## 🧠 Metodología: ¿Por qué seguimos este orden de desarrollo?

En la ingeniería de software profesional, el orden de los pasos no es aleatorio; busca minimizar el retrabajo, garantizar la seguridad y asegurar la estabilidad. Aquí te explico por qué avanzamos en esta secuencia:

### 1. ¿Por qué primero diseñamos la Base de Datos (Tablas y Relaciones)?
* **La base de datos es el cimiento de la casa:** En una aplicación, todo gira en torno a los datos. Si empiezas a construir pantallas (el frontend) o lógica en el servidor sin saber exactamente qué datos vas a almacenar, vas a tener que rehacer las pantallas una y otra vez cada vez que descubras que te faltó un campo o que una relación estaba mal diseñada.
* **El diseño conceptual previene errores caros:** Es infinitamente más rápido y barato cambiar un borrador o un diagrama en un papel o un archivo `.md` que tener que reestructurar tablas reales con miles de registros de pacientes reales más adelante.

### 2. ¿Por qué luego configuramos el Entorno y la Conexión?
* **Asegurar la viabilidad técnica:** Antes de escribir lógica compleja, debemos certificar que nuestra aplicación local puede "hablar" con la nube (en este caso, Supabase). Resolver problemas de credenciales, red y compatibilidad al inicio nos evita dolores de cabeza cuando ya tenemos código complejo corriendo.

### 3. ¿Por qué el siguiente paso es programar los Modelos y configurar los Roles en Django Admin?
* **Validación rápida sin costo de frontend:** Django viene con un panel de administración integrado y funcional. Al crear los modelos y configurar los permisos allí inmediatamente después de conectar la base de datos, podemos **probar las reglas de negocio reales** (por ejemplo: *"¿Puede un alumno ver las citas de otro?"*) usando una interfaz real sin haber gastado ni un solo minuto diseñando HTML o CSS para un frontend a medida.

### 4. ¿Por qué diseñamos el Dashboard antes de la API y el Móvil?
* **Alineación de datos analíticos:** Para poder mostrarle estadísticas al profesor, primero debemos asegurarnos de que la base de datos ya está capturando los datos necesarios y que podemos hacer consultas de agregación (por ejemplo, promedios o conteos) de forma eficiente. Si dejamos esto para el final, podríamos darnos cuenta tarde de que nos falta información clave para los reportes.

### 5. ¿Por qué la API y el Frontend Móvil a medida se hacen al final?
* **El frontend es solo una "ventana":** Una aplicación móvil o un frontend personalizado es una interfaz visual que simplemente "pide" datos al backend y los muestra de forma bonita. Si el backend (el motor y los datos) no está completamente listo, seguro y estable, construir el frontend es como pintar las paredes de una casa que aún no tiene tuberías ni electricidad. Al hacerlo al final, garantizamos que el frontend se conecte a un sistema sólido y ya probado.

---

## 🗄️ 1. Modelo de Datos (Esquema de Base de Datos - Opción B Elegida)

Hemos optado por la **Opción B**, que separa la información en dos tablas vinculadas. Esto nos permite un control profesional del historial de consultas sin duplicar ni comprometer datos.

### Esquema de Tablas Diseñado:

#### A. Tabla: `Usuario` (Custom User Model - Extendido de Django)
Esta tabla representa a los usuarios del sistema. Al heredar de `AbstractUser` en Django, heredamos la seguridad, encriptación y gestión nativas, agregando campos propios.
* **`id`** (Entero, Clave Primaria, Autoincremental): Identificador único interno.
* **`username`** (Texto/Varchar de 150 caracteres, Único): Nombre de usuario para iniciar sesión.
* **`email`** (Texto/Varchar de 254 caracteres, Único, NOT NULL): Correo electrónico académico. Es el método de login principal.
* **`password`** (Texto largo encriptado): Contraseña segura gestionada por Django.
* **`rol`** (Texto/Varchar de 20 caracteres, Enum): Rol en la plataforma. Opciones: `ESTUDIANTE` (acceso limitado a sus datos) o `PROFESOR` (acceso docente global).
* **`user_ci`** (Texto/Varchar de 20 caracteres, Único, **Opcional/Nullable**): Cédula de identidad del usuario. Campo opcional al registrarse. Sirve como **método de login alternativo** en caso de que el usuario olvide su correo electrónico. PostgreSQL permite múltiples `NULL` en columnas `UNIQUE`, por lo que usuarios sin cédula registrada no colisionan entre sí.
* **`first_name`** y **`last_name`** (Texto/Varchar de 150 caracteres): Nombre y apellido. Campos nativos de Django.
* **`is_active`** (Booleano, Default: `TRUE`): Para activar o suspender la cuenta del alumno/docente.
* **`is_staff`** (Booleano, Default: `FALSE`): Determina si tiene acceso a la consola del Django Admin.
* **`date_joined`** (Fecha/Hora, AUTO): Momento de registro del usuario. Lo llena Django automáticamente.

#### B. Tabla: `Paciente` (Información del Paciente Anónimo)
Esta tabla representa a la persona. No contiene nombres ni identificaciones reales, solo un código clínico.
* **`id`** (Entero, Clave Primaria, Autoincremental): El identificador único interno para la base de datos.
* **`codigo_anonimo`** (Texto/Varchar de 50 caracteres, Único): El código visible auto-generado secuencialmente por el sistema (ej: `PAC-0001`, `PAC-0002`). Servirá para buscar al paciente de forma anónima y no es editable.
* **`creado_por`** (Clave Foránea hacia `Usuario`): Registra qué estudiante creó el código de este paciente (apunta a `id` de `Usuario`).
* **`fecha_registro`** (Fecha/Hora): Momento en que se registró por primera vez en el sistema.

#### C. Tabla: `Consulta` (Registro de cada Cita Médica)
Esta tabla almacena cada visita o consulta que realiza un paciente. Un paciente puede tener muchas consultas.
* **`id`** (Entero, Clave Primaria, Autoincremental): El identificador único interno.
* **`paciente`** (Clave Foránea hacia `Paciente`): Vincula la consulta al paciente anónimo. Si el paciente se borra, sus consultas se borran en cascada.
* **`estudiante`** (Clave Foránea hacia `Usuario`): Vincula la consulta al estudiante que la atendió.
* **`fecha_consulta`** (Fecha/Hora): Cuándo ocurrió la consulta.
* **`diagnostico_estudiante`** (Texto largo / TextField): El diagnóstico propuesto por el alumno.
* **`diagnostico_medico`** (Texto largo / TextField): El diagnóstico del médico supervisor/tutor.
* **`diagnostico_final`** (Texto largo / TextField): El diagnóstico definitivo acordado.
* **`requiere_seguimiento`** (Booleano - Sí/No): Indica si el paciente debe regresar.
* **`fecha_proxima_consulta`** (Fecha, Opcional/Permite Nulo): Fecha programada para la siguiente cita (solo obligatoria si `requiere_seguimiento` es Verdadero).
* **`comentarios_previos`** (Texto largo, Opcional): Notas adicionales sobre el historial del paciente o detalles de consultas anteriores.
* **`calificacion`** (`DECIMAL(4,1)`, Rango 1.0 a 20.0, Opcional/Permite Nulo): Nota asignada por el profesor. Permite medios puntos (ej: `8.5`, `15.0`). Se usa `DECIMAL` en lugar de `FLOAT` para garantizar precisión exacta al calcular promedios en el dashboard.
* **`precision_diagnostica`** (Texto/Enum, Opcional/Permite Nulo): Métrica estructurada de evaluación. Opciones: `TOTAL` (Totalmente Acertado), `PARCIAL` (Parcialmente Acertado), `DESACERTADO` (Desacertado).
* **`observaciones_evaluacion`** (Texto largo / TextField, Opcional): Retroalimentación cualitativa detallada escrita por el profesor.
* **`creado_en`** (Fecha/Hora): Fecha de creación del registro.
* **`actualizado_en`** (Fecha/Hora): Fecha del último cambio del registro.

---

## 🔒 2. Matriz de Roles y Permisos (Seguridad - Decisiones Definidas)

Debemos definir con precisión qué puede hacer cada tipo de usuario. En el desarrollo profesional, esto se conoce como **Control de Acceso Basado en Roles (RBAC)**.

### Matriz de Permisos (CRUD):

| Entidad / Tabla | Estudiante (Rol) | Profesor (Rol) | Administrador (TI) |
| :--- | :--- | :--- | :--- |
| **Citas/Consultas** | Crear, Leer (propias), Editar (propias y no bloqueadas). No borrar. | Leer (todas). No crear ni editar de otros (salvo corrección médica especial). | Control total (CRUD). |
| **Pacientes** | Crear, Leer (Búsqueda global por código). | Leer (todos). | Control total. |
| **Usuarios/Alumnos** | Ningún acceso. | Leer lista de alumnos. | Crear alumnos, asignar roles. |

### Reglas de Negocio Implementadas:
1. **Pacientes Compartidos (Globales):** La lista de códigos de pacientes es **global**. Cualquier estudiante puede buscar un código existente y registrar una consulta para él, manteniendo la continuidad del historial clínico. Sin embargo, un estudiante **solo puede ver e interactuar con sus propias consultas realizadas**, mientras que el Profesor puede ver todas las consultas asociadas a ese paciente de forma consolidada.
2. **Bloqueo Automático de Edición:** Una consulta quedará **bloqueada para edición por parte del estudiante** inmediatamente después de que se registre el `diagnostico_final` (diagnóstico definitivo). Una vez bloqueada, si se requiere una corrección, solo el Profesor o un Administrador de TI podrán realizar modificaciones.
3. **Autogeneración Secuencial del Código Clínico:** Para evitar colisiones en la base de datos por ingreso manual repetido, el código clínico del paciente no es inventado por el estudiante. El sistema lo autogenera con el formato `PAC-XXXX` de forma secuencial al hacer clic en "Crear Paciente".
4. **Login Dual (Email o Cédula):** El formulario de inicio de sesión acepta un único campo de credencial que puede ser el **correo electrónico** o la **cédula de identidad**. Esto requiere un Backend de Autenticación Personalizado en Django (`backends.py`) que busque primero por email y, si no encuentra, por cédula.

   ```text
   Función autenticar_usuario(credencial, contraseña):
       usuario = BuscarUsuario(email = credencial)
       Si usuario no existe:
           usuario = BuscarUsuario(user_ci = credencial)
       Si usuario no existe:
           Retornar Error("Correo o cédula no registrados.")
       Si verificar_contraseña(contraseña, usuario.password) == Falso:
           Retornar Error("Contraseña incorrecta.")
       Retornar usuario
   ```
   > ⚠️ **Privacidad:** El campo `user_ci` solo debe ser visible para el Administrador del sistema. El Profesor no tiene acceso a la cédula de sus estudiantes.

---

## 📊 3. Especificación del Dashboard (Requerimientos del Profesor - Decisiones Definidas)

El profesor necesita analizar, comparar resultados e identificar tendencias de aprendizaje. Definimos las siguientes funcionalidades clave para el Dashboard:

### Métricas y Reportes Clave:
1. **Calificación Promedio por Alumno:** Calcula el promedio aritmético de los puntajes de evaluación (de 1 a 10) asignados por el docente. Permite ver el rendimiento académico del estudiante.
2. **Evolución del Estudiante (Puntaje/Tiempo):** Gráfico de línea temporal que muestra cómo cambia la calificación del alumno a lo largo de las semanas/meses para ver si hay aprendizaje y mejora.
3. **Distribución de Precisión Clínica:** Gráfico circular (torta/dona) que agrupa las consultas según la categorización del profesor (`Totalmente Acertado`, `Parcialmente Acertado`, `Desacertado`).
4. **Volumen de Trabajo:** Conteo total de pacientes atendidos por cada estudiante en el período.
5. **Control de Seguimientos:** Proporción de consultas marcadas con "requiere seguimiento posterior" que ya han tenido una nueva cita registrada para ese paciente.
6. **Patologías Comunes:** Las 5 enfermedades o diagnósticos definitivos más recurrentes en el grupo.

### Filtros e Interacción Requerida:
* **Filtro Temporal:** Posibilidad de filtrar todas las estadísticas por un rango de fechas específico (rango de inicio y rango de fin).
* **Filtro por Estudiante:** Ver las estadísticas individuales detalladas de un estudiante en particular para evaluar su desempeño en solitario.
* **Módulo de Comparación Cruzada:** Una funcionalidad que permite seleccionar a varios estudiantes a la vez para superponer sus promedios de calificación y volumen de consultas en un solo gráfico comparativo.
* **Bandeja de Pendientes de Calificar:** Un contador y listado de las citas cargadas por los estudiantes que aún tienen el campo `calificacion` vacío, permitiendo al profesor hacer clic y evaluarlas rápidamente.

---

## 📱 4. Diseño de Interfaz (Wireframes Conceptuales)

Aunque inicialmente usaremos el Django Admin (el cual se adaptará a este flujo), estructuramos las pantallas para que en la futura fase móvil la experiencia de usuario (UX) sea limpia, rápida y enfocada.

### A. Estudiante: Pantalla de Registro de Consulta (Enfoque Móvil)

Diseñada para ser completada en 1 o 2 minutos al lado del paciente:

```text
+-------------------------------------------------------+
|  🩺 NUEVA CONSULTA MÉDICA                             |
+-------------------------------------------------------+
| 👤 Paciente:                                          |
|    [ PAC-0001 (Ver Historial)      ▼ ]  [ + Registrar ]|
+-------------------------------------------------------+
| 📜 Historial Clínico Rápido (Comentarios de Citas Previas):|
|    "Cefalea tensional severa. Se recomendó reposo e   |
|     hidratación. Pendiente evaluar analítica."         |
+-------------------------------------------------------+
| ✍️ Diagnóstico del Estudiante (Provisional):          |
|    [ Escribe aquí tu impresión diagnóstica...       ] |
+-------------------------------------------------------+
| 👨‍⚕️ Diagnóstico del Médico Encargado (Supervisor):     |
|    [ Diagnóstico del tutor de práctica...            ] |
+-------------------------------------------------------+
| 🏁 Diagnóstico Final (Decisión Conjunta):             |
|    [ Diagnóstico definitivo para el expediente...   ] |
+-------------------------------------------------------+
| 📅 Continuidad del Cuidado:                           |
|    [ ] ¿Requiere seguimiento posterior?                |
|    Fecha Próxima Consulta: [ AAAA-MM-DD  📅 ] (Bloqueado|
|    si el check no está marcado)                       |
+-------------------------------------------------------+
|                [ 💾 GUARDAR CONSULTA ]                |
+-------------------------------------------------------+
|                                                       |
|  🔒 EVALUACIÓN DEL DOCENTE (Solo lectura para alumno) |
|  Calificación: ⭐⭐⭐⭐☆ (8/10)                         |
|  Métrica: [ Totalmente Acertado ]                     |
|  Feedback: "Excelente deducción. Recuerda asociar..." |
+-------------------------------------------------------+
```

---

### B. Profesor: Dashboard de Control y Comparación (Enfoque Computadora)

Estructura de cuatro niveles: Resumen, Comparación Interactiva, Bandeja de Pendientes y Tabla de Detalle.

```text
+-----------------------------------------------------------------------+
| 📊 PANEL DE CONTROL - DOCENTES                   📅 [ Rango de Fechas ▼ ] |
+-----------------------------------------------------------------------+
| [ Total Consultas ]      [ Calificación Promedio ]   [ Pendientes Eval. ]|
|       148 citas                  8.2 / 10               12 consultas  |
+-----------------------------------------------------------------------+
| 👥 COMPARACIÓN DE ALUMNOS (Selecciona para comparar):                  |
|   [x] Juan Pérez    [x] María López    [ ] Pedro Gómez   [ ] Ana Ruiz |
+-----------------------------------------------------------------------+
| 📈 GRÁFICO: EVOLUCIÓN DEL APRENDIZAJE (Calificación Promedio / Tiempo) |
|  10.0 |                                  /--- Juan Pérez              |
|   8.0 |         /\      /--------\------/                             |
|   6.0 |   -----/  \----/---------\           --- María López          |
|   4.0 |  /                                                            |
|       +--------------------------------------------->                 |
|         Semana 1    Semana 2    Semana 3    Semana 4                  |
+-----------------------------------------------------------------------+
| 📥 BANDEJA DE EVALUACIONES PENDIENTES                                 |
|  - PAC-0024 (María López) - Cefalea - 06/05/2026   --> [ Evaluar 📝 ] |
|  - PAC-0019 (Juan Pérez)  - Diabetes - 05/05/2026  --> [ Evaluar 📝 ] |
+-----------------------------------------------------------------------+
| 🏆 RENDIMIENTO GENERAL DE LA SECCIÓN                                  |
|  Estudiante     | Consultas | Calificación Prom. | Precisión (A/P/D)* |
|  ---------------+-----------+--------------------+--------------------|
|  Juan Pérez     | 48        | 8.9 / 10           | 40 / 6 / 2         |
|  María López    | 40        | 7.5 / 10           | 30 / 8 / 2         |
|  Pedro Gómez    | 32        | 8.4 / 10           | 25 / 5 / 2         |
|                                                                       |
|  * (A/P/D) = Casos: Totalmente Acertados / Parcialmente / Desacertados|
+-----------------------------------------------------------------------+
```

---

## 🏗️ 5. Responsabilidades por Capa y Prevención de Código Espagueti

Para mantener nuestro **Monolito Modular** limpio y evitar el "código espagueti" (código desordenado, donde las pantallas guardan datos y la base de datos toma decisiones de negocio), estableceremos responsabilidades muy claras para cada capa.

Cuando me pidas evaluar o refactorizar tu código, usaré esta estructura como estándar clínico de calidad:

### 📱 A. Frontend / Cliente (La Fachada)
* **Responsabilidad:** Presentación visual, experiencia de usuario (UX), estado local y validaciones rápidas de formato (ej. *"El código del paciente no puede contener caracteres especiales"* o *"La fecha no puede ser en el futuro"*).
* **Regla de Oro:** **Nunca confíes en el cliente.** Las validaciones del frontend son solo para guiar al usuario y mejorar la velocidad. Un usuario avanzado o un bug de red pueden saltarse el frontend. Toda regla crítica se valida en el backend.

### 🔌 B. Capa de API / Presentación del Servidor (El Portero - Views & Serializers)
* **Responsabilidad:** Recibir la petición HTTP, verificar quién la envía (Autenticación/Permisos JWT), validar los tipos de datos generales de entrada (ej: *"calificacion debe ser un número entero"*), y entregar la respuesta correcta en JSON o HTML.
* **Regla de Oro (Thin Controllers):** Los controladores/vistas de Django deben ser **delgados**. No deben contener fórmulas matemáticas, reglas médicas de negocio ni consultas directas complejas a la base de datos. Solo delegan el trabajo a la capa de servicios.

### 🧠 C. Capa de Servicios (El Cerebro - `services.py` - Recomendado para Monolito Modular)
* **Responsabilidad:** Lógica de negocio pura y dura de la aplicación (ej: *"Si la consulta es guardada con Diagnóstico Final, bloquear el registro, calcular si requiere seguimiento y disparar la alerta"*).
* **Regla de Oro:** Cada aplicación o módulo de Django tendrá su propio archivo de servicios (ej: `agenda/services.py`). Así, si en el futuro migras de Django Admin a una app móvil en React Native, la lógica de negocio no cambia: la nueva vista móvil llamará exactamente a la misma función del servicio que usaba el Django Admin. Esto **elimina el código espagueti**.

### 🗄️ D. Capa de Base de Datos / ORM (El Libro Mayor Inmutable - Supabase/PostgreSQL)
* **Responsabilidad:** Almacenamiento seguro, índices de rendimiento y constraints físicos de base de datos (ej. `NOT NULL`, `UNIQUE`, `FOREIGN KEY`, llaves primarias).
* **Regla de Oro:** La base de datos es la última línea de defensa. Aunque la aplicación en Django falle, la base de datos de Supabase debe rechazar relaciones inválidas o valores corruptos por diseño físico.

### 📏 E. Mantenibilidad: Límites de Tamaño de Archivo (Clean Code)

Para evitar que el código se vuelva inmanejable, difícil de leer y propenso a errores (los llamados "Archivos Dios"), aplicaremos los siguientes límites en el proyecto:

* **Límite Ideal por Archivo:** Mantener cada archivo de código entre **150 y 250 líneas de código**.
* **Límite de Alerta (Refactorización Obligatoria):** Si cualquier archivo supera las **400 - 500 líneas**, es un indicador claro de que el archivo viola el *Principio de Responsabilidad Única* (hace demasiadas cosas). La regla será dividirlo en archivos más pequeños o crear un paquete (ej: convertir un archivo grande `views.py` en una carpeta `views/` con pequeños archivos por vista).
* **Límite por Función:** Ninguna función o método individual debe superar las **30 - 40 líneas**. Si una función se alarga más de eso, debe subdividirse en subfunciones más pequeñas con responsabilidades únicas.

---

## 📝 6. Especificación de Reglas de Validación y Lógica (Pseudocódigo)

Para que el desarrollo en código real sea directo, aquí definimos los algoritmos de validación y de dashboard en formato de pseudocódigo lógico.

### A. Variables de Entrada y Salida (Formulario CRUD de Consulta)

#### Formulario: Registrar Consulta (Estudiante)
* **Datos de Entrada (Input):**
  * `paciente_id` (Entero): ID del paciente seleccionado.
  * `fecha_consulta` (Fecha/Hora): Cuándo se realizó la cita.
  * `diagnostico_estudiante` (Texto): Diagnóstico propuesto por el alumno.
  * `diagnostico_medico` (Texto): Diagnóstico del tutor supervisor.
  * `diagnostico_final` (Texto, Opcional): Diagnóstico acordado.
  * `requiere_seguimiento` (Booleano): Indica si necesita volver.
  * `fecha_proxima_consulta` (Fecha, Opcional): Fecha de la nueva cita.
  * `comentarios_previos` (Texto, Opcional): Notas rápidas históricas.
* **Datos de Salida (Output / Respuesta del Servidor):**
  * Si es exitoso: Retorna el objeto `Consulta` completo (incluyendo `id` autogenerado, estado `bloqueado=falso`, etc.) y código HTTP 201 (Creado).
  * Si falla: Retorna un listado de errores específicos por campo (ej: `"fecha_consulta": "La fecha no puede ser en el futuro"`) y código HTTP 400 (Bad Request).

---

### B. Algoritmos de Validación (Capa de Servicios / Backend)

#### 1. Validar que la Fecha de Consulta no sea futura
```text
Función validar_fecha_consulta(fecha_consulta):
    fecha_actual = ObtenerFechaYHoraActual()
    Si fecha_consulta > fecha_actual:
        Retornar Error("La fecha de la consulta no puede ser una fecha futura.")
    Retornar OK
```

#### 2. Validar Calificación del Profesor
```text
Función validar_calificacion(calificacion):
    Si calificacion está definida:
        Si calificacion < 0.5 O calificacion > 20.0:
            Retornar Error("La calificación debe estar entre 0.5 y 20.")
        Si (calificacion * 2) no es un número entero:
            Retornar Error("La calificación solo permite incrementos de 0.5 (ej: 8.0, 8.5, 9.0).")
    Retornar OK
```
> **Nota técnica:** El tipo `DECIMAL(4,1)` en PostgreSQL garantiza que valores como `8.5` se almacenen con precisión exacta, evitando errores de punto flotante al calcular promedios.

#### 3. Validar Reglas de Seguimiento Posterior
```text
Función validar_seguimiento(requiere_seguimiento, fecha_proxima_consulta, fecha_consulta):
    Si requiere_seguimiento == Verdadero:
        Si fecha_proxima_consulta es Nula o Vacía:
            Retornar Error("Debe ingresar la fecha de la próxima consulta si el paciente requiere seguimiento.")
        Si fecha_proxima_consulta <= fecha_consulta:
            Retornar Error("La fecha de la próxima consulta debe ser posterior a la fecha de la consulta actual.")
    Sino:
        Si fecha_proxima_consulta está definida:
            Retornar Error("No puede asignar una fecha de próxima consulta si no marcó que requiere seguimiento.")
    Retornar OK
```

#### 4. Validar Bloqueo de Edición para Alumnos
```text
Función validar_permiso_edicion(usuario_actual, consulta_id):
    consulta = BuscarConsultaEnBaseDatos(consulta_id)
    Si usuario_actual.rol == "Estudiante":
        Si consulta.diagnostico_final no está vacío:
            Retornar Error("Operación no permitida: Esta consulta ya tiene un diagnóstico final y se encuentra bloqueada para estudiantes.")
        Si consulta.estudiante != usuario_actual:
            Retornar Error("Operación no permitida: No tienes permiso para editar consultas de otros estudiantes.")
    Retornar OK

#### 5. Autogenerar Código Clínico de Paciente Secuencial
```text
Función generar_codigo_paciente_secuencial():
    último_paciente = ObtenerÚltimoPacienteCreadoOrdenadoPorIdDescendente()
    Si último_paciente no existe:
        número_siguiente = 1
    Sino:
        # Extraer el número del código (ej. de "PAC-0042" extrae 42)
        número_actual = ExtraerNúmeroDeTexto(último_paciente.codigo_anonimo)
        número_siguiente = número_actual + 1
    
    # Formatear el número con 4 ceros a la izquierda (ej. "PAC-0043")
    código_nuevo = "PAC-" + FormatearConCerosIzquierda(número_siguiente, 4)
    
    Retornar código_nuevo
```
```

---

### C. Lógica del Dashboard y Analíticas (Profesor)

#### 1. Calcular Nota Promedio de un Estudiante
```text
Función calcular_promedio_estudiante(estudiante_id, fecha_inicio, fecha_fin):
    consultas_calificadas = ObtenerConsultas(
        estudiante_id = estudiante_id, 
        fecha_consulta entre fecha_inicio y fecha_fin, 
        calificacion no sea nulo
    )
    Si consultas_calificadas está vacía:
        Retornar 0.0
    
    suma_notas = 0
    Para cada consulta en consultas_calificadas:
        suma_notas = suma_notas + consulta.calificacion
        
    Retornar suma_notas / Longitud(consultas_calificadas)
```

#### 2. Calcular Distribución de Casos (Total / Parcial / Desacertado)
```text
Función obtener_distribucion_precision(estudiante_id, fecha_inicio, fecha_fin):
    consultas_evaluadas = ObtenerConsultas(
        estudiante_id = estudiante_id,
        fecha_consulta entre fecha_inicio y fecha_fin,
        precision_diagnostica no sea nulo
    )
    
    conteo = { "TOTAL": 0, "PARCIAL": 0, "DESACERTADO": 0 }
    
    Para cada consulta en consultas_evaluadas:
        Si consulta.precision_diagnostica == "TOTAL":
            conteo["TOTAL"] = conteo["TOTAL"] + 1
        Sino si consulta.precision_diagnostica == "PARCIAL":
            conteo["PARCIAL"] = conteo["PARCIAL"] + 1
        Sino si consulta.precision_diagnostica == "DESACERTADO":
            conteo["DESACERTADO"] = conteo["DESACERTADO"] + 1
            
    Retornar conteo
```

---

## 🏁 ¡Diseño Listo para Desarrollo!

Una vez que revises y apruebes estas especificaciones visuales, de arquitectura y de calidad, habremos concluido la **etapa de diseño conceptual**. A partir de este momento, podemos proceder a la **Fase 1 de la Hoja de Ruta (Roadmap)**: la preparación del entorno de base de datos en Supabase y el entorno virtual local de Python.

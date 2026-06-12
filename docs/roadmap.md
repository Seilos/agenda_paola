# Proyecto: Agenda Médica Estudiantil (AGENDA_PAOLA)

Este documento sirve como hoja de ruta (roadmap) y registro de progreso para el desarrollo de la aplicación de agenda médica. Aquí se detallan las decisiones de arquitectura, los requerimientos y el estado de cada tarea.

---

## 🏗️ Arquitectura y Tecnologías

- **Enfoque:** Monolito Modular (Uso de Django Apps para separar responsabilidades).
- **Backend:** Django (Python).
- **Base de Datos:** Supabase (PostgreSQL remoto).
- **Interfaz Inicial:** Django Admin (módulo nativo personalizable).
- **Interfaz Futura:** Frontend móvil a medida (conectado vía API REST).

---

## 📋 Control de Requerimientos

### Citas/Consultas Médicas
- [ ] Registro de Paciente Anónimo (ID o número correlativo).
- [ ] Diagnóstico del Estudiante.
- [ ] Diagnóstico del Médico Encargado.
- [ ] Diagnóstico Final de la consulta.
- [ ] Indicador de seguimiento posterior (Sí/No).
- [ ] Fecha de la próxima consulta (opcional/condicionada).
- [ ] Comentarios sobre consultas previas (historial rápido).

### Roles y Permisos
- [ ] **Estudiantes:** Solo pueden ver, buscar y gestionar sus propias citas cargadas.
- [ ] **Profesores:** Acceso global de lectura, reportes y comparación estadística.

---

## 🚀 Fases del Proyecto

### Fase 0: Diseño y Planeación Conceptual (Pre-código)
- [ ] **0.1: Arquitectura de Datos e Identificación de Tablas**
  - [x] Elegir estrategia para Pacientes Anónimos (Opción B: Tabla separada para `Paciente`).
  - [x] Especificar campos de la tabla `Paciente` (id, codigo_anonimo, creado_por, fecha_registro).
  - [x] Especificar campos de la tabla `Consulta` (campos clínicos y campos de evaluación).
  - [x] Especificar campos de la tabla `Usuario` (incluyendo `user_ci` para login alternativo por cédula).
  - [ ] Dibujar el diagrama Entidad-Relación (ERD) físico en papel con las relaciones indicadas.
- [ ] **0.2: Definición de Variables y Flujo de Interfaces (Input/Output)**
  - [x] Diseñar el wireframe conceptual del Formulario de Consultas (Estudiante).
  - [x] Diseñar el wireframe conceptual del Dashboard Docente (Profesor).
  - [ ] Especificar las variables de entrada/salida para el Formulario de Consultas.
  - [ ] Especificar las variables dinámicas de consulta para el Dashboard del Profesor.
- [ ] **0.3: Especificación de Reglas de Validación (Lógica en Pseudocódigo)**
  - [ ] Redactar el pseudocódigo para la validación de fecha de consulta (no futura).
  - [ ] Redactar el pseudocódigo para la validación de calificación (rango 1 a 20).
  - [ ] Redactar el pseudocódigo para el bloqueo de edición (si existe diagnóstico final).
  - [ ] Redactar el pseudocódigo para la obligatoriedad de fecha de próxima cita (si requiere_seguimiento = True).
- [ ] **0.4: Lógica de Consultas Analíticas (Cálculos en Pseudocódigo)**
  - [ ] Escribir el pseudocódigo para el cálculo de la Nota Promedio de un estudiante.
  - [ ] Escribir el pseudocódigo para el cálculo de la Distribución de Casos (Aciertos/Desaciertos).

### Fase 1: Configuración del Entorno y Conexión de Base de Datos
- [ ] Crear el proyecto en Supabase y obtener la cadena de conexión de PostgreSQL.
- [ ] Crear el entorno virtual de Python y configurar la estructura inicial de Django.
- [ ] Instalar dependencias necesarias (`django`, `psycopg2-binary` o `dj-database-url` para la conexión de BD).
- [ ] Configurar las variables de entorno (`.env`) para proteger las credenciales de Supabase.
- [ ] Configurar `settings.py` en Django para conectar a la base de datos de Supabase.
- [ ] Ejecutar las migraciones iniciales de Django en la base de datos de Supabase.

### Fase 2: Diseño del Modelo de Datos (Base de Datos)
- [ ] Crear la Django app para la gestión de citas (ej. `consultas` o `agenda`).
- [ ] Diseñar el modelo `Cita` / `Consulta` con los campos requeridos en `models.py`.
- [ ] Crear la relación de clave foránea (Foreign Key) entre `Cita` y el modelo de usuario (`User` de Django) para saber qué estudiante registró la cita.
- [ ] Generar y ejecutar las migraciones del modelo en Supabase.

### Fase 3: Personalización del Django Admin y Roles
- [ ] Configurar dos grupos de usuarios en Django: `Estudiantes` y `Profesores`.
- [ ] Registrar el modelo de Citas en `admin.py`.
- [ ] Modificar el método `get_queryset` en el panel de administración de Django para que los usuarios del grupo `Estudiantes` solo vean sus propios registros.
- [ ] Configurar que los usuarios del grupo `Profesores` tengan acceso de lectura a todos los registros.
- [ ] Mejorar la visualización en el admin (filtros por fecha, búsqueda por número de paciente, campos de diagnóstico visibles).

### Fase 4: Consultas de Negocio y Dashboard para el Profesor
- [ ] Diseñar vistas o consultas agregadas en Django para obtener estadísticas (ej. cantidad de citas por estudiante, porcentaje de diagnósticos coincidentes entre estudiante y médico a cargo, etc.).
- [ ] Crear una interfaz simple dentro del admin o una vista personalizada para mostrar estas estadísticas al Profesor en forma de Dashboard.

### Fase 5: API REST y Frontend Móvil (Fase Futura)
- [ ] Instalar e integrar Django Rest Framework (DRF).
- [ ] Crear Serializers y ViewSets para exponer los datos de las citas mediante endpoints seguros.
- [ ] Implementar autenticación por Tokens (JWT) para la app móvil.
- [ ] Diseñar y construir el frontend móvil adaptado a teléfonos.

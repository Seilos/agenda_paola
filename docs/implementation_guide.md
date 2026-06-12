# 📘 Guía de Implementación Paso a Paso (AGENDA_PAOLA)

Esta guía detalla los pasos exactos y comandos necesarios para construir el backend del proyecto. Cada sección contiene el **"¿Por qué de este orden?"** para que comprendas la lógica detrás del flujo de trabajo estándar de la industria.

---

## 📂 Índice de Pasos

1. **Paso 1:** Configurar el Entorno Virtual de Python (Aislamiento).
2. **Paso 2:** Instalar Dependencias del Sistema.
3. **Paso 3:** Inicializar el Proyecto Django.
4. **Paso 4:** Configurar Variables de Entorno (`.env`).
5. **Paso 5:** Configurar la Conexión de Base de Datos en Django (`settings.py`).
6. **Paso 6:** Ejecutar Migraciones Iniciales (Tablas del Sistema).
7. **Paso 7:** Crear la App Modular de Django (`agenda`).
8. **Paso 8:** Escribir los Modelos en Código (`models.py`).
9. **Paso 9:** Generar y Aplicar las Migraciones del Proyecto.
10. **Paso 10:** Crear Superusuario de Administración.

---

## 🛠️ Paso 1: Configurar el Entorno Virtual (Aislamiento)

### 💻 Qué hacer (Comandos):
En tu terminal (PowerShell en Windows):
```powershell
# 1. Crear el entorno virtual llamado 'venv'
python -m venv venv

# 2. Activar el entorno
.\venv\Scripts\Activate

# 3. Actualizar pip (el gestor de paquetes de Python)
python -m pip install --upgrade pip
```

### 🧠 ¿Por qué este orden?
* **Aislamiento absoluto:** Antes de instalar cualquier librería (como Django), debemos crear un entorno virtual limpio. Si instalamos dependencias globalmente en la computadora, eventualmente entrarán en conflicto con otros proyectos de software y romperán tu sistema. El entorno virtual garantiza que todo lo instalado pertenezca *únicamente* a este proyecto.

---

## 📦 Paso 2: Instalar Dependencias del Sistema

### 💻 Qué hacer (Comandos):
Con el entorno virtual activo `(venv)`:
```powershell
pip install django psycopg2-binary python-dotenv
```
*(Opcional: guarda las dependencias en un archivo estándar de texto)*:
```powershell
pip freeze > requirements.txt
```

### 🧠 ¿Por qué este orden?
* **El kit de herramientas antes del trabajo:** Necesitamos instalar las librerías fundamentales antes de inicializar el proyecto:
  * `django`: El framework web.
  * `psycopg2-binary`: El conector que permite a Python "hablar" con PostgreSQL (Supabase).
  * `python-dotenv`: La herramienta para leer archivos de configuración ocultos (`.env`).

---

## 🚀 Paso 3: Inicializar el Proyecto Django

### 💻 Qué hacer (Comandos):
```powershell
# Crear el proyecto base en la carpeta actual (.) sin carpetas duplicadas
django-admin startproject agenda_project .
```

### 🧠 ¿Por qué este orden?
* **Crear la estructura antes de configurarla:** Necesitamos que Django genere automáticamente los archivos base del servidor (como `settings.py` y `manage.py`) antes de poder editarlos para conectarlos a nuestra base de datos o definir variables. El punto `.` al final evita que Django cree carpetas anidadas confusas.

---

## 🔒 Paso 4: Configurar Variables de Env (`.env`)

### 💻 Qué hacer (Pseudocódigo de Configuración):
Crea un archivo llamado `.env` en la raíz de tu proyecto (junto a `manage.py`):
```ini
# Variables de Entorno del Proyecto (.env)
SECRET_KEY=tu_secret_key_super_segura_de_django
DEBUG=True

# Credenciales de Supabase (PostgreSQL)
DB_NAME=postgres
DB_USER=postgres.[tu_proyecto_id]
DB_PASSWORD=tu_contraseña_segura_de_supabase
DB_HOST=aws-0-us-east-1.pooler.supabase.com
DB_PORT=6543
```

### 🧠 ¿Por qué este orden?
* **Seguridad antes de la exposición:** Nunca se escriben contraseñas directas dentro del código fuente (`settings.py`). Si subes el código a GitHub, tus credenciales de base de datos quedarían expuestas a atacantes. Por eso, el archivo `.env` se crea y se añade al archivo `.gitignore` antes de enlazar la base de datos a Django.

---

## 🔌 Paso 5: Configurar la Base de Datos en Django (`settings.py`)

### 💻 Qué hacer (Pseudocódigo en `settings.py`):
Abrir `agenda_project/settings.py` y configurar para leer el archivo `.env`:

```python
import os
from pathlib import Path
from dotenv import load_dotenv  # Importar dotenv

# 1. Cargar variables de entorno
load_dotenv()

# 2. Configurar base de datos apuntando a las variables cargadas
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# 3. Registrar que usaremos un Custom User Model (Usuario Personalizado)
AUTH_USER_MODEL = 'agenda.Usuario'
```

### 🧠 ¿Por qué este orden?
* **Conectar las tuberías:** Django necesita saber a dónde enviar los datos antes de que podamos hacer cualquier migración. Configurar `DATABASES` y registrar `AUTH_USER_MODEL` es el puente de comunicación con Supabase.

---

## 🗃️ Paso 6: Ejecutar Migraciones Iniciales (Tablas del Sistema)

### 💻 Qué hacer (Comandos):
```powershell
python manage.py migrate
```

### 🧠 ¿Por qué este orden?
* **Preparar los cimientos de Django:** Django viene con tablas nativas de administración, seguridad y sesiones. Correr `migrate` en este punto crea esas tablas en Supabase. Hacemos esto antes de crear nuestra propia aplicación para verificar que la conexión de base de datos funciona perfectamente y que Django puede escribir datos en la nube sin errores de red.

---

## 📁 Paso 7: Crear la App Modular de Django (`agenda`)

### 💻 Qué hacer (Comandos):
```powershell
# 1. Crear el módulo "agenda"
python manage.py startapp agenda
```
En `agenda_project/settings.py`, registrar la app en la lista `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ... apps de django ...
    'agenda',  # Registrar nuestro módulo
]
```

### 🧠 ¿Por qué este orden?
* **El módulo contenedor:** Creamos la app `agenda` ahora porque en el siguiente paso escribiremos los modelos de las tablas (`Usuario`, `Paciente`, `Consulta`). Django necesita que la app exista y esté registrada en `settings.py` antes de que intente leer los modelos y mapear las tablas correspondientes.

---

## 🐍 Paso 8: Escribir los Modelos en Código (`models.py`)

### 💻 Qué hacer (Estructura lógica en `agenda/models.py`):
Definir los campos que diseñamos en papel:

```python
from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Modelo de Usuario Personalizado
class Usuario(AbstractUser):
    ROLES = (
        ('ESTUDIANTE', 'Estudiante'),
        ('PROFESOR', 'Profesor'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='ESTUDIANTE')

# 2. Modelo de Paciente Anónimo
class Paciente(models.Model):
    codigo_anonimo = models.CharField(max_length=50, unique=True)
    creado_por = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)

# 3. Modelo de Consulta Médica
class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_consulta = models.DateTimeField()
    
    # Diagnósticos
    diagnostico_estudiante = models.TextField()
    diagnostico_medico = models.TextField()
    diagnostico_final = models.TextField()
    
    # Seguimiento
    requiere_seguimiento = models.BooleanField(default=False)
    fecha_proxima_consulta = models.DateField(null=True, blank=True)
    comentarios_previos = models.TextField(blank=True)
    
    # Evaluaciones del Profesor
    calificacion = models.IntegerField(null=True, blank=True)
    precision_diagnostica = models.CharField(max_length=20, null=True, blank=True)
    observaciones_evaluacion = models.TextField(blank=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
```

### 🧠 ¿Por qué este orden?
* **El orden de las dependencias:** Definimos `Usuario` primero porque `Paciente` y `Consulta` lo necesitan como Clave Foránea (`ForeignKey`). Luego definimos `Paciente` porque `Consulta` necesita asociarse a un paciente. Escribir modelos en el orden de sus dependencias evita que Python lance errores de "clase no definida".

---

## 🚀 Paso 9: Generar y Aplicar las Migraciones

### 💻 Qué hacer (Comandos):
```powershell
# 1. Crear el plano arquitectónico (los archivos de migración en Python)
python manage.py makemigrations

# 2. Aplicar los planos físicamente en Supabase
python manage.py migrate
```

### 🧠 ¿Por qué este orden?
* **El plano antes de la construcción:** `makemigrations` analiza tus clases en `models.py` y redacta un archivo instructivo en la carpeta `migrations/` detallando cómo deben modificarse las tablas de la base de datos. `migrate` toma ese archivo e implementa físicamente las tablas e índices en Supabase. Siempre deben ejecutarse en esta secuencia.

---

## 👑 Paso 10: Crear Superusuario de Administración

### 💻 Qué hacer (Comandos):
```powershell
python manage.py createsuperuser
```
*(Sigue las instrucciones en consola para definir tu usuario, correo y contraseña).*

### 🧠 ¿Por qué este orden?
* **Las llaves del castillo al final:** Para poder crear un superusuario administrador, todas las tablas de usuarios y perfiles ya deben estar creadas e instaladas físicamente en la base de datos de Supabase. Una vez creado, puedes iniciar el servidor (`python manage.py runserver`) e ingresar al panel de administración para empezar a usar la aplicación.

---
resumen: "Tutorial del 2026-09-14: cómo se creó el proyecto Django del backend, paso a paso."
tipo: guia
titulo: "AdMind — Backend: inicialización desde cero"
proyecto: "Proyecto de Ingeniería de Software II — Universidad de Cundinamarca, Facatativá"
fecha: 2026-09-14
actualizado: 2026-09-14
proposito: "Cómo se creó el proyecto Django del backend, paso a paso y con el porqué de cada decisión. Para repasar, para sustentar y para repetirlo en otro proyecto."
---

# AdMind — Backend: inicialización desde cero

> [!NOTE]
> **Qué es este documento.** El registro de cómo se levantó el backend el 2026-09-14: de una carpeta con READMEs a las primeras tablas en PostgreSQL.
>
> - Si lo que necesitas es **correr el proyecto que ya existe en otra PC**, la guía es [Admind_Backend_Instalacion_Local](Admind_Backend_Instalacion_Local.md).
> - El código vive en el repositorio `Admind_Backend`. Aquí se explica, no se copia completo.
> - Si algo de aquí choca con `Admin_Master.md`, manda el maestro.

---

## Resultado

| Qué | Cómo quedó |
| --- | --- |
| Proyecto Django | `config/` + `manage.py` · Django 5.2.17 + Django REST Framework 3.18.1 |
| Base de datos | PostgreSQL 18 local · base `admind_db` · usuario `admind_user` |
| Apps | `apps.personas` con el modelo `Persona` · `apps.cuentas` con el modelo `Usuario` |
| Migraciones | `personas 0001_initial` y `cuentas 0001_initial`, aplicadas |
| Commits en `desarrollo` | `8600244` git ignore · `6021bb9` crear proyecto y conectar PostgreSQL · `962853f` modelos Persona y Usuario |

## Mapa de pasos

- [x] **Paso 0** — Preparar la rama y el `.gitignore`
- [x] **Paso 1** — Entorno virtual e instalación de paquetes
- [x] **Paso 2** — Crear el proyecto Django
- [x] **Paso 3** — Crear la base y el usuario en PostgreSQL
- [x] **Paso 4** — Conectar Django con la base (`settings.py` + `.env`)
- [x] **Paso 5** — Probar con `runserver`
- [x] **Paso 6** — Primer commit
- [x] **Paso 7** — Convertir las carpetas en apps
- [x] **Paso 8** — Modelo `Persona`
- [x] **Paso 9** — Modelo `Usuario`, reiniciar la base y primer `migrate` de verdad

---

## Conceptos que hay que tener claros

| Concepto | Qué es, en una frase |
| --- | --- |
| **Entorno virtual** (`.venv`) | Una carpeta con un Python propio del proyecto, para que los paquetes no se mezclen con los de otros proyectos. Se activa en cada terminal nueva |
| **`requirements.txt`** | La lista exacta de paquetes y versiones. Con ella otra PC instala lo mismo |
| **Proyecto** | La configuración general: `config/` y `manage.py`. Hay uno solo |
| **App** | Un módulo del producto con sus propios modelos, vistas y rutas (`personas`, `cuentas`…). Hay muchas |
| **`settings.py`** | La configuración del proyecto: apps instaladas, base de datos, idioma, seguridad |
| **`.env`** | Archivo con los secretos de cada máquina (contraseña de la base, clave secreta). **Nunca se sube a GitHub** |
| **Modelo** | Una clase de Python que describe una tabla. Django la convierte en SQL |
| **`makemigrations`** | Lee los modelos y **escribe** archivos de migración: las instrucciones para crear o cambiar tablas. No toca la base |
| **`migrate`** | **Ejecuta** esas instrucciones en la base. Es el que crea las tablas |
| **`AUTH_USER_MODEL`** | Le dice a Django qué modelo es el usuario del sistema. Hay que fijarlo **antes** del primer `migrate` |

---

## Paso 0 — Preparar la rama

Todo se hizo en la rama `desarrollo` del repositorio `Backend/Admind_Backend`, en **Git Bash**.

```bash
cd "/c/Users/Alejandro/Documents/A D M I N D/Backend/Admind_Backend"
```
```bash
git pull
```

El `.gitignore` solo existía en la rama `lab`, así que se creó otro en `desarrollo` (commit `8600244`):

```
.venv
__pycache__/
*.pyc
.pytest_cache/
.env
```

**Por qué primero:** si se crea el entorno virtual o el `.env` antes del `.gitignore`, un `git add .` los sube. El `.env` lleva contraseñas.

## Paso 1 — Entorno virtual y paquetes

```bash
source .venv/Scripts/activate
```
```bash
python -m pip install "Django>=5.2.8,<6.0" djangorestframework "psycopg[binary]" python-dotenv
```
```bash
python -m pip freeze > requirements.txt
```

| Paquete | Para qué |
| --- | --- |
| `Django` | El framework. Mínimo 5.2.8 porque es la primera que soporta Python 3.14 |
| `djangorestframework` | Construir la API que consume el frontend |
| `psycopg[binary]` | El conector entre Python y PostgreSQL |
| `python-dotenv` | Leer el archivo `.env` |

> [!TIP]
> Cuando el prompt muestra `(.venv)` al principio, el entorno está activo. **Cada terminal nueva empieza sin activar.**

## Paso 2 — Crear el proyecto

```bash
django-admin startproject config .
```

**El punto final importa:** crea `config/` y `manage.py` en la carpeta actual. Sin él queda `config/config/`. No pisa el `README.md` que ya estaba en `config/`.

## Paso 3 — Crear la base y el usuario

Se entra a PostgreSQL con el superusuario `postgres`:

```bash
"/c/Program Files/PostgreSQL/18/bin/psql.exe" -U postgres
```

Y se crean un usuario propio y una base **vacía** de la que ese usuario es dueño:

```sql
CREATE ROLE admind_user LOGIN PASSWORD 'la-contraseña';
```
```sql
CREATE DATABASE admind_db OWNER admind_user;
```

**Por qué no el usuario `postgres`:** es el superusuario y puede hacer cualquier cosa en todo el servidor. La aplicación debe tener solo lo que necesita.

**Por qué una base vacía y no la que ya estaba diseñada:** ver la sección *Decisiones tomadas en el camino*, más abajo. La base `admind`, con el esquema hecho a mano, sigue existiendo como **plano de referencia** y no se toca.

## Paso 4 — Conectar Django con la base

Los secretos van en un archivo `.env`, en la raíz del backend, al lado de `manage.py`:

```
DJANGO_SECRET_KEY=la-clave-larga
DB_NAME=admind_db
DB_USER=admind_user
DB_PASSWORD=la-contraseña
```

Y `config/settings.py` los lee así:

```python
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

| Línea | Qué hace |
| --- | --- |
| `load_dotenv(BASE_DIR / ".env")` | Carga el `.env` como variables de entorno. **Python no lo lee solo** |
| `os.environ["DB_NAME"]` | Busca la variable que **se llama** `DB_NAME`. Entre corchetes va el **nombre**, nunca el valor |
| `SECRET_KEY` desde el `.env` | Si queda escrita en `settings.py`, se sube a GitHub con el primer commit |

## Paso 5 — Probar

```bash
python manage.py runserver
```

En `http://127.0.0.1:8000` aparece **el cohete** de Django: el proyecto arranca y la conexión con PostgreSQL funciona.

> [!WARNING]
> Sale un aviso de "migraciones sin aplicar". **En este punto no se corre `migrate`.** Si se corre, Django crea su usuario por defecto (`auth_user`), y después cambiarlo por el usuario propio da el error `InconsistentMigrationHistory`. Pasó aquí; la solución está en el paso 9.

## Paso 6 — Primer commit

```bash
git add config manage.py requirements.txt
```
```bash
git commit -m "chore: crear proyecto Django y conectar PostgreSQL"
```

Antes del `add` se revisa con `git status` que **no** aparezcan `.env` ni `.venv`.

## Paso 7 — Convertir las carpetas en apps

Las carpetas `apps/personas/` y `apps/cuentas/` ya existían, con un README cada una.

```bash
touch apps/__init__.py
```
```bash
python manage.py startapp personas apps/personas
```
```bash
python manage.py startapp cuentas apps/cuentas
```

| Paso | Por qué |
| --- | --- |
| `apps/__init__.py` | Convierte `apps/` en paquete de Python, para que exista `apps.personas` |
| `startapp` con ruta | Llena la carpeta existente con `models.py`, `apps.py`, `migrations/`… sin tocar el README |
| Cambiar `name` en cada `apps.py` | `startapp` escribe `name = 'personas'`. Como la app vive dentro de `apps/`, debe ser `name = 'apps.personas'` (y `'apps.cuentas'`) |
| Registrar en `INSTALLED_APPS` | Django solo busca modelos y migraciones en las apps de esa lista |

```python
INSTALLED_APPS = [
    # ...las de Django...
    "apps.personas",
    "apps.cuentas",
]
```

Se comprueba con:

```bash
python manage.py check
```

> [!TIP]
> Cada app se registra **una sola vez, cuando se crea**. Las carpetas de las demás apps se convierten con `startapp` cuando les toque tener código, no antes.

## Paso 8 — El modelo `Persona`

Archivo: `apps/personas/models.py`. Las decisiones de contenido están en el maestro §5.2.

| Pieza | Qué hace |
| --- | --- |
| `TipoDocumento` (`TextChoices`) | La lista cerrada: `CC`, `TI`, `CE`, `PAS`, `PPT`. A la izquierda el código que se guarda, a la derecha el nombre en pantalla |
| `normalizar_documento()` | Quita puntos y espacios, pasa a mayúsculas y quita ceros a la izquierda. `" 01.032.456.780 "` queda `"1032456780"` |
| `id = UUIDField(...)` | Llave primaria UUID (decisión 24). `editable=False` impide cambiarla desde un formulario |
| `nombres`, `apellidos`, `telefono`, `activo` | `telefono` es opcional (`blank=True`). `activo` es la baja lógica |
| `creado_en`, `actualizado_en` | Fechas que Django llena solo (`auto_now_add`, `auto_now`) |
| `Meta.constraints` | Un `UNIQUE` (tipo + número) y tres `CHECK` (tipo válido, documento normalizado, teléfono válido). **Django los crea en PostgreSQL**: la base rechaza el dato aunque alguien se salte el código |
| `save()` | Normaliza el documento **siempre antes de guardar**, venga de donde venga el dato |

## Paso 9 — `Usuario`, reiniciar la base y primer `migrate`

### 9.1 El modelo

Archivo: `apps/cuentas/models.py`.

| Pieza | Qué hace |
| --- | --- |
| `AbstractBaseUser` | Trae `password` (guardada con hash) y `last_login` |
| `PermissionsMixin` | Trae `is_superuser` y los permisos internos de Django. **No son los roles de AdMind**: esos van en la app `permisos`. Los de Django solo sirven para el panel de administración |
| `persona = OneToOneField(..., on_delete=PROTECT)` | Cada usuario es una persona, y una persona tiene como máximo un usuario. `PROTECT` impide borrar una persona que tiene cuenta (§5.11) |
| `correo = EmailField(unique=True)` | Con el correo se inicia sesión (`USERNAME_FIELD = "correo"`) y a él llega la recuperación de contraseña |
| `is_active`, `is_staff` | **En inglés a propósito**: Django los busca por ese nombre exacto (el login y la recuperación de contraseña filtran por `is_active`) |
| `save()` y `get_by_natural_key()` | Guardan y buscan el correo en minúsculas: `Ana@Correo.com` y `ana@correo.com` son la misma cuenta |
| `UsuarioManager` | La forma correcta de crear usuarios. `set_password` cifra la contraseña; nunca se asigna directo |

Los campos de TOTP del esquema de referencia no van aquí: los maneja `django-otp` en su propia tabla cuando llegue el 2FA.

### 9.2 Decirle a Django que use ese usuario

En `config/settings.py`, debajo de `INSTALLED_APPS`:

```python
AUTH_USER_MODEL = "cuentas.Usuario"
```

`cuentas` es la etiqueta de la app (la última parte de `apps.cuentas`) y `Usuario` el nombre de la clase.

### 9.3 Reiniciar la base

Como en el paso 5 ya se había corrido `migrate`, la base tenía las tablas de Django con su usuario por defecto. Sin datos que perder, lo más limpio fue borrarla y crearla de nuevo.

1. Detener `runserver` (Ctrl+C) y desconectar DBeaver: con conexiones abiertas PostgreSQL no deja borrar la base.
2. En `psql` como `postgres`:

```sql
DROP DATABASE admind_db;
```
```sql
CREATE DATABASE admind_db OWNER admind_user;
```

### 9.4 Migraciones

```bash
python manage.py makemigrations personas cuentas
```

Escribe `apps/personas/migrations/0001_initial.py` y `apps/cuentas/migrations/0001_initial.py`. La de `cuentas` depende de la de `personas`, porque `Usuario` apunta a `Persona`.

```bash
python manage.py migrate
```

**Verificación:** en la base aparecen `personas_persona` y `cuentas_usuario`, **no** aparece `auth_user`, y las restricciones del paso 8 existen en PostgreSQL. `python manage.py makemigrations --check` responde `No changes detected`.

### 9.5 Commit

```bash
git add apps config
```
```bash
git commit -m "feat(personas,cuentas): modelos Persona y Usuario"
```

> [!IMPORTANT]
> **Commit apenas algo funcione.** En este paso se perdió el modelo `Persona` por sobrescribir el archivo en el editor, y como no estaba en ningún commit, Git no podía devolverlo.

---

## Decisiones tomadas en el camino

| Decisión | Por qué | Dónde queda |
| --- | --- | --- |
| **Las tablas salen de los modelos de Django** (`migrate`), no de un script SQL ni de `inspectdb` | Camilo recrea la base con un solo `migrate`; las FK compuestas y los privilegios viajan en las migraciones (§7.1); Django necesita sus tablas y su usuario integrados | Este documento |
| **La base diseñada a mano (`admind`) queda como plano** | Ya sigue casi todo el maestro. Se usa para escribir los modelos, no se conecta a Django | Este documento |
| **Tipos de documento: `CC`, `TI`, `CE`, `PAS`, `PPT`**, códigos sin puntos | `PPT` reemplazó al `PEP`; `NIT` identifica empresas | Maestro §3.1 y §5.2 |
| **`nombres` y `apellidos` separados, `telefono` en `Persona`** | Decisión de Alejo, tomada del esquema de referencia | Pendiente de reflejar en el maestro §5.2 |
| **El correo vive solo en `Usuario`** | Es una credencial: con él se entra y a él llega la recuperación. Repetido en dos tablas, un día dirían cosas distintas | Pendiente de reflejar en el maestro §5.2 |
| **Usuario propio antes del primer `migrate`** | Cambiarlo después obliga a reiniciar la base | Paso 9 |
| **Restricciones declaradas en `Meta.constraints`** | Llegan a PostgreSQL: la base es la última defensa, no el código | Paso 8 |

---

## Problemas que salieron y cómo se resolvieron

| Síntoma | Causa | Solución |
| --- | --- | --- |
| `SyntaxError: '{' was never closed` en `settings.py` | Faltaba cerrar una llave en `DATABASES` | Cerrar la llave |
| `KeyError: 'admind_db'` | Se escribió el **valor** dentro de `os.environ[...]` en vez del **nombre** de la variable | `os.environ["DB_NAME"]`, y el valor en el `.env` |
| (habría salido) `KeyError: 'DB_NAME'` | Faltaba `load_dotenv` | Agregar `load_dotenv(BASE_DIR / ".env")` debajo de `BASE_DIR` |
| `la autentificación password falló para el usuario "admind_user"` | La contraseña del `.env` no era la del usuario de PostgreSQL. El mismo mensaje sale si el usuario no existe | Poner la misma contraseña en los dos lados (`ALTER ROLE ... PASSWORD`) |
| `ModuleNotFoundError: No module named 'django'` | Terminal nueva sin el entorno virtual activado | `source .venv/Scripts/activate` |
| `startapp personas app/personas` | Faltaba la "s" de `apps` | `apps/personas` |
| `Cannot import 'personas'. Check that 'apps.personas.apps.PersonasConfig.name' is correct` | `name` seguía en `'personas'` | `name = 'apps.personas'` |
| `AUTH_USER_MODEL refers to model 'cuentas.Usuario' that has not been installed` | `apps/cuentas/models.py` no estaba guardado con el código | Pegar el modelo y guardar |
| `TypeError: isinstance() arg 2 must be a type…` | `apps/personas/models.py` se había sobrescrito: `"personas.Persona"` apuntaba a una clase que ya no existía | Restaurar el modelo `Persona` |
| `migrate` corrido en el paso 5 | Django creó `auth_user` antes del usuario propio | Borrar y recrear la base antes del primer `migrate` real (9.3) |

---

## Preguntas que puede hacer el jurado

Las respuestas están en este documento. Conviene poder decirlas sin leerlas.

1. ¿Por qué el esquema sale de los modelos de Django y no de un script SQL?
2. ¿Por qué hay que definir el usuario propio antes del primer `migrate`?
3. ¿Qué diferencia hay entre `makemigrations` y `migrate`?
4. ¿Por qué la contraseña de la base no está en `settings.py`?
5. Si alguien inserta a mano un documento con puntos directamente en PostgreSQL, ¿qué pasa?
6. ¿Por qué el correo vive en `Usuario` y no en `Persona`?
7. ¿Por qué `is_active` está en inglés si todo lo demás está en español?
8. Los permisos de Django (`PermissionsMixin`) y los roles de AdMind, ¿son lo mismo?

---

## Pendiente

- [ ] Reflejar en el maestro §5.2 los campos de `Persona` (`nombres`, `apellidos`, `telefono`) y el correo en `Usuario`
- [ ] Subir una plantilla `.env.example` sin valores reales
- [ ] Registrar `Persona` y `Usuario` en el panel de administración y crear la primera cuenta con `createsuperuser`
- [ ] App `conjuntos` y los modelos base de `apps/comun/modelos_base/` (primer modelo con `conjunto_id`)
- [ ] Capa de servicios que pide el profesor (vista → servicio → repositorio)
- [ ] Decidir los choques del esquema de referencia con el maestro: `asignacion.conjunto_id NOT NULL`, roles y permisos como tablas, estados de `reserva`, `clasificacion` de áreas, reglas y notificaciones
- [ ] Los dos usuarios de base, dueño y aplicación (maestro §11.5)

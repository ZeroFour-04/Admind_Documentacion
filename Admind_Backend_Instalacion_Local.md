---
titulo: "AdMind — Backend: instalación local"
proyecto: "Proyecto de Ingeniería de Software II — Universidad de Cundinamarca, Facatativá"
fecha: 2026-09-14
actualizado: 2026-09-14
proposito: "Guía para que Camilo baje el backend de GitHub y lo deje corriendo en su PC, y para el trabajo del día a día."
---

# AdMind — Backend: correrlo en tu PC

> [!IMPORTANT]
> **Camilo, léelo antes de empezar.**
>
> - Se trabaja en la rama **`desarrollo`** del repositorio `ZeroFour-04/Admind_Backend`.
> - Los comandos están escritos para **Git Bash**, no para PowerShell.
> - Salvo que diga otra cosa, todo se corre desde la **carpeta raíz del backend**, la que tiene `manage.py`.
> - Cómo y por qué se armó el proyecto: [Admind_Backend_Inicializacion](Admind_Backend_Inicializacion.md).

---

## Lo que necesitas instalado

| Programa | Versión | Cómo comprobarlo |
| --- | --- | --- |
| Git (con Git Bash) | Cualquiera reciente | `git --version` |
| Python | **3.12 o superior** (Alejo usa 3.14) | `python --version` |
| PostgreSQL | **16 o superior** (Alejo usa 18), con el servicio corriendo | Que abra `psql` o pgAdmin |
| DBeaver o pgAdmin | Opcional | Para ver las tablas |

> [!NOTE]
> Durante la instalación de PostgreSQL se te pidió una contraseña para el usuario `postgres`. La vas a necesitar en el paso 4.

---

## Resumen rápido

Si ya conoces Django, esto es todo. Si no, sigue los pasos de abajo, que explican cada uno.

- [ ] Clonar o actualizar el repo y quedar en `desarrollo`
- [ ] `python -m venv .venv` y activarlo
- [ ] `python -m pip install -r requirements.txt`
- [ ] Crear en PostgreSQL el usuario `admind_user` y la base `admind_db`
- [ ] Crear el `.env` con las cuatro variables
- [ ] `python manage.py migrate`
- [ ] `python manage.py runserver` y ver el cohete en `http://127.0.0.1:8000`

---

## Paso 1 — Bajar el código

**Si todavía no tienes el repositorio**, en la carpeta donde lo quieras guardar:

```bash
git clone https://github.com/ZeroFour-04/Admind_Backend.git
```
```bash
cd Admind_Backend
```  
```bash
git switch desarrollo
```

**Si ya lo tienes clonado**, desde su carpeta:

```bash
git fetch origin
```
```bash
git switch desarrollo
```
```bash
git pull
```

**Comprueba** que llegó el código:

```bash
git log --oneline -3
```

Tiene que aparecer el commit `feat(personas,cuentas): modelos Persona y Usuario`. Si no aparece, Alejo todavía no ha hecho `push`: pídeselo antes de seguir.

## Paso 2 — Crear el entorno virtual

El entorno virtual es un Python propio del proyecto. **No se sube a GitHub**, así que cada quien crea el suyo.

```bash
python -m venv .venv
```
```bash
source .venv/Scripts/activate
```

Quedó activo cuando el prompt empieza con `(.venv)`.

> [!WARNING]
> **Cada terminal nueva empieza sin el entorno activado.** Si ves `No module named 'django'`, es eso: vuelve a correr `source .venv/Scripts/activate`.

## Paso 3 — Instalar los paquetes

```bash
python -m pip install -r requirements.txt
```

`requirements.txt` tiene las versiones exactas que usa Alejo (Django 5.2.17, Django REST Framework, psycopg, python-dotenv, pytest…). Así los dos trabajan con lo mismo.

## Paso 4 — Crear la base de datos

Entra a PostgreSQL con el usuario `postgres`. Cambia `18` por tu versión si es otra:

```bash
"/c/Program Files/PostgreSQL/18/bin/psql.exe" -U postgres
```

Si Git Bash se queda colgado, antepón `winpty` al comando. También puedes hacerlo desde el editor SQL de pgAdmin o DBeaver, conectado como `postgres`.

Crea el usuario y la base con **los mismos nombres que usa Alejo**, para que el `.env` sea igual en las dos máquinas:

```sql
CREATE ROLE admind_user LOGIN PASSWORD 'la-contraseña-acordada';
```
```sql
CREATE DATABASE admind_db OWNER admind_user;
```

Para salir de `psql`:

```sql
\q
```

> [!IMPORTANT]
> - **La base se crea vacía.** No copies la de Alejo ni corras ningún script SQL: las tablas las crea Django en el paso 6, a partir de las migraciones que vienen en el repositorio.
> - **`OWNER admind_user` es obligatorio.** Sin eso, el paso 6 falla con un error de permisos sobre el esquema `public`.
> - La contraseña pídesela a Alejo. No se escribe en la documentación porque el repositorio está en GitHub.

## Paso 5 — Crear el archivo `.env`

El `.env` guarda los secretos de tu máquina. Va en la **raíz del backend, al lado de `manage.py`**, y se llama exactamente `.env`. El `.gitignore` ya lo excluye, así que nunca se sube.

Primero genera tu propia clave secreta de Django (con el entorno activado):

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Crea el `.env` con este contenido. Sin comillas y sin espacios alrededor del `=`:

```
DJANGO_SECRET_KEY=la-clave-que-acabas-de-generar
DB_NAME=admind_db
DB_USER=admind_user
DB_PASSWORD=la-contraseña-acordada
```

| Variable | Qué es |
| --- | --- |
| `DJANGO_SECRET_KEY` | Clave que Django usa para firmar sesiones. Cada máquina tiene la suya |
| `DB_NAME` | La base del paso 4 |
| `DB_USER` | El usuario del paso 4 |
| `DB_PASSWORD` | La contraseña de ese usuario. **Tiene que ser exactamente la misma** |

## Paso 6 — Crear las tablas

```bash
python manage.py migrate
```

Vas a ver una lista de líneas `Applying ... OK`, entre ellas `personas.0001_initial` y `cuentas.0001_initial`. Eso crea en tu base las mismas tablas que tiene Alejo.

> [!WARNING]
> **No corras `makemigrations` para arrancar el proyecto.** Las migraciones ya vienen en el repositorio. `makemigrations` solo se usa cuando cambias un modelo (ver *Día a día*).

## Paso 7 — Probar

```bash
python manage.py check
```

Debe responder `System check identified no issues (0 silenced).`

```bash
python manage.py runserver
```

Abre `http://127.0.0.1:8000` en el navegador. **Si ves el cohete de Django, quedó funcionando.** Para detener el servidor: Ctrl+C.

Si abres DBeaver o pgAdmin sobre `admind_db`, en el esquema `public` tienen que estar `personas_persona` y `cuentas_usuario`, y **no** debe estar `auth_user`.

### Checklist final

- [ ] `git log` muestra el commit de `Persona` y `Usuario`
- [ ] El prompt muestra `(.venv)`
- [ ] Existe `.env` al lado de `manage.py`
- [ ] `python manage.py migrate` terminó sin errores
- [ ] `python manage.py check` dice `no issues`
- [ ] El cohete aparece en `http://127.0.0.1:8000`

---

## Día a día

### Cada vez que te sientas a trabajar

```bash
source .venv/Scripts/activate
```
```bash
git pull
```

Y según lo que haya traído el `pull`:

| Si cambió… | Corre |
| --- | --- |
| `requirements.txt` | `python -m pip install -r requirements.txt` |
| Algún archivo dentro de `migrations/` | `python manage.py migrate` |

Luego `python manage.py runserver`.

### Cuando cambias o creas un modelo

1. Edita el `models.py` de la app.
2. `python manage.py makemigrations nombre_app`
3. `python manage.py migrate`
4. Haz commit del **modelo y su migración juntos**.
5. **Avísale a Alejo.** Si los dos crean migraciones en la misma app al mismo tiempo, chocan.

### Cuando instalas un paquete nuevo

```bash
python -m pip install nombre-del-paquete
```
```bash
python -m pip freeze > requirements.txt
```

Y haz commit del `requirements.txt` para que Alejo instale lo mismo.

### Commits

- Siempre sobre `desarrollo`. No hay ramas por historia (maestro §8.5).
- Formato del maestro §8.4: `tipo(app): descripción [HU-XX]`. Ejemplo: `feat(reservas): agregar bloqueo de 3 minutos [HU-11]`.
- Antes de `git add`, revisa con `git status` que no aparezcan `.env` ni `.venv`.

---

## Problemas comunes

| Síntoma | Causa probable | Qué hacer |
| --- | --- | --- |
| `No module named 'django'` | Entorno virtual sin activar | `source .venv/Scripts/activate` |
| `KeyError: 'DB_NAME'` (o cualquier otra variable) | Falta el `.env`, no está al lado de `manage.py` o el nombre de la variable está mal escrito | Revisa el paso 5 |
| `la autentificación password falló para el usuario "admind_user"` | La contraseña del `.env` no es la del usuario, o el usuario no existe (PostgreSQL da el mismo mensaje en los dos casos) | En `psql`: `\du` para ver si existe y `ALTER ROLE admind_user WITH LOGIN PASSWORD '...';` para fijarla |
| `la base de datos «admind_db» no existe` | No se hizo el paso 4 | Crear la base |
| `permiso denegado al esquema public` al migrar | La base no es de `admind_user` | `ALTER DATABASE admind_db OWNER TO admind_user;` como `postgres` |
| `connection refused` o no conecta | El servicio de PostgreSQL está apagado | Arrancar el servicio de PostgreSQL en Servicios de Windows |
| `InconsistentMigrationHistory` o `relation ... already exists` | La base no estaba vacía | Borrarla y crearla de nuevo (paso 4) y volver a migrar |
| `psql: command not found` | `psql` no está en el PATH | Usar la ruta completa del paso 4 |
| `warning: LF will be replaced by CRLF` | Diferencia de saltos de línea entre Windows y Git | Es inofensivo. Está pendiente definir un `.gitattributes` |

---

## Lo que todavía no hay

- **Endpoints de API.** Por ahora solo existen los modelos `Persona` y `Usuario`.
- **Forma cómoda de crear usuarios.** El panel `/admin` abre, pero no tiene los modelos registrados; y `createsuperuser` pide el id de una `Persona` que primero hay que crear.
- **Plantilla `.env.example` en el repositorio.** Mientras no exista, el `.env` se arma con el paso 5.

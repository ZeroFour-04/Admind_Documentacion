---
resumen: "Cómo correr los dos servidores y las pruebas, qué cubre cada suite y cuál falla hoy."
tipo: arquitectura
origen: "guía de estructura §4.8, §8 y §9 (2026-09-30) + plan de los Sprints 2 y 3 §0.4"
actualizado: 2026-09-30
---

# Pruebas y ejecución

La terminal es **Git Bash**: sintaxis POSIX y rutas entre comillas, porque `A D M I N D` tiene espacios.

## Comandos de verificación (sin activar el entorno)

```bash
cd "/c/Users/Alejandro/Documents/A D M I N D/Backend/Admind_Backend"
./.venv/Scripts/python.exe -m pytest -q
./.venv/Scripts/python.exe manage.py makemigrations --check --dry-run
```
```bash
cd "/c/Users/Alejandro/Documents/A D M I N D/Frontend/Admind_Front-End"
./.venv/Scripts/python.exe -m pytest -q
```

- **Crear migraciones:** `./.venv/Scripts/python.exe manage.py makemigrations <app>`. Revisa el archivo y agrega a mano las `fk_compuesta(...)` al final de `operations`.
- **Aplicar en `admind_db`:** solo si D11 lo autoriza.

## Las pruebas

Las pruebas se escriben como funciones `def test_…():` con `assert`. `pytest-django` les da una base de datos de prueba que se crea y se borra sola.

- **Back**: usa `config/settings_pruebas.py` (lo fija `pytest.ini`), que agrega una app de apoyo (`tests.aislamiento`) y un cifrado de contraseñas rápido (provisional, decisión de Alejo).
- **Front**: no tiene base de datos ni API de verdad; las pruebas **simulan la API** con `mock.patch("cliente_api.reservas.franjas", return_value=…)` y revisan el HTML que sale.

| Dónde | Cuántas | Qué cubren |
|---|---|---|
| `Backend/…/apps/*/tests.py` y `test_*.py` | la mayoría de las 330 (329 pasan, 1 falla) | Cada app: modelos, servicios, endpoints, códigos de error. `conjuntos/test_identidad.py` cubre el color propio y la foto 1:1 (PNG, JPG y WebP no cuadrados); `permisos/test_roles.py`, el rol único por conjunto y el cambio de rol |
| `Backend/…/tests/aislamiento/` | — | Filtro por conjunto y la **prueba del intruso** sobre todas las rutas. **Hoy falla** `test_toda_ruta_de_la_api_esta_cubierta`: las rutas `usuario-perfil` y `usuario-eliminar` (29/09) no están en las listas de la prueba |
| `Backend/…/tests/concurrencia/` | — | N personas contra la misma franja → un solo bloqueo |
| `Backend/…/tests/esquema/` | — | La **lista cerrada de tablas globales**: si aparece una tabla sin `conjunto_id` que no esté en la lista, falla |
| `Frontend/…/tests/` | 140 | Cada pantalla con la API simulada: qué muestra, qué oculta sin permiso, cómo presenta los errores. `test_acentos.py` y `test_identidad.py` cubren la rampa del color propio, la advertencia de contraste y el marcador con iniciales |

Las pruebas automáticas **no reemplazan** la prueba manual de la DoD: nadie ha recorrido HU-06 a HU-13 en el navegador todavía. El recortador de foto y el diálogo de "Eliminar usuario" son JavaScript y **no tienen prueba automática**: solo se prueban a mano.

## Correr todo en el PC

Con PostgreSQL encendido (servicio `postgresql-x64-18`) y cada proyecto con su `.venv` y su `.env`. En Git Bash, **una terminal por servidor**:

```bash
cd "/c/Users/Alejandro/Documents/A D M I N D/Backend/Admind_Backend" && source .venv/Scripts/activate && python manage.py migrate && python manage.py runserver 8000
```

```bash
cd "/c/Users/Alejandro/Documents/A D M I N D/Frontend/Admind_Front-End" && source .venv/Scripts/activate && python manage.py runserver 8001
```

Luego abre `http://127.0.0.1:8001`.

Para tener con quién entrar, el comando `crear_usuarios_prueba` crea un "Conjunto de prueba" y un usuario por rol (`administracion@example.com`, `residente@example.com`, …), todos con la contraseña que le escribas. Solo funciona con `DEBUG` activo:

```bash
cd "/c/Users/Alejandro/Documents/A D M I N D/Backend/Admind_Backend" && source .venv/Scripts/activate && python manage.py crear_usuarios_prueba
```

> [!NOTE]
> Para probar una reserva de punta a punta, el residente necesita estar vinculado a una **unidad** con "reside" y debe existir un **área** activa. Eso se hace desde las pantallas de Apartamentos y Áreas entrando como Administración.

Para correr las pruebas, dentro de cada proyecto con su `.venv` activo:

```bash
python -m pytest -q
```

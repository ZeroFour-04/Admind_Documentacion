---
resumen: "Cómo correr los dos servidores y las pruebas, qué cubre cada suite y cuál falla hoy."
tipo: arquitectura
origen: "guía de estructura §4.8, §8 y §9 (2026-09-30) + plan de los Sprints 2 y 3 §0.4"
actualizado: 2026-10-10
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
| `Backend/…/apps/*/tests.py` y `test_*.py` | la mayoría de las 362 (361 pasan, 1 falla; 2026-10-05, con las fotos de los anuncios sin commit; en el último commit, `5ed32a5`, son 344). `anuncios/tests.py` cubre las fotos: lo que guarda la base, publicar, los rechazos y a quién se le entrega la imagen. `cuentas/tests.py` cubre también el límite de 3 enlaces por hora (con la caché vaciada antes de cada prueba); `cuentas/test_dos_factores.py`, el enlace por correo que quita el segundo factor | Cada app: modelos, servicios, endpoints, códigos de error. `conjuntos/test_identidad.py` cubre el color propio y la foto 1:1 (PNG, JPG y WebP no cuadrados); `permisos/test_roles.py`, el rol único por conjunto y el cambio de rol |
| `Backend/…/tests/aislamiento/` | — | Filtro por conjunto y la **prueba del intruso** sobre todas las rutas. **Hoy falla** `test_toda_ruta_de_la_api_esta_cubierta`: no están en las listas de la prueba cinco rutas: `usuario-perfil` y `usuario-eliminar` (29/09), y `solicitudes-bandeja`, `solicitudes-area` y `solicitud-decision` (HU-14, 05/10). Verificado el 2026-10-08 |
| `Backend/…/tests/concurrencia/` | — | N personas contra la misma franja → un solo bloqueo |
| `Backend/…/tests/esquema/` | — | La **lista cerrada de tablas globales**: si aparece una tabla sin `conjunto_id` que no esté en la lista, falla |
| `Frontend/…/tests/` | 180 (169 en el último commit, `ea0e9e5`) | Cada pantalla con la API simulada: qué muestra, qué oculta sin permiso, cómo presenta los errores. `test_anuncios.py` cubre también subir fotos al publicar y la galería del tablón. `test_acentos.py` y `test_identidad.py` cubren la rampa del color propio, la advertencia de contraste y el marcador con iniciales; `test_recuperacion.py`, las pantallas de recuperar la contraseña (sin sesión, con la API simulada); `test_segundo_factor.py`, las de pedir y confirmar el enlace que quita el segundo factor |

**Al 2026-10-06**, con el motor de reglas por niveles sin commit: Backend **378** (377 pasan y falla la misma de siempre, que ya lista 5 rutas sin registrar) y Frontend **193**, todas pasan. Sobre los últimos commits (`2d11dbe` y `a3792d7`) eran 368 y 188. `apps/reglas/tests.py` cubre los niveles, la regla única por tipo, los tipos retirados, el catálogo, las tres restricciones de la base y el evaluador; `tests/test_reglas.py` del front, el tablero, los días que no abre y el paso del asistente.

**Al 2026-10-06, con el asistente completo y las viviendas sin commit** (sobre `9b3b231` y `b5d96df`, que ya traen el motor): Backend **415** (414 pasan y falla la misma, con las mismas 5 rutas) y Frontend **206**, todas pasan. Antes eran 378 y 196. `apps/unidades/test_estructura.py` prueba el generador de viviendas **sin base de datos**: son funciones puras. `apps/unidades/tests.py` suma la API de la estructura (vista previa que no guarda, generar, repetir sin duplicar, mixtos, topes y orden natural); `apps/documentos/tests.py`, subir, ver y descargar el reglamento, los rechazos y quién puede; `apps/conjuntos/tests.py`, que un conjunto completo queda operativo y qué falta cuando no. En el front, `tests/test_asistente_viviendas.py` y `tests/test_asistente_reglamento.py`. `static/js/viviendas.js` **no tiene prueba automática**: solo a mano.

**Al 2026-10-08, con las zonas con ingreso sin commit** (sobre `279e963` y `f5b3d08`): Backend **478** (477 pasan y falla la misma de siempre, por las mismas cinco rutas: ninguna de `ingresos`) y Frontend **246**, todas pasan. Antes eran 416 y 210. `apps/ingresos/tests.py` cubre el servicio (aforo, acompañantes, horario, vencimiento con la hora simulada, búsqueda, restricciones de la base) y la API por rol; `tests/concurrencia/test_aforo_de_ingresos.py` prueba contra PostgreSQL real que diez registros sobre el último cupo dejan uno solo adentro y que una persona en dos zonas a la vez queda en una. En el front, `tests/test_ingresos.py` cubre la pantalla de Vigilancia, el historial y el menú; `tests/test_areas.py`, `test_reglas.py` y `test_reservas.py`, el modo de uso, los acompañantes y la tabla de zonas con cupos.

**Al 2026-10-10, con dos reglas de reserva nuevas sin commit** (sobre `2d6bbe0` y `1f624b5`): Backend **491** (490 pasan y falla la misma de siempre) y Frontend **260**, todas pasan. Antes eran 482 y 256. `apps/reglas/tests.py` y `apps/reservas/tests.py` cubren *una reserva al día* y *sin franjas seguidas*, y `tests/concurrencia/test_bloqueo_de_franjas.py` gana una prueba: tres envíos a la vez sobre franjas distintas del mismo día dejan una sola apartada.

**Al 2026-10-10 (noche), con HU-16, el pago declarado de una reserva, sin commit** (encima de lo anterior): Backend **528** (526 pasan y fallan dos) y Frontend **288**, todas pasan. Antes eran 491 y 260. Las dos del backend: la de las cinco rutas de siempre y `apps/ingresos/tests.py::test_un_registro_que_no_cumple_responde_400_con_todos_los_motivos_y_no_deja_fila`, que **usa la hora real** (la zona de prueba abre de 05:00 a 22:00 y de noche responde 3 motivos en vez de 2; ya fallaba antes de este cambio). `tests/archivos/test_comprobantes.py` prueba la validación por firma sin tocar la base; `apps/reservas/tests.py` cubre declarar, retirar, subir y descargar; `tests/aislamiento/test_intruso.py` suma las cuatro rutas nuevas. En el front, `tests/test_reservas.py` y `tests/test_triage.py` cubren el bloque de pago de las dos pantallas. Para probar el front real contra la API real sin tocar `admind_db` sirvió un pytest desechable con `live_server` del backend (base de pruebas), que lanza el front con `ADMIND_API_URL` apuntando al servidor de prueba; no está en el repositorio.

**Al 2026-10-10 (más tarde), con HU-28, el parqueadero de visitantes, sin commit** (encima de HU-16): Backend **565** (563 pasan y fallan las dos de antes) y Frontend **318**, todas pasan. Antes eran 528 y 288. `apps/parqueaderos/tests.py` cubre el catálogo y que ninguna ruta ni el modelo asignan un parqueadero a una unidad; `apps/visitantes/test_visitantes.py` suma la capa de servicio, la salida, la auditoría y los cinco criterios de HU-28; `tests/concurrencia/test_parqueadero_de_visitantes.py` prueba contra PostgreSQL real que diez registros sobre el mismo puesto dejan a una sola visita con él; el intruso suma `parqueaderos`, `parqueadero-desactivar` y `visitante-salida`. En el front, `tests/test_parqueaderos.py` y las pruebas nuevas de `tests/test_visitantes.py`, que ahora simula la lista de libres con una fixture automática. `static/js/visitantes.js` **no tiene prueba automática**.

**Al 2026-10-10 (al final del día), con HU-35, el pago de la administración, sin commit** (encima de HU-28): Backend **642** (640 pasan y fallan las dos de antes) y Frontend **352**, todas pasan. Antes eran 565 y 318. `apps/pagos/tests.py` cubre los meses (funciones puras), la tabla, el buscador sin tildes y por documento, el check idempotente, el reporte con validación por firma, la descarga por vínculo, «Mis pagos» y la mora con la hora simulada, y de punta a punta que una vivienda en mora no reserva y al confirmar el mes sí; `apps/reglas/tests.py`, el tipo nuevo y su parámetro; el intruso suma cinco rutas. En el front, `tests/test_pagos.py` y dos pruebas nuevas en `tests/test_reglas.py`. `apps/pagos/mora.py` se calcula en el conjunto de la vivienda, así que sus pruebas no necesitan una petición.

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

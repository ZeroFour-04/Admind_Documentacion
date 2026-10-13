---
resumen: "Cómo correr los dos servidores y las pruebas, cuántas hay, qué cubre cada archivo de pruebas y cuál falla hoy."
tipo: arquitectura
origen: "guía de estructura §4.8, §8 y §9 (2026-09-30) + plan de los Sprints 2 y 3 §0.4; conteos y archivos verificados el 2026-10-11"
actualizado: 2026-10-13
revisado: 2026-10-13
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

- **Crear migraciones:** `./.venv/Scripts/python.exe manage.py makemigrations <app>`. Revisa el archivo y agrega a mano las `fk_compuesta(...)` al final de `operations` ([invariantes](../03_Reglas/invariantes.md)).
- **Aplicar en `admind_db`:** solo si el pedido o el plan lo autorizan ([convenciones](../03_Reglas/convenciones.md)). En los últimos planes las corrió Alejo.
- **Migraciones pendientes:** `./.venv/Scripts/python.exe manage.py showmigrations` marca con `[ ]` las que faltan por aplicar.

## Cómo están hoy (2026-10-13)

Sobre Backend `87d67c5` y Frontend `0adf5eb`, más lo del dashboard de gestión del 13/10 (HU-14 y HU-29), que está sin commit:

| Suite | Pruebas | Resultado | Tiempo |
|---|---|---|---|
| Backend | **706** | Todas pasan | 96 s |
| Frontend | **414** | Todas pasan | 14 s |

`makemigrations --check` no encuentra cambios. En `admind_db` faltan por aplicar `reservas/0006_categoria_de_rechazo` y `casos/0004_ciclo_del_caso`.

> [!NOTE] La prueba del intruso ya pasa
> Desde el 13/10 todas las rutas de la API están registradas en `tests/aislamiento/test_intruso.py`: las de HU-14, las de casos, `campanas`, `usuario-eliminar` y `usuario-perfil` (esta, como ruta sin conjunto). Una ruta nueva que no se registre vuelve a poner en rojo `test_toda_ruta_de_la_api_esta_cubierta`.

> [!NOTE] La que falla de noche
> `apps/ingresos/tests.py::test_un_registro_que_no_cumple_responde_400_con_todos_los_motivos_y_no_deja_fila` usa la hora real: la zona de prueba abre de 05:00 a 22:00 y entre las 22:00 y las 05:00 responde tres motivos en vez de dos. De día pasa.

Cómo fue creciendo el conteo, corte por corte, está en [bitacora](../08_Estado/bitacora.md).

## Cómo se escriben

Funciones `def test_…():` con `assert`. `pytest-django` les da una base de datos de prueba que se crea y se borra sola.

- **Back:** usa `config/settings_pruebas.py` (lo fija `pytest.ini`), que agrega una app de apoyo (`tests.aislamiento`) y un cifrado de contraseñas rápido. Ese cifrado es provisional y decisión de Alejo: el archivo no se toca sin preguntarle.
- **Front:** no tiene base de datos ni API de verdad. Las pruebas **simulan la API** con `mock.patch("cliente_api.reservas.franjas", return_value=…)` y revisan el HTML que sale.

## Qué cubre cada archivo del backend

Rutas relativas a `Backend/Admind_Backend/`.

| Archivo | Qué cubre |
|---|---|
| `apps/personas/tests.py`, `test_busqueda.py` | Persona única por documento, normalización, y buscar y vincular con su límite |
| `apps/cuentas/tests.py` | Login, token, conjunto activo, usuarios del conjunto, recuperación de contraseña y su límite de 3 enlaces por hora (con la caché vaciada antes de cada prueba) |
| `apps/cuentas/test_dos_factores.py` | El segundo factor y el enlace por correo que lo quita |
| `apps/permisos/tests.py`, `test_roles.py` | Catálogo, permisos efectivos, el rol único por conjunto, el cambio de rol y quién puede crear conjuntos |
| `apps/conjuntos/tests.py` | El asistente: que un conjunto completo queda operativo y qué falta cuando no |
| `apps/conjuntos/test_identidad.py` | El color propio y la foto 1:1 (PNG, JPG y WebP no cuadrados) |
| `apps/unidades/tests.py` | Vínculos y la API de la estructura: vista previa que no guarda, generar, repetir sin duplicar, mixtos, topes y orden natural |
| `apps/unidades/test_estructura.py` | El generador de viviendas, **sin base de datos**: son funciones puras |
| `apps/documentos/tests.py` | Subir, ver y descargar el reglamento, los rechazos y quién puede |
| `apps/areas/tests.py` | El catálogo de áreas, el aforo obligatorio, el modo de uso y su cambio (qué queda y qué reglas se retiran) |
| `apps/reglas/tests.py` | Los niveles, la regla única por tipo, los tipos retirados, el catálogo, las restricciones de la base y el evaluador |
| `apps/reservas/tests.py` | Franjas, bloqueo, envío, las reglas de reserva, la decisión, y declarar, retirar, subir y descargar el pago |
| `apps/ingresos/tests.py` | Aforo, acompañantes, horario, vencimiento con la hora simulada, búsqueda, restricciones de la base y la API por rol |
| `apps/pagos/tests.py` | Los meses (funciones puras), la tabla, el buscador, el check idempotente, el reporte con validación por firma, «Mis pagos» y la mora con la hora simulada |
| `apps/parqueaderos/tests.py` | El catálogo, y que ninguna ruta ni el modelo asignan un parqueadero a una unidad |
| `apps/visitantes/test_visitantes.py` | Ingreso, capa de servicio, salida, auditoría y los cinco criterios de HU-28 |
| `apps/anuncios/tests.py` | Los dos alcances y las fotos: lo que guarda la base, publicar, los rechazos y a quién se le entrega la imagen |
| `apps/notificaciones/tests.py`, `apps/auditoria/tests.py` | El canal y el registro de solo inserción |
| `tests/aislamiento/test_filtro_por_conjunto.py` | El filtro por conjunto del manager |
| `tests/aislamiento/test_intruso.py` | La **prueba del intruso** sobre todas las rutas |
| `tests/esquema/test_tablas_globales.py` | La **lista cerrada de tablas globales**: falla si aparece una tabla sin `conjunto_id` que no esté en la lista |
| `tests/concurrencia/test_bloqueo_de_franjas.py` | N personas contra la misma franja dejan un solo bloqueo; tres envíos a la vez sobre franjas distintas del mismo día dejan una sola apartada |
| `tests/concurrencia/test_aforo_de_ingresos.py` | Diez registros sobre el último cupo dejan uno solo adentro; una persona en dos zonas a la vez queda en una |
| `tests/concurrencia/test_parqueadero_de_visitantes.py` | Diez registros sobre el mismo puesto dejan a una sola visita con él |
| `tests/archivos/test_comprobantes.py` | La validación de un archivo por su firma, sin tocar la base |

Las tres de concurrencia corren contra PostgreSQL real, con hilos.

## Qué cubre cada archivo del frontend

En `Frontend/Admind_Front-End/tests/`. Cada uno prueba sus pantallas con la API simulada: qué muestra, qué oculta sin permiso y cómo presenta los errores.

| Archivo | Pantallas |
|---|---|
| `test_recuperacion.py`, `test_segundo_factor.py`, `test_cuenta_perfil.py` | Recuperar la contraseña, pedir y confirmar el enlace que quita el segundo factor, y el perfil |
| `test_identidad.py`, `test_acentos.py` | Selector, barra, lateral, la rampa del color propio, la advertencia de contraste y el marcador con iniciales |
| `test_asistente_viviendas.py`, `test_asistente_reglamento.py` | Los pasos 2 y 6 del asistente |
| `test_usuarios.py`, `test_unidades.py` | Usuarios por rol, el rol por defecto, viviendas, vínculos y crear un residente |
| `test_areas.py`, `test_reglas.py`, `test_reservas.py`, `test_triage.py` | Áreas con su modo de uso, el tablero de reglas, la reserva con el bloque de pago y las solicitudes |
| `test_ingresos.py`, `test_visitantes.py`, `test_parqueaderos.py`, `test_pagos.py` | Vigilancia y su historial, portería con parqueadero y salida, el catálogo de parqueaderos y los pagos |
| `test_anuncios.py` | El tablón, publicar con fotos y la galería |

## Lo que las pruebas automáticas no cubren

- **La prueba manual de la DoD.** Nadie ha recorrido las historias en el navegador con usuarios reales ([pendientes](../08_Estado/pendientes.md), sección 2).
- **JavaScript sin prueba automática:** el recortador de foto (`identidad.js`), el diálogo de «Eliminar usuario», `viviendas.js`, `visitantes.js`, `unidades.js`, `directorio-usuarios.js`, `vinculos.js` y `busqueda.js`. Se prueban a mano.
- **El front real contra la API real.** Para hacerlo sin tocar `admind_db` sirvió un pytest desechable con `live_server` del backend (base de pruebas), que lanza el front con `ADMIND_API_URL` apuntando al servidor de prueba. No está en el repositorio.

## Correr todo en el PC

Con PostgreSQL encendido (servicio `postgresql-x64-18`) y cada proyecto con su `.venv` y su `.env`. En Git Bash, **una terminal por servidor**:

```bash
cd "/c/Users/Alejandro/Documents/A D M I N D/Backend/Admind_Backend" && source .venv/Scripts/activate && python manage.py migrate && python manage.py runserver 8000
```

```bash
cd "/c/Users/Alejandro/Documents/A D M I N D/Frontend/Admind_Front-End" && source .venv/Scripts/activate && python manage.py runserver 8001
```

Luego abre `http://127.0.0.1:8001`. Claude arranca los dos con `A D M I N D/.claude/launch.json` (`admind-backend` y `admind-front`).

Para tener con quién entrar, el comando `crear_usuarios_prueba` crea un «Conjunto de prueba» y un usuario por rol (`administracion@example.com`, `residente@example.com`, …), todos con la contraseña que le escribas. Solo funciona con `DEBUG` activo:

```bash
cd "/c/Users/Alejandro/Documents/A D M I N D/Backend/Admind_Backend" && source .venv/Scripts/activate && python manage.py crear_usuarios_prueba
```

> [!NOTE]
> Para probar una reserva de punta a punta, el residente necesita estar vinculado a una **unidad** con «reside» y debe existir un **área** activa con reserva. Eso se hace desde las pantallas Unidades y Áreas comunes, entrando como Administración.

Para correr las pruebas, dentro de cada proyecto con su `.venv` activo:

```bash
python -m pytest -q
```

## Ver también

- [mapa_codigo](mapa_codigo.md) — dónde está cada app y cada carpeta de pruebas
- [entorno_local](entorno_local.md) — la máquina y sus versiones
- [invariantes](../03_Reglas/invariantes.md) — la prueba del intruso y las FK compuestas al crear algo
- [lista_de_salida](../03_Reglas/lista_de_salida.md) — qué se comprueba antes de decir *terminé*
- [estado_actual](../08_Estado/estado_actual.md) — los commits y el conteo del corte

---
resumen: "Inventario histórico del código, pieza por pieza y con su commit, en los cortes del 15/09 y del 27/09."
tipo: estado
origen: "avance §2 (cortes 2026-09-15 y 2026-09-27)"
actualizado: 2026-09-27
---

# Inventario del código, pieza por pieza

> [!WARNING] Es histórico
> 2.1, 2.2 y 2.4 son del **2026-09-15**; 2.5, del **2026-09-27**. Lo construido entre el 15/09 y el 25/09 y después del 27/09 no está aquí. Para saber qué hay hoy y dónde: [mapa_codigo](../02_Arquitectura/mapa_codigo.md).

Referencias sin nombre de documento (*§2*, *§4*, *§6*…) son del antiguo `Admind_Avance.md`: §2 → [inventario_codigo](inventario_codigo.md) · §3 → [bitacora](bitacora.md) · §4 → [construccion](../06_Decisiones/construccion.md) · §5 → [historias](historias.md) y [historias_evidencia](historias_evidencia.md) · §6 → [pendientes](pendientes.md). *Maestro §N* se resuelve en `Admin_Master.md`.

## 2.1 Repositorios

| Repositorio | Rama | Último commit | En el remoto |
|---|---|---|---|
| Backend | `desarrollo` | `d9b6271` — selector de conjunto activo y aislamiento por endpoint (2026-09-15 09:11) | Sí |
| Frontend | `desarrollo` | `1a4e7d1` — merge con dos commits de Camilo, sobre `557bc9f`: proyecto Django, login y maquetas (2026-09-15 10:14) | Sí |
| Documentación | `main` | `c556285` — este archivo al corte de las 09:00 (2026-09-15 09:13) | Sí. Las actualizaciones de las 09:25, las 10:13 y las 10:35 de este archivo, sin commit, y cambios sin commit en otros dos archivos |

## 2.2 Backend, pieza por pieza

| Pieza | Estado | Dónde |
|---|---|---|
| Django 5.2.17, Django REST Framework 3.18, psycopg 3.3, pytest-django 4.14 | Instalado; `rest_framework` en `INSTALLED_APPS` | `requirements.txt`, `config/settings.py` |
| Proyecto Django (`startproject config .`) | Hecho | `config/` |
| Clave secreta y conexión a la base por variables de entorno | Hecho | `config/settings.py` + `.env` (fuera del repositorio) |
| `TIME_ZONE = 'America/Bogota'` y `LANGUAGE_CODE = 'es-co'` (mensajes de Django y DRF en español) | Hecho | `config/settings.py` |
| PostgreSQL 18 local, base `admind_db`, usuario `admind_user` con `CREATEDB` | Hecho, en la máquina de Alejo | — |
| App `personas` con el modelo `Persona` | Hecho | `apps/personas/models.py` |
| App `cuentas` con el modelo `Usuario` y `AUTH_USER_MODEL` | Hecho | `apps/cuentas/models.py` |
| App `conjuntos` con el modelo `Conjunto` (UUID, `nombre`, `direccion`, `activo`, `operativo`) | Hecho. `operativo` nace en falso; sin campo de color | `apps/conjuntos/models.py` |
| Catálogo fijo en código: 6 roles, 46 permisos, 18 sensibles y el reparto por rol | Hecho. **El reparto por rol es provisional** | `apps/permisos/catalogo.py` |
| Modelo `Asignacion` (persona, rol, conjunto, vigencias) | Hecho | `apps/permisos/models.py` |
| `Asignacion.objects.vigentes()`: empezaron y no han terminado | Hecho | `apps/permisos/models.py`, `d9b6271` |
| Servicios de permisos: conjuntos disponibles de una persona, `puede_operar_en` y permisos efectivos | Hecho | `apps/permisos/servicios.py`, `d9b6271` |
| Conjunto activo de la operación (`ContextVar`): `usar_conjunto()` para fijarlo a mano; `contexto_limpio()` y `fijar_conjunto_activo()` para las peticiones | Hecho; los dos últimos en `d9b6271` | `apps/comun/aislamiento/contexto.py` |
| Modelo base `ModeloDeConjunto` con `ManagerDeConjunto` (filtra toda consulta por el conjunto activo) | Hecho. **Ningún modelo del producto lo usa todavía** | `apps/comun/modelos_base/modelos.py`, `apps/comun/aislamiento/managers.py` |
| `fk_compuesta()`: FK `(x_id, conjunto_id)` escrita en la migración | Hecho. Probada solo con tablas de apoyo | `apps/comun/aislamiento/migraciones.py` |
| `VistaDeConjunto`: vista base de DRF que fija el conjunto activo desde el token, rechaza `conjunto` o `conjunto_id` en la ruta, la URL o el cuerpo (400) y exige conjunto activo (403). Hace el papel del middleware del maestro (§4) | Hecho | `apps/comun/aislamiento/vistas.py`, `d9b6271` |
| Modelo `TokenDeSesion`: huella SHA-256 del token, usuario, conjunto activo, 2FA verificado y vencimiento | Hecho | `apps/cuentas/models.py`, `0b0c4f8` |
| Autenticación de DRF por `Authorization: Token <token>`. Toda vista exige token, salvo las que lo declaren | Hecho | `apps/cuentas/autenticacion.py`, `config/settings.py` |
| Duración del token: 1 hora fija | Hecho | `DURACION_TOKEN_DE_SESION` en `config/settings.py` |
| `POST /auth/login/` y `POST /auth/logout/` | Hecho (`0b0c4f8`). Desde el paso 6 el login también devuelve `conjunto_activo` y `permisos` | `apps/cuentas/` |
| `GET /auth/conjuntos/` y `POST /auth/conjunto-activo/` | Hecho (`d9b6271`) | `apps/cuentas/` |
| Capa de servicios (flujo controlador → servicio → repositorio que pide el profesor) | Hecho en `cuentas` y `permisos`. `apps/README.md` todavía no la declara | `apps/*/servicios.py` |
| Migraciones: `0001` de `personas`, `conjuntos` y `permisos`; `0001` y `0002` de `cuentas`. Todas aplicadas en `admind_db` | Hecho. El paso 6 no trae migraciones | `apps/*/migrations/` |
| Pruebas con `pytest` y `pytest-django`: 69 (10 de personas, 17 de cuentas, 2 de conjuntos, 20 de permisos, 7 del filtro por conjunto, 10 del intruso y de rutas, 3 de tablas globales) | Hecho, todas pasan. 21 son del paso 6 (`d9b6271`) | `pytest.ini`, `apps/*/tests.py`, `tests/` |
| Configuración de pruebas: app de apoyo `tests.aislamiento` (`Area`, `Reserva` y dos endpoints), URLs de pruebas y cifrado rápido de contraseñas | Hecho; las URLs de pruebas, en `d9b6271` | `config/settings_pruebas.py`, `config/urls_pruebas.py`, `tests/aislamiento/` |
| Plantilla de variables de entorno | Hecho | `.env _ejemplo` |
| Recuperación de contraseña por correo, 2FA TOTP y clase de permiso por vista | **No hay** | — |
| `ALLOWED_HOSTS` para desplegar | **No hay**, tampoco en el front | — |
| Resto de apps (`unidades`, `areas`, `reservas`, …) | Solo carpeta con README | `apps/` |

## 2.4 Frontend, pieza por pieza

En `557bc9f` (2026-09-15 10:14), en la rama `desarrollo` de `Admind_Front-End` y en el remoto. Construido a partir del borrador de Alejo (`C:\Users\Alejandro\Desktop\Pagina`, seis páginas HTML) y adaptado al sistema de diseño (§4).

| Pieza | Estado | Dónde |
|---|---|---|
| Proyecto Django del servidor web: Django 5.2.17, requests 2.34, python-dotenv | Hecho | `config/`, `manage.py`, `requirements.txt` |
| Sin base de datos (`DATABASES = {}`). Las sesiones de este servidor se guardan en archivos de la carpeta temporal del sistema | Hecho | `config/settings.py` |
| Clave secreta y dirección de la API por variables de entorno (`DJANGO_SECRET_KEY`, `ADMIND_API_URL`), con plantilla | Hecho | `.env` (fuera del repositorio), `.env _ejemplo` |
| `.gitignore` con `.venv`, `.env` y cachés | Hecho | `.gitignore` |
| `pedir()`: el único punto que llama a la API. Agrega `Authorization: Token`, convierte un 400 en errores por campo, da texto a 401, 403 y 404 ("No encontrado.") y avisa si la API no responde | Hecho | `cliente_api/http.py` |
| `iniciar_sesion` (`POST /auth/login/`) y `cerrar_sesion` (`POST /auth/logout/`) | Hecho | `cliente_api/cuentas.py` |
| **Ingreso funcional**: errores bajo cada campo, mensaje genérico de la API, token guardado en la sesión del servidor, sesión que vence con el token e id de sesión nuevo al entrar | Hecho | `apps/cuentas/` |
| Salir (`POST /salir/`): llama al logout de la API y vacía la sesión aunque la API falle | Hecho | `apps/cuentas/views.py` |
| `SesionRequeridaMiddleware`: toda pantalla exige sesión, salvo las marcadas con `@publica` | Hecho | `apps/cuentas/sesion.py` |
| Plantillas base (`base`, `sin_sesion`, `aplicacion`) y los componentes `BarraSuperior` y `Lateral`, sobre las clases de `design-system/` | Hecho | `templates/` |
| CSS propio, solo con variables del sistema de diseño | Hecho | `static/css/estructura.css`, `static/css/reservas.css` |
| **Maquetas** con datos de ejemplo y sin llamadas a la API: recuperar contraseña, selector de conjunto, inicio, calendario de zonas comunes, reglas y anuncios. Solicitudes y apartamentos y parqueaderos, como estado vacío | Hecho | `apps/cuentas`, `conjuntos`, `paneles`, `reservas`, `reglas`, `anuncios`, `triage`, `unidades` |
| Pruebas automáticas del front | **No hay**. El login se verificó con un script fuera del repositorio (§3) | `tests/` solo tiene README |
| Selector conectado a la API, recuperación de contraseña real, 2FA y Alpine.js | **No hay** | — |
| `index.html` y `apps/Administrador/Home.html`: dos HTML de prueba de Camilo (`57a45c0`, `fd6a03d`, 2026-09-14) que llegaron con el merge `1a4e7d1`. Quedan fuera de la estructura de Django y ninguna vista los sirve | Por decidir con Camilo (§6) | Raíz y `apps/Administrador/` del front |

Las maquetas **no cuentan como avance** de las historias de esas pantallas (HU-08, HU-10, HU-11, HU-22, HU-25, HU-26): no llaman a la API ni cumplen sus criterios.

## 2.5 Construido en los Sprints 2 y 3 (2026-09-27)

**Backend** (`3c70e3a..66f8897`). Toda tabla nueva hereda `ModeloDeConjunto`, sus FK entre tablas de conjunto son compuestas y toda ruta nueva está en la prueba del intruso.

| Pieza | Dónde |
|---|---|
| Auditoría de solo inserción: tabla `auditoria_registro` (actor, acción, entidad, antes, después, detalle, `via_superusuario`). Modificar o borrar una fila lanza `RegistroInmutable`, también por el queryset. Quitarle `UPDATE` y `DELETE` al usuario de base de datos queda para después (D8 a) | `apps/auditoria/` |
| Áreas comunes: clasificación cerrada (`comun`, `comun_esencial`, `comun_uso_exclusivo`), `es_esencial` derivado, horario con bloques fijos (D1 a), mantenimiento y desactivar sin borrar. `franjas_del_dia()` | `apps/areas/`, rutas `/areas/` |
| Unidades y vínculos: crear unidad, detalle con vigentes e históricos, registrar y cerrar vínculos (solo para quien ya tiene rol en el conjunto, P3), `unidades_para_solicitar()` | `apps/unidades/`, rutas `/unidades/<id>/…` |
| Roles: `asignar_rol` y `retirar_rol` con auditoría; retirar al último de Administración responde 409, con `select_for_update` sobre las asignaciones de Administración | `apps/permisos/servicios.py`, rutas `/auth/usuarios/<id>/roles/…` |
| `UsuarioResumenSerializer` gana `persona` y `asignaciones` (P2) | `apps/cuentas/serializers.py` |
| Búsqueda por documento exacto (POST) con auditoría y límite de 20 por hora, 429 al pasarse (D6); vincular reutiliza `asignar_rol` | `apps/personas/`, rutas `/personas/buscar/` y `/personas/vincular/` |
| Reglas beta: catálogo de 7 tipos que solo restringen (D4 a), validador de parámetros, descripción en palabras, versionado al editar (`reemplaza`) y retirar por vigencia | `apps/reglas/catalogo.py`, `models.py`, `servicios.py`, rutas `/reglas/` |
| Motor de reglas: alfas `RESIDE`, `NO_EN_EL_PASADO` y `AREA_DISPONIBLE`; un evaluador por tipo; AND sin detenerse en la primera falla. `unidad_en_mora()` provisional en `False` hasta HU-35 (D5 b) | `apps/reglas/alfa.py`, `evaluador.py`, `mora.py` |
| Mecanismo compartido de bloqueo (R1): `tomar()` traduce el índice único parcial en `RecursoOcupado`; `expirar_vencidos()` es un solo `UPDATE` idempotente | `apps/comun/bloqueo/bloqueo.py` |
| Reservas: `Solicitud` con 7 estados (`LIBERADA` nuevo, D2 a), índices únicos parciales por franja y por persona (D3 a); franjas, tomar el bloqueo de 3 minutos, liberar, avisos del panel, enviar con evaluación guardada (P10) y aviso a la Administración | `apps/reservas/`, rutas `/reservas/…` |
| `requisitos_para_operar`: `areas` y `reglas_beta` pasan a disponibles. El reglamento sigue en construcción, así que ningún conjunto queda operativo | `apps/conjuntos/servicios.py` |
| Pruebas de concurrencia obligatorias del maestro §5.1 (10 hilos con barrera sobre la misma franja) | `tests/concurrencia/test_bloqueo_de_franjas.py` |
| Migraciones nuevas, **aplicadas en `admind_db`**: `auditoria 0001`, `areas 0001`, `reglas 0001`, `reservas 0001` | `apps/*/migrations/` |

**Frontend** (`b42ce93..c1d8f6b`)

| Pieza | Dónde |
|---|---|
| Áreas comunes: lista, alta con clasificación obligatoria, edición con mantenimiento, desactivar; ítem "Áreas comunes" en el lateral con `area.gestionar` | `apps/areas/`, `cliente_api/areas.py` |
| Asistente de HU-03 en cinco pasos: 1 Datos, 2 Administración, 3 Áreas, 4 Reglas, 5 Resumen | `apps/conjuntos/` |
| Apartamentos: lista con vínculos vigentes, registrar apartamento, detalle con vigentes e históricos, agregar y cerrar vínculos. Reemplaza la maqueta | `apps/unidades/`, `cliente_api/unidades.py` |
| Roles en el detalle del usuario: retirar y asignar los que no tiene; el 409 del último administrador como alerta | `apps/usuarios/`, `cliente_api/cuentas.py` |
| Registrar persona: buscar por documento, vincular si existe, o pasar al alta con el documento por la sesión, nunca por la URL (P4) | `apps/usuarios/`, `cliente_api/personas.py` |
| Reglas: lista agrupada por área, alta en dos pasos sin JavaScript con un formulario por tipo, edición que avisa la versión nueva. Reemplaza la maqueta | `apps/reglas/`, `cliente_api/reglas.py` |
| Reservas: selector de área, franjas del día con su estado en texto, Reservar, solicitud con cuenta regresiva, Cancelar y `sendBeacon` al salir, panel de confirmación y envío | `apps/reservas/`, `cliente_api/reservas.py`, `static/js/reservas.js` |
| Fragmento de confirmación del contenido, solo con clases existentes (P7) | `templates/componentes/confirmacion_de_contenido.html` |
| Alpine.js 3.17.4 autoalojado, con versión y SHA-256 anotados; se carga solo donde se usa (P13) | `static/js/vendor/`, `templates/base/base.html` |
| Mensajes de 409 y 429 en el cliente de la API (P12) | `cliente_api/http.py` |

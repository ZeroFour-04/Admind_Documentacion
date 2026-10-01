---
resumen: "Mapa del código: qué hay en cada carpeta de los tres repos, qué hace cada app del backend y qué nota la explica."
tipo: arquitectura
origen: "guía de estructura §2 y §5.5 (2026-09-30)"
actualizado: 2026-09-30
---

# Mapa del código

Las rutas son relativas a la carpeta del espacio de trabajo (`A D M I N D/`).

```text
A D M I N D/
├── Backend/Admind_Backend/          ← repo GitHub ZeroFour-04/Admind_Backend   (la API, puerto 8000)
│   ├── config/                      ← ajustes del proyecto y rutas principales
│   ├── apps/                        ← un módulo por tema del negocio
│   │   ├── comun/                   ← piezas compartidas: aislamiento, modelo base, bloqueo
│   │   ├── personas/ cuentas/ conjuntos/ permisos/ unidades/
│   │   ├── areas/ reglas/ reservas/ anuncios/ notificaciones/ auditoria/
│   │   └── casos/ citas/ pagos/ …   ← solo README: módulos futuros, sin código
│   ├── tests/                       ← pruebas transversales (aislamiento, concurrencia, esquema)
│   ├── bd/                          ← notas sobre la base de datos
│   ├── manage.py  requirements.txt  pytest.ini  .env
│
├── Frontend/Admind_Front-End/       ← repo GitHub ZeroFour-04/Admind_Front-End (las pantallas, puerto 8001)
│   ├── config/                      ← ajustes (sin base de datos) y rutas principales
│   ├── cliente_api/                 ← el "mesero": funciones que llaman a la API
│   ├── apps/                        ← un módulo por sección de la interfaz: vistas, formularios, plantillas
│   ├── templates/base/              ← el esqueleto de toda página
│   ├── templates/componentes/       ← piezas reutilizables: barra, lateral, campo, confirmación
│   ├── static/css  static/js        ← estilos propios y el JavaScript: reservas.js, identidad.js, usuarios.js y vendor/alpine.min.js
│   ├── design-system/               ← tokens de color, tipografía y componentes CSS (de Claude Design)
│   └── tests/                       ← pruebas de pantallas con la API simulada
│
├── Documentacion/Admind_Documentacion/  ← repo de documentación (esta bóveda de Obsidian)
├── Backend.zip                      ← la demo descartada de septiembre. No se usa
└── .claude/launch.json              ← cómo arranca Claude los dos servidores
```

Cada carpeta de `apps/` tiene un `README.md` que dice para qué existe. Las apps que **solo** tienen README (`casos`, `citas`, `pagos`, `visitantes`, `infracciones`, `documentos`, `parqueaderos`, `triage` en el back, `importacion_respaldo`) son el lugar reservado para historias futuras.

## Apps del backend

| App | Qué guarda / hace | Endpoints principales | HU |
|---|---|---|---|
| `personas` | `Persona` global, única por tipo y número de documento (normalizado) | `GET /personas/buscar/`, `POST /personas/vincular/` | HU-04, HU-07 |
| `cuentas` | `Usuario` (entra con correo), `TokenDeSesion`, 2FA, recuperación, usuarios del conjunto | `/auth/login/`, `/auth/logout/`, `/auth/conjuntos/`, `/auth/conjunto-activo/`, `/auth/usuarios/…` (incluye `perfil/`, `<id>/eliminar/` y `<id>/roles/<asignación>/cambiar/`), `/auth/recuperar/…`, `/auth/dos-factores/…` | HU-01, HU-02, HU-06, HU-26 |
| `conjuntos` | `Conjunto` (acento y `color_personalizado`), `LogoDeConjunto` (la foto 1:1), asistente de creación | `POST /conjuntos/`, `/conjuntos/actual/…` (activar, identidad, logo), `/conjuntos/logos/<huella>/` | HU-03, HU-21 |
| `permisos` | Catálogo de 5 roles, `Asignacion` (un rol vigente por persona y conjunto), permisos efectivos | (se usan desde `cuentas`: `/auth/usuarios/<id>/roles/`) | HU-06 |
| `unidades` | `Unidad` (apartamento) y `VinculoUnidad` (propietario, reside…) con histórico; a quién avisar de qué | `/unidades/`, `/unidades/<id>/vinculos/…` | HU-08 |
| `areas` | `Area` común: clasificación cerrada, horario por bloques, mantenimiento | `/areas/`, `/areas/<id>/`, `/areas/<id>/desactivar/` | HU-09 |
| `reglas` | Reglas **beta** configurables y versionadas; reglas **alfa** fijas; el evaluador | `/reglas/`, `/reglas/<id>/`, `/reglas/<id>/retirar/` | HU-10, HU-13 |
| `reservas` | `Solicitud`: franjas, bloqueo de 3 min, envío y evaluación | `/reservas/franjas/`, `/reservas/solicitudes/…` | HU-11, HU-12, HU-13 |
| `anuncios` | Anuncios del conjunto o de una vivienda | `/anuncios/`, `/anuncios/<id>/` | HU-25 |
| `notificaciones` | Bandeja en la app + correo; `canal.notificar(aviso, personas)` | `GET /notificaciones/` | HU-25, HU-08 |
| `auditoria` | Registro de solo inserción | (sin endpoints: lo usan los servicios) | transversal |
| `comun` | Aislamiento, modelo base, bloqueo | — | HU-05, HU-11 |

Las pantallas del front, sección por sección, están en [frontend](frontend.md).

## De la app a su nota

| App | Nota con sus reglas de negocio |
|---|---|
| `reservas` | [reservas](../05_Modulos/reservas.md) |
| `reglas` | [motor_reglas](../05_Modulos/motor_reglas.md) |
| `personas` | [personas](../05_Modulos/personas.md) |
| `permisos` | [permisos](../05_Modulos/permisos.md) |
| `cuentas` | [cuentas](../05_Modulos/cuentas.md) |
| `conjuntos` | [conjuntos](../05_Modulos/conjuntos.md) |
| `unidades` | [unidades](../05_Modulos/unidades.md) |
| `parqueaderos` | [parqueaderos](../05_Modulos/parqueaderos.md) |
| `triage, anuncios` | [triage](../05_Modulos/triage.md) |
| `infracciones` | [infracciones](../05_Modulos/infracciones.md) |
| `citas` | [citas](../05_Modulos/citas.md) |
| `comun/aislamiento` | [aislamiento](../03_Reglas/aislamiento.md) |
| `comun/bloqueo, auditoria` | [backend](backend.md) |

---
resumen: "Tecnologías y versiones en uso, y por qué Django, PostgreSQL y las cuatro piezas técnicas propias de AdMind."
tipo: arquitectura
origen: "guía de estructura §4.1 (2026-09-30) + maestro v1.4 (2026-09-14) §7.1 y §7.2"
actualizado: 2026-09-30
---

# Stack técnico

> [!WARNING] Decisiones posteriores al texto del maestro
> - **Frontend:** está construido sobre plantillas de Django + Alpine.js (elegido por Alejo el 2026-09-13). El aviso *Decisión bloqueada* de abajo y §12.1 siguen abiertos solo por escrito.
> - **Sesión entre front y API:** token opaco con registro en la base (2026-09-15). Resuelve §12.7 b.
> - **Docker** no se usa: PostgreSQL 18 nativo ([entorno_local](entorno_local.md)).
>
> Detalle en [construccion](../06_Decisiones/construccion.md).

## Versiones en uso (2026-09-30)

| Tecnología | Versión | Dónde | Para qué |
|---|---|---|---|
| **Python** | 3.14 | back y front | El lenguaje de todo el proyecto |
| **Django** | 5.2.17 (LTS) | back y front | Framework web: rutas, vistas, modelos, plantillas, sesiones, formularios |
| **Django REST Framework (DRF)** | 3.18 | back | Convierte Django en una API JSON: vistas `APIView`, serializers, autenticación, permisos |
| **PostgreSQL** | 18, nativo en Windows | back | La base de datos. Su motor hace cumplir reglas (restricciones, índices únicos parciales, FK compuestas) |
| **psycopg** | 3.3 | back | El "cable" entre Django y PostgreSQL |
| **python-dotenv** | 1.2 | back y front | Lee `.env` para no escribir contraseñas en el código |
| **django-otp** + **qrcode** | 1.7 / 8.2 | back | Segundo factor (códigos de 6 dígitos tipo Google Authenticator) y su QR |
| **requests** | 2.34 | front | Hace las peticiones HTTP del front a la API |
| **Plantillas de Django** | — | front | Generan el HTML en el servidor |
| **Alpine.js** | 3.17.4 | front | Interactividad pequeña dentro del HTML (hoy, en la solicitud de reserva y en el color y la foto del conjunto) |
| **CSS propio** (design system) | — | front | Colores, tipografías (Archivo e Inter) y componentes `am-*`. Sin Tailwind ni Bootstrap |
| **pytest** + **pytest-django** | 9.1 / 4.14 | back y front | Pruebas automáticas |
| **Git + GitHub** | — | los tres repos | Ramas `main`, `desarrollo`, `pruebas` (las fijó el profesor) |

## Por qué este stack (maestro §7)

> [!DANGER] Decisión bloqueada — leer antes de escribir cualquier código **El frontend está definido de dos formas incompatibles en documentos ambos vigentes.** Ver §12.1. Hasta que el equipo cierre esto, ningún agente debe asumir uno u otro.

### 7.1 Lo que sí está cerrado

**Backend: Django 5.2 LTS + Django REST Framework + PostgreSQL 16+.**

Por qué Django y no FastAPI — la comparación no se gana con "cuál es más moderno" sino con qué exige AdMind:

|Lo que el diseño exige|Django|FastAPI|
|---|---|---|
|Autenticación, hash, sesiones, recuperación|De fábrica|Desde cero|
|Catálogo de permisos y comprobación por vista|Sí|Desde cero|
|Migraciones versionadas|`makemigrations`|Alembic a mano|
|Panel para cargar datos semilla|`django-admin`|No existe|
|2FA TOTP|`django-otp`, maduro|Librería suelta|
|ORM con managers personalizables (el filtro por conjunto)|Sí|SQLAlchemy, más manual|

El Sprint 1 completo —login, 2FA, roles, conjunto activo, 25 SP— es en Django mayoritariamente configuración y modelos. En FastAPI es construir autenticación desde cero mientras se aprende POO.

_Contrapunto listo para el jurado:_ FastAPI es más rápido y tiene `async` nativo, pero **nada de eso es el cuello de botella de AdMind** — la latencia la decide la transacción en PostgreSQL, idéntica en ambos. Se eligió por identidad, permisos, auditoría y migraciones, no por benchmarks que no aplican.

**Por qué la 5.2 y no la 6.1:** LTS con soporte hasta abril de 2028 contra abril de 2027, y más de un año de material acumulado. Para aprender, la versión con más material gana a la más nueva.

**Por qué PostgreSQL desde el día 1 y nunca SQLite.** Tres cosas que SQLite no da:

- **Índice único parcial** (`UNIQUE ... WHERE estado IN (...)`) para la solicitud bloqueante — R7
- **Llaves foráneas compuestas** contra claves únicas compuestas — el corazón del blindaje R6
- **Privilegios por tabla** para que la aplicación no tenga `UPDATE` ni `DELETE` sobre auditoría

Desarrollar en SQLite y migrar después es descubrir en el Sprint 5 que la mitad de los invariantes no se pueden implementar.

> [!NOTE] Entorno real de la máquina de desarrollo (verificado el 2026-09-11)
> Python **3.14.3**, el único instalado — Django 5.2 lo soporta desde el parche **5.2.8** · Git 2.53 · **Docker no instalado** · **PostgreSQL 18** corriendo como servicio de Windows `postgresql-x64-18` en el puerto 5432 · terminal por defecto, PowerShell.
>
> El Postgres nativo ya da las tres cosas que el diseño exige, así que **no bloquea el arranque ni la Fase 0**. Docker sigue siendo deseable para que los dos entornos sean idénticos; queda como pendiente de infraestructura, no como requisito previo.

> [!TIP] FK compuestas en Django — el detalle técnico que va a preguntar el jurado `CompositePrimaryKey` de Django 5.2 **no es lo que se necesita y además rompe el admin**. El caso es una FK compuesta contra una **clave única**, con PK UUID normal. Tres piezas:
> 
> 1. FK normal (`area = models.ForeignKey(Area, ...)`) más el campo `conjunto`
> 2. `UniqueConstraint(fields=["id", "conjunto"])` en el modelo padre
> 3. Una migración con `RunSQL` que añade `ALTER TABLE ... ADD CONSTRAINT ... FOREIGN KEY (area_id, conjunto_id) REFERENCES areas (id, conjunto_id)`
> 
> Django no sabe que esa restricción existe; **PostgreSQL sí, y la impone**. Va como ADR.

**Otras piezas cerradas:** pruebas con `pytest` + `pytest-django` y `factory-boy` · entorno con Docker Compose · Git + GitHub + GitHub Projects · correo por **SMTP** con contraseña de aplicación en variables de entorno, nunca en el repositorio · OAuth descartado a favor de usuario/contraseña + TOTP.

### 7.2 Piezas técnicas que solo AdMind necesita

Aquí no hay tutorial que copiar. **Esta parte es el proyecto**, y es lo que se sustenta.

1. **Aislamiento multiconjunto (R6).** Middleware que resuelve el conjunto activo desde la sesión; `Manager` base que inyecta el filtro; ningún controlador acepta `conjunto_id`. Más la prueba transversal de tablas globales (R12)
2. **Transacciones y concurrencia (R1, R7).** `transaction.atomic`, `select_for_update`, índice único parcial como red de seguridad. Prueba obligatoria: N solicitudes simultáneas producen exactamente un bloqueo
3. **Auditoría de solo inserción.** No es código: son **privilegios de PostgreSQL**, en una migración con `RunSQL`, probados intentando un `UPDATE` que debe fallar
4. **2FA para permisos sensibles.** `django-otp` más un permiso de DRF que verifique el 2FA cuando el permiso está marcado como sensible

## Ver también

- [abiertas](../06_Decisiones/abiertas.md) — maestro §12.1
- [riesgos](../06_Decisiones/riesgos.md) — R1, R6, R7, R12

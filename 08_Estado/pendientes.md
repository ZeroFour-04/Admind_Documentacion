---
resumen: "Lista de pendientes: lo que frena los story points, lo que hay que corregir en Notion, decisiones de equipo y pendientes técnicos."
tipo: estado
origen: "informe por sprints §4 a §6 (2026-09-29) + avance §6 (2026-09-27)"
actualizado: 2026-10-05
---

# Pendientes

Lo más urgente, ya resumido, está en [estado_actual](estado_actual.md). Aquí va la lista completa.

## Qué frena que se cuenten SP (2026-09-29)

1. **La rama `pruebas` del backend no existe en GitHub** (solo en local). Sin ella no se puede abrir el PR `desarrollo → pruebas`. En el front sí existe, pero está igual a `main`.
2. **Falta la revisión y la prueba manual de Camilo.** Casi todos los commits son tuyos, así que le toca a Camilo. El guion de prueba manual de HU-06 a HU-13 está en `07_Planes/hechos/Admind_Plan_Sprints_2_3.md` §6.
3. **Falta decidir el alcance** que entra antes de la entrega (maestro §12.8). Con unos 15 días, lo natural es HU-14. Queda por ver si se suma algo más del Sprint 4.
4. **HU-03 depende del reglamento (HU-33).** Hay dos caminos: construir un reglamento mínimo, o aceptar la historia con ese requisito pendiente. Esa decisión es tuya.

## Por corregir en Notion (2026-09-29)

Esto sale de lo que registran los documentos locales, no de Notion:

- **HU-06 a HU-13:** quedaron en "En revisión" el 27/09. Si Camilo las vuelve a marcar "Finalizado" sin PR ni prueba manual (ya pasó dos veces con HU-06), el estado no sería real.
- **HU-01, HU-02, HU-04, HU-05 y HU-26:** en Notion seguían "En progreso" y con fracciones viejas de tareas. Tienen todas sus tareas hechas.
- **HU-21 y HU-25:** probablemente siguen "Sin empezar" y están construidas.
    - Además, los criterios de HU-21 se reescribieron el 22/09 en términos de los 8 acentos ("slug"). El cambio de hoy vuelve al hex libre, así que otra vez no coinciden con el código.
- **Sprint 1:** no tiene fechas, y HU-01, HU-05 y HU-26 no tienen responsable. La DoD necesita saber quién programó cada historia para saber quién la prueba.

## Otros pendientes (2026-09-29)

- **Seguridad:** la contraseña real de la base está en GitHub, en el `.env _ejemplo` del backend y en `Credenciales/` del repositorio de documentación. Borrar esos archivos no la saca del historial, así que hay que cambiar la contraseña.
- **Documentación desactualizada:**
    - [historias_evidencia](historias_evidencia.md) sigue con el estado viejo de las historias del Sprint 1; la tabla de [historias](historias.md) se actualizó el 2026-09-30.
    - La guía de estructura dice que HU-21 está "sin commit", y ya está commiteada.
    - En el repositorio de documentación quedan sin commit la guía nueva y `Notas/Desarrollo 22-09.md`.
- **Maestro:** le faltan decisiones ya tomadas al construir: el estado `LIBERADA`, un solo bloqueo por persona y conjunto, el catálogo de reglas beta, el token con registro en la base, el stack del front y el color propio de HU-21.

Sobre el punto de seguridad: el 2026-09-30 Alejo decidió dejar `Credenciales/` en el repositorio de documentación porque es privado.

## Lista larga (corte 2026-09-27)

Referencias sin nombre de documento (*§2*, *§4*, *§6*…) son del antiguo `Admind_Avance.md`: §2 → [inventario_codigo](inventario_codigo.md) · §3 → [bitacora](bitacora.md) · §4 → [construccion](../06_Decisiones/construccion.md) · §5 → [historias](historias.md) y [historias_evidencia](historias_evidencia.md) · §6 → [pendientes](pendientes.md). *Maestro §N* se resuelve en `Admin_Master.md`. *El plan* es `07_Planes/hechos/Admind_Plan_Sprints_2_3.md`.

**Decisiones de equipo:**
- [ ] Fecha exacta de entrega y qué historias entran en el mes (maestro §12.8). Sin esto no se puede planear el Sprint 1
- [ ] Stack del frontend (maestro §12.1). Desde el 2026-09-15 el front ya está construido sobre plantillas de Django; si el equipo cierra por otro camino, se rehace
- [ ] ¿Reglas y anuncios se pueden eliminar? Las maquetas quitaron "Eliminar" del borrador hasta decidirlo (§4)
- [ ] Alcance de "HU-03 mínima" (paso 7). Propuesta del agente: crear el conjunto con sus datos básicos y asignarle administrador, dejando la validación completa de activación para cuando existan áreas, reglamento y reglas
- [ ] Confirmar que `vigencia_hasta` es **el primer día sin el rol** (así está en `Asignacion.objects.vigentes()`): con la fecha de hoy, el rol se pierde de inmediato
- [ ] ¿Se ocultan del selector los conjuntos no operativos? Hoy el selector solo excluye los desactivados, como dice HU-26
- [ ] Pasar HU-05 a "En revisión" en Notion cuando exista el PR `desarrollo → pruebas`

**Choques entre el esquema de diseño (base `admind`) y el maestro**, a decidir antes de construir la app que los toca:
- [x] `asignacion.conjunto_id` es `NOT NULL`, pero el maestro lo deja nulo para el Superusuario (§5.3) — resuelto el 2026-09-15 a favor del maestro (§4)
- [x] Roles y permisos como tablas, contra "catálogos fijos en código" (§5.3) — resuelto el 2026-09-15 a favor del maestro (§4)
- [ ] Estados de `reserva` con nombres distintos a los del maestro — app `reservas`
- [x] `area_comun` sin `clasificacion` (§3.1) — resuelto el 2026-10-05: la clasificación se eliminó de las áreas
- [ ] No hay tablas de reglas (§5.10) ni de notificaciones
- [ ] Columnas `registrado_por`, `decidido_por`, `priorizado_por` y `anulado_por` sin FK ni destino claro (¿persona o usuario?). Mientras tanto `Asignacion` se creó sin `registrado_por`
- [ ] `auditoria` sin `via_superusuario` (§5.3)

**Diferencias entre el código y el maestro**, a llevar al maestro o corregir en el código:
- [ ] Lista cerrada de tablas globales: el código agrega `conjuntos_conjunto`, `cuentas_tokendesesion`, `cuentas_usuario_groups` y `cuentas_usuario_user_permissions`, y admite `conjunto_id` nulo en `permisos_asignacion`. El maestro §5.4 solo nombra `Persona`, `Usuario` y los catálogos de roles y permisos, y su R12 todavía dice "falta escribir la lista cerrada"
- [ ] Reparto de permisos por rol en `catalogo.py`: interpretado del maestro §5.3, provisional hasta validarlo con un administrador real (maestro §11.4)
- [ ] Maestro §12.7 b (token contra sesión): resuelto en el código a favor del token con registro en la base (§4). Falta cerrarlo en el maestro y en los README de `cliente_api/` y `config/` del front, que lo siguen teniendo como pendiente aunque el front ya lo implementa
- [ ] El maestro §5.4 y §7.2 hablan de "middleware"; en el código es `VistaDeConjunto` (§4)
- [ ] El README de `apps/conjuntos` dice que ahí va el cambio de conjunto activo; quedó en `apps/cuentas`
- [ ] HU-26 pide logo y color en el selector; están fuera de v1 (maestro §6.3, ya registrado en §12.3)
- [ ] Quedaron desactualizados el README raíz del front ("Todavía no hay código") y la Guía de desarrollo §13 ("el proyecto Django del frontend no existe")

**Del plan de los Sprints 2 y 3 (2026-09-27):**
- [ ] Revisar los 15 commits del backend y los 9 del front, y subirlos (el agente no hace push)
- [ ] Volver a crear la rama `pruebas` del backend en GitHub y abrir los PR `desarrollo → pruebas`, revisados por quien no programó (plan §5)
- [ ] Prueba manual de HU-06 a HU-13 con el guion del plan §6, por quien no las programó. El agente no pudo recorrerlas en el navegador: pide iniciar sesión con las cuentas de prueba
- [ ] Llevar al maestro D2 (`LIBERADA`), D3 (bloqueo por conjunto) y D4 (catálogo beta y versionado): §5.1, §5.10 y §12.7 c
- [x] Notion: HU-06 a HU-13 en "En revisión", con casillas y nota de revisión; tareas 4 y 5 de HU-06 restauradas — hecho el 2026-09-27 17:50
- [ ] `alpine.min.js` se versionó con `core.autocrlf=true`: en otra máquina con Windows el archivo puede quedar con CRLF y su SHA-256 no coincidir con el del README de `vendor/`. Un `.gitattributes` con `*.js -text` para `vendor/` lo evitaría
- [ ] El límite de búsquedas cuenta por conjunto: un administrador de dos conjuntos puede hacer 20 en cada uno. Decidir si debe ser global
- [ ] Fuera del plan, sin hacer: la lista, el detalle y el alta de usuarios del front no sobreescribían `estado_vista` y mostraban "Maqueta"; se corrigió en la lista y el detalle porque el plan las tocaba, pero `usuarios/nuevo.html` sigue mostrándola

**Técnicos:**
- [x] Commit del paso 6 del backend (selector, `VistaDeConjunto`, permisos efectivos, prueba del intruso) — `d9b6271`
- [x] Subir `81f6298` y la actualización de las 09:00 del repositorio de documentación — `c556285`, en `origin/main`
- [ ] Commit y subida de las actualizaciones de las 09:25, las 10:13 y las 10:35 de este archivo
- [x] Commit del front (proyecto, login y maquetas) — `557bc9f`, en `origin/desarrollo`. El mensaje no lleva `[HU-01]`
- [ ] Pruebas automáticas del front en `tests/` (`pytest-django` con la API simulada). Hoy solo existe un script fuera del repositorio
- [x] En Notion: marcar la tarea "Pantalla de login y manejo de errores" de HU-01 — hecho el 2026-09-15 10:34
- [ ] Conectar el selector a la API (`GET /auth/conjuntos/`, `POST /auth/conjunto-activo/`) y mostrar el conjunto activo real en la barra. Para probarlo, el usuario de prueba necesita un conjunto y una asignación
- [ ] Camilo: crear el `.venv` del front, instalar `requirements.txt` y armar su `.env` a partir de `.env _ejemplo`
- [ ] Decidir con Camilo qué pasa con `index.html` y `apps/Administrador/Home.html` del front: HTML de prueba fuera de la estructura (§2.4)
- [ ] **Contraseñas en los repositorios**: `.env _ejemplo` del backend trae un valor en `DB_PASSWORD`, y el repositorio de documentación versiona `Credenciales/`. Quitarlas no las borra del historial: hay que cambiar la contraseña
- [x] Subir a `origin/desarrollo` los commits del backend — `desarrollo` al día hasta `d9b6271`
- [x] Instalar `pytest` y `pytest-django` y escribir las pruebas de HU-04 — `dc6a414`
- [ ] Declarar la capa de servicios en `apps/README.md`, que todavía describe el flujo vista → modelo. Ya hay `servicios.py` en `cuentas` y `permisos`
- [x] Commit de este archivo y de los cambios del maestro en el repositorio de documentación — `b08754f`
- [x] En Notion: pasar a "En progreso" las historias con avance (ninguna a Terminada, aunque los mensajes de commit digan "completada" o "hechos") — HU-01, HU-03, HU-04, HU-05 y HU-06 a las 05:55; HU-02 y HU-26 a las 09:00
- [x] En Notion: corregir la lista de tipos de documento de HU-04 — hecho el 2026-09-15
- [x] En Notion: marcar las tareas técnicas hechas — hecho el 2026-09-15 09:00
- [ ] Darle `CREATEDB` al `admind_user` de Camilo y correr `migrate` en su máquina: sin eso `pytest` no puede crear la base de pruebas
- [ ] Clase de permiso por vista ("esta vista exige `reserva.aprobar`"): hoy ninguna vista exige un permiso concreto (HU-06)
- [x] Recuperación de contraseña por correo (HU-01): límite de 3 enlaces por hora, SMTP real y pruebas del front — hecho el 2026-10-05 ([Plan_Recuperacion_Contrasena](../07_Planes/hechos/Plan_Recuperacion_Contrasena.md)). Falta la prueba manual de la DoD
- [ ] `send_mail` de la recuperación es síncrono y sin `try` ni `EMAIL_TIMEOUT`: con SMTP real, si el servidor de correo falla, `/auth/recuperar/` responde 500 solo cuando la cuenta existe, y tarda más que con un correo inexistente (deja adivinar qué correos están registrados)
- [ ] `/auth/login/` no limita los intentos de contraseña
- [ ] El límite de enlaces de recuperación vive en memoria: se pierde al reiniciar y no se comparte entre procesos. Una tabla global o una caché compartida lo arreglaría (decisión D3 del plan)
- [x] Flujo de 2FA en el front (HU-02) — ya existe: pantallas de configurar, verificar y códigos de respaldo en `apps/cuentas/` (visto el 2026-10-05)
- [ ] HU-27 (visitantes, de Camilo) está parcial: falta registrar la salida, la finalidad declarada, la autorización y el plazo de retención (Ley 1581, R2), el parqueadero de visitantes (HU-28) y el aviso a quienes residen en el apartamento
- [ ] `apps/visitantes/views.py` del backend consulta y crea con el ORM directo: no hay `servicios.py`, no deja registro en la auditoría y la regla "solo Vigilancia registra" vive en la vista ([capas](../03_Reglas/capas.md)). Es de Camilo: se le avisa
- [ ] Los `README.md` de `apps/visitantes/` (back y front) describen el alcance previsto, no lo construido: les falta la ruta `/visitantes/` y lo que quedó pendiente
- [ ] Enlace para quitar el segundo factor (HU-02, 2026-10-05): falta recorrerlo a mano con la API encendida y un correo real, y hacer el commit en los dos repositorios
- [ ] Quitar el segundo factor y restablecer la contraseña no dejan registro en la auditoría: `apps/auditoria/` escribe en el conjunto activo y esas rutas no tienen ninguno. Registrarlo pide una tabla global (R12), que es decisión de equipo
- [ ] El envío del enlace del segundo factor comparte el hueco del de la contraseña: `send_mail` síncrono y sin `try`; si el servidor de correo falla, la ruta responde 500
- [ ] Comando que borre los tokens vencidos: dejan de servir, pero se acumulan en `cuentas_tokendesesion`
- [ ] Índices compuestos `(conjunto_id, …)` para consultas concretas, con cada tabla del producto que herede de `ModeloDeConjunto`
- [x] Paso 5 del plan del Sprint 1: login con token — `0b0c4f8`

---
resumen: "Lista de pendientes: lo que frena los story points, lo que hay que corregir en Notion, decisiones de equipo y pendientes técnicos."
tipo: estado
origen: "informe por sprints §4 a §6 (2026-09-29) + avance §6 (2026-09-27)"
actualizado: 2026-10-06
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

## Anuncios con fotos (2026-10-05)

Lo que el agente no pudo hacer al cerrar [Plan_Anuncios_Con_Fotos](../07_Planes/hechos/Plan_Anuncios_Con_Fotos.md):

- [ ] **Commits** en `desarrollo` de los dos repositorios. El plan trae los cuatro mensajes sugeridos; la migración `anuncios/0002_fotos` va en el mismo commit que el modelo.
- [ ] **Prueba manual** con los dos servidores y usuarios reales, con el guion del plan. El agente no tiene la contraseña ni el segundo factor de los usuarios de prueba, y publicar en `admind_db` manda correo real.
- [ ] **Avisarle a Camilo:** hay una migración nueva en `anuncios` (correr `migrate`) y la respuesta de `/anuncios/` ahora trae `fotos`.
- [ ] **Notion:** anotar en HU-25 que ahora lleva fotos.
- [ ] PR `desarrollo → pruebas` revisado, como el resto de las historias.

## Estructura de viviendas, HU-39 (2026-10-06)

Historia nueva, definida con Alejo tras la retroalimentación del docente. Sin construir.

- [ ] **Alejo:** responder D1 a D5 de [Plan_Estructura_De_Viviendas](../07_Planes/activos/Plan_Estructura_De_Viviendas.md) y ejecutarlo.
- [ ] **Notion:** crear HU-39 con los criterios que están en [historias](historias.md), y ponerle sprint, puntos y prioridad. El agente no toca Notion.
- [ ] **Avisarle a Camilo:** hay una historia nueva; el plan trae una migración en `unidades`, tres rutas nuevas en `/unidades/` y el asistente pasa de 5 a 6 pasos.
- [ ] **Segunda parte de HU-39**, sin plan todavía: las palabras del conjunto en las pantallas («Apartamento» está fijo en unas 70 menciones de 12 plantillas), el listado agrupado, registrar una vivienda a mano dentro de una agrupación, y retirar viviendas y agrupaciones con confirmación.
- [ ] **Decidir** los tres puntos que quedan de [abiertas](../06_Decisiones/abiertas.md) 12.9: persona principal, cómo se cumple lo legal con los datos de quienes se mudan, y retiro de varias viviendas a la vez.

## Habitantes de la vivienda (2026-10-06)

Alejo decidió el tercer tipo de vínculo, `habitante` ([construccion](../06_Decisiones/construccion.md), [unidades](../05_Modulos/unidades.md)). Sin historia, sin plan y sin construir.

- [ ] **Orden:** las zonas con ingreso dependen de esto. Propuesta del agente, sin decidir: que sea la primera fase del plan de ingresos. Qué entra antes de la entrega lo decide Alejo.
- [ ] **Lo legal, antes de construir la pantalla:** qué finalidad se declara, quién autoriza el registro (el adulto responsable, si es un menor) y cuánto tiempo se conserva ([legal](../01_Contexto/legal.md) §4.2). Las pantallas de registro de hoy tampoco muestran la autorización.
- [ ] **Avisarle a Camilo:** un tipo nuevo de vínculo, una migración en `unidades` y una operación que crea una persona sin cuenta.
- [ ] **Historia y Notion:** no tiene historia. El agente no toca Notion.

## Motor de reglas y zonas con ingreso (2026-10-06)

Definición nueva con Alejo: [motor_reglas](../05_Modulos/motor_reglas.md) e [ingresos](../05_Modulos/ingresos.md). El motor para las áreas con reserva se construyó el 2026-10-06; el ingreso sigue sin construir.

- [ ] **Alejo:** confirmar los supuestos del agente (están al final de las dos notas) y decidir los puntos de [abiertas](../06_Decisiones/abiertas.md) 12.10.
- [ ] **Definir la creación de conjuntos** con las reglas nuevas: qué paso del asistente llena las alfa y qué exige para quedar operativo.
- [ ] **Avisarle a Camilo:** alfa y beta cambiaron de significado; hay una funcionalidad nueva que usa el rol Vigilancia, pide un permiso nuevo y se parece a HU-27.
- [ ] **Historia y Notion:** el ingreso a zonas no tiene historia, y los criterios de HU-09, HU-10 y HU-13 describen el modelo anterior. El agente no toca Notion.
- [x] **Alejo:** responder D1 a D4 de [Plan_Motor_De_Reglas](../07_Planes/activos/Plan_Motor_De_Reglas.md) y ejecutarlo — respondidas (las cuatro en a) y construido por el agente el 2026-10-06, fases F0 a F5. El ingreso a zonas todavía no tiene plan.
- [ ] **Alejo, para cerrar el plan del motor:** correr `migrate` en `admind_db` (bloque B3.6 del plan): aplica `areas/0004` y `reglas/0002` a `0004`, **cierra todas las reglas que había** y deja con aforo 1 las áreas que no tenían regla de aforo. Después, poner el aforo real de cada área y volver a definir las reglas en el tablero.
- [ ] **Alejo:** revisar y hacer los commits del motor en los dos repositorios (el agente no hace commits sin que se los pidan; los mensajes sugeridos están al cierre de cada fase del plan). Sin `push` hasta probarlo.
- [ ] **Prueba manual** del motor con el guion del final del plan (11 pasos). El agente recorrió las pantallas del front contra una API con la base de pruebas, sin usuarios reales ni navegador.
- [ ] **Avisarle a Camilo, del motor:** crear un área ahora exige `aforo_maximo` y hay migración en `areas`; `migrate` cierra las reglas que tenía definidas y hay que volver a definirlas; la pantalla de reglas cambió, y `POST /reglas/` ya no exige `area` (va solo en las reglas de un área) y responde `409` si la regla ya está definida.
- [ ] **Pagos:** *paz y salvo* y *día límite de pago* no tienen efecto hasta que exista el módulo (HU-16, HU-35), que además necesita la cuota mensual por vivienda (maestro §11.5).
- [ ] **Texto de diseño:** el maestro §5.10 y [alcance](../01_Contexto/alcance.md) 3.1 siguen con el modelo anterior; solo llevan el aviso.
- [ ] **READMEs del código:** el de `apps/reglas/` del Backend se corrigió el 2026-10-06. Sigue sin tocar `Backend/Admind_Backend/apps/conjuntos/README.md`, que dice que áreas y reglas cuentan como no cumplidas y que la auditoría «llega con `apps/auditoria/`», que ya existe.

## Asistente de creación completo (2026-10-06)

Tres planes abiertos el mismo día tocan el asistente; el orden está en [planes](../07_Planes/planes.md).

- [ ] **Alejo:** responder D1 a D5 de [Plan_Asistente_De_Creacion](../07_Planes/activos/Plan_Asistente_De_Creacion.md).
- [ ] **Alejo, confirmar el choque sobre *días que no abre*.** En el chat del asistente respondió que el motivo y los periodos quedaban para después; [Plan_Motor_De_Reglas](../07_Planes/activos/Plan_Motor_De_Reglas.md) los construye (B2.3, B4.4 y F5). El 2026-10-06 pidió ejecutar el plan y respondió D2 a, así que **quedaron construidos**. Falta que confirme que así lo quería; el agente no lo preguntó antes de construir porque no había leído esta nota.
- [ ] **Avisarle a Camilo:** hay una app nueva, `documentos`, registrada en `config/`; el asistente pasa a siete pasos; y un conjunto ya puede quedar operativo.
- [ ] **Decidir** si reservar exige que el conjunto esté operativo. Hoy no se revisa (plan D7 a del 27/09) y hasta ahora no importaba, porque ninguno podía estarlo.

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

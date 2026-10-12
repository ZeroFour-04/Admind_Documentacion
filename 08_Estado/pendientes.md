---
resumen: "Lista de pendientes: lo que frena los story points, lo que hay que corregir en Notion, decisiones de equipo y pendientes técnicos."
tipo: estado
origen: "informe por sprints §4 a §6 (2026-09-29) + avance §6 (2026-09-27)"
actualizado: 2026-10-11
---

# Pendientes

Lo más urgente, ya resumido, está en [estado_actual](estado_actual.md). Aquí va la lista completa.

## Qué frena que se cuenten SP (2026-09-29)

1. **La rama `pruebas` del backend no existe en GitHub** (solo en local). Sin ella no se puede abrir el PR `desarrollo → pruebas`. En el front sí existe, pero está igual a `main`.
2. **Falta la revisión y la prueba manual de Camilo.** Casi todos los commits son tuyos, así que le toca a Camilo. El guion de prueba manual de HU-06 a HU-13 está en `07_Planes/hechos/Admind_Plan_Sprints_2_3.md` §6.
3. **Falta decidir el alcance** que entra antes de la entrega (maestro §12.8). Con unos 15 días, lo natural es HU-14. Queda por ver si se suma algo más del Sprint 4.
4. **HU-03 depende del reglamento (HU-33).** Hay dos caminos: construir un reglamento mínimo, o aceptar la historia con ese requisito pendiente. Esa decisión es tuya. **Resuelto el 2026-10-06:** se construyó el reglamento mínimo y un conjunto ya puede quedar operativo.

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

Historia nueva, definida con Alejo tras la retroalimentación del docente. La primera parte se construyó el 2026-10-06 y ya tiene commit.

- [x] **Alejo:** responder D1 a D5 de [Plan_Estructura_De_Viviendas](../07_Planes/activos/Plan_Estructura_De_Viviendas.md) y ejecutarlo. Respondió todas en a y lo construyó el agente (2026-10-06).
- [ ] **Alejo, para cerrar el plan de viviendas:** el `migrate` (`unidades/0002_estructura`) y los commits ya están (verificado el 2026-10-11); queda mover el plan a `hechos/` con Obsidian abierto.
- [ ] **Prueba manual** del paso «Viviendas» con el guion del final del plan (12 pasos). El JavaScript no tiene prueba automática: el agente lo comprobó con Node y en el panel del navegador con la página servida aparte, sin usuarios reales.
- [x] ~~**Notion:** crear HU-39 con los criterios que están en [historias](historias.md), y ponerle sprint, puntos y prioridad.~~ Creada el 2026-10-11 («En progreso», con sus criterios y su estado real); sprint, puntos y prioridad los pone el equipo. La «HU 39» de accesibilidad que ya existía pasó a HU-40.
- [ ] **Avisarle a Camilo:** hay una historia nueva; el plan trae una migración en `unidades`, tres rutas nuevas en `/unidades/` y el asistente pasa de 5 a 6 pasos.
- [ ] **Segunda parte de HU-39**, sin plan todavía: las palabras del conjunto en las pantallas («Apartamento» está fijo en unas 70 menciones de 12 plantillas), el listado agrupado, registrar una vivienda a mano dentro de una agrupación, y retirar viviendas y agrupaciones con confirmación.
- [ ] **Decidir** los tres puntos que quedan de [abiertas](../06_Decisiones/abiertas.md) 12.9: persona principal, cómo se cumple lo legal con los datos de quienes se mudan, y retiro de varias viviendas a la vez.

## Habitantes de la vivienda (2026-10-06)

Alejo decidió el tercer tipo de vínculo, `habitante` ([construccion](../06_Decisiones/construccion.md), [unidades](../05_Modulos/unidades.md)). Sin historia, sin plan y sin construir.

- [x] **Orden:** las zonas con ingreso dependen de esto. Propuesta del agente, sin decidir: que sea la primera fase del plan de ingresos. Qué entra antes de la entrega lo decide Alejo. — Decidido el 2026-10-08: **no entra** en el plan de ingresos; mientras no exista, la familia entra como acompañante de un titular. Sigue sin plan propio.
- [ ] **Lo legal, antes de construir la pantalla:** qué finalidad se declara, quién autoriza el registro (el adulto responsable, si es un menor) y cuánto tiempo se conserva ([legal](../01_Contexto/legal.md) §4.2). Las pantallas de registro de hoy tampoco muestran la autorización.
- [ ] **Avisarle a Camilo:** un tipo nuevo de vínculo, una migración en `unidades` y una operación que crea una persona sin cuenta.
- [ ] **Historia y Notion:** no tiene historia. El agente no toca Notion.

## Motor de reglas y zonas con ingreso (2026-10-06)

Definición nueva con Alejo: [motor_reglas](../05_Modulos/motor_reglas.md) e [ingresos](../05_Modulos/ingresos.md). El motor para las áreas con reserva se construyó el 2026-10-06; el ingreso sigue sin construir.

- [x] **Alejo, para destrabar el plan de ingresos:** verificar con la guía legal o el docente los tres puntos de [abiertas](../06_Decisiones/abiertas.md) 12.10 b (si la mora puede restringir el gimnasio o la piscina; finalidad, autorización y plazo de retención del registro de quién entra; la Ley 1209 de piscinas) y cambiar la D3 de [Plan_Zonas_Con_Ingreso](../07_Planes/hechos/Plan_Zonas_Con_Ingreso.md). Desde el 2026-10-08 el plan está escrito y **detenido** ahí.
- [x] **Alejo:** responder D5 a D9 del mismo plan: qué ve Vigilancia en el menú, quién corre las migraciones, las palabras en pantalla (12.10 d), qué pasa con los acompañantes si la regla no está definida, y tres supuestos que faltó preguntar.
- [ ] **Alejo:** confirmar los supuestos del agente (están al final de las dos notas) y decidir los puntos de [abiertas](../06_Decisiones/abiertas.md) 12.10. — El 2026-10-08 confirmó seis y decidió los permisos (12.10 c). Quedan 12.10 b y d, y los supuestos de la D9 del plan y del día límite de pago.
- [ ] **Definir la creación de conjuntos** con las reglas nuevas: qué paso del asistente llena las alfa y qué exige para quedar operativo.
- [ ] **Avisarle a Camilo:** alfa y beta cambiaron de significado; hay una funcionalidad nueva que usa el rol Vigilancia, pide un permiso nuevo y se parece a HU-27. Desde el 2026-10-08 los permisos son dos (`ingreso.registrar` e `ingreso.ver_historico`), y el plan, si D5 queda en a, cambia su prueba del lateral de `tests/test_visitantes.py`.
- [ ] **Historia y Notion:** el ingreso a zonas no tiene historia, y los criterios de HU-09, HU-10 y HU-13 describen el modelo anterior. El agente no toca Notion.
- [x] **Zonas con ingreso, construido el 2026-10-08** con [Plan_Zonas_Con_Ingreso](../07_Planes/hechos/Plan_Zonas_Con_Ingreso.md) (F0 a F7; ya con commit). Alejo no verificó lo legal y eligió construir con salvaguardas (D3 a); respondió D5 b, D6 a, D7 a, D8 a y D9 a.
- [ ] **Alejo, lo legal de las zonas con ingreso (12.10 b):** verificar con la guía legal o el docente los tres puntos, y **dar el texto del aviso de finalidad**. Hoy la pantalla de Vigilancia dice «Aviso de finalidad pendiente de la verificación legal»; se reemplaza en `AVISO_DE_FINALIDAD` de `Frontend/Admind_Front-End/apps/ingresos/views.py`. De la verificación sale también qué hacer con el historial al cumplirse el plazo de retención.
- [x] **Alejo, para cerrar el plan de ingresos:** el `migrate` (`areas/0005_modo_de_uso`, `reglas/0005_acompanantes` e `ingresos/0001_initial`) y los commits ya están (verificado el 2026-10-11). Las áreas que existían quedaron **con reserva**.
- [ ] **Prueba manual** de las zonas con ingreso con el guion del final del plan (12 pasos), por quien no las programó. El agente recorrió el front real contra la API real y la base de pruebas (25 comprobaciones) y revisó las pantallas a 360 px, pero **no a 200 % de zoom** ni con usuarios reales, y no esperó a que pasara el tiempo de una permanencia real (eso lo cubren las pruebas con la hora simulada).
- [ ] **Avisarle a Camilo, de las zonas con ingreso:** dos permisos nuevos (`ingreso.registrar` e `ingreso.ver_historico`); migraciones en `areas`, `reglas` e `ingresos`; `GET /areas/` trae `modo_uso` y `permanencia_maxima_minutos` y la duración de la franja puede llegar vacía; `POST /reservas/solicitudes/` responde 409 sobre un área con ingreso; una línea nueva en `config/` de cada repositorio (`INSTALLED_APPS` y `urls.py`); y la regla `ACOMPANANTES` en el catálogo de reglas. Con D5 b **no cambia** su prueba del lateral de `test_visitantes.py`.
- [ ] **Vigilancia ve «Zonas comunes» y «Reglas» en el menú, pero le responden sin permiso** (D5 b la dejó así a propósito). Si se decide quitarlos, cambia `test_vigilancia_solo_ve_las_secciones_permitidas_en_el_lateral`, que es de Camilo.
- [ ] **Historia y Notion:** el ingreso a zonas sigue sin historia ni número. El agente no toca Notion.
- [ ] **Fuera del plan de ingresos, para después:** el vínculo `habitante`, las reglas de piscina de la Ley 1209, depurar el historial al cumplirse la retención, que el vigilante confirme que quien venció de verdad salió, cambiar el modo de un área ya creada, cupos que se actualicen solos, áreas típicas con ingreso (gimnasio, piscina) en el paso de áreas del asistente, el panel de Vigilancia como bento y enlazar los acompañantes con los visitantes de portería (HU-27).
- [x] **Alejo:** responder D1 a D4 de [Plan_Motor_De_Reglas](../07_Planes/activos/Plan_Motor_De_Reglas.md) y ejecutarlo — respondidas (las cuatro en a) y construido por el agente el 2026-10-06, fases F0 a F5. El ingreso a zonas todavía no tiene plan.
- [ ] **Alejo, para cerrar el plan del motor:** el `migrate` (`areas/0004` y `reglas/0002` a `0004`) ya está aplicado (verificado el 2026-10-11); **cerró todas las reglas que había** y dejó con aforo 1 las áreas que no tenían regla de aforo. Queda poner el aforo real de cada área y volver a definir las reglas en el tablero (no verificado).
- [x] **Alejo:** los commits del motor ya están en los dos repositorios (verificado el 2026-10-11).
- [ ] **Prueba manual** del motor con el guion del final del plan (11 pasos). El agente recorrió las pantallas del front contra una API con la base de pruebas, sin usuarios reales ni navegador.
- [ ] **Avisarle a Camilo, del motor:** crear un área ahora exige `aforo_maximo` y hay migración en `areas`; `migrate` cierra las reglas que tenía definidas y hay que volver a definirlas; la pantalla de reglas cambió, y `POST /reglas/` ya no exige `area` (va solo en las reglas de un área) y responde `409` si la regla ya está definida.
- [x] ~~**Pagos:** *paz y salvo* y *día límite de pago* no tienen efecto hasta que exista el módulo (HU-16, HU-35), que además necesita la cuota mensual por vivienda (maestro §11.5).~~ Construido el 2026-10-10 ([pagos](../05_Modulos/pagos.md)): *paz y salvo* y *día límite de pago* ya tienen efecto. La cuota por vivienda no hizo falta: registra si el mes se pagó, no cuánto. — Desde el 2026-10-10 tiene plan: [Plan_Pago_De_Administracion](../07_Planes/hechos/Plan_Pago_De_Administracion.md), que es HU-35 (HU-16 es otra cosa: el pago de la reserva) y no usa la cuota, porque registra si el mes se pagó y no cuánto.
- [ ] **Texto de diseño:** el maestro §5.10 y [alcance](../01_Contexto/alcance.md) 3.1 siguen con el modelo anterior; solo llevan el aviso.
- [ ] **READMEs del código:** el de `apps/reglas/` del Backend se corrigió el 2026-10-06. Sigue sin tocar `Backend/Admind_Backend/apps/conjuntos/README.md`, que dice que áreas y reglas cuentan como no cumplidas y que la auditoría «llega con `apps/auditoria/`», que ya existe.

## Reglas de reserva nuevas y planes de HU-28 y HU-35 (2026-10-10)

- [ ] **Alejo, de las dos reglas nuevas** (*una reserva al día* y *sin franjas seguidas*): el `migrate` de `reglas/0006` y los commits ya están (verificado el 2026-10-11); falta probarlas a mano. El agente no las recorrió en el navegador.
- [ ] **Avisarle a Camilo, de las dos reglas:** migración en `reglas`; dos tipos nuevos en `GET /reglas/catalogo/`; `GET /reservas/franjas/` puede responder `no_disponible` en franjas libres cuando el día ya tiene reserva y el área tiene la regla.
- [x] ~~**Alejo:** responder D3 a D8 de Plan_Parqueadero_De_Visitantes y ejecutarlo.~~ Respondidas (todas en a) y construido por el agente el 2026-10-10 ([Plan_Parqueadero_De_Visitantes](../07_Planes/hechos/Plan_Parqueadero_De_Visitantes.md)).
- [ ] **Alejo, de HU-28** (el `migrate` de `parqueaderos/0001`, `visitantes/0002` y `0003` y los commits ya están, verificado el 2026-10-11): falta la prueba manual con su guion, que incluye dos navegadores con un solo puesto libre. El agente la probó de punta a punta en la base de pruebas, no en el navegador; `static/js/visitantes.js` no tiene prueba automática.
- [ ] **Avisarle a Camilo, de HU-28:** su app `visitantes` cambió: migraciones `0002` y `0003`; capa de servicio nueva (`servicios.py`) y su vista quedó delgada; `POST /visitantes/` acepta `parqueadero`; `GET /visitantes/` trae `hora_salida` y `parqueadero`; ruta nueva `POST /visitantes/<id>/salida/`; **el vigilante ve también las visitas de días anteriores sin salida**; permiso nuevo `parqueadero.gestionar` en el catálogo; app nueva `parqueaderos` en `config/` de los dos repositorios; y su plantilla `lista.html`, su `forms.py`, su `views.py` y su `visitantes.js`. Además se agregó una fixture automática a su `tests/test_visitantes.py` sin tocar ninguna aserción.
- [x] ~~**Notion, de HU-28:** pasar la historia a «En revisión»; HU-27 gana la salida y la capa de servicio.~~ Hecho el 2026-10-11: HU-28 ya estaba «En revisión» (la movió el equipo) y sus 5 tareas pasaron a «Finalizada»; HU-27 quedó «En progreso» con 2 tareas finalizadas.
- [x] ~~**Alejo:** responder D5 a D10 de Plan_Pago_De_Administracion y ejecutarlo.~~ Respondidas (todas en a) y construido por el agente el 2026-10-10 ([Plan_Pago_De_Administracion](../07_Planes/hechos/Plan_Pago_De_Administracion.md)).
- [ ] **Alejo, de HU-35** (el `migrate` de `pagos/0001`, `pagos/0002` y `reglas/0007` y los commits ya están, verificado el 2026-10-11): falta la prueba manual con su guion. El agente la probó de punta a punta en la base de pruebas, no en el navegador ni en `admind_db`.
- [ ] **Lo legal de la mora, antes de encender *paz y salvo* en un conjunto real:** la mora ya restringe de verdad reservas e ingresos a zonas comunes. Sigue sin verificarse que restringir por mora las zonas de recreación proceda y que nada impida hoy crear como área un bien esencial y exigirle paz y salvo ([abiertas](../06_Decisiones/abiertas.md) 12.10 b). Además, con la mora contada desde la primera definición del día límite, definirlo a mitad de mes pone en mora a toda vivienda sin su mes confirmado: confirmar primero.
- [ ] **Avisarle a Camilo, de HU-35:** tres permisos nuevos en el catálogo (`pago.ver`, sensible; `pago.confirmar`; `pago.reportar`); app nueva `pagos` en `config/` de los dos repositorios; una regla nueva en el catálogo de reglas con su migración `reglas/0007`; el ítem «Pagos» en el lateral (`lateral.html`); y que *paz y salvo* **empieza a restringir de verdad** (las pruebas que la simulaban siguen igual).
- [x] ~~**Notion, de HU-35:** moverla y ajustar sus criterios.~~ Hecho el 2026-10-11: ya estaba «En revisión» (la movió el equipo) y 4 de sus 5 tareas pasaron a «Finalizada»; la tercera, almacenamiento fuera de la base, quedó sin cerrar con una nota. Sus criterios no se ajustaron.
- [ ] **Visto y no tocado (HU-35):** el buscador de «Pagos» es un formulario `GET` (P7), así que lo que se escribe, incluida una cédula, queda en la dirección, en el historial del navegador y en el registro del servidor, y vuelve en el campo y en los enlaces de mes. La API nunca devuelve el documento de nadie en las filas. Pasarlo a `POST` evitaría dejarlo en la URL, a cambio de no poder compartir ni recargar la búsqueda: decisión de equipo (Ley 1581).
- [x] ~~**Alejo:** responder D5 a D7 de Plan_Pago_De_Reserva (HU-16) y ejecutarlo.~~ Respondidas (D5 a, D6 a, D7 a) y construido por el agente el 2026-10-10 ([Plan_Pago_De_Reserva](../07_Planes/hechos/Plan_Pago_De_Reserva.md)).
- [ ] **Alejo, de HU-16** (el `migrate` de `reservas/0003` y `0004` y los commits ya están, verificado el 2026-10-11): falta la prueba manual con el guion del plan. El agente probó la integración de punta a punta en la base de pruebas, no en el navegador ni en `admind_db`.
- [ ] **Avisarle a Camilo, de HU-16:** permiso nuevo `reserva.declarar_pago` en el catálogo; dos migraciones en `reservas`; módulo nuevo `apps/comun/archivos/comprobantes.py`; el campo `pago` en las respuestas de solicitudes (`GET /reservas/solicitudes/`, `…/areas/<id>/solicitudes/`, `…/bandeja/` y los detalles); y cambios en `solicitudes_area.html` y `triage/bandeja.html`, que son suyos (la vista del historial del residente ahora enlaza al detalle).
- [x] ~~**Notion, de HU-16:** pasar la historia a «En revisión» y cambiar la tarea «Almacenamiento del archivo fuera de la base de datos, con ruta por conjunto».~~ Hecho el 2026-10-11: ya estaba «En revisión» y 4 de sus 5 tareas pasaron a «Finalizada»; la de almacenamiento quedó sin cerrar con una nota (D5 quedó en a: el archivo va dentro de la base), para que el equipo la reformule. El residente ahora puede subir su comprobante (D4 b), que la historia no preveía.
- [ ] **Notion:** lo que el equipo llamaba HU-16 al hablar del pago de administración es HU-35 (Sprint 7). Las dos reglas nuevas no están en los criterios de HU-10. El agente no toca Notion.
- [ ] **Visto y no tocado:** `apps/ingresos/tests.py::test_un_registro_que_no_cumple_responde_400_con_todos_los_motivos_y_no_deja_fila` usa la hora real: la zona de prueba abre de 05:00 a 22:00 y de noche responde 3 motivos en vez de 2. Falla entre las 22:00 y las 05:00 aunque nada esté mal (ya fallaba antes de HU-16). Es de Camilo.
- [ ] **Visto y no tocado (HU-16):** `cliente_api/reservas.py` lee el archivo entero con `archivo.read()` y lo reenvía; la API es la que rechaza por peso (5 MB). Un archivo enorme se carga en la memoria del front antes de ese rechazo. El reglamento (`cliente_api/documentos.py`) funciona igual. Poner un tope en el front sería decisión de equipo.
- [ ] **Visto y no tocado:** `visitantes/0001` no trae la FK compuesta de `unidad_id` que pide [aislamiento](../03_Reglas/aislamiento.md). Es de Camilo: se le avisa.
- [ ] **Visto y no tocado:** en el tablero, una regla sin valores (paz y salvo y las dos nuevas) muestra «Cambiar», que abre un formulario sin campos y guarda una versión idéntica. Sobra ese botón para esos tipos.

## Notion al día contra el código (2026-10-11)

Alejo decidió que Notion refleje la realidad ([construccion](../06_Decisiones/construccion.md)). Lo que queda:

- [ ] **HU-14, para cerrarla:** categorías de motivo de rechazo (tarea 3), aviso al residente por ambos canales (tarea 5), hilo de mensajes (tarea 4) y la bandeja ordenada por antigüedad (tarea 1). Está «En progreso»; el informe 4 la contó como terminada con un criterio menos estricto.
- [ ] **HU-29 (Camilo):** en Notion lleva dos tareas finalizadas y no hay código en el repositorio. Cuando lo suba: verificarlo, compararlo con sus criterios y actualizar [historias](historias.md). Hasta entonces, no verificado.
- [ ] **HU-21 y HU-25:** siguen «Finalizado» en Notion sin *PR revisado* ni *Probada por el otro*. Las corrige Alejo.
- [ ] **HU-16 (tarea 5) y HU-35 (tarea 3):** «almacenamiento fuera de la base» contradice lo construido; el equipo decide si se reformulan o se cierran con esa decisión. Mientras tanto el tablero muestra la alerta de la historia.
- [ ] **HU-27 y HU-33:** cada una tiene en su página de Notion una tabla de criterios contra lo que hay; lo que falta está en [historias](historias.md).
- [ ] **Sprints:** el Sprint 4 sigue «Planificado» con HU-14 y HU-16 en marcha, y el 5, «En curso». Los estados de los sprints los cambia el equipo.
- [ ] **Limpieza en Notion:** una página vacía («Reglamento y manual de convivencia visibles…») cuelga de la página principal y figura como tarea de HU-33 sin estar en la base Tareas; hay una fila «Prueba» en «Finalizado» y una «Mini HU: Tipos de Zona» sin tareas ni sprint (¿es la historia de las zonas con ingreso?).

## Asistente de creación completo (2026-10-06)

Tres planes abiertos el mismo día tocan el asistente; el orden está en [planes](../07_Planes/planes.md).

- [x] **Alejo:** responder D1 a D5 de [Plan_Asistente_De_Creacion](../07_Planes/activos/Plan_Asistente_De_Creacion.md). Respondió D1 en b y las demás en a, y lo construyó el agente (2026-10-06).
- [ ] **Alejo, para cerrar el plan del asistente:** correr `migrate` en `admind_db` (aplica `documentos/0001_initial`), revisar y hacer los commits en los dos repositorios, y mover el plan a `hechos/` con Obsidian abierto.
- [ ] **Prueba manual** del asistente con el guion del final del plan (9 pasos), con una cuenta de Administración. El agente lo recorrió con el front de verdad contra una API con la base de pruebas, sin usuarios reales ni navegador.
- [ ] **Avisarle a Camilo, del catálogo de permisos:** `conjunto.activar` ahora también lo tiene Administración (D1 b). Y que el requisito de reglas cambió: ya no basta «alguna regla vigente», hace falta la anticipación máxima del conjunto.
- [ ] **Notion:** HU-03 cambia de criterios (siete pasos, seis requisitos, activa Administración) y HU-33 queda cubierta solo en el reglamento. El agente no toca Notion.
- [ ] **Sin decidir, visto al construir:** dejar operativo un conjunto no deja registro en la auditoría, y un conjunto operativo no se vuelve a revisar si después deja de cumplir un requisito (por ejemplo, si retiran la anticipación máxima).
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

---
resumen: "Todo lo que falta, ordenado por tipo: lo que frena los story points, pruebas manuales, avisos a Camilo, lo legal, decisiones de equipo, Notion, textos desactualizados y deuda técnica."
tipo: estado
corte: 2026-10-13
origen: "listas anteriores (2026-09-27 a 2026-10-11), reordenadas por tipo y contrastadas con el código el 2026-10-11; puesta al día el 2026-10-13"
actualizado: 2026-10-24
revisado: 2026-10-24
---

# Pendientes

Lo más urgente, ya resumido, está en [estado_actual](estado_actual.md). Aquí va la lista completa, **solo con lo que sigue abierto**. Lo resuelto queda en [bitacora](bitacora.md); lo que se cerró al revisar esta lista está al final.

La fecha entre paréntesis es cuándo se anotó. *Verificado el 11/10* quiere decir que se miró en el código ese día.

## 1. Qué frena que se cuenten story points

- [ ] **Mezclar a `desarrollo` la rama `ccr-4213a943-1fgq6z`** de Backend y Frontend (plan de triage, 24/10). Es lineal sobre `7eb5b5a` y `8279616`: entra como *fast-forward* si nadie subió nada antes. Hasta entonces, nada de HU-22 ni HU-24 del 24/10 está en `desarrollo`. *(24/10)*
- [ ] **La rama `pruebas` del backend no existe en GitHub** (solo en local, y en un commit viejo). En el front existe, igual a `main`. Sin ella no hay PR `desarrollo → pruebas`. *(29/09, verificado el 11/10)*
- [ ] **PR `desarrollo → pruebas` revisado** por quien no programó. Ninguna historia ha pasado por uno.
- [ ] **Pruebas manuales** de quien no programó: sección 2.
- [ ] **Decidir el alcance** que entra antes de la entrega: sección 5.

## 2. Pruebas manuales

El agente no las hace: no tiene la contraseña ni el segundo factor de los usuarios de prueba, y en `admind_db` algunas acciones mandan correo real. Cada plan trae su guion al final.

| Qué | Guion | Ojo con |
|---|---|---|
| HU-06 a HU-13 | [Admind_Plan_Sprints_2_3](../07_Planes/hechos/Admind_Plan_Sprints_2_3.md) §6 | El `sendBeacon` que libera el bloqueo al cerrar la pestaña (HU-11); «corregir sin perder lo escrito» y «el reloj no se detiene» (HU-12) |
| Recuperación de contraseña (HU-01) | [Plan_Recuperacion_Contrasena](../07_Planes/hechos/Plan_Recuperacion_Contrasena.md) | — |
| Enlace que quita el segundo factor (HU-02) | Sin guion: recorrerlo con la API encendida y un correo real | — |
| Anuncios con fotos (HU-25) | [Plan_Anuncios_Con_Fotos](../07_Planes/hechos/Plan_Anuncios_Con_Fotos.md) | Publicar manda correo real |
| Paso «Viviendas» (HU-39) | [Plan_Estructura_De_Viviendas](../07_Planes/hechos/Plan_Estructura_De_Viviendas.md), 12 pasos | `static/js/viviendas.js` no tiene prueba automática |
| Asistente completo (HU-03) | [Plan_Asistente_De_Creacion](../07_Planes/hechos/Plan_Asistente_De_Creacion.md), 9 pasos | Con una cuenta de Administración |
| Motor de reglas | [Plan_Motor_De_Reglas](../07_Planes/hechos/Plan_Motor_De_Reglas.md), 11 pasos | — |
| Zonas con ingreso | [Plan_Zonas_Con_Ingreso](../07_Planes/hechos/Plan_Zonas_Con_Ingreso.md), 12 pasos | No se revisó a 200 % de zoom ni se esperó una permanencia real |
| Dos reglas de reserva del 10/10 | Sin guion | El agente no las recorrió en el navegador |
| Pago de una reserva (HU-16) | [Plan_Pago_De_Reserva](../07_Planes/hechos/Plan_Pago_De_Reserva.md) | — |
| Parqueadero de visitantes (HU-28) | [Plan_Parqueadero_De_Visitantes](../07_Planes/hechos/Plan_Parqueadero_De_Visitantes.md) | Dos navegadores con un solo puesto libre. `static/js/visitantes.js` no tiene prueba automática |
| Pago de administración (HU-35) | [Plan_Pago_De_Administracion](../07_Planes/hechos/Plan_Pago_De_Administracion.md) | — |
| Cambiar el modo de uso de un área (13/10) | Sin guion: en «Editar área», pasar una con reservas apartadas y reglas propias a «Con ingreso» y volver | El agente lo recorrió con un guion contra la base de pruebas, no en el navegador ni con usuarios reales |
| Usuarios, detalle de la vivienda y «Crear conjunto» (11/10) | Sin guion | Usuarios y el detalle de la vivienda se vieron en el navegador con datos inventados, no con usuarios reales |
| «Eliminar conjunto» del resumen (13/10) | Sin guion | Lo subió Camilo; las pruebas lo cubren con la API simulada y `conjuntos.js`, que abre el diálogo, no tiene prueba automática. En la bóveda no consta que alguien lo haya recorrido |

- [ ] **Filtros del dashboard y rechazo formal (HU-22 y HU-24):** el guion de [Plan_Triage_HU-22_HU-24](../07_Planes/hechos/Plan_Triage_HU-22_HU-24.md), después de mezclar la rama a `desarrollo`.
- [ ] **Dashboard de gestión (HU-14 y HU-29):** el guion de [Plan_Dashboard_De_Solicitudes](../07_Planes/hechos/Plan_Dashboard_De_Solicitudes.md), con Administración, Secretaría, dos residentes y Vigilancia. Lo recorrió el agente con el front real contra la API de pruebas (43 comprobaciones); falta la prueba de una persona en el navegador. *(13/10)*

## 3. Avisarle a Camilo

En la bóveda no consta que se le haya avisado de nada de esto. Lo que tiene que saber, por tema:

- [ ] **Migraciones que no hizo él** (del 05/10 al 10/10): `anuncios/0002`; `areas/0002`, `0004` y `0005`; `reglas/0002` a `0007`; `unidades/0002`; `documentos/0001`; `ingresos/0001`; `reservas/0003` y `0004`; `parqueaderos/0001`; `visitantes/0002` y `0003`; `pagos/0001` y `0002`. La `reglas/0003` **cierra las reglas que tuviera definidas** y pasa el aforo a su área: hay que volver a definirlas.
- [ ] **Apps nuevas** registradas en `config/` de los dos repositorios: `documentos`, `ingresos`, `parqueaderos` y `pagos`.
- [ ] **Catálogo de permisos:** `conjunto.activar` también lo tiene Administración; nuevos `ingreso.registrar`, `ingreso.ver_historico`, `reserva.declarar_pago`, `parqueadero.gestionar`, `pago.ver` (sensible), `pago.confirmar` y `pago.reportar`.
- [ ] **Su app `visitantes` cambió** (HU-28): `servicios.py` nuevo y su vista quedó delgada; `POST /visitantes/` acepta `parqueadero`; `GET /visitantes/` trae `hora_salida` y `parqueadero`; ruta nueva `POST /visitantes/<id>/salida/`; el vigilante ve también las visitas de días anteriores sin salida. Cambiaron su `lista.html`, `forms.py`, `views.py` y `visitantes.js`, y su `tests/test_visitantes.py` ganó una fixture automática, sin tocar ninguna aserción.
- [ ] **Sus pantallas de solicitudes cambiaron** (HU-16): `solicitudes_area.html` y `triage/bandeja.html` muestran el bloque «Pago», y las respuestas de solicitudes traen el campo `pago`.
- [ ] **Contratos que cambiaron:** crear un área exige `aforo_maximo` y trae `modo_uso` y `permanencia_maxima_minutos` (la duración de la franja puede llegar vacía); `POST /reglas/` ya no exige `area` y responde 409 si la regla ya está definida; `GET /reglas/catalogo/` trae los tipos nuevos; `POST /reservas/solicitudes/` responde 409 sobre un área con ingreso; `GET /reservas/franjas/` puede responder `no_disponible` en franjas libres; `/anuncios/` trae `fotos`; `/unidades/` tiene tres rutas nuevas y más campos; `GET /auth/usuarios/` trae `unidades`.
- [ ] **Límites de texto** (13/10): nombre del conjunto, nombres y apellidos hasta 30 caracteres y teléfono hasta 10, a pedido de Alejo; la restricción `persona_telefono_valido` que él escribió pasó de 7–15 a 7–10 dígitos y hay dos migraciones nuevas (`conjuntos/0005`, `personas/0002`). `componentes/campo.html` ahora emite `maxlength`, así que sus campos (cédula, nombre del visitante, placa) también cortan al límite que ya tenía. **Ese mismo día subió el teléfono a 15** (`7eb5b5a`), en el campo y editando la `personas/0002` ya aplicada, sin tocar la restricción del modelo ni el formulario del front: confirmar con él cuál es el límite y cerrarlo con una migración nueva (sección 8).- [ ] **El modo de uso de un área ya se puede cambiar** (13/10): `PATCH /areas/<id>/` acepta `modo_uso` y su respuesta trae siempre `cambio_de_modo` (vacío si el modo no cambió); se revirtió la decisión del 08/10.
- [ ] **Alfa y beta cambiaron de significado** (alfa = del conjunto, beta = del área) y *paz y salvo* **restringe de verdad** desde el 10/10.
- [ ] **El asistente tiene siete pasos**, un conjunto ya puede quedar operativo y hay una historia nueva, HU-39.
- [ ] **Vistas y no tocadas, suyas:** la prueba de `ingresos` que usa la hora real y `visitantes/0001` sin la FK compuesta de `unidad_id` (sección 8).

- [ ] **Dashboard y casos (13/10):** la Secretaría ya no aprueba ni rechaza reservas (su rol pierde `reserva.aprobar` y `reserva.rechazar`; descarta con `solicitud.rechazar_formal`), y cambiaron las pruebas suyas que afirmaban lo contrario. `POST …/decision/` pide `categoria` al rechazar. `/reservas/bandeja/` exige `solicitud.bandeja_ver` y ordena por antigüedad. Su app `casos` se amplió sin tocar sus migraciones: estados nuevos, `APROBADO` ya no existe, la ruta de Secretaría es `/casos/<id>/descartar/` (con causal) y `/casos/<id>/rechazar/` pasó a ser de Administración; Administración ve todos los casos, no solo los redirigidos. En el front, `/solicitudes/` de gestión es el dashboard y `/casos/` de gestión redirige allá. Se corrigió su prueba `test_el_detalle_de_solicitud_incluye_condiciones_de_renta_de_su_area`, que guardaba sin conjunto activo.

## 4. Lo legal sin verificar

Mientras haya duda legal, no se construye más encima ([legal](../01_Contexto/legal.md)). Detalle en [abiertas](../06_Decisiones/abiertas.md) 12.10 b.

- [ ] **Zonas con ingreso:** verificar con la guía legal o el docente si la mora puede restringir el gimnasio o la piscina; la finalidad, la autorización y el plazo de retención del registro de quién entra; y la Ley 1209 de piscinas. *(08/10)*
- [ ] **El texto del aviso de finalidad.** La pantalla de Vigilancia dice «Aviso de finalidad pendiente de la verificación legal»; se reemplaza en `AVISO_DE_FINALIDAD` de `Frontend/Admind_Front-End/apps/ingresos/views.py`. De ahí sale también qué hacer con el historial al cumplirse la retención. *(08/10, verificado el 11/10)*
- [ ] **La mora, antes de encender *paz y salvo* en un conjunto real.** Ya restringe reservas e ingresos. Sigue sin verificarse que proceda para zonas de recreación, y nada impide crear como área un bien esencial y exigirle paz y salvo. Además, definir el día límite a mitad de mes pone en mora a toda vivienda sin su mes confirmado: confirmar primero ([pagos](../05_Modulos/pagos.md)). *(10/10)*
- [ ] **Visitantes (HU-27):** finalidad declarada, autorización y plazo de retención (Ley 1581, R2). *(05/10)*
- [ ] **Habitantes de la vivienda,** antes de construir su pantalla: qué finalidad se declara, quién autoriza (el adulto responsable, si es un menor) y cuánto se conserva. Las pantallas de registro de hoy tampoco muestran la autorización. *(06/10)*
- [ ] **Plazo de retención de los comprobantes** de pago (Ley 1581): no está definido. *(10/10)*

## 5. Decisiones de equipo sin tomar

Un agente no las resuelve ([abiertas](../06_Decisiones/abiertas.md)).

- [ ] **Fecha exacta de entrega y qué historias entran** (12.8). *(27/09)*
- [ ] **Stack del frontend** (12.1): el front está construido sobre plantillas de Django y Alpine; falta cerrarlo por escrito con Camilo. *(27/09)*
- [ ] **HU-39, lo que queda de 12.9:** persona principal, cómo se cumple lo legal con los datos de quienes se mudan, y retiro de varias viviendas a la vez. *(06/10)*
- [ ] **¿Reservar exige que el conjunto esté operativo?** Hoy no se revisa (plan D7 a del 27/09). *(06/10, verificado el 11/10)*
- [ ] **Dejar operativo un conjunto no queda en la auditoría,** y un conjunto operativo no se vuelve a revisar si después deja de cumplir un requisito. *(06/10)*
- [ ] **Días que no abre:** Alejo dijo en el chat del asistente que el motivo y los periodos quedaban para después, y el plan del motor los construyó. Falta que confirme que así lo quería. *(06/10)*
- [ ] **Supuestos del agente por confirmar:** los de la D9 del plan de ingresos y los del día límite de pago, al final de [motor_reglas](../05_Modulos/motor_reglas.md) e [ingresos](../05_Modulos/ingresos.md). *(08/10)*
- [ ] **Vigilancia ve «Zonas comunes» en el menú, pero la API le responde sin permiso** (D5 b lo dejó así a propósito). «Reglas» se le quitó el 13/10 a pedido de Alejo; quitar también «Zonas comunes» cambia otra vez `test_vigilancia_solo_ve_las_secciones_permitidas_en_el_lateral`, que es de Camilo y ya se tocó una vez. Falta avisarle. *(08/10, 13/10)*
- [ ] **El buscador de «Pagos» es un formulario `GET`:** lo que se escribe, incluida una cédula, queda en la dirección, en el historial y en el registro del servidor. Pasarlo a `POST` lo evita a cambio de no poder compartir ni recargar la búsqueda (Ley 1581). *(10/10)*
- [ ] **Tope de peso en el front para los archivos:** `cliente_api/reservas.py`, `documentos.py` y `pagos.py` leen el archivo entero con `archivo.read()` y lo reenvían; la API es la que rechaza por peso. *(10/10, verificado el 11/10)*
- [ ] **Límite de búsquedas de personas:** cuenta por conjunto, así que un administrador de dos conjuntos puede hacer 20 en cada uno. ¿Debe ser global? *(27/09)*
- [ ] **¿Los anuncios se pueden eliminar?** Hoy solo se editan (`PATCH`). Las reglas se quitan cerrando su vigencia desde el 06/10. *(27/09, verificado el 11/10)*
- [ ] **¿Se ocultan del selector los conjuntos no operativos?** A quien no es Superusuario, el selector le excluye los dados de baja y le deja los no operativos; el Superusuario ve todos. *(27/09, 13/10)*
- [ ] **La baja del conjunto que subió Camilo el 13/10** (`servicios.eliminar`, `DELETE /conjuntos/actual/`), contra lo que ya estaba diseñado: **(a)** [eliminacion](../03_Reglas/eliminacion.md) pide doble confirmación escrita con el nombre exacto y el botón da un «Sí, eliminar / No»; la API no pide ninguna; **(b)** no deja fila en la auditoría; **(c)** el Superusuario sigue viendo el conjunto dado de baja en su selector, sin marca, y `puede_operar_en` lo deja volver a entrar; no hay cómo reactivarlo, y el diseño decía «reversible 30 días»; **(d)** se pregunta `es_superusuario` en la vista, no un permiso del catálogo (no existe `conjunto.eliminar`). Alejo decide si se deja así. *(13/10, verificado en el código)*
- [ ] **`vigencia_hasta` es el primer día sin el rol:** con la fecha de hoy, el rol se pierde de inmediato. Confirmarlo. *(27/09)*
- [ ] **Reparto de permisos por rol** en `catalogo.py`: interpretado del diseño, provisional hasta validarlo con un administrador real. *(27/09)*
- [ ] **Quitar el segundo factor y restablecer la contraseña no dejan auditoría:** esas rutas no tienen conjunto activo. Registrarlo pide una tabla global (R12). *(05/10)*

**Del plan original, para la sustentación** ([backlog_y_plazo](backlog_y_plazo.md) 11.4 y 11.5): conseguir un reglamento real y la entrevista con el administrador de contacto; documentar las entrevistas a residentes; decidir si las consultas del Superusuario quedan en la auditoría (R10); quién es PO y quién SM; el ambiente de pruebas; y los dos usuarios de la base de datos que pide la auditoría de solo inserción.

## 6. Notion

El agente no toca Notion por su cuenta. Alejo decidió el 11/10 que refleje la realidad ([construccion](../06_Decisiones/construccion.md)).

- [ ] **HU-22 y HU-24 (24/10):** HU-22 sigue «Sin empezar» y ya es parcial (solo faltan las citas); HU-24 está «En revisión» y cumple cuatro criterios y medio. Actualizar su tabla *Estado real*.

- [ ] **HU-14 y HU-29:** pasarlas de estado en Notion. En HU-29, la tarea «Tablero de tres columnas con filtros e hilo» ya no describe lo construido (es una tabla con pestañas, sin hilo) y la de la FK desde la infracción figura «Finalizada» sin estar en el código. *(13/10)*
- [ ] **HU-21 y HU-25** siguen «Finalizado» sin *PR revisado* ni *Probada por el otro*. Las corrige Alejo.
- [ ] **HU-16 (tarea 5) y HU-35 (tarea 3):** «almacenamiento fuera de la base» contradice lo construido. El equipo decide si se reformulan o se cierran con esa decisión.
- [ ] **Criterios que describen el modelo anterior:** HU-03 (siete pasos, seis requisitos, activa Administración), HU-06 (un solo rol), HU-09, HU-10 y HU-13 (motor por niveles y las dos reglas nuevas), HU-21 (color propio), HU-25 (fotos) y HU-33 (solo el reglamento).
- [ ] **El ingreso a zonas no tiene historia ni número.** En Notion hay una «Mini HU: Tipos de Zona» sin tareas ni sprint: ¿es esa?
- [ ] **Sprints:** el 3 sigue sin pasar a «Finalizado», el 4 sigue «Planificado» con HU-14 y HU-16 en marcha, y el 5, «En curso». Los cambia el equipo.
- [ ] **Limpieza:** una página vacía («Reglamento y manual de convivencia visibles…») cuelga de la página principal; hay una fila «Prueba» en «Finalizado».
- [ ] **Sin revisar desde el 29/09:** si HU-01, HU-02, HU-04, HU-05 y HU-26 siguen «En progreso» con fracciones viejas; que el Sprint 1 no tiene fechas, y HU-01, HU-05 y HU-26 no tienen responsable (la DoD necesita saber quién programó para saber quién prueba).

## 7. Textos desactualizados

**Texto de diseño** (antes, el maestro). Las decisiones tomadas al construir solo están avisadas al inicio de cada nota; reescribir el texto lo decide el equipo ([documentacion](../03_Reglas/documentacion.md)):

- [ ] Estado `LIBERADA`, un bloqueo por persona y conjunto, y el catálogo de reglas con versionado ([reservas](../05_Modulos/reservas.md), [motor_reglas](../05_Modulos/motor_reglas.md)).
- [ ] Motor por niveles y zonas con dos modos de uso: §5.10 y [alcance](../01_Contexto/alcance.md) 3.1 siguen con el modelo anterior.
- [ ] Token con registro en la base y stack del front ([stack](../02_Arquitectura/stack.md)).
- [ ] Color propio y foto 1:1 de HU-21: §6.3 todavía dice que el acento está aplazado ([sistema_visual](../04_Diseno/sistema_visual.md)).
- [ ] Rol único por conjunto y Superusuario con todos los permisos: §3.1 y R5 dicen varios roles ([permisos](../05_Modulos/permisos.md)).
- [ ] Lista cerrada de tablas globales y `VistaDeConjunto` en vez de *middleware* ([aislamiento](../03_Reglas/aislamiento.md)).

**README del código** (verificado el 11/10; son de los repositorios de código, no de esta bóveda):

- [ ] `Backend/Admind_Backend/apps/README.md` no menciona la capa de servicios.
- [ ] `Backend/Admind_Backend/apps/conjuntos/README.md` dice que la auditoría de la creación «llega con `apps/auditoria/`», que ya existe.
- [ ] `Frontend/Admind_Front-End/README.md` dice que el repositorio solo tiene el sistema de diseño y carpetas con README.
- [ ] `cliente_api/README.md` y `config/README.md` del front siguen con sesión o token (12.7 b) como pendiente, y ya está resuelto.

## 8. Deuda técnica y cosas vistas sin tocar

**Cuentas y correo**

- [ ] `send_mail` es síncrono y sin `try` ni `EMAIL_TIMEOUT` en la recuperación de contraseña y en el enlace del segundo factor: si el servidor de correo falla, responde 500 solo cuando la cuenta existe, y tarda más (deja adivinar qué correos están registrados). *(verificado el 11/10)*
- [ ] `/auth/login/` no limita los intentos de contraseña. *(verificado el 11/10)*
- [ ] Los límites de enlaces viven en memoria: se pierden al reiniciar y no se comparten entre procesos.
- [ ] No hay comando que borre los tokens vencidos: se acumulan en `cuentas_tokendesesion`. *(verificado el 11/10)*
- [ ] **La contraseña de la base estuvo en GitHub.** El `.env _ejemplo` del backend ya no la trae (verificado el 11/10), pero sigue en el historial: hay que cambiarla. `Credenciales/` se queda en este repositorio porque es privado (Alejo, 30/09).

**Datos en `admind_db`**

- [ ] La migración del motor cerró todas las reglas que había y dejó con aforo 1 las áreas que no tenían regla de aforo. Falta poner el aforo real de cada área y volver a definir las reglas en el tablero. *(06/10, no verificado)*
- [ ] La foto vacía de «Estancia 1» sigue en la base hasta que se suba otra. *(05/10, no verificado)*

**Backend**

- [ ] **`makemigrations --check` falla** desde `7eb5b5a`: pide `personas/0003` porque la restricción `persona_telefono_valido` del modelo sigue en `{7,10}` y la `personas/0002`, editada a mano después de aplicada, dice `{7,15}`. En `admind_db` quedó la versión vieja (`telefono` en `varchar(10)` y 7 a 10 dígitos): quien aplique `personas/0002` desde cero obtiene otra base. Se arregla con una migración nueva, no editando la aplicada. *(13/10, verificado en el código y en la base)*
- [ ] `apps/ingresos/tests.py::test_un_registro_que_no_cumple_responde_400_con_todos_los_motivos_y_no_deja_fila` usa la hora real: falla entre las 22:00 y las 05:00 aunque nada esté mal. Es de Camilo.
- [ ] `visitantes/0001` no trae la FK compuesta de `unidad_id` que pide [aislamiento](../03_Reglas/aislamiento.md). Es de Camilo. *(verificado el 11/10)*
- [ ] `Asignacion` no tiene `registrado_por`. *(27/09, verificado el 11/10)*
- [ ] Índices compuestos `(conjunto_id, …)` para consultas concretas, tabla por tabla.

**Frontend**

- [ ] `usuarios/nuevo.html` no sobreescribe `estado_vista`: muestra la pastilla «Maqueta con datos de ejemplo» aunque es una pantalla real. `paneles/inicio.html` sí es maqueta. *(verificado el 13/10)*
- [ ] En el tablero, una regla sin valores (paz y salvo y las dos del 10/10) muestra «Cambiar», que abre un formulario sin campos y guarda una versión idéntica.
- [ ] `alpine.min.js` se versionó con `core.autocrlf=true`: en otra máquina con Windows puede quedar con CRLF y su SHA-256 no coincidir con el del README de `vendor/`. Un `.gitattributes` lo evitaría. *(verificado el 11/10: no existe)*

**En la máquina de Camilo** (no verificable desde aquí; ya subió pantallas y pruebas, así que probablemente está hecho): `.venv` y `.env` del front, y `CREATEDB` para su `admind_user`.

## 9. Lo que sigue sin plan

- **Segunda parte de HU-39:** las palabras del conjunto en las pantallas, registrar una vivienda a mano dentro de una agrupación, y retirar viviendas y agrupaciones con confirmación ([historias](historias.md)).
- **El vínculo `habitante`** ([unidades](../05_Modulos/unidades.md)): decidido el 06/10, sin historia, sin plan y sin construir. Mientras no exista, la familia entra a una zona como acompañante de un titular.
- **Después de las zonas con ingreso:** las reglas de piscina de la Ley 1209, depurar el historial al cumplirse la retención, que el vigilante confirme que quien venció de verdad salió, cupos que se actualicen solos, áreas típicas con ingreso en el asistente, el panel de Vigilancia como bento y enlazar los acompañantes con los visitantes de portería.
- **De HU-27:** el aviso a quienes residen en el apartamento, la liberación manual de un parqueadero sin salida y el listado de ocupaciones de más de N horas.
- **Preguntas sueltas de Alejo** (`Archivo/Notas/Nuevas reglas.md`, 06/10): cuántos parqueaderos tiene y puede tener cada vivienda (toca HU-34), y las correcciones del docente.

## Cerrado al revisar esta lista (2026-10-11)

Estaban abiertos en la lista anterior y el código o los repositorios muestran que ya no lo están:

| Pendiente | Por qué se cierra |
|---|---|
| Commits de anuncios con fotos, del enlace del segundo factor, del asistente, de las viviendas, del motor y de los tres planes del 10/10 | Los dos repositorios están limpios e iguales a `origin/desarrollo` |
| `migrate` de `documentos/0001` y de todo lo demás | `showmigrations` no deja ninguna sin aplicar |
| Mover a `hechos/` los planes del asistente, de viviendas y del motor | Movidos el 11/10 |
| HU-03 dependía del reglamento | Construido el 06/10 |
| Pruebas automáticas del front; conectar el selector a la API | 373 pruebas; HU-26 conectada |
| Clase de permiso por vista | `exigir_permiso` se usa en 71 puntos de las vistas |
| `auditoria` sin `via_superusuario`; sin tablas de reglas ni de notificaciones | Existen |
| `visitantes` sin capa de servicio, sin salida y con el README desfasado | Hecho el 10/10; los dos README ya lo describen |
| `index.html` y `apps/Administrador/Home.html` en el front | Ya no existen |
| Logo y color en el selector (HU-26) | Llegaron con HU-21 |
| Definir cómo entran las reglas al asistente (12.10 e) | Resuelta el 06/10 |

## Ver también

- [estado_actual](estado_actual.md) — el resumen de lo que más pesa
- [historias](historias.md) — lo que le falta a cada historia
- [abiertas](../06_Decisiones/abiertas.md) — las contradicciones entre documentos, con sus opciones
- [bitacora](bitacora.md) — lo que ya pasó

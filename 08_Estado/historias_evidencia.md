---
resumen: "Evidencia por historia en progreso: cada tarea técnica y cada criterio de aceptación con su estado y su commit."
tipo: estado
origen: "avance §5.3 (cortes 2026-09-15 y 2026-09-27)"
actualizado: 2026-10-11
revisado: 2026-10-11
---

# Historias: evidencia tarea por tarea

> [!NOTE] Qué cubre y de cuándo es
> - **HU-01, HU-02, HU-03 y HU-26:** revisadas contra el código el 2026-10-11.
> - **HU-04 y HU-05:** corte del 2026-09-15. **HU-06 a HU-13:** corte del 2026-09-27; desde entonces cambiaron HU-06 (un solo rol), HU-09, HU-10 y HU-13 (motor por niveles), como dice [historias](historias.md).
> - **HU-14 en adelante no están aquí.** Su evidencia está en la nota de su módulo, en su plan ([planes](../07_Planes/planes.md)) y en [historias](historias.md).

Referencias sin nombre de documento (*§2*, *§4*, *§6*…) son del antiguo `Admind_Avance.md`: §2 → [inventario del 27/09](../Archivo/Avances/Inventario_codigo_2026-09-27.md) · §3 → [bitacora](bitacora.md) · §4 → [construccion](../06_Decisiones/construccion.md) · §5 → [historias](historias.md) y [historias_evidencia](historias_evidencia.md) · §6 → [pendientes](pendientes.md). *Maestro §N* se resuelve en `Admin_Master.md`. *El plan* es `07_Planes/hechos/Admind_Plan_Sprints_2_3.md`.

Las tareas y criterios salen de Notion, que coincide con la copia local del Excel V11.1 (hoja `HU`). Las casillas de las tareas en Notion se marcaron el 2026-09-15 09:00 con lo que se describe aquí, y la pantalla de login de HU-01 a las 10:34, con su commit.

## HU-04 · Persona global única por documento — 5 de 5 tareas, falta la DoD

| Tarea técnica (Notion) | Estado | Evidencia |
|---|---|---|
| Modelo Persona con PK UUID y campos `tipo_documento` y `numero_documento` | Hecha | `apps/personas/models.py`, `962853f` |
| Restricción `UNIQUE (tipo_documento, numero_documento)` en base de datos | Hecha | `persona_documento_unico`, verificada en PostgreSQL |
| Catálogo cerrado de tipos de documento | Hecha, con la lista revisada | `TipoDocumento` + `persona_tipo_documento_valido`. Notion ya dice `CC, TI, CE, PAS, PPT` (corregido el 2026-09-15) |
| Normalización del número al guardar | Hecha | `normalizar_documento()` en `save()` + `persona_documento_normalizado` |
| Pruebas: dos altas con el mismo documento producen una sola Persona | Hecha | `apps/personas/tests.py`, 10 pruebas, `dc6a414` |

| Criterio de aceptación | Estado |
|---|---|
| Un documento que ya existe no crea un segundo registro | Hecho y probado, también cuando el segundo se escribe con puntos |
| El mismo número con distinto tipo es otra persona | Hecho y probado |
| En la API o en una URL la persona se identifica por UUID, nunca por documento | La llave es UUID y hay prueba de eso; **todavía no hay endpoint que exponga personas** |
| Un número escrito con puntos o espacios queda normalizado | Hecho y probado. La base además rechaza un número sin normalizar aunque se salte `save()` |
| Una persona con roles en dos conjuntos es un solo registro con dos asignaciones | Hecho y probado en `apps/permisos/tests.py` (`531e854`) |

Para pasar a Terminada (maestro §8.1) le falta: el criterio de la API, el PR `desarrollo → pruebas` revisado por Camilo y la prueba manual de quien no la programó. "El endpoint está documentado" aplica cuando exista el endpoint.

## HU-05 · Aislamiento de datos entre conjuntos — 5 de 5 tareas, falta la DoD

| Tarea técnica (Notion) | Estado | Evidencia |
|---|---|---|
| Llaves foráneas compuestas `(id, conjunto_id)` e índices encabezados por `conjunto_id` | Hecha | `fk_compuesta()` + `UNIQUE (id, conjunto)` en `ModeloDeConjunto`, probada con las tablas de apoyo. Cada tabla que hereda de `ModeloDeConjunto` recibe un índice sobre `conjunto_id` por su FK (verificado en la migración de apoyo). Los índices compuestos para consultas concretas se agregan con cada tabla |
| Lista cerrada de tablas globales exenta del `conjunto_id` | Hecha | `TABLAS_GLOBALES` en `tests/esquema/test_tablas_globales.py`. No coincide del todo con el maestro §5.4 (§6) |
| Middleware que resuelve el conjunto activo desde la sesión, como contexto de solo lectura | Hecha (`d9b6271`) | `VistaDeConjunto` en `apps/comun/aislamiento/vistas.py`: toma el conjunto activo de la sesión del token (§4) |
| Repositorio base que inyecta `WHERE conjunto_id` en toda consulta | Hecha | `ManagerDeConjunto` + `ModeloDeConjunto`, `531e854`. "Sin SQL crudo fuera de ahí" queda como convención: nada lo impide |
| Prueba del intruso por endpoint + prueba transversal de rutas y tablas registradas | Hecha; la parte de rutas y del intruso, en `d9b6271` | `tests/aislamiento/test_intruso.py` y `tests/esquema/test_tablas_globales.py` |

| Criterio de aceptación | Estado |
|---|---|
| Un usuario del conjunto A pide un recurso del B por su identificador y recibe 404, no 403 | Hecho y probado por endpoint, con los endpoints de apoyo |
| Una petición con `conjunto_id` en la URL o el cuerpo se rechaza | Hecho y probado: 400 con `conjunto_id` en la URL y con `conjunto` en el cuerpo |
| Una reserva del conjunto 3 que apunta a un área del conjunto 8 la rechaza la base por la FK compuesta | Hecho y probado con las tablas de apoyo, también por `bulk_create`, que se salta `save()` |
| Una tabla nueva fuera de la lista de globales sin `conjunto_id` hace fallar la suite | Hecho y probado, incluida una prueba de que la revisión detecta la tabla nueva |
| Un endpoint nuevo sin prueba del intruso hace fallar la prueba transversal | Hecho y probado, incluida una prueba de que la revisión detecta la ruta nueva |

Todo se prueba con las tablas y endpoints de apoyo, porque todavía no existen áreas ni reservas reales. Para pasar a Terminada le falta el PR revisado por Camilo y la prueba manual. Cuando exista el PR, puede pasar a "En revisión" en Notion.

## HU-26 · Selector de conjunto activo — 5 de 5 tareas, falta la DoD

Verificado el 2026-10-11.

| Tarea técnica (Notion) | Estado | Evidencia |
|---|---|---|
| Consulta de los conjuntos con asignación vigente de la persona autenticada (backend) | Hecha (`d9b6271`) | `conjuntos_disponibles()` en `apps/permisos/servicios.py` y `GET /auth/conjuntos/` |
| Escritura del conjunto activo en la sesión como contexto de solo lectura, nunca como parámetro de la petición | Hecha (`d9b6271`) | `POST /auth/conjunto-activo/` escribe en `TokenDeSesion.conjunto_activo`; `VistaDeConjunto` rechaza el conjunto en cualquier otra petición |
| Selección automática y sin pantalla cuando la persona pertenece a un solo conjunto | Hecha (`d9b6271`) | `iniciar_sesion()` en `apps/cuentas/servicios.py` |
| Pantalla de selección con nombre, logo y color base de cada conjunto (frontend) | Hecha | `conjuntos/selector.html` pide la lista con `cliente_api.cuentas.listar_conjuntos()` y pinta cada tarjeta con su color (`atributos_de_acento`) y su foto o sus iniciales (`_foto.html`). La foto y el color llegaron con HU-21 |
| Cambio de conjunto activo desde la barra superior, con recálculo de permisos efectivos | Hecha | «Cambiar de conjunto» lleva al selector, que llama `cliente_api.cuentas.elegir_conjunto()`; la sesión del front guarda los permisos y el rol del conjunto nuevo |

| Criterio de aceptación | Estado |
|---|---|
| Con asignaciones vigentes en tres conjuntos, al iniciar sesión los ve y debe elegir uno antes de continuar | Hecho y probado: entra sin conjunto activo, ve los tres y una vista de conjunto responde 403 hasta que elija |
| Con un solo conjunto entra directo, sin pantalla de selección | Hecho y probado |
| Con un conjunto activo, cualquier módulo muestra solo datos de ese conjunto | Hecho y probado, también al cambiar de conjunto |
| Al cambiar de conjunto, los permisos pasan a ser los de su rol en el nuevo y ninguno del anterior | Hecho y probado (Administración en un conjunto, Residente en otro) |
| Un conjunto desactivado o sin asignación vigente no aparece en la lista | Hecho y probado. Un conjunto no operativo sí aparece ([pendientes](pendientes.md), sección 5) |

Desde el 2026-10-11 el selector ofrece «Crear conjunto» a quien es Administración en alguno de sus conjuntos (`puede_crear_conjunto`), con cuatro pruebas en `tests/test_identidad.py` del front.

## HU-06 · Asignación de roles del catálogo fijo — 5 de 5 tareas, falta la DoD

Actualizado el 2026-09-27 con `b5003af` (API) y `25132e8` (pantalla). Las pruebas nuevas están en `apps/permisos/test_roles.py`.

| Criterio de aceptación | Prueba | Pasa |
|---|---|---|
| Al asignar un rol, la persona obtiene la unión de permisos de todos sus roles | `test_asignar_un_rol_suma_los_permisos_de_todos_sus_roles` | Sí |
| Nadie puede crear ni editar un rol desde la interfaz o la API | `test_no_existe_crear_ni_editar_roles`: solo existen `usuario-roles` y `usuario-rol-retirar`; `"operador"` y `"superusuario"` → 400 | Sí |
| Un rol asignado en el conjunto A no da permisos en el B | `test_rol_de_un_conjunto_no_da_permisos_en_otro` (ya existía) | Sí |
| El rol de plataforma no incluye `reserva.aprobar`, `anuncio.publicar` ni `infraccion.registrar` | `test_rol_de_plataforma_no_opera_dentro_de_un_conjunto` (ya existía) | Sí |
| Retirar el rol al último usuario con Administración falla | `test_retirar_el_rol_al_ultimo_de_administracion_falla`, `test_con_dos_administradores_se_retira_uno` y `test_dos_retiros_a_la_vez_no_dejan_el_conjunto_sin_administracion` (dos hilos) | Sí |
| Auditoría de asignaciones (tarea) | `test_asignar_y_retirar_quedan_en_la_auditoria` | Sí |

Extras: retirar quita los permisos de inmediato; asignar un rol vigente → 409; sin `rol.asignar` → 403. En el front, `tests/test_usuarios.py`: sin `rol.asignar` no hay botones, el 409 se muestra y asignar vuelve al detalle.

## HU-07 · Vincular persona existente por búsqueda de documento — criterios en código, falta la DoD

`37aeb85` (API) y `f4da065` (pantalla). Pruebas en `apps/personas/test_busqueda.py`.

| Criterio de aceptación | Prueba | Pasa |
|---|---|---|
| Documento existente → se vincula sin crear un registro nuevo | `test_documento_existente_se_vincula_sin_crear_otra_persona` | Sí |
| Documento inexistente → se ofrece crear | API: `test_documento_inexistente_no_encuentra_a_nadie`. Front: `test_no_encontrada_lleva_al_alta_con_el_documento_y_sin_ponerlo_en_la_url` | Sí |
| Cada búsqueda queda en la auditoría con quién y qué documento | `test_cada_busqueda_queda_en_la_auditoria_con_quien_y_que_documento` | Sí |
| Pasar el límite de búsquedas se rechaza | `test_pasar_el_limite_de_busquedas_se_rechaza`: 20 en la última hora → 429; una de hace 2 h no cuenta | Sí |
| Vinculada a dos conjuntos, sus roles del otro no dan permisos | `test_vinculada_a_dos_conjuntos_sus_roles_del_otro_no_dan_permisos` | Sí |

Extras: con puntos y espacios encuentra igual, un número parcial no; la respuesta no trae teléfono, correo ni datos de otros conjuntos; vincular un rol vigente → 409. En el front, el documento nunca aparece en una URL.

## HU-08 · Vínculos de unidad y enrutamiento de notificaciones — criterios en código, falta la DoD

`89e793c` (API) y `a9350c2` (pantalla). Pruebas en `apps/unidades/tests.py`.

| Criterio de aceptación | Prueba | Pasa |
|---|---|---|
| Propietario y arrendatario vigentes coexisten | `test_propietario_y_arrendatario_vigentes_coexisten` | Sí |
| Al cerrar el vínculo del arrendatario, el histórico se conserva | `test_al_cerrar_el_vinculo_del_arrendatario_el_historico_se_conserva` (sin `DELETE`: 405) | Sí |
| Convocatoria a asamblea → al propietario aunque no resida | `test_cada_hecho_llega_a_quien_corresponde_segun_el_vinculo` (ya existía) | Sí |
| Infracción → propietario y arrendatario | La misma prueba (ya existía) | Sí |
| Propietario no residente con rol Residente no puede reservar | `test_un_propietario_que_no_vive_ahi_no_puede_reservar` (tomar → 400) y `test_sin_vivir_en_la_unidad_elegida_la_alfa_lo_impide` (alfa `RESIDE`), en `apps/reservas/tests.py` | Sí |

Extras: vincular a una persona sin rol en el conjunto → 400 (P3); vínculo duplicado → 409; cerrar dos veces → 409; cierre antes del inicio → 400; auditoría de unidad y vínculo.

## HU-09 · Catálogo de áreas comunes del conjunto — criterios en código, falta la DoD

`f933349`, `ff24541` (API) y `daf56af` (pantalla y paso del asistente). Pruebas en `apps/areas/tests.py`.

| Criterio de aceptación | Prueba | Pasa |
|---|---|---|
| Al crear un área hay que elegir la clasificación de la lista cerrada | `test_al_crear_un_area_hay_que_elegir_la_clasificacion_de_la_lista_cerrada` | Sí |
| Un área común esencial tiene `es_esencial` verdadero | `test_solo_un_area_comun_esencial_es_esencial` | Sí |
| Un área en mantenimiento no admite solicitudes | `test_un_area_en_mantenimiento_no_admite_solicitudes` (tomar → 409), en `apps/reservas/tests.py` | Sí |
| Sin `area.gestionar`, editar → 403 | `test_sin_area_gestionar_no_se_crea_ni_se_edita_y_solo_se_ven_las_activas` | Sí |
| Un área retirada se desactiva, no se borra | `test_un_area_retirada_se_desactiva_y_no_se_borra` | Sí |
| Regla alfa de mora sobre áreas esenciales | `test_una_unidad_en_mora_no_pide_un_area_no_esencial_pero_si_una_esencial`, en `apps/reservas/tests.py` | Sí |

Extras: el requisito `areas` de `requisitos_para_operar` se cumple con un área activa; nombre repetido → 400; cierre antes de la apertura → 400; auditoría de crear, editar, mantenimiento y desactivar.

## HU-10 · Configuración de reglas beta de reserva — criterios en código, falta la DoD

`bb5586f`, `a8be0ae` (API) y `2e11201` (pantalla y paso del asistente). Pruebas en `apps/reglas/tests.py`.

| Criterio de aceptación | Prueba | Pasa |
|---|---|---|
| Sin reglas, el conjunto no puede quedar operativo | `test_sin_reglas_el_conjunto_no_puede_quedar_operativo` | Sí |
| Una regla exige tipo, parámetros, área y vigencia | `test_una_regla_exige_tipo_parametros_area_y_vigencia` (cuatro casos) | Sí |
| Una regla permisiva se rechaza | `test_una_regla_permisiva_se_rechaza` | Sí |
| Una regla beta no relaja una alfa | `test_una_regla_beta_no_relaja_una_alfa` | Sí |
| Se aplican en AND sin precedencias | `test_el_evaluador_no_se_detiene_en_la_primera_falla` y `test_si_incumple_tres_reglas_ve_los_tres_motivos_y_se_libera_el_bloqueo` | Sí |
| Una regla editada deja autor y fecha | `test_una_regla_editada_deja_version_autor_y_fecha` | Sí |

Extras: cada tipo se crea y se describe en palabras; parámetros de más o equivocados → 400; área de otro conjunto → 400; retirar cierra la vigencia y la conserva.

## HU-11 · Bloqueo exclusivo de 3 minutos sobre una franja — criterios en código, falta la DoD

`ddac827`, `05c621c`, `9d99568`, `06f2340` (backend) y `d7b04a8`, `6aa1a3d` (front). Pruebas en `apps/reservas/tests.py` y `tests/concurrencia/`.

| Criterio de aceptación | Prueba | Pasa |
|---|---|---|
| Franja libre + Reservar → `EN_SOLICITUD` y reloj de 3 minutos | `test_franja_libre_y_reservar_deja_la_solicitud_en_tramite_con_3_minutos` | Sí |
| Otra persona sobre una franja en trámite → aviso inmediato | `test_otra_persona_sobre_una_franja_en_tramite_recibe_el_aviso_de_inmediato` y `test_n_residentes_sobre_la_misma_franja_producen_exactamente_un_bloqueo` (10 hilos) | Sí |
| Bloqueo vencido + acceso → `EXPIRADA` y franja libre | `test_un_bloqueo_vencido_expira_al_siguiente_acceso_y_la_franja_queda_libre` y `test_un_bloqueo_vencido_no_bloquea` | Sí |
| Con un bloqueo activo no toma otro en ninguna área | `test_con_un_bloqueo_activo_no_se_toma_otro_en_ninguna_area` | Sí |
| Al cerrar el formulario, el bloqueo se libera sin esperar | `test_al_cerrar_el_formulario_el_bloqueo_se_libera_sin_esperar` y `test_uno_liberado_a_mano_no_expira_dos_veces`. El `sendBeacon` al cerrar la pestaña va al guion manual | Sí (el beacon, pendiente de prueba manual) |

Extras: cada quien ve la franja propia como "Tuya" y la ajena sin saber de quién es; una franja que ya empezó no se toma; solo se ven las solicitudes propias.

## HU-12 · Confirmación de contenido antes de enviar — criterios en código, falta la DoD

`000c335` (avisos) y `f6b8fef` (panel). Pruebas en `apps/reservas/tests.py` y `tests/test_reservas.py` del front.

| Criterio de aceptación | Prueba | Pasa |
|---|---|---|
| Ve el área, el día de la semana en letras, la fecha y el horario | `test_el_panel_dice_el_area_el_dia_de_la_semana_en_letras_la_fecha_y_el_horario` (front) | Sí |
| Corregir vuelve sin perder lo escrito | Guion manual (JavaScript). En código: el formulario se oculta con `x-show`, no se destruye | Pendiente de prueba manual |
| Una fecha atípica se resalta sin impedir el envío | Tres pruebas de `avisos` en el backend y `test_los_avisos_se_muestran_con_texto_y_no_deshabilitan_el_envio` (front). Alta demanda llega con PB-24 | Sí |
| El panel abierto no detiene ni extiende el reloj | Guion manual. En código: el reloj vive en el mismo `x-data` y no se reinicia | Pendiente de prueba manual |
| Un envío que salta la interfaz se evalúa igual | `test_un_envio_que_salta_la_interfaz_se_evalua_igual` | Sí |

## HU-13 · Envío de solicitud y motor de reglas alfa/beta — criterios en código, falta la DoD

`a8e6ca5`, `66f8897` (backend) y `c1d8f6b` (front). Pruebas en `apps/reservas/tests.py` y `apps/reglas/tests.py`.

| Criterio de aceptación | Prueba | Pasa |
|---|---|---|
| Una solicitud válida pasa a `APARTADA` y se avisa a la Administración | `test_una_solicitud_valida_queda_apartada_y_se_avisa_a_la_administracion` (Consejo no recibe el aviso) | Sí |
| Si incumple tres reglas, ve los tres motivos y se libera el bloqueo | `test_si_incumple_tres_reglas_ve_los_tres_motivos_y_se_libera_el_bloqueo` | Sí |
| Sin vínculo vigente con `reside`, la alfa lo impide | `test_sin_vivir_en_la_unidad_elegida_la_alfa_lo_impide` | Sí |
| Una unidad en mora no puede pedir un área no esencial | `test_una_unidad_en_mora_no_pide_un_area_no_esencial_pero_si_una_esencial` y `test_paz_y_salvo_solo_restringe_areas_no_esenciales` | Sí |
| Queda registrado qué reglas se evaluaron y con qué resultado | `test_queda_registrado_que_reglas_se_evaluaron_y_con_que_resultado` | Sí |
| Pruebas por cada tipo de regla | `test_cada_tipo_cumple_o_no_segun_sus_parametros` (5 tipos), `test_el_cupo_por_unidad_cuenta_las_apartadas_de_la_ventana` y la de paz y salvo | Sí |

Extras: enviar vencida → `EXPIRADA` y 409; la de otra persona → 404; dos veces → 409; sin motivo o con 0 asistentes → 400. Las alfas de piscina y de cobro quedan fuera: no hay datos con qué evaluarlas.

## HU-01 · Inicio de sesión con correo y contraseña — 5 de 5 tareas, falta la DoD

Verificado el 2026-10-11.

| Tarea técnica (Notion) | Estado | Evidencia |
|---|---|---|
| Modelo Usuario y hash de contraseña (backend) | Hecha | `apps/cuentas/models.py`, `962853f`. Contraseña con el hash de Django, login por correo sin distinguir mayúsculas |
| Endpoint `POST /auth/login` con emisión de token de sesión | Hecha | `POST /auth/login/`, `0b0c4f8` |
| Flujo de recuperación de contraseña por SMTP | Hecha | `POST /auth/recuperar/` y `POST /auth/recuperar/confirmar/` (`eab833e`, 21/09). Desde el 05/10 (`1c82605`), 3 enlaces por hora por correo (`limites.py`) y correo real por SMTP cuando el `.env` trae `EMAIL_HOST` |
| Pantalla de login y manejo de errores (frontend) | Hecha | `557bc9f`. `apps/cuentas/` y `cliente_api/` del front: errores por campo, mensaje genérico y aviso si la API no responde |
| Pruebas unitarias de autenticación y expiración de token | Hecha | `apps/cuentas/tests.py`; la recuperación tiene nueve pruebas propias ahí y `tests/test_recuperacion.py` en el front |

| Criterio de aceptación | Estado |
|---|---|
| Con credenciales válidas accede y ve el selector de conjunto activo | Hecho: el selector es real (HU-26) |
| Con credenciales inválidas ve un mensaje genérico sin revelar si el correo existe | Hecho y probado en la API; la pantalla muestra ese mismo mensaje |
| Un usuario desactivado no puede entrar | Hecho y probado, también si se desactiva la persona o se desactiva con la sesión abierta |
| Quien olvidó la contraseña recibe un enlace de un solo uso por correo | Hecho y probado: `test_quien_olvido_la_contrasena_recibe_un_enlace_por_correo`, `test_el_enlace_sirve_una_sola_vez` y `test_el_enlace_vencido_no_sirve` |
| Con un token vencido el sistema exige iniciar sesión de nuevo | Hecho y probado en la API (401). En el front la sesión vence a la misma hora que el token y vuelve al ingreso |

Lo que queda abierto, que no es de ningún criterio: `send_mail` síncrono y sin `try`, y `/auth/login/` sin límite de intentos ([pendientes](pendientes.md), sección 8).

## HU-03 · Asistente por pasos para crear un conjunto — 5 de 5 tareas, falta la DoD

Verificado el 2026-10-11. Cómo quedó: [conjuntos](../05_Modulos/conjuntos.md).

| Tarea técnica (Notion) | Estado | Evidencia |
|---|---|---|
| Modelo Conjunto con campo `activo` y `conjunto_id NOT NULL` en toda tabla salvo las globales declaradas | Hecha | `apps/conjuntos/models.py` (`activo`, y `operativo`, que nace en falso). El `NOT NULL` lo imponen `ModeloDeConjunto` y la prueba transversal |
| Endpoints del asistente por pasos con guardado parcial | Hecha | `POST /conjuntos/` crea el conjunto en el paso 1 y cada paso siguiente guarda en su propia app (`unidades`, `cuentas`, `areas`, `reglas`, `documentos`): se puede salir y volver |
| Validación de mínimos para marcar el conjunto como operativo | Hecha | `servicios.requisitos_para_operar()` con seis requisitos y `POST /conjuntos/actual/activar/`, que responde 400 con los `faltantes` |
| Asistente multipaso en frontend con resumen final | Hecha | Siete pasos en `apps/conjuntos/` del front (`asistente_datos`, `_viviendas`, `_administracion`, `_areas`, el tablero de reglas, `_reglamento` y `_resumen`) |
| Pruebas del invariante: conjunto incompleto no queda operativo | Hecha | `test_conjunto_incompleto_no_queda_operativo`, `test_sin_viviendas_el_conjunto_no_queda_operativo`, `test_sin_reglamento_el_conjunto_no_queda_operativo` y `test_un_conjunto_completo_queda_operativo`, en `apps/conjuntos/tests.py` |

**Criterios de aceptación: sin comparar uno por uno.** Los de Notion describen el asistente anterior, de cinco pasos; el de hoy tiene siete pasos, seis requisitos y lo activa también Administración ([pendientes](pendientes.md), sección 6).

## HU-02 · Segundo factor (TOTP) para permisos sensibles — 5 de 5 tareas, falta la DoD

Verificado el 2026-10-11. Las pruebas citadas están en `apps/cuentas/test_dos_factores.py`.

| Tarea técnica (Notion) | Estado | Evidencia |
|---|---|---|
| Marcar permisos sensibles en el catálogo fijo (backend) | Hecha | `PERMISOS_SENSIBLES` en `apps/permisos/catalogo.py`: hoy son 20, todos los de plataforma incluidos |
| Generación de secreto TOTP y código QR de vinculación | Hecha | `POST /auth/dos-factores/configurar/` y `…/activar/` (`eab833e`, 21/09), con `django-otp` y `qrcode`. `test_configurar_entrega_el_qr_y_la_clave_para_la_aplicacion` |
| Verificación del código en el login y códigos de respaldo | Hecha | `POST /auth/dos-factores/verificar/`; al activar entrega 10 códigos de respaldo. `test_un_codigo_de_respaldo_sirve_una_sola_vez` |
| Pantallas de activación y de verificación (frontend) | Hecha | `apps/cuentas/` del front: configurar, verificar, códigos de respaldo y, desde el 05/10, pedir y confirmar el enlace que lo quita. `tests/test_segundo_factor.py` |
| Pruebas: usuario con permiso sensible no puede operar sin 2FA activo | Hecha | `test_con_permiso_sensible_y_sin_configurar_no_puede_continuar` |

| Criterio de aceptación | Estado |
|---|---|
| Con un permiso sensible y sin 2FA configurado, debe configurarlo antes de continuar | Hecho y probado: `test_con_permiso_sensible_y_sin_configurar_no_puede_continuar` |
| Con 2FA activo y un código válido, accede | Hecho y probado: `test_con_un_codigo_valido_accede` |
| Un código expirado o repetido se rechaza | Hecho y probado: `test_un_codigo_vencido_se_rechaza` y `test_un_codigo_repetido_se_rechaza` |
| Un usuario solo con rol Residente no necesita 2FA | Hecho y probado: `test_residente_no_necesita_segundo_factor` |
| Un Superusuario siempre necesita 2FA | Hecho y probado: `test_superusuario_siempre_necesita_segundo_factor` |

El enlace por correo que quita el segundo factor (05/10) no es de ningún criterio y tiene ocho pruebas en el mismo archivo.

## Ver también

- [historias](historias.md) — el estado de las 40 historias, con su módulo y su plan
- [pruebas_y_ejecucion](../02_Arquitectura/pruebas_y_ejecucion.md) — qué cubre cada archivo de pruebas
- [scrum_y_dod](../03_Reglas/scrum_y_dod.md) — la Definition of Done que les falta a todas
- [Admind_Plan_Sprints_2_3](../07_Planes/hechos/Admind_Plan_Sprints_2_3.md) — el plan de HU-06 a HU-13

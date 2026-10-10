# AdMind — índice de la documentación

Una línea por nota: qué tiene y cuándo abrirla. Las reglas para agentes de IA están en [AGENTS](AGENTS.md); cómo se mantiene esta bóveda, en [documentacion](03_Reglas/documentacion.md).

## 01 Contexto — qué es el proyecto

| Nota | Qué tiene |
|---|---|
| [que_es_admind](01_Contexto/que_es_admind.md) | El problema, los cuatro pilares y el diferenciador |
| [equipo](01_Contexto/equipo.md) | Alejo y Camilo, punto de partida técnico y disponibilidad |
| [alcance](01_Contexto/alcance.md) | Núcleo, Comprometido, Condicional y Fuera de alcance |
| [legal](01_Contexto/legal.md) | Marco normativo y reglas duras. Manda sobre todo lo demás |
| [glosario](01_Contexto/glosario.md) | Términos del proyecto y del código |

## 02 Arquitectura — cómo está hecho

| Nota | Qué tiene |
|---|---|
| [mapa_codigo](02_Arquitectura/mapa_codigo.md) | Qué hay en cada carpeta, qué hace cada app y qué nota la explica. **Empieza aquí para ubicar código** |
| [vision_general](02_Arquitectura/vision_general.md) | Dos servidores Django, el diagrama y el flujo por capas que pide el profesor |
| [backend](02_Arquitectura/backend.md) | Anatomía de una app, bloqueo compartido y auditoría |
| [frontend](02_Arquitectura/frontend.md) | `cliente_api`, la sesión del front y el estado de cada pantalla |
| [stack](02_Arquitectura/stack.md) | Versiones en uso y por qué Django y PostgreSQL |
| [pruebas_y_ejecucion](02_Arquitectura/pruebas_y_ejecucion.md) | Comandos, qué cubre cada suite y cuál falla hoy |
| [restricciones_bd](02_Arquitectura/restricciones_bd.md) | Lo que hace cumplir PostgreSQL |
| [repositorios](02_Arquitectura/repositorios.md) | Los tres repositorios y por qué no submódulos |
| [entorno_local](02_Arquitectura/entorno_local.md) | La máquina de Alejo: Python 3.14, PostgreSQL 18, sin Docker |

## 03 Reglas — lo que se respeta al construir

| Nota | Qué tiene |
|---|---|
| [invariantes](03_Reglas/invariantes.md) | Lo que toda pieza nueva respeta y cómo se hace en este código. **Antes de crear tabla, endpoint o pantalla** |
| [capas](03_Reglas/capas.md) | Regla de dirección, códigos HTTP y en qué archivo va cada regla |
| [aislamiento](03_Reglas/aislamiento.md) | Blindaje entre conjuntos: diseño, cómo está construido y límites |
| [eliminacion](03_Reglas/eliminacion.md) | Sin borrado físico, baja lógica, anulación |
| [reglas_frontend](03_Reglas/reglas_frontend.md) | Qué va en cada carpeta del front y qué no hace nunca |
| [convenciones](03_Reglas/convenciones.md) | Estilo del código, nombres y lo que no se toca sin preguntar |
| [lista_de_salida](03_Reglas/lista_de_salida.md) | Comprobación antes de dar algo por terminado |
| [git](03_Reglas/git.md) | Ramas del curso, formato de commit y rutina diaria |
| [scrum_y_dod](03_Reglas/scrum_y_dod.md) | Sprints, Definition of Done y evidencias para el jurado |
| [trabajo_con_ia](03_Reglas/trabajo_con_ia.md) | Cómo trabaja un agente aquí: construir lo pedido, qué preguntar |
| [documentacion](03_Reglas/documentacion.md) | Cómo está organizada esta bóveda y cómo se escribe en ella |

## 04 Diseño — sistema visual

| Nota | Qué tiene |
|---|---|
| [sistema_visual](04_Diseno/sistema_visual.md) | Principios, tokens, acentos, bento, voz y DoD visual |
| [implementacion](04_Diseno/implementacion.md) | Cómo está en el código: tokens, componentes `am-*`, acento y foto |

## 05 Módulos — reglas de negocio de cada uno

| Nota | App | Qué tiene |
|---|---|---|
| [reservas](05_Modulos/reservas.md) | `reservas` | Estados, bloqueo de 3 minutos, confirmación y el recorrido completo en el código |
| [motor_reglas](05_Modulos/motor_reglas.md) | `reglas` | Reglas del sistema, alfa (del conjunto) y beta (de la zona): definición del 2026-10-06 y cómo quedó construida para las áreas con reserva |
| [ingresos](05_Modulos/ingresos.md) | `ingresos` | Zonas con ingreso: registro en la puerta, aforo simultáneo y salida. Construido el 2026-10-08 con salvaguardas legales (sin commit ni `migrate`); sin historia; lo legal sigue sin verificar |
| [personas](05_Modulos/personas.md) | `personas` | Identidad global, UUID y documento normalizado |
| [permisos](05_Modulos/permisos.md) | `permisos` | Catálogo de roles y permisos, Superusuario, un rol por conjunto |
| [cuentas](05_Modulos/cuentas.md) | `cuentas` | Sesión, token, conjunto activo y segundo factor |
| [conjuntos](05_Modulos/conjuntos.md) | `conjuntos` | Color propio y foto 1:1 del conjunto |
| [unidades](05_Modulos/unidades.md) | `unidades` | Vínculos de unidad y a quién se notifica cada hecho |
| [triage](05_Modulos/triage.md) | `triage`, `anuncios` | Secretaría, prioridad, rechazo formal, bandeja y anuncios |
| [parqueaderos](05_Modulos/parqueaderos.md) | `parqueaderos` | Asignación a apartamentos y parqueaderos de visitantes |
| [infracciones](05_Modulos/infracciones.md) | `infracciones` | Registro y notificación; el sistema no sanciona |
| [citas](05_Modulos/citas.md) | `citas` | Citas y cambio de horario con alternativas |

## 06 Decisiones

| Nota | Qué tiene |
|---|---|
| [cerradas](06_Decisiones/cerradas.md) | Las 30 decisiones de diseño. No se rediscuten |
| [construccion](06_Decisiones/construccion.md) | Decisiones tomadas al construir, por fecha (incluye D1 a D12). **Lo más reciente** |
| [abiertas](06_Decisiones/abiertas.md) | Contradicciones sin cerrar. Un agente no las resuelve |
| [decidido_y_propuesto](06_Decisiones/decidido_y_propuesto.md) | Qué es un hecho y qué es solo una sugerencia |
| [riesgos](06_Decisiones/riesgos.md) | R1 a R14 con su mitigación |

## 07 Planes

| Nota | Qué tiene |
|---|---|
| [planes](07_Planes/planes.md) | Lista de planes activos y hechos |

## 08 Estado — cómo va

| Nota | Qué tiene |
|---|---|
| [estado_actual](08_Estado/estado_actual.md) | Commits, pruebas, historias por grupo y qué frena. **Empieza aquí para saber cómo va** |
| [historias](08_Estado/historias.md) | Las 38 historias con su avance y lo que le falta a cada una |
| [pendientes](08_Estado/pendientes.md) | Lista completa de pendientes |
| [bitacora](08_Estado/bitacora.md) | Un hecho por fila, con fecha y commit |
| [historias_evidencia](08_Estado/historias_evidencia.md) | Tarea por tarea y criterio por criterio (parte es vieja) |
| [inventario_codigo](08_Estado/inventario_codigo.md) | Inventario histórico pieza por pieza (15/09 y 27/09) |
| [backlog_y_plazo](08_Estado/backlog_y_plazo.md) | Plan original de 7 sprints, velocidad y plazo de un mes |

## 09 Protocolos — tareas que se repiten

| Protocolo | Cuándo |
|---|---|
| [actualizar_contexto](09_Protocolos/actualizar_contexto.md) | Al terminar una tarea que cambió código, decisiones o estado |
| [generar_informe_de_avance](09_Protocolos/generar_informe_de_avance.md) | Entregable para el docente, con capturas |
| [generar_documento_de_avance](09_Protocolos/generar_documento_de_avance.md) | Foto fechada del proyecto para el equipo, solo texto |
| [abrir_y_cerrar_un_plan](09_Protocolos/abrir_y_cerrar_un_plan.md) | Antes de un trabajo largo y al terminarlo |
| [Inicio](Inicio.md) | Prompt de arranque de un chat de planeación: recibe una funcionalidad y entrega un plan guiado |
| [ejecutar_plan_guiado](09_Protocolos/ejecutar_plan_guiado.md) | Al ejecutar un plan con `modo: guiado`, si Alejo lo aprueba cuando el agente le pregunta: explica por bloques, Alejo aplica y el avance se anota en el plan |

Las plantillas están en `09_Protocolos/Plantillas/`.

## Fuera del recorrido de un agente

| Carpeta | Qué hay |
|---|---|
| `Guias/` | Tutoriales para personas: [estructura actual](Guias/Admind_Guia_Estructura_Actual.md) (30/09), [guía de desarrollo](Guias/Admind_Guia_Desarrollo.md) (15/09), [instalación local](Guias/Admind_Backend_Instalacion_Local.md) e [inicialización del backend](Guias/Admind_Backend_Inicializacion.md) |
| `Archivo/` | Fotos de avance, informes al docente, lab y notas. Histórico |
| `Credenciales/` | No la abre un agente |
| [Admin_Master](Admin_Master.md) | Tabla de equivalencias: dónde quedó cada sección del maestro |

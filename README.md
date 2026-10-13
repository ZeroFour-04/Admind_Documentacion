# AdMind — índice de la documentación

**Última revisión completa de la bóveda: 2026-10-11**, contra Backend `d4e98e5`, Frontend `a946880` y `admind_db` ([bitacora](08_Estado/bitacora.md)). Cada nota lleva en su frontmatter `actualizado` (cuándo cambió su contenido) y `revisado` (cuándo se contrastó por última vez con el proyecto).

Las reglas para agentes de IA están en [AGENTS](AGENTS.md); cómo se mantiene esta bóveda, en [documentacion](03_Reglas/documentacion.md).

## Por dónde entrar

| Si buscas… | Empieza en |
|---|---|
| Cómo va el proyecto hoy | [estado_actual](08_Estado/estado_actual.md) |
| Una **historia** (HU-16): qué hay, qué le falta, su módulo y su plan | [historias](08_Estado/historias.md) |
| Una **app o una carpeta** del código: qué hace y qué nota la explica | [mapa_codigo](02_Arquitectura/mapa_codigo.md) |
| Las **reglas de negocio** de un módulo | Su nota en la tabla *05 Módulos*, más abajo |
| Qué respetar **antes de crear** una tabla, un endpoint o una pantalla | [invariantes](03_Reglas/invariantes.md) |
| Lo que **falta**: pruebas manuales, avisos a Camilo, lo legal, decisiones | [pendientes](08_Estado/pendientes.md) |
| **Por qué** algo es así | [construccion](06_Decisiones/construccion.md) (al construir) y [cerradas](06_Decisiones/cerradas.md) (de diseño) |
| Algo que **no está decidido** | [abiertas](06_Decisiones/abiertas.md) |
| **Qué pasó un día** | [bitacora](08_Estado/bitacora.md) |
| Una cita como *maestro §5.4*, *R12*, *D3* o *decisión 24* | [Admin_Master](Admin_Master.md) |
| Un **término** | [glosario](01_Contexto/glosario.md) |
| El **plan** con que se construyó algo y su guion de prueba | [planes](07_Planes/planes.md) |

Cómo se relacionan las notas: toda nota termina en una sección *Ver también*, y las de módulo dicen en su frontmatter `modulo:` (la app) y `hu:` (sus historias). Para ver quién enlaza una nota, busca su nombre de archivo en la bóveda o ábrela en el grafo de Obsidian.

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
| [backend](02_Arquitectura/backend.md) | Anatomía de una app, bloqueo compartido, auditoría y validación de archivos |
| [frontend](02_Arquitectura/frontend.md) | `cliente_api`, la sesión del front y el estado de cada pantalla |
| [stack](02_Arquitectura/stack.md) | Versiones en uso y por qué Django y PostgreSQL |
| [pruebas_y_ejecucion](02_Arquitectura/pruebas_y_ejecucion.md) | Comandos, cuántas pruebas hay, qué cubre cada archivo y cuál falla hoy |
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

*Estado* es el del código al 2026-10-11; el detalle por historia está en [historias](08_Estado/historias.md).

| Nota | App | Historias | Estado | Qué tiene |
|---|---|---|---|---|
| [reservas](05_Modulos/reservas.md) | `reservas` | HU-11 a HU-19 | Construido hasta HU-14 y HU-16 | Estados, bloqueo de 3 minutos, confirmación, decisión, pago declarado y el recorrido completo en el código |
| [motor_reglas](05_Modulos/motor_reglas.md) | `reglas`, `areas` | HU-09, HU-10, HU-13 | Construido | Reglas del sistema, alfa (del conjunto) y beta (de la zona), y los dos modos de uso de una zona |
| [ingresos](05_Modulos/ingresos.md) | `ingresos` | Sin historia | Construido; lo legal sin verificar | Zonas con ingreso: registro en la puerta, aforo simultáneo y salida |
| [pagos](05_Modulos/pagos.md) | `pagos` | HU-35 | Construido; la mora, sin verificar lo legal | Pago de la administración por vivienda y mes, y la mora de paz y salvo |
| [parqueaderos](05_Modulos/parqueaderos.md) | `parqueaderos`, `visitantes` | HU-27, HU-28, HU-34 | HU-28 construida, HU-27 parcial, HU-34 sin empezar | Catálogo de parqueaderos y el de visitantes atado a la visita |
| [unidades](05_Modulos/unidades.md) | `unidades`, `notificaciones` | HU-08, HU-39 | Construido; HU-39, primera parte | Viviendas, agrupaciones, vínculos y a quién se notifica cada hecho |
| [conjuntos](05_Modulos/conjuntos.md) | `conjuntos`, `documentos` | HU-03, HU-21, HU-33 | Construido; HU-33, solo el reglamento | Asistente de creación, requisitos para quedar operativo, color propio y foto 1:1 |
| [cuentas](05_Modulos/cuentas.md) | `cuentas` | HU-01, HU-02, HU-26 | Construido | Sesión, token, conjunto activo, segundo factor y recuperación |
| [permisos](05_Modulos/permisos.md) | `permisos` | HU-06 | Construido | Catálogo de roles y permisos, Superusuario, un rol por conjunto |
| [personas](05_Modulos/personas.md) | `personas` | HU-04, HU-07 | Construido | Identidad global, UUID y documento normalizado |
| [triage](05_Modulos/triage.md) | `anuncios`, `triage`, `casos` | HU-22 a HU-25, HU-29 | Solo los anuncios (HU-25) | Secretaría, prioridad, rechazo formal, bandeja y anuncios |
| [infracciones](05_Modulos/infracciones.md) | `infracciones` | HU-30 | Sin construir | Registro y notificación; el sistema no sanciona |
| [citas](05_Modulos/citas.md) | `citas` | HU-31, HU-32 | Sin construir | Citas y cambio de horario con alternativas |

El aislamiento entre conjuntos (HU-05) y la auditoría no tienen nota de módulo: están en [aislamiento](03_Reglas/aislamiento.md) y [backend](02_Arquitectura/backend.md).

## 06 Decisiones

| Nota | Qué tiene |
|---|---|
| [cerradas](06_Decisiones/cerradas.md) | Las 30 decisiones de diseño. No se rediscuten |
| [construccion](06_Decisiones/construccion.md) | Decisiones tomadas al construir, por fecha (incluye D1 a D12). **Lo más reciente** |
| [abiertas](06_Decisiones/abiertas.md) | Contradicciones y vacíos sin cerrar (12.1 a 12.10). Un agente no los resuelve |
| [decidido_y_propuesto](06_Decisiones/decidido_y_propuesto.md) | Qué es un hecho y qué es solo una sugerencia (corte 14/09) |
| [riesgos](06_Decisiones/riesgos.md) | R1 a R14 con su mitigación |

## 07 Planes

| Nota | Qué tiene |
|---|---|
| [planes](07_Planes/planes.md) | Los diez planes ejecutados, con su historia y la nota donde quedó lo vigente. No hay ninguno activo |

Los planes están en `07_Planes/hechos/` y son históricos: se abren para ver el guion de prueba manual o cómo se decidió algo, no para saber cómo es hoy.

## 08 Estado — cómo va

| Nota | Qué tiene |
|---|---|
| [estado_actual](08_Estado/estado_actual.md) | Commits, pruebas, migraciones, historias por sprint y qué frena. **Empieza aquí para saber cómo va** |
| [historias](08_Estado/historias.md) | Las 40 historias: estado, módulo, plan y lo que le falta a cada una |
| [pendientes](08_Estado/pendientes.md) | Todo lo que falta, ordenado por tipo |
| [bitacora](08_Estado/bitacora.md) | Un hecho por fila, con fecha y commit |
| [historias_evidencia](08_Estado/historias_evidencia.md) | Tarea por tarea y criterio por criterio de HU-01 a HU-13 y HU-26 |
| [backlog_y_plazo](08_Estado/backlog_y_plazo.md) | Plan original de 7 sprints, velocidad y plazo de un mes |

## 09 Protocolos — tareas que se repiten

| Protocolo | Cuándo |
|---|---|
| [actualizar_contexto](09_Protocolos/actualizar_contexto.md) | Al terminar una tarea que cambió código, decisiones o estado |
| [generar_informe_de_avance](09_Protocolos/generar_informe_de_avance.md) | Entregable para el docente, con capturas |
| [generar_documento_de_avance](09_Protocolos/generar_documento_de_avance.md) | Foto fechada del proyecto para el equipo, solo texto |
| [abrir_y_cerrar_un_plan](09_Protocolos/abrir_y_cerrar_un_plan.md) | Antes de un trabajo largo y al terminarlo |
| [Inicio](Inicio.md) | Prompt de arranque de un chat de planeación: recibe una funcionalidad y entrega un plan guiado |
| [ejecutar_plan_guiado](09_Protocolos/ejecutar_plan_guiado.md) | Al ejecutar un plan con `modo: guiado`, si Alejo lo aprueba cuando el agente le pregunta |

Plantillas, en `09_Protocolos/Plantillas/`: [nota](09_Protocolos/Plantillas/nota.md), [plan](09_Protocolos/Plantillas/plan.md), [plan_guiado](09_Protocolos/Plantillas/plan_guiado.md), [informe_de_avance](09_Protocolos/Plantillas/informe_de_avance.md) y [documento_de_avance](09_Protocolos/Plantillas/documento_de_avance.md).

## Fuera del recorrido de un agente

| Carpeta | Qué hay |
|---|---|
| `Guias/` | Tutoriales para personas, con fecha de corte: [estructura actual](Guias/Admind_Guia_Estructura_Actual.md) (30/09), [guía de desarrollo](Guias/Admind_Guia_Desarrollo.md) (15/09), [instalación local](Guias/Admind_Backend_Instalacion_Local.md) e [inicialización del backend](Guias/Admind_Backend_Inicializacion.md) (14/09). No se actualizan: lo vigente está en las carpetas numeradas |
| `Archivo/` | Histórico, no se edita: `Avances/` (fotos fechadas y el [inventario del código al 27/09](Archivo/Avances/Inventario_codigo_2026-09-27.md)), `Informes/` (los cuatro informes al docente), `Lab/` y `Notas/` (apuntes de Alejo) |
| `Credenciales/` | No la abre un agente |
| [Admin_Master](Admin_Master.md) | Tabla de equivalencias: dónde quedó cada sección del maestro y qué es cada identificador |

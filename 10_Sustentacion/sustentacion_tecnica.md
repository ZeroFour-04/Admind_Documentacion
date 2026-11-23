---
resumen: "Qué es la sustentación técnica final de AdMind, su fecha (movida del martes 17-nov al lunes 23-nov), la rúbrica del profesor, qué se entregó, cómo está cada criterio el 18-nov y dónde está cada fuente. Entrada para cualquier tarea sobre la sustentación."
tipo: contexto
origen: "guía del profesor (clase del 3-nov), plan de Alejo (F0 a F3), tareas.md (auditada el 17-nov a las 10:00), chats del 14 al 18-nov, y GitHub y el VPS el 18-nov. La fecha nueva la dijo Alejo en chat el 2026-11-18."
actualizado: 2026-11-23
revisado: 2026-11-23
---

# Sustentación técnica final de AdMind

**Si Alejo dice «la sustentación», «la sustentación técnica» o «lo del lunes», es esto.** Esta nota es la entrada; el detalle de cada tarea está en [tareas](tareas.md).

## Qué es y cuándo

| | |
|---|---|
| **Qué es** | Sustentación técnica final del proyecto de aula de Ingeniería de Software II, ante el profesor Oscar Gómez (técnico). Lo de negocio ya se presentó: esto es técnica «pura y dura». |
| **Duración** | Unos 15 minutos por equipo. |
| **Fecha original** | Martes **2026-11-17**, desde las 10:15. |
| **Fecha nueva** | **Lunes 2026-11-23.** Alejo lo dijo el 18-nov. La hora y el motivo del cambio no están escritos en ningún chat ni nota: preguntárselos antes de planear a la hora. |
| **Documentación** | Al aula el sábado **2026-11-14** antes de las 18:00. **Entregada.** Regla del profesor: *sin documentación no hay sustentación.* |
| **Dinámica** | QR en pantalla con el enlace de la app, o el enlace por Teams, para que el profesor la pruebe desde su equipo. Va a revisar GitHub: PR e historial del CI. |
| **Equipo** | Alejo y Camilo. Alejo lleva la documentación, el despliegue, el CI y el correo; Camilo, lo técnico del código (reparto en [tareas](tareas.md)). |
| **Clase de recuperación** | El profesor dijo el 3-nov que habría una sesión virtual grabada, «tentativamente lunes o martes», sobre CORS y SonarQube. No consta si se dio. |

> [!NOTE] Con la fecha movida
> El plan de [tareas](tareas.md) se escribió para el 17-nov: sus «lunes en la noche» y «martes temprano» ya no corresponden a los días de ahora. Las tareas siguen siendo las mismas; lo que cambió es cuánto tiempo hay. Si con ese tiempo se implementan JWT, CORS y Swagger, o se defienden como no hechos, es decisión de Alejo y Camilo, no de un agente.

## La rúbrica: 12 criterios

La mandó el profesor (guía de la clase del 3-nov) y es la base de todo. Estado al **2026-11-22**: `main` del back en `4cbb86b` y del front en `00d0f7e` (validación de formato del 23-nov), desplegados en el VPS, con el CI en verde (comprobado con `gh` y por SSH). Ese día entraron a `main` CORS (PR #19) y Swagger (PR #20) de Camilo, y el CI endurecido de Alejo (PR #21 del back y #12 del front), más un arreglo de sintaxis del `ci.yml` subido directo a `main` con permiso de Alejo.

| # | Criterio | Qué exige | Estado | Cómo se muestra |
|---|---|---|---|---|
| 1 | UX/UI | Línea gráfica uniforme, navegación intuitiva | Hecho (A4, en `main`). Inicio sigue vacío: sin decidir | La app desplegada, con el verde de AdMind |
| 2 | Roles, front y back | Mínimo 4; un rol no ve ni accede a lo de otro; permisos CRUD acotados | 5 roles; menú y endpoints por permiso | `tests/aislamiento/test_intruso.py` (recorre las 97 rutas) y A5 en vivo |
| 3 | Seguridad | Contraseñas con hash moderno; sin secretos expuestos | PBKDF2 de Django (`settings.py` no define `PASSWORD_HASHERS`; el MD5 de `settings_pruebas.py` es solo de pruebas). `DEBUG` y `ALLOWED_HOSTS` salen del entorno (C3, en `main`) | Manual técnico, sección de seguridad |
| 4 | API, CORS y JWT | Consumo funcional; JWT; CORS bien configurado | El consumo funciona. **CORS hecho** (PR #19 de Camilo, en `main` y en la nube el 22-nov): `django-cors-headers`, lista blanca desde `CORS_ALLOWED_ORIGINS`, que en el `.env` del back del VPS vale `https://admind.detkor.com`; pruebas en `tests/test_cors.py`. La rama `feat/cors` de Alejo quedó sin subir: la reemplaza la de Camilo. **JWT: no implementado** | `curl -X OPTIONS` en el VPS con dos `Origin` (comando en [reparto_sustentacion](reparto_sustentacion.md)); JWT, ver *Qué decir de lo que falta* |
| 5 | Documentación de la API | Swagger/OpenAPI **o** colección de Postman organizada | **Swagger hecho** (PR #20 de Camilo, en `main` y en la nube el 22-nov): `drf-spectacular` 0.30.0, `/api/schema/` y `/api/docs/`. El esquema de la nube tiene 101 rutas de negocio, 123 operaciones y 18 grupos | Captura `evidencias/swagger_nube_2026-11-22.jpg`; en vivo, por túnel SSH al puerto 8000 del VPS |
| 6 | Correo | Automático, HTML con logo y estilos | Hecho (A7: `EmailMultiAlternatives`, logo incrustado). Falta la captura desde la nube | Captura del correo en Gmail |
| 7 | Reportes | PDF o Excel con formato profesional | Hecho (C6: PDF de zonas y Excel de pagos, pantalla `/reportes/`; solo Administración y Superusuario). Falta descargarlos desde la nube | Archivos descargados de la app desplegada |
| 8 | Pruebas del back | 70 % de cobertura, camino feliz y de excepción, con reporte | 854 pruebas y 94,2 % en el CI de `main` del 22-nov; 865 en local el 23-nov. El front tiene 557 | El paso de cobertura en *Actions* y el artefacto `cobertura-backend` |
| 9 | Base de datos | Sustentar el diseño frente al MER inicial; 5 procedimientos y 5 triggers que sirvan | 4 funciones, 1 procedimiento (`sp_expirar_bloqueos_vencidos`) y 5 triggers, en migraciones, aplicados en el VPS el 17-nov | `\df`, `information_schema.triggers` y el [diccionario](datos/diccionario_datos.md), que hay que regenerar con esto |
| 10 | CI | Flujos automáticos, con historial | GitHub Actions en los dos repos, con ejecuciones desde el 16-nov. **Endurecido** (PR #21 del back y #12 del front, 22-nov): instala desde `requirements.lock` con hashes y solo wheels, token de solo lectura y acciones en Node 24. El back fija además las dependencias de `drf-spectacular`. Las dos primeras ejecuciones fallaron por un error de YAML (los dos puntos de `:all:`), corregido el mismo día. 30 ejecuciones en el back y 15 en el front. Las ramas no están protegidas | Pestaña *Actions* de cada repo |
| 11 | SonarQube | Primer escaneo, una vulnerabilidad alta o media corregida **por integrante**, segundo escaneo | SonarCloud analiza `main` y los PR. Primer escaneo el 17-nov: back 3 vulnerabilidades MAJOR (dos en `ci.yml`, una contraseña de ejemplo en `.env _ejemplo`), front 17 (las dos de `ci.yml`, una MAJOR en `cliente_api/http.py` y 14 MINOR). La de Alejo (las dos de `ci.yml`) entró a `main` el 22-nov. **Segundo escaneo el 22-nov: back 3 → 1, front 17 → 15**, seguridad C en los dos. **Falta la de Camilo**; la candidata es la del `.env _ejemplo`, que deja el back en 0 | Capturas `sonar_1_*` y `sonar_2_*`, y la pestaña *Activity* |
| 12 | Despliegue | 100 % en la nube (front, back y base) y operativo | `https://admind.detkor.com`, VPS de Oracle detrás de Cloudflare. Desplegado igual a `main` (back `4cbb86b`, front `00d0f7e`) desde el 23-nov, con CORS, Swagger y la validación de formato de los campos | QR, la app en vivo, `systemctl status` y la consola de Oracle |

Sobre los criterios 9 y 11: el profesor escribió «5 *stored procedures*» y «mínimo 4 integrantes». Son 2 personas, y 4 de los 5 triggers son el mismo `trg_sin_borrado_fisico` en cuatro tablas. Saber explicar por qué cuatro rutinas son funciones y una es procedimiento, y que el segundo trigger distinto es `trg_infraccion_anulada_inmutable`.

## Qué va a preguntar el profesor

Además de la rúbrica, según Alejo, casi seguro:
- **Pruebas unitarias** (sí o sí, porque no se definió a tiempo) y **despliegue**.
- **Seguridad básica** y **manejo de tokens de sesión.**
- **Romper la app desde el navegador:** jugar con la URL, darle *Atrás* tras cerrar sesión, entrar a pantallas de otro rol.
- **Errores legibles:** que la app diga por qué falló, no un código crudo.
- **Límites en los campos de texto:** va a intentar pasarlos.
- **Separación de roles:** lo que un rol no tiene no se puede ver de ninguna forma.
- **GitHub:** PR en vez de commits directos. Los dos primeros meses no hubo PR; ahora todo cambio entra por PR a `desarrollo`.

**Datos que hay que saber decir:** la sesión dura **1 hora contada desde el ingreso**, no «una hora sin uso». El token de sesión es **opaco y vive en una tabla**, así que cerrar sesión lo invalida de verdad, y nunca llega al navegador: lo guarda el servidor del front tras una cookie `HttpOnly`.

## Qué decir de lo que falta

Está en [tareas](tareas.md) (decisiones del 14-nov y bloque del 17-nov); el resumen:
- **JWT:** se decidió un híbrido (JWT firmado más la tabla de sesiones para revocar) y no se construyó. La defensa de hoy es el token opaco con revocación.
- **CORS y Swagger:** hechos desde el 22-nov. Si preguntan para qué sirve CORS si el navegador nunca llama a la API: cierra la puerta de atrás por si algún día la API se publica.
- **Otros faltantes que Alejo anotó el 14-nov:** accesibilidad (solo superficial: revisión por script en A4, sin prueba con teclado), validar el dominio del correo al registrar o recuperar, la importación por Excel (una HU de Camilo) y algunas HU de Notion. Estado sin verificar salvo la accesibilidad.

## Lo que ya se entregó

| Qué | Cuándo | Dónde |
|---|---|---|
| **F0, documentación al aula:** Manual Técnico (40 págs.), Manual de Usuario (80 págs., 57 capturas), Diccionario de Datos (33 págs. y Excel, 42 tablas), PDF del tablero de seguimiento Scrum y PDF con los enlaces a los repos | 14-nov | `Entregables_Sustentacion/Documentacion_Entregable/` y los `.docx` en `Entregables_Sustentacion/` |
| **Tres documentos de entrega final:** *Entrega Documentación Metodología Ágil* (7 págs.), *Entrega del Código del Proyecto* (3 págs.) y *Despliegue de Aplicaciones Empresariales - Entrega Final Proyecto de Curso* (13 págs.). Sin fechas, con los nombres de los dos en la portada | 18-nov, generados; Alejo los revisa | `Entregables_Sustentacion/Entrega_Final/` (`.docx` y `.pdf`). Su plan, con los datos del VPS y del tablero, es [plan_entrega_final_documentos](plan_entrega_final_documentos.md) |
| **Presentación anterior** de 27 diapositivas y su guía de estudio, con corte del 3-nov, antes de la rúbrica final | 3-nov | [guía](../Guias/Admind_Guia_Sustentacion_Tecnica.md) |
| **Material de estudio (F2):** guía por los 12 criterios, con el recorrido de una petición, la demo y la pregunta difícil de cada tema; y el artefacto «Repaso de AdMind» (47 tarjetas, quiz de 28 preguntas que explica cada respuesta, recorrido paso a paso y simulacro de 8 preguntas con 60 s cada una) | 19-nov | [guía](../Guias/Admind_Guia_Sustentacion_Final.md) y https://claude.ai/artifact/73Ndy5mB9VvXgxC9rLTvn4 (privado: Alejo lo comparte con Camilo desde *Share*) |
| **Presentación final** (16 diapositivas, criterios A a K y demostración, con notas del orador, tiempos y quién presenta cada una, como sugerencia). Capturas reales de la nube, de GitHub Actions y de la cobertura; datos de SonarCloud y de la base del 18-nov. JWT, CORS y Swagger salen como «No implementado» | 18-nov | `Entregables_Sustentacion/AdMind_Sustentacion_Final.pptx`. Se regenera con `_generador_presentacion/build_deck.js` (Node con `pptxgenjs` e `image-size`); las imágenes recortadas están en `_generador_presentacion/img/`. El borrador del 16-nov sigue al lado |

Cómo se generan los Word: [estilo_entregables](estilo_entregables.md) y los generadores `_generador_manual_tecnico` y `_generador_diccionario` en `Entregables_Sustentacion/`.

## Lo que falta antes de la sustentación

De [tareas](tareas.md), sin repetir el detalle:
- **Reparto:** quién presenta cada diapositiva, qué estudia cada uno y las preguntas probables están en [reparto_sustentacion](reparto_sustentacion.md) (22-nov).
- **F2, material de estudio:** hecho el 19-nov (ver *Lo que ya se entregó*). Falta que los dos estudien, el simulacro y compartir el artefacto con Camilo.
- **F3, presentación:** actualizada el 22-nov: CORS y Swagger como «Hecho» (8 y 9, con captura de Swagger desde la nube), 854 pruebas y 94,2 % (11), CI endurecido (13), segundo escaneo (14), despliegue del 22-nov (15) y presentador fijo en cada nota. Le faltan: la captura del correo en Gmail enviado desde la nube (diapositiva 10), las diferencias frente al MER inicial (notas de la 12) y, si Camilo corrige su vulnerabilidad, pasar el paso 2 de la 14 a «Hecho». Siguen pendientes el plan B y el ensayo cronometrado.
- **Sonar:** la vulnerabilidad de Camilo (criterio 11).
- **Evidencias desde la nube:** correo en Gmail, reportes descargados, `systemctl status` y la instancia en la consola de Oracle.
- **A5, la prueba de romper la app** sobre la versión desplegada, hecha por quien no programó.
- **Regenerar el diccionario** con las funciones y los triggers (`datos/scripts/`).
- **C12**, el bug de casos redirigidos y de «Page not found» tras responder, sin commit visible.
- **Ramas:** proteger `desarrollo` y `main`, y borrar `Desarrollo` (mayúscula) y las `revert-*`.
- **Del servidor, sin comprobar:** a qué interfaces escucha PostgreSQL y qué bloquea el firewall de Oracle; el token de `cloudflared` quedó visible en una salida del 17-nov y conviene rotarlo; `deploy_queue.py` termina bien aunque el despliegue falle, y el 17-nov falló por un `gunicorn` fijado a mano en los scripts (ya corregido). El `.env` del back tiene la línea `CORS_ALLOWED_ORIGINS` repetida tres veces (mismo valor, no afecta).
- **Notion:** las páginas de seguimiento ya no coinciden con la fecha nueva, y el tablero tiene dos HU-40 y una fila «Prueba».

## Dónde está cada cosa

| Qué | Dónde |
|---|---|
| Guía del profesor (clase del 3-nov) | `C:\Users\Alejandro\Downloads\indicaciones-clase-nov3-software.pdf` |
| Plan de Alejo (F0 a F3) y sus notas sobre lo que preguntará el profesor | `00 Obsidian Alpha\02 UNIVERSIDAD\026 SEXTO SEMESTRE\Ing Software II\SUSTENTACION TECNICA\Preparacion para Sustentacion Tecnica.md` |
| Tablero Scrum público | https://useful-vest-416.notion.site/Seguimiento-Scrum-2-0-AdMind-3f1739efa3338109b3f1e256d441de64 |
| Página «Sustentacion» de Notion (tareas por persona; la sección de Alejo se titula «Manuel») | En Notion, copia de [tareas](tareas.md); su enlace no está en la bóveda |
| Evidencias y capturas | `Entregables_Sustentacion/evidencias/` y `Entregables_Sustentacion/capturas/` (el QR es `qr_admind.png`) |
| Repositorios | `ZeroFour-04/Admind_Backend` y `ZeroFour-04/Admind_Front-End` en GitHub |
| La app desplegada | https://admind.detkor.com (sin `www`). Cuentas de demostración para el profesor: Residente y Vigilancia, que no piden segundo factor (las contraseñas no van en la bóveda) |

**Qué es el PGC:** Proyecto de Gestión del Conocimiento, que la universidad hace cada tres semestres. Este semestre pidió una sustentación de negocio del proyecto, que es la que ya se presentó. Junto con esta sustentación técnica hizo crecer el Sprint 7 y creó el Sprint 8 en el tablero; en los documentos se menciona de pasada, en una frase.

## Ver también

- [tareas](tareas.md) — la lista completa de tareas de Alejo y Camilo, con las decisiones y las evidencias
- [reparto_sustentacion](reparto_sustentacion.md) — quién presenta qué, qué estudia cada uno y las preguntas probables (22-nov)
- [tareas_por_persona](tareas_por_persona.md) — lo que le falta a cada uno, con el estado de GitHub del 16-nov
- [plan_entrega_final_documentos](plan_entrega_final_documentos.md) — los tres documentos de entrega final y sus datos
- [estilo_entregables](estilo_entregables.md) — el estilo común de los Word
- [estado_actual](../08_Estado/estado_actual.md) — cómo va el proyecto hoy
- [scrum_y_dod](../03_Reglas/scrum_y_dod.md) — la Definition of Done y las evidencias para el jurado
- [Guía de la sustentación final (19-nov)](../Guias/Admind_Guia_Sustentacion_Final.md) — la guía de estudio vigente
- [Guía de sustentación técnica (3-nov)](../Guias/Admind_Guia_Sustentacion_Tecnica.md) — la guía de estudio anterior

# Informe de avance de AdMind por sprints e historias (corte: 29/09/2026)

Para armarlo usé solo el código y los documentos locales, sin mirar Notion. Hoy hice `git fetch` en los dos repositorios, corrí las dos suites de pruebas y revisé el estado de las migraciones. Lo demás sale de `Admind_Avance.md`, del corte `Avance 22092026.md` y de `Admind_Guia_Estructura_Actual.md`.

## 1. Resumen

|Indicador|Valor|
|---|---|
|Plazo|Día 16 de unos 30 (del 14/09 al ~14/10; la fecha exacta sigue sin confirmar). Quedan unos 15 días|
|**Historias terminadas según la DoD**|**0 de 38 (0 de 188 SP)**|
|Historias con el código hecho, a falta de la DoD|**16 de 38, que suman 81 de 188 SP (43 %)**|
|Historias sin empezar|22, que suman 107 SP|
|Prioridad Alta|De 79 SP hay 71 construidos. Solo falta **HU-14** (8 SP)|
|Backend|`desarrollo` en `f053d31`, al día con GitHub. **320 pruebas, todas pasan.** No quedan migraciones pendientes|
|Frontend|`desarrollo` en `96a30b4`, al día con GitHub. **127 pruebas, todas pasan**|

Hay mucho código hecho y ninguna historia cerrada. Lo que falta no es programar. Ninguna historia ha pasado por un PR `desarrollo → pruebas` revisado, ni por la prueba manual de quien no la programó. Por eso la velocidad oficial sigue en 0 SP.

## 2. Avance por sprint

La columna "Sprint" es el reparto previsto en el Excel V11.1, que ya no se cumple con el plazo de un mes.

|Sprint|Historias|SP|Construido (sin DoD)|Sin empezar|
|---|---|---|---|---|
|**1**|HU-01 a HU-05, HU-26|25|6 de 6 (HU-03 parcial)|—|
|**2**|HU-06 a HU-09|20|4 de 4|—|
|**3**|HU-10 a HU-13|26|4 de 4|—|
|**4**|HU-14 a HU-19|28|0|6|
|**5**|HU-20, 21, 25, 27, 28, 29|28|2 (HU-21, HU-25, 10 SP)|4|
|**6**|HU-22 a 24, HU-30 a 34|38|0|8|
|**7**|HU-35, 36, 37|16|0|3|
|Condicional|HU-38|7|0|1|
|**Total**|**38**|**188**|**16 (81 SP)**|**22 (107 SP)**|

## 3. Detalle por historia

### Sprint 1: todo construido entre el 15/09 y el 21/09 (commits "sprint 1 terminado", `eab833e` y `c796773`)

|HU|SP|Estado|Qué le falta|
|---|---|---|---|
|HU-01 Login con correo y contraseña|3|5/5 tareas y 5/5 criterios. Incluye la recuperación de contraseña por enlace de un solo uso|La DoD. Además tiene dos huecos de seguridad: `/auth/recuperar/` no limita los intentos y `send_mail` es síncrono. El SMTP real no está configurado (hoy el correo sale por consola)|
|HU-02 Segundo factor (TOTP)|5|5/5 y 5/5. TOTP con QR y 10 códigos de respaldo|La DoD|
|HU-03 Asistente para crear un conjunto|6|Parcial. Desde el 27/09 los pasos de Áreas y Reglas son reales|**Está bloqueada**: el reglamento no tiene módulo (HU-33) y cuenta como no cumplido, así que **ningún conjunto puede quedar operativo**. Tampoco verifiqué si registra en la auditoría quién creó el conjunto|
|HU-04 Persona única por documento|3|5/5 y 5/5|La DoD|
|HU-05 Aislamiento entre conjuntos|2|5/5 y 5/5. Desde el 27/09 ya lo usan tablas reales (áreas, reservas y demás)|La DoD|
|HU-26 Selector de conjunto activo|6|5/5 y 5/5, conectado a la API|La DoD|

### Sprints 2 y 3: construidos el 27/09 con el plan F0–F10 (15 commits en el backend y 9 en el front)

Cada criterio de aceptación tiene una prueba automática con nombre propio.

|HU|SP|Estado|Observaciones|
|---|---|---|---|
|HU-06 Asignar y retirar roles|6|Todos los criterios con prueba|"Nunca cero Administración" responde 409 y hay una prueba con dos hilos a la vez|
|HU-07 Vincular persona por documento|3|Todos los criterios con prueba|Máximo 20 búsquedas por hora, contadas **por conjunto** (falta decidir si el límite debe ser global)|
|HU-08 Unidades y vínculos|7|Todos los criterios con prueba|Solo se vincula a quien ya tiene un rol en el conjunto|
|HU-09 Áreas comunes|4|Todos los criterios con prueba|Franjas por bloques fijos (D1 a)|
|HU-10 Reglas beta|9|Todos los criterios con prueba|7 tipos de regla que solo restringen, con versionado|
|HU-11 Bloqueo de 3 minutos|7|Todos los criterios con prueba, incluida la de concurrencia con 10 hilos|Falta probar a mano el `sendBeacon` que libera el bloqueo al cerrar la pestaña|
|HU-12 Confirmación antes de enviar|2|3 de 5 criterios con prueba automática|"Corregir sin perder lo escrito" y "el reloj no se detiene" necesitan prueba manual. La alta demanda depende de PB-24, que no existe|
|HU-13 Envío y motor de reglas|8|Todos los criterios con prueba|La mora siempre da `False` hasta que exista HU-35 (D5 b). Las alfas de piscina y de cobro quedan fuera|

### Adelantadas del Sprint 5

|HU|SP|Estado|
|---|---|---|
|HU-21 Identidad del conjunto|4|Construida el 22/09 (8 acentos y logo). **Hoy se amplió** con color propio en hex y foto cuadrada 1:1, commiteado y subido (`f053d31` y `96a30b4`). Esto **revierte** la decisión de "solo 8 acentos, sin hex libre", y el maestro §6.3 todavía no lo recoge|
|HU-25 Anuncios|6|Construida el 22/09, con lo mínimo del canal de notificaciones (bandeja y correo) y de HU-08|

### Sin empezar

- **Sprint 4:** HU-14 a HU-19.
- **Sprint 5:** HU-20, HU-27, HU-28 y HU-29.
- **Sprints 6 y 7:** todas.
- **Condicional:** HU-38.

**HU-14 (aprobar o rechazar, 8 SP)** es la que cierra el ciclo de la reserva: hoy una solicitud llega a `APARTADA` y ahí se queda.

## 4. Qué frena que se cuenten SP

1. **La rama `pruebas` del backend no existe en GitHub** (solo en local). Sin ella no se puede abrir el PR `desarrollo → pruebas`. En el front sí existe, pero está igual a `main`.
2. **Falta la revisión y la prueba manual de Camilo.** Casi todos los commits son tuyos, así que le toca a Camilo. El guion de prueba manual de HU-06 a HU-13 está en `Guias/Admind_Plan_Sprints_2_3.md` §6.
3. **Falta decidir el alcance** que entra antes de la entrega (maestro §12.8). Con unos 15 días, lo natural es HU-14. Queda por ver si se suma algo más del Sprint 4.
4. **HU-03 depende del reglamento (HU-33).** Hay dos caminos: construir un reglamento mínimo, o aceptar la historia con ese requisito pendiente. Esa decisión es tuya.

## 5. Lo que probablemente hay que corregir en Notion

Esto sale de lo que registran los documentos locales, no de Notion:

- **HU-06 a HU-13:** quedaron en "En revisión" el 27/09. Si Camilo las vuelve a marcar "Finalizado" sin PR ni prueba manual (ya pasó dos veces con HU-06), el estado no sería real.
- **HU-01, HU-02, HU-04, HU-05 y HU-26:** en Notion seguían "En progreso" y con fracciones viejas de tareas. Tienen todas sus tareas hechas.
- **HU-21 y HU-25:** probablemente siguen "Sin empezar" y están construidas.
    - Además, los criterios de HU-21 se reescribieron el 22/09 en términos de los 8 acentos ("slug"). El cambio de hoy vuelve al hex libre, así que otra vez no coinciden con el código.
- **Sprint 1:** no tiene fechas, y HU-01, HU-05 y HU-26 no tienen responsable. La DoD necesita saber quién programó cada historia para saber quién la prueba.

## 6. Otros pendientes

- **Seguridad:** la contraseña real de la base está en GitHub, en el `.env _ejemplo` del backend y en `Credenciales/` del repositorio de documentación. Borrar esos archivos no la saca del historial, así que hay que cambiar la contraseña.
- **Documentación desactualizada:**
    - `Admind_Avance.md` sigue con el estado viejo de las historias del Sprint 1.
    - La guía de estructura dice que HU-21 está "sin commit", y ya está commiteada.
    - En el repositorio de documentación quedan sin commit la guía nueva y `Notas/Desarrollo 22-09.md`.
- **Maestro:** le faltan decisiones ya tomadas al construir: el estado `LIBERADA`, un solo bloqueo por persona y conjunto, el catálogo de reglas beta, el token con registro en la base, el stack del front y el color propio de HU-21.

Si quieres, reviso Notion historia por historia contra esta lista y te digo qué cambiar antes de tocar nada.
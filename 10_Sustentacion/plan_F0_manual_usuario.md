---
titulo: "F0 · Manual de usuario en Word"
fecha: 2026-11-14
alcance: "Guía visual y de uso de AdMind por rol, con capturas de la app corriendo en local y la identidad verde de la marca"
punto_de_partida: "Frontend main bdcb5c3, Backend main b89d9f2; permisos por rol leídos de apps/permisos/catalogo.py el 2026-11-14"
resumen: "Plan para armar el manual de usuario por rol: datos de demostración, lista de capturas y contenido de cada capítulo."
estado: activo
ejecutado:
hu:
---

# Plan F0 · Manual de usuario

**Entregable:** `Entregables_Sustentacion\AdMind_Manual_Usuario.docx` (y su PDF).
**Tiempo estimado:** 4 a 5 horas: 1 de datos, 1,5 de capturas y 2 de redacción y armado. Es el entregable más largo: **empezarlo primero**.
**Antes de empezar:** leer [estilo_entregables](estilo_entregables.md).

## Reglas de este plan

- **Va dirigido al usuario final**, no a un programador: nada de rutas de código, endpoints ni nombres técnicos. Se habla de "pantallas", "botones" y "campos".
- **Los nombres de botones, campos, menús y mensajes se copian tal cual aparecen en la pantalla**: de la captura o de la plantilla (`Frontend/Admind_Front-End/apps/<app>/templates/<app>/*.html`). No se inventan ni se "mejoran".
- **Se describe solo lo que existe hoy.** Citas, la importación masiva, el respaldo y los reportes no se documentan; tampoco la anulación general de registros (HU-20), que no está construida.
- Solo datos inventados en las capturas (nombres como "Laura Gómez", correos `@example.com`). Ningún dato real.

## Paso 1. Preparar la app con datos de demostración (el agente, con Alejo para el segundo factor)

**Quién hace qué.** El agente maneja el panel del navegador de Claude Code (`mcp__Claude_Browser__*`) y entra con las **cuentas de prueba** de `crear_usuarios_prueba`. Las condiciones:
- Solo esas cuentas `@example.com`, en `http://127.0.0.1:8001`. Nunca una contraseña personal de Alejo ni de otro servicio.
- Alejo le da en el chat la contraseña de esas cuentas. El agente no la repite en sus mensajes ni la escribe en ningún archivo.
- En los tres roles con segundo factor, el código de 6 dígitos lo escribe Alejo en el panel, desde su celular. La sesión dura una hora, así que conviene hacer todo lo de cada rol de una vez.

1. Encender PostgreSQL y los dos servidores. En Claude Code: `preview_start` con `admind-backend` y `admind-front` (están en `A D M I N D/.claude/launch.json`). A mano: los comandos de la sección *Correr todo en el PC* de [pruebas_y_ejecucion](../02_Arquitectura/pruebas_y_ejecucion.md).
2. Si no existen las cuentas de prueba, correr `crear_usuarios_prueba` desde `Backend/Admind_Backend`. Crea un "Conjunto de prueba" y una cuenta por rol: `administracion@example.com`, `residente@example.com`, etc., todas con la contraseña que se le escriba.
3. **Segundo factor:** Superusuario, Administración y Secretaría lo exigen. Configurarlo en el celular de Alejo la primera vez que entre cada una, y **capturar la pantalla del QR justo en ese momento** (captura U03).
4. **Conjunto en verde:** en *Color y foto* del conjunto, dejar el acento **verde** y poner una foto. Así las capturas coinciden con los colores del manual.
5. Cargar lo mínimo para que ninguna pantalla salga vacía, entrando como **Administración**:
   - dos agrupaciones (Torre 1 y Torre 2) con viviendas;
   - el residente vinculado a una vivienda con "reside";
   - dos zonas: Salón social **con reserva** y Gimnasio **con ingreso** y aforo;
   - una regla alfa y una beta;
   - dos parqueaderos, uno asignado al residente;
   - un anuncio con foto y el reglamento en PDF.
6. Entrando como **Residente**: una reserva enviada, un caso abierto con foto y un pago de administración reportado.
7. Entrando como **Vigilancia**: un visitante con parqueadero y un ingreso al gimnasio.

## Paso 2. Tomar las capturas

Se guardan en `Entregables_Sustentacion\capturas\usuario\`, con el nombre de la columna *Archivo*.

**El límite:** el panel del navegador le muestra la captura al agente, pero **no la guarda como archivo**. Por eso hay dos formas de hacerlo; probar la A durante 10 minutos y, si no sale limpia, pasar a la B.

**A. Automática (el agente).** El script `10_Sustentacion/datos/scripts/captura_pantalla.ps1` (probado el 2026-11-14) guarda en PNG un rectángulo de la pantalla. No instala nada: usa `System.Drawing`, que trae Windows.
1. **Preparar la ventana:** `tabs_context` debe decir que el panel está **visible** (si está oculto, pedirle a Alejo que lo muestre). Pedirle que maximice la ventana de Claude y ensanche el panel lo más posible. La pantalla es de 2160 × 1440 px con escala de Windows, así que un panel angosto mostraría el diseño de celular.
2. **Fijar el tamaño:** `resize_window` con ancho 1280 y alto 800, para forzar el diseño de escritorio aunque el panel sea angosto.
3. **Calibrar:** capturar la pantalla entera una vez (`powershell -ExecutionPolicy Bypass -File <script> -Salida <ruta>\calibrar.png`). Abrir el PNG con Read, ubicar el rectángulo exacto de la página dentro del panel (sin la barra de pestañas) y anotar `X`, `Y`, `Ancho` y `Alto`.
4. **Capturar cada pantalla:** llevar la página al estado de la tabla y luego correr `-Salida <ruta>\U08_zonas.png -X .. -Y .. -Ancho .. -Alto ..`. Abrir el PNG con Read para comprobar que salió la pantalla correcta, completa y sin nada encima.
5. **Durante las capturas, Alejo no mueve ni tapa la ventana de Claude.** Si la mueve, se vuelve a calibrar.
6. Al terminar, `resize_window` con `preset: "desktop"`.
- Para U37 (celular): `resize_window` con `preset: "mobile"`, recargar la página y volver a calibrar.

**B. Manual (Alejo).** El agente deja cada pantalla en el estado de la tabla y le avisa ("lista U08"). Alejo la captura con `Win + Shift + S`, recortando solo la página, y la guarda con su nombre. Si las toma en su navegador normal: ventana maximizada, zoom al 100 % y sin barra de marcadores.
- Si una pantalla trae la etiqueta "Maqueta con datos de ejemplo" (Inicio y Registrar persona la traen hoy), se captura igual y se le avisa al agente. Es la tarea A4 de [tareas](tareas.md).

La app corre en `http://127.0.0.1:8001`.

| N | Rol | Pantalla | URL | Qué debe verse | Archivo |
|---|---|---|---|---|---|
| U01 | — | Ingreso | `/` | Formulario vacío con el logo | `U01_ingreso.png` |
| U02 | — | Recuperar contraseña | `/recuperar-contrasena/` | Formulario y, después de enviarlo, el mensaje de confirmación | `U02_recuperar.png` |
| U03 | Administración | Configurar segundo factor | `/segundo-factor/configurar/` | El QR (taparlo en la imagen después: es secreto) | `U03_2fa_configurar.png` |
| U04 | Administración | Verificar segundo factor | `/segundo-factor/verificar/` | Campo del código de 6 dígitos | `U04_2fa_verificar.png` |
| U05 | Superusuario | Selector de conjuntos | `/conjuntos/` | Tarjetas de los conjuntos con su color | `U05_selector.png` |
| U06 | Residente | Pantalla general | `/inicio/` | Barra superior, menú lateral y foto del conjunto | `U06_pantalla_general.png` |
| U07 | Residente | Mi perfil | `/perfil/` | Datos personales y tipo de usuario | `U07_perfil.png` |
| U08 | Residente | Zonas comunes | `/reservas/` | Tarjetas de zonas con calendario y franjas | `U08_zonas.png` |
| U09 | Residente | Solicitud en trámite | (al tomar una franja) | La cuenta regresiva de 3 minutos | `U09_solicitud_tramite.png` |
| U10 | Residente | Confirmación antes de enviar | (al pulsar enviar) | El panel con la fecha en letras | `U10_confirmacion.png` |
| U11 | Residente | Solicitud enviada | `/reservas/solicitudes/<id>/` | Estado "Apartada" y el bloque de pago con el comprobante | `U11_solicitud_enviada.png` |
| U12 | Residente | Abrir un caso | `/casos/nuevo/` | Formulario con foto | `U12_caso_nuevo.png` |
| U13 | Residente | Mis casos | `/casos/` | La lista con estados | `U13_mis_casos.png` |
| U14 | Residente | Anuncios | `/anuncios/` | Un anuncio con foto | `U14_anuncios.png` |
| U15 | Residente | Documentos | `/documentos/` | El reglamento para descargar | `U15_documentos.png` |
| U16 | Residente | Mis pagos | `/pagos/administracion/` | Reportar el pago del mes | `U16_mis_pagos.png` |
| U17 | Residente | Mi parqueadero | `/parqueaderos/mios/` | El puesto asignado | `U17_mi_parqueadero.png` |
| U18 | Residente | Notificaciones | `/notificaciones/` | La bandeja con avisos | `U18_notificaciones.png` |
| U19 | Vigilancia | Visitantes | `/visitantes/` | Formulario de ingreso y los de hoy, con "Registrar salida" | `U19_visitantes.png` |
| U20 | Vigilancia | Ingreso a zonas | `/ingresos/` | Personas adentro y el aforo | `U20_ingresos.png` |
| U21 | Vigilancia | Registrar ingreso | `/ingresos/registrar/` | Formulario | `U21_ingreso_registrar.png` |
| U22 | Secretaría | Solicitudes | `/solicitudes/` | Pestañas Reservas y Casos | `U22_solicitudes.png` |
| U23 | Secretaría | Detalle de un caso | `/casos/<id>/` | Acciones: tomar, prioridad, redirigir, descartar | `U23_caso_gestion.png` |
| U24 | Secretaría | Publicar anuncio | `/anuncios/nuevo/` | Formulario con alcance | `U24_anuncio_nuevo.png` |
| U25 | Administración | Decidir una reserva | `/reservas/areas/<id>/solicitudes/` | Aprobar o rechazar con categoría, y el bloque de pago | `U25_decidir_reserva.png` |
| U26 | Administración | Zonas comunes (gestión) | `/areas/` y `/areas/nueva/` | Lista con "Cómo se usa" y el formulario | `U26_areas.png` |
| U27 | Administración | Reglas | `/reglas/` | El tablero de reglas del conjunto y de cada zona | `U27_reglas.png` |
| U28 | Administración | Usuarios | `/usuarios/` | La lista agrupada por rol, con buscador | `U28_usuarios.png` |
| U29 | Administración | Detalle de usuario | `/usuarios/<id>/` | Cambiar rol y "Eliminar usuario" | `U29_usuario_detalle.png` |
| U30 | Administración | Viviendas | `/unidades/` y `/unidades/<id>/` | Agrupaciones; el detalle con "Agregar vínculo" | `U30_unidades.png` |
| U31 | Administración | Parqueaderos | `/parqueaderos/` | La tabla con asignar y liberar | `U31_parqueaderos.png` |
| U32 | Administración | Pagos de administración | `/pagos/administracion/` | La tabla del mes con el check de confirmar | `U32_pagos_admin.png` |
| U33 | Administración | Color y foto | `/conjuntos/identidad/` | Los acentos y la foto | `U33_identidad.png` |
| U34 | Administración | Infracciones | `/infracciones/` y `/infracciones/nueva/` | Lista y formulario | `U34_infracciones.png` |
| U35 | Superusuario | Asistente de creación | `/conjuntos/asistente/datos/` (y uno o dos pasos más) | Los pasos del asistente | `U35_asistente.png` |
| U36 | Superusuario | Resumen del conjunto | `/conjuntos/asistente/resumen/` | Requisitos, activar y "Eliminar conjunto" | `U36_resumen.png` |
| U37 | — | Celular | `/reservas/` en un ancho de 390 px (F12 → modo dispositivo) | El menú lateral desplegable | `U37_movil.png` |
| U38 | Residente | Un error claro | Ej.: tomar una franja ya tomada, o enviar un formulario incompleto | El mensaje en español | `U38_error.png` |

## Paso 3. Redactar y armar el Word (agente)

Cada tarea se escribe igual:
1. **Para qué sirve**, en una frase.
2. **Quién puede hacerlo.**
3. **Pasos numerados**, con los nombres exactos de la pantalla.
4. **La captura**, con un pie que la numere ("Figura 12. Solicitud en trámite").
5. **Qué pasa después**, y un recuadro "Tenga en cuenta" con las reglas que vea el usuario.

Para el comportamiento de cada pantalla, consultar la tabla *Las pantallas* de [frontend](../02_Arquitectura/frontend.md) y, si hace falta, la nota del módulo en `05_Modulos/`. Solo la sección necesaria.

### Capítulos

1. **Bienvenida:**
   - qué es AdMind (en lenguaje de residente y de administrador);
   - qué se necesita (un navegador actual e internet; funciona también en el celular);
   - cómo está organizado el manual;
   - **tabla de los 5 roles y qué hace cada uno** (abajo).
2. **Primeros pasos (todos los roles):**
   - ingresar (U01);
   - verificación en dos pasos: configurarla con una aplicación de autenticación como Google Authenticator, verificarla, guardar los códigos de respaldo y qué hacer si se pierde el celular ("¿Problemas con la verificación en dos pasos?") (U03, U04);
   - recuperar la contraseña (U02: el enlace llega al correo, sirve una vez y vence en 1 hora);
   - elegir conjunto (U05);
   - conocer la pantalla: barra superior, menú lateral, perfil y cambiar de conjunto (U06, U07);
   - cerrar sesión;
   - la sesión vence a la hora sin uso.
3. **Residente:**
   - reservar una zona común: elegir la franja, los 3 minutos para completar, confirmar y enviar; qué significa cada estado (U08 a U11);
   - subir el comprobante de pago de la reserva;
   - abrir un caso y seguirlo (U12, U13);
   - anuncios (U14);
   - documentos del conjunto (U15);
   - reportar el pago de la administración (U16);
   - mi parqueadero (U17);
   - notificaciones (U18).
4. **Vigilancia:**
   - registrar un visitante, con parqueadero si llega en vehículo, y registrar su salida (U19);
   - registrar el ingreso a una zona con aforo y la salida (U20, U21).
5. **Secretaría:**
   - el tablero de solicitudes (U22);
   - gestionar casos: tomar, prioridad, redirigir y descartar con causal (U23);
   - publicar anuncios (U24);
   - consultar pagos.
   - Aclarar que **Secretaría no aprueba reservas**.
6. **Administración:**
   - aprobar o rechazar reservas (con la categoría obligatoria; "Otro" pide texto) y declarar el pago (U25);
   - zonas comunes y sus dos modos de uso, con reserva o con ingreso (U26);
   - reglas (U27);
   - usuarios: registrar, asignar o cambiar el rol (una persona tiene un solo rol por conjunto) y eliminar del conjunto (U28, U29);
   - viviendas y vínculos (U30);
   - parqueaderos (U31);
   - confirmar pagos de administración (U32);
   - documentos;
   - color y foto del conjunto (U33);
   - infracciones (U34);
   - responder casos.
7. **Superusuario:**
   - crear un conjunto con el asistente de 7 pasos: datos, viviendas, administración, zonas, reglas, reglamento y resumen (U35);
   - activarlo (U36);
   - crear otros superusuarios;
   - anular una infracción registrada por error;
   - eliminar un conjunto.
8. **Mensajes y solución de problemas:** una tabla Mensaje o situación | Qué significa | Qué hacer (U38). Por ejemplo:
   - la franja ya está tomada;
   - se venció el tiempo de la solicitud;
   - no aparece una sección en el menú (depende del rol);
   - la sesión venció;
   - no llega el correo (revisar *spam*);
   - perdí el celular del segundo factor.

   Sacar los mensajes reales de las plantillas o de los servicios del backend (`apps/<app>/servicios.py`), no inventarlos.
9. **Glosario corto:** conjunto, zona común, franja, solicitud, caso, vínculo, rol, acento.

### Roles (verificados en `apps/permisos/catalogo.py` el 2026-11-14)

| Rol | Qué puede hacer en AdMind |
|---|---|
| **Residente** | Ver zonas y reservarlas, abrir casos, ver documentos, reportar su pago de administración, ver anuncios, su parqueadero y sus notificaciones |
| **Vigilancia** | Registrar visitantes e ingresos a zonas con aforo, y ver las reservas del día |
| **Secretaría** | Gestionar el tablero de solicitudes: prioridad, redirigir y descartar casos con causal. Publicar anuncios y consultar pagos y reservas. No aprueba reservas |
| **Administración** | Todo lo del conjunto: aprobar o rechazar reservas, zonas, reglas, usuarios y roles, viviendas, parqueaderos, pagos, documentos, identidad visual, infracciones y respuesta a casos |
| **Superusuario** | Opera la plataforma: crea y activa conjuntos, crea superusuarios, anula registros equivocados y puede entrar a cualquier conjunto |

## Al terminar

- Exportar a PDF y revisar:
  - que las 38 figuras estén numeradas y referidas en el texto;
  - que el QR de U03 esté tapado;
  - que no haya rutas de código ni términos técnicos;
  - que los nombres de botones coincidan con las capturas.
- Avisarle a Alejo de cualquier pantalla que se vio rota, vacía o con la etiqueta "Maqueta", para la lista de A4.

## Ver también

- [estilo_entregables](estilo_entregables.md) — colores, fuentes, portada y salida
- [frontend](../02_Arquitectura/frontend.md) — qué hace cada pantalla y quién la ve
- [permisos](../05_Modulos/permisos.md) — el catálogo de roles
- [tareas](tareas.md) — A4, las pantallas a prueba del profe

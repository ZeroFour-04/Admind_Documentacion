---
resumen: "El frontend por dentro: config sin base de datos, cliente_api, la sesión del front y el estado de cada pantalla."
tipo: arquitectura
origen: "guía de estructura §6 (2026-09-30)"
actualizado: 2026-10-11
revisado: 2026-10-11
---

# El frontend por dentro

## `config/`

- `DATABASES = {}`: no hay base de datos.
- Las sesiones se guardan **en archivos** (`SESSION_ENGINE = …file`), con cookie `HttpOnly` (el JavaScript del navegador no la puede leer).
- `ADMIND_API_URL` sale del `.env` (`http://127.0.0.1:8000` en local).
- `STATICFILES_DIRS` sirve `static/` y `design-system/`.

## `cliente_api/`: el mesero

Un archivo por app del backend (`reservas.py`, `areas.py`, `cuentas.py`…), con una función por endpoint. Todas usan `http.py` → `pedir(request, metodo, ruta, datos)`, que:

1. Saca el token de la sesión y lo pone en `Authorization: Token …`.
2. Llama a la API con `requests` (máximo 10 segundos).
3. Si la API no responde → `ApiNoDisponible` ("No hay conexión con el servidor de AdMind…").
4. Si responde con error → `ErrorDeApi`, que ya trae el mensaje en español para mostrar y los errores por campo (`error.campos`).

Así ninguna vista del front repite la lógica HTTP: solo hace `try: api_reservas.tomar(...) except ErrorDeApi as error: …`.

## `apps/cuentas/sesion.py`: la sesión del front

- `abrir_sesion()`: al entrar, guarda en la sesión el **token**, el **conjunto activo**, los **permisos**, los **roles** y el **tipo de usuario** y el estado del **segundo factor**, y hace que la sesión venza a la misma hora que el token.
- `tiene_permiso(request, "area.gestionar")`: lo usan las plantillas para **mostrar u ocultar** botones y secciones del lateral. Ojo: es solo para decidir qué se ve. **Quien decide de verdad es la API** en cada petición.
- `SesionRequeridaMiddleware`: toda pantalla exige sesión salvo las marcadas con `@publica` (ingreso, recuperar contraseña y el enlace del correo que quita el segundo factor). Con el segundo factor pendiente, solo deja abrir las pantallas para completarlo.

## Las pantallas

Cada app del front tiene `views.py` (funciones), `urls.py`, a veces `forms.py` (formularios de Django para validar antes de llamar a la API) y `templates/<app>/`.

| Sección del lateral | App del front | Estado |
|---|---|---|
| Ingreso, recuperar contraseña, segundo factor (con «¿Problemas con la verificación en dos pasos?»: pedir por correo el enlace que lo quita y confirmarlo), **Mi perfil** (ícono de la barra superior: datos personales y tipo de usuario) | `cuentas` | Real, contra la API |
| Selector de conjunto, asistente de creación, *Color y foto* (8 acentos o color propio, foto 1:1 con recortador) | `conjuntos` | Real. El asistente tiene siete pasos desde el 06/10: datos, viviendas, administración, áreas, reglas (el tablero de `reglas`), reglamento y resumen. **Aquí también está Alpine** (29/09), y desde el 06/10 en el paso de viviendas (`static/js/viviendas.js`): arma la descripción del conjunto, y lo que se crea lo calcula la API |
| Inicio | `paneles` | **Maqueta** con datos de ejemplo |
| Zonas comunes (la tabla de todas las zonas con su modo y sus cupos, el calendario y la solicitud) | `reservas` | Real. **Aquí está Alpine**, solo en la solicitud en trámite. Desde el 10/10 también el bloque «Pago» (`_pago.html`, sin JavaScript): en la tarjeta de las solicitudes del área, para Administración (declarar con comprobante opcional y retirar) y Secretaría (solo ver), y en el detalle del residente (ve si el pago está declarado y sube su comprobante). El archivo del comprobante lo pide el servidor del front a la API y lo entrega por `/reservas/comprobantes/<id>/` |
| Áreas comunes (con el modo de uso al crear y su columna «Cómo se usa») | `areas` | Real (solo con `area.gestionar`) |
| Reglas | `reglas` | Real |
| Anuncios | `anuncios` | Real |
| Notificaciones | `notificaciones` | Real |
| Solicitudes | `triage` | **Maqueta** vacía (HU-22, futuro) |
| Visitantes ("Visitante" para Vigilancia: formulario de ingreso y los de hoy; con `visitante.ver_historico`, el historial sin formulario) | `visitantes` | Real, parcial (HU-27): solo el ingreso, sin salida ni parqueadero |
| Conjunto | `conjuntos` | Real (resumen del asistente) |
| Usuarios (la lista en un desplegable por rol —Administración, Secretaría, Vigilancia, Residentes—, con buscador arriba y, en cada grupo, «Ordenar por» nombre, agrupación y vivienda o correo; detalle con **un** rol que se asigna o se cambia, "Eliminar usuario" con confirmación, registrar persona) | `usuarios` | Real. Desde el 11/10 la lista se agrupa, busca y ordena en el navegador (**aquí también está Alpine**, `static/js/directorio-usuarios.js`; la página le entrega las cuentas como JSON). Un grupo de más de 10 personas arranca recogido; al buscar se abren los que tienen resultados. Al registrar a alguien, el rol marcado es **Residente**. `usuarios/nuevo.html` aún muestra la etiqueta "Maqueta" |
| Unidades | `unidades` | Real (viviendas y vínculos; parqueaderos no). Desde el 10/10: un recuadro por agrupación (Torre, Etapa, Bloque…), la tabla de cada una y un buscador que filtra mientras se escribe. **Aquí también está Alpine** (`static/js/unidades.js`). Desde el 11/10, en el detalle de la vivienda, «Agregar vínculo» busca a la persona (nombre, correo o cédula) y trae el botón «Crear nuevo residente», que abre un modal: desde ahí solo se crean residentes (`static/js/vinculos.js`; la búsqueda por palabras, compartida con la lista de Usuarios, está en `static/js/busqueda.js`) |

**Quién ve Usuarios y Unidades.** El lateral los muestra solo si el rol de la sesión es Superusuario, Administración ("Administrador") o Secretaría; con otro rol, no aparecen. Es solo presentación: la API decide con el permiso de cada petición. "Eliminar usuario" no borra a la persona: cierra sus roles en el conjunto activo (`retirar_roles_del_conjunto`), y es la forma de desvincularla.

**Qué ve Vigilancia.** Desde el 01/10 el lateral le muestra solo Inicio, Zonas comunes, Reglas, Anuncios y Visitante; Áreas comunes, Notificaciones, Solicitudes, Conjunto y los enlaces de gestión se le ocultan por el rol, no por un permiso.

`templates/componentes/` guarda lo reutilizable: `barra_superior.html` (nombre y foto del conjunto activo o sus iniciales, el tipo de usuario y el ícono del perfil), `lateral.html` (marca solo el ítem activo leyendo la URL; desde el 06/10, bajo 900px es un panel que sale desde la izquierda: lo abre el botón de menú de la barra y lo maneja `static/js/lateral.js`, que carga `base/aplicacion.html`; en ese ancho la barra queda en una sola fila y el lateral muestra en su pie el tipo de usuario y «Cambiar de conjunto», y bajo 480px la marca en su cabeza), `_enlaces_gestion.html` (los dos enlaces de gestión), `campo.html`, `errores_formulario.html` y `confirmacion_de_contenido.html` (el panel de HU-12).

Cuando una app necesita piezas propias las guarda dentro de ella: `conjuntos/_foto.html` y `conjuntos/_selector_acento.html` (el guion bajo indica "pedazo para incluir, no página"), y las **etiquetas de plantilla** en `apps/conjuntos/templatetags/conjuntos.py` (`atributos_de_acento`, `iniciales`, `color_seguro`, `poco_legible`, `contraste_con_blanco`), que se cargan con `{% load conjuntos %}`.

## Ver también

- [reglas_frontend](../03_Reglas/reglas_frontend.md) — lo que el front nunca hace
- [implementacion](../04_Diseno/implementacion.md) — tokens, componentes `am-*`, acento y foto
- [reservas](../05_Modulos/reservas.md) — la pantalla que usa Alpine, paso a paso
- [mapa_codigo](mapa_codigo.md) — las carpetas del front y las apps de la API
- [cuentas](../05_Modulos/cuentas.md) — la sesión, del lado de la API
- [permisos](../05_Modulos/permisos.md) — de dónde salen los permisos que muestran u ocultan
- [pruebas_y_ejecucion](pruebas_y_ejecucion.md) — qué prueba cubre cada pantalla

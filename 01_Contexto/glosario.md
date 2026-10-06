---
resumen: "Términos del proyecto y del código en una frase cada uno."
tipo: contexto
origen: "guía de estructura §11 (2026-09-30) y guía de desarrollo §14 (2026-09-15)"
actualizado: 2026-10-06
---

# Glosario

| Término | Significa |
|---|---|
| **Conjunto** | Un conjunto residencial. Es la unidad de aislamiento: todo dato pertenece a uno |
| **Conjunto activo** | El conjunto con el que estás trabajando en esta sesión. Sale del token, nunca de la petición |
| **Tabla global** | Tabla sin `conjunto_id` (Persona, Usuario, Conjunto, tokens…). Están en una lista cerrada que una prueba vigila |
| **Persona / Usuario** | Persona = el ser humano, único por documento, puede estar en varios conjuntos. Usuario = su cuenta para entrar (correo + contraseña) |
| **Asignación** | El rol de una persona en un conjunto, con vigencia. Solo puede haber una vigente por persona y conjunto |
| **Unidad / Vínculo** | Unidad = una vivienda del conjunto, apartamento o casa (en pantalla, «vivienda»). Vínculo = relación de una persona con la unidad (propietario, reside…), con histórico |
| **Agrupación** | Lo que junta viviendas dentro de un conjunto: una torre, un bloque, una manzana. La palabra la pone cada conjunto y es opcional. Definida el 2026-10-06 (HU-39), todavía sin construir. No se llama *bloque*: esa palabra ya es de las franjas y del bloqueo |
| **Habitante** | Quien vive en una vivienda sin ser propietario ni arrendatario: la familia, un conviviente. Es un tercer tipo de vínculo, siempre con `reside`, y puede no tener cuenta. Decidido el 2026-10-06, sin construir. No es el rol *Residente*, que dice qué puede hacer una cuenta |
| **Franja** | Un bloque de horario de un área en una fecha: (área, fecha, hora de inicio, hora de fin) |
| **Bloqueo** | Los 3 minutos exclusivos para llenar y enviar una solicitud sobre una franja |
| **Regla alfa / beta** | **Alfa** = regla del conjunto (una `Regla` sin área); **beta** = regla de un área. Las dos las define Administración, una sola vez por tipo, y son versionadas. Las fijas en el código se llaman **reglas del sistema** (`apps/reglas/sistema.py`). Así está construido desde el 2026-10-06; antes alfa era «fija» y beta «configurable», y los planes y notas anteriores usan ese sentido ([motor_reglas](../05_Modulos/motor_reglas.md)) |
| **Zona / Área** | Un espacio común del catálogo del conjunto. En el código es `Area`; al definir las reglas se dice *zona*. Qué palabra va en pantalla está sin decidir |
| **Modo de uso** | Cómo se usa una zona: *con reserva* (se aparta una franja) o *con ingreso* (vigilancia registra a quien entra). Definido el 2026-10-06, sin construir |
| **Ingreso** | El registro de que un residente entró a una zona con ingreso, con sus acompañantes y su hora de salida ([ingresos](../05_Modulos/ingresos.md)). Sin construir |
| **Token** | La "llave" que el front manda a la API en cada petición. Vence en 1 hora |
| **Segundo factor (2FA, TOTP)** | El código de 6 dígitos de una app autenticadora, obligatorio con permisos sensibles |
| **Serializer** | Valida lo que entra a la API y da forma a lo que sale (el "DTO") |
| **Servicio** | Donde viven las reglas del negocio. No sabe de HTTP |
| **Manager** | El objeto `Modelo.objects` por el que se consulta. El de AdMind filtra por conjunto |
| **Migración** | Archivo que crea o cambia tablas. `makemigrations` lo genera, `migrate` lo aplica |
| **Índice único parcial** | "Único, pero solo entre las filas que cumplen X". Es lo que resuelve la concurrencia de reservas |
| **Acento / color propio** | El color con que se pinta la interfaz de un conjunto: uno de los 8 del catálogo o un hex que elige la Administración |
| **Foto del conjunto** | Imagen cuadrada (1:1) que lo identifica en la barra y el selector. En el código se sigue llamando "logo". Sin foto, se muestran sus iniciales |
| **Maqueta** | Pantalla con datos de ejemplo, todavía sin conectar a la API |
| **DoD** | *Definition of Done*: lo que debe cumplir una historia para contarse como Terminada (maestro §8.1) |
| **Endpoint** | Una dirección de la API que atiende un método HTTP: `POST /api/reservas/solicitudes/<id>/rechazar/` |
| **Controlador / vista** | La capa que recibe la petición HTTP y entrega la respuesta. En DRF, una clase `APIView` en `views.py` |
| **FK compuesta** | Llave foránea de dos columnas (`area_id`, `conjunto_id`) que hace imposible, en la base, apuntar a algo de otro conjunto |
| **Transacción** | Un grupo de cambios que se guardan todos o ninguno (`transaction.atomic`) |
| **`select_for_update`** | Bloquear filas dentro de una transacción para que nadie más las cambie hasta que termine |
| **Contrato** | El JSON acordado entre backend y frontend para un endpoint |
| **Operación inexistente** | Lo que la ley prohíbe no se programa como permiso denegado: no hay método, ni ruta, ni campo |

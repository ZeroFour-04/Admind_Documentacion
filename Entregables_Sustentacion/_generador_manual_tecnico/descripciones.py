# -*- coding: utf-8 -*-
"""Frases para las rutas de endpoints_api.md que no tienen descripción (su vista no tiene docstring).

Salen del nombre de la vista y de su código en `Backend/Admind_Backend/apps/<app>/views.py`.
Las rutas que ya traen descripción en el archivo conservan la suya.
"""

DESC = {
    # anuncios
    "AnunciosView": "GET lista los anuncios que la persona puede ver; POST publica uno nuevo, con hasta 4 fotos.",
    "DetalleDeAnuncioView": "GET muestra un anuncio; PATCH edita su título y su texto (el alcance y las fotos no "
                            "cambian).",
    # areas
    "AreasView": "GET lista las áreas comunes del conjunto; POST crea una.",
    "DetalleDeAreaView": "GET muestra un área común; PATCH edita sus datos.",
    "DesactivarAreaView": "Desactiva un área común sin borrarla.",
    # casos
    "CasosView": "GET lista los casos (los propios o, con permiso, todos); POST abre un caso, con una foto opcional.",
    "DetalleDeCasoView": "Muestra un caso. El de otra persona o de otro conjunto responde 404.",
    "FotoDeCasoView": "Entrega la imagen de una foto del caso.",
    "PriorizarCasoView": "Asigna la prioridad de un caso.",
    "RechazarCasoView": "Rechaza un caso; lo hace quien puede responder casos.",
    "RedirigirCasoView": "La Secretaría pasa el caso al administrador, con una nota interna opcional.",
    "ResponderCasoView": "Responde un caso; la respuesta es obligatoria.",
    "TomarCasoView": "Toma un caso para revisarlo.",
    # citas
    "AgendaDeCitasView": "GET consulta el horario, las franjas de un día y la cita propia; POST agenda una cita "
                         "dentro del horario de atención.",
    "CitasDeAdministracionView": "Lista las citas del conjunto para la Administración.",
    "HorarioDeAtencionView": "GET consulta el horario de atención del conjunto; PUT lo define.",
    # conjuntos
    "ActivarConjuntoView": "Deja el conjunto operativo si cumple los requisitos del asistente; si no, responde 400 "
                           "con lo que falta.",
    "IdentidadDelConjuntoView": "GET consulta y PATCH cambia el color de identidad del conjunto.",
    "LogoDelConjuntoView": "PUT sube y DELETE quita la foto cuadrada (1:1) del conjunto.",
    # cuentas
    "ConjuntosDisponiblesView": "Lista los conjuntos a los que puede entrar quien inició sesión.",
    "ActivarDosFactoresView": "Confirma el código y activa el segundo factor; devuelve los códigos de respaldo.",
    "ConfigurarDosFactoresView": "Inicia la configuración del segundo factor y devuelve los datos para el código QR.",
    "RestablecerDosFactoresView": "Quita el segundo factor con el enlace firmado enviado al correo. No exige token.",
    "VerificarDosFactoresView": "Verifica el código del segundo factor en la sesión actual.",
    "IniciarSesionView": "Inicia sesión con correo y contraseña y devuelve el token. No exige token.",
    "CerrarSesionView": "Cierra la sesión: el token deja de valer.",
    "SolicitarRecuperacionView": "Envía el enlace para restablecer la contraseña (máximo 3 por hora). Responde igual "
                                 "exista o no la cuenta. No exige token.",
    "RestablecerContrasenaView": "Cambia la contraseña con el enlace de un solo uso y cierra las sesiones abiertas. "
                                 "No exige token.",
    "UsuariosView": "GET lista los usuarios del conjunto; POST crea uno con su rol.",
    "DetalleDeUsuarioView": "Muestra un usuario del conjunto.",
    "RetirarUsuarioDelConjuntoView": "Retira al usuario del conjunto activo.",
    "RolesDeUsuarioView": "Asigna un rol del catálogo a un usuario del conjunto.",
    "RetirarRolView": "Retira un rol de un usuario.",
    "PerfilDeUsuarioView": "Muestra los datos de la persona que inició sesión.",
    # infracciones
    "InfraccionesView": "GET lista las infracciones; POST registra una nueva.",
    "DetalleDeInfraccionView": "Muestra una infracción.",
    "AnulacionView": "Anula un registro equivocado (solo el Superusuario); la fila queda marcada, no se borra.",
    "CierreView": "Cierra una infracción.",
    # ingresos
    "IngresosView": "GET lista quién está adentro de las zonas con ingreso; POST registra una entrada y controla el "
                    "aforo.",
    "SalidaView": "Registra la salida de una persona de una zona.",
    "BuscarResidenteView": "Busca residentes para registrar su ingreso.",
    "ZonasView": "Lista las zonas con ingreso.",
    # pagos
    "PagosDeAdministracionView": "La tabla del mes: una fila por vivienda, con buscador en el servidor.",
    "ConfirmacionView": "Pone o quita el check de pago confirmado de una vivienda y un mes; solo Administración.",
    "ComprobanteView": "Entrega el archivo del comprobante; quien no puede verlo recibe 404.",
    "MisPagosView": "Por cada vivienda de la persona, sus últimos 6 periodos con su estado.",
    "ReportesView": "El residente reporta el pago del mes de una vivienda suya subiendo el comprobante; no confirma "
                    "nada.",
    # parqueaderos
    "ParqueaderosView": "GET lista los puestos de parqueadero; POST crea uno.",
    "HistorialDeAsignacionesView": "Historial de asignaciones de un puesto.",
    "DesactivarParqueaderoView": "Desactiva un puesto sin borrarlo.",
    # personas
    "BuscarPersonaView": "Busca una persona por su documento.",
    "VincularPersonaView": "Le da un rol en el conjunto activo a una persona que ya existe, sin crear otra.",
    # reglas
    "ReglasView": "GET lista las reglas del conjunto; POST crea una.",
    "DetalleDeReglaView": "GET muestra una regla; PATCH la edita, lo que crea una versión nueva.",
    "RetirarReglaView": "Retira una regla vigente.",
    # reservas
    "SolicitudesDeAreaView": "Lista las solicitudes de un área.",
    "BandejaDeSolicitudesView": "La pestaña Reservas del dashboard de gestión: Administración y Secretaría.",
    "MarcarDisponibilidadView": "Marca el aviso (campana) para saber cuándo se libera una franja.",
    "ComprobanteDeSolicitudView": "Entrega el archivo del comprobante; quien no puede verlo recibe 404.",
    "FranjasView": "Lista las franjas de un área para un día.",
    "SolicitudesView": "GET lista las solicitudes propias; POST toma el bloqueo de la franja: 3 minutos exclusivos "
                       "para llenar y enviar.",
    "DetalleDeSolicitudView": "Muestra una solicitud.",
    "ComprobantesDeSolicitudView": "El residente sube un comprobante a una solicitud suya; subirlo no declara el pago.",
    "DecidirSolicitudView": "Administración aprueba o rechaza una solicitud.",
    "DescartarSolicitudView": "La Secretaría descarta una solicitud por causal formal; no aprueba.",
    "EnviarSolicitudView": "Envía la solicitud: se evalúa contra todas las reglas y queda apartada, o liberada con "
                           "todos los motivos.",
    "LiberarSolicitudView": "Suelta el bloqueo a propósito: la franja queda libre de inmediato.",
    "PagoDeSolicitudView": "Administración declara que recibió el pago, con un comprobante opcional.",
    "RetirarPagoDeSolicitudView": "Administración retira una declaración de pago hecha por error; el motivo es "
                                  "obligatorio.",
    # unidades
    "DetalleDeUnidadView": "Muestra una vivienda.",
    "VinculosDeUnidadView": "Agrega un vínculo de una persona con la vivienda.",
    "CerrarVinculoView": "Cierra un vínculo de la vivienda; queda en el histórico.",
    # visitantes
    "VisitantesView": "GET lista las visitas; POST registra el ingreso de un visitante.",
    "SalidaDeVisitanteView": "Registra la salida. Si la visita tenía parqueadero, queda libre al instante.",
}

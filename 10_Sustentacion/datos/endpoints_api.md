# Endpoints de la API de AdMind

Generado de las rutas reales del backend (`main` `b89d9f2`), 2026-11-14. Total: **97 rutas**.

Toda ruta exige `Authorization: Token <token>` salvo las de ingreso y recuperación de contraseña.


## anuncios

| Ruta | Métodos | Vista | Qué hace |
|---|---|---|---|
| `/anuncios/` | GET, POST | `AnunciosView` |  |
| `/anuncios/<uuid:anuncio_id>/` | GET, PATCH | `DetalleDeAnuncioView` |  |
| `/anuncios/<uuid:anuncio_id>/fotos/<uuid:foto_id>/` | GET | `FotoDeAnuncioView` | La imagen de una foto. Se entrega a quien puede ver el anuncio; a los demás, 404. |

## areas

| Ruta | Métodos | Vista | Qué hace |
|---|---|---|---|
| `/areas/` | GET, POST | `AreasView` |  |
| `/areas/<uuid:area_id>/` | GET, PATCH | `DetalleDeAreaView` |  |
| `/areas/<uuid:area_id>/desactivar/` | POST | `DesactivarAreaView` |  |

## casos

| Ruta | Métodos | Vista | Qué hace |
|---|---|---|---|
| `/casos/` | GET, POST | `CasosView` |  |
| `/casos/<uuid:caso_id>/` | GET | `DetalleDeCasoView` |  |
| `/casos/<uuid:caso_id>/descartar/` | POST | `DescartarCasoView` | La Secretaría cierra por causal formal. Responder de fondo no le corresponde. |
| `/casos/<uuid:caso_id>/fotos/<uuid:foto_id>/` | GET | `FotoDeCasoView` |  |
| `/casos/<uuid:caso_id>/prioridad/` | POST | `PriorizarCasoView` |  |
| `/casos/<uuid:caso_id>/rechazar/` | POST | `RechazarCasoView` |  |
| `/casos/<uuid:caso_id>/redirigir/` | POST | `RedirigirCasoView` |  |
| `/casos/<uuid:caso_id>/responder/` | POST | `ResponderCasoView` |  |
| `/casos/<uuid:caso_id>/tomar/` | POST | `TomarCasoView` |  |

## citas

| Ruta | Métodos | Vista | Qué hace |
|---|---|---|---|
| `/citas/agenda/` | GET, POST | `AgendaDeCitasView` |  |
| `/citas/bandeja/` | GET | `CitasDeAdministracionView` |  |
| `/citas/horario/` | GET, PUT | `HorarioDeAtencionView` |  |

## conjuntos

| Ruta | Métodos | Vista | Qué hace |
|---|---|---|---|
| `/conjuntos/` | POST | `CrearConjuntoView` | Paso 1: datos básicos. |
| `/conjuntos/actual/` | GET, PATCH, DELETE | `ConjuntoActualView` | Resumen del asistente (paso 3) y edición de los datos básicos del conjunto activo. |
| `/conjuntos/actual/activar/` | POST | `ActivarConjuntoView` |  |
| `/conjuntos/actual/identidad/` | GET, PATCH | `IdentidadDelConjuntoView` |  |
| `/conjuntos/actual/identidad/logo/` | PUT, DELETE | `LogoDelConjuntoView` |  |
| `/conjuntos/logos/(?P<huella>[0-9a-f]{64})/` | GET | `ImagenDelLogoView` | La imagen del logo, pedida por su huella. |

## cuentas

| Ruta | Métodos | Vista | Qué hace |
|---|---|---|---|
| `/auth/conjunto-activo/` | POST | `ConjuntoActivoView` | El único punto de la API que recibe un conjunto: es donde se elige (HU-26). |
| `/auth/conjuntos/` | GET | `ConjuntosDisponiblesView` |  |
| `/auth/dos-factores/activar/` | POST | `ActivarDosFactoresView` |  |
| `/auth/dos-factores/configurar/` | POST | `ConfigurarDosFactoresView` |  |
| `/auth/dos-factores/restablecer/` | POST | `SolicitarRestablecerDosFactoresView` | Para quien entró con su contraseña y no tiene la aplicación ni los códigos de respaldo. |
| `/auth/dos-factores/restablecer/confirmar/` | POST | `RestablecerDosFactoresView` |  |
| `/auth/dos-factores/verificar/` | POST | `VerificarDosFactoresView` |  |
| `/auth/login/` | POST | `IniciarSesionView` |  |
| `/auth/logout/` | POST | `CerrarSesionView` |  |
| `/auth/recuperar/` | POST | `SolicitarRecuperacionView` |  |
| `/auth/recuperar/confirmar/` | POST | `RestablecerContrasenaView` |  |
| `/auth/superusuarios/` | POST | `SuperusuariosView` | Alta de un Superusuario desde el selector (2026-10-30). |
| `/auth/usuarios/` | GET, POST | `UsuariosView` |  |
| `/auth/usuarios/<uuid:usuario_id>/` | GET | `DetalleDeUsuarioView` |  |
| `/auth/usuarios/<uuid:usuario_id>/eliminar/` | POST | `RetirarUsuarioDelConjuntoView` |  |
| `/auth/usuarios/<uuid:usuario_id>/roles/` | POST | `RolesDeUsuarioView` |  |
| `/auth/usuarios/<uuid:usuario_id>/roles/<uuid:asignacion_id>/cambiar/` | POST | `CambiarRolView` | Una persona tiene un solo rol por conjunto: para darle otro se cambia el que tiene. |
| `/auth/usuarios/<uuid:usuario_id>/roles/<uuid:asignacion_id>/retirar/` | POST | `RetirarRolView` |  |
| `/auth/usuarios/perfil/` | GET | `PerfilDeUsuarioView` |  |

## documentos

| Ruta | Métodos | Vista | Qué hace |
|---|---|---|---|
| `/documentos/` | GET | `DocumentosView` | El vigente de cada tipo, sin el contenido: lo que muestra la pantalla «Documentos». |
| `/documentos/<tipo_de_documento:tipo>/` | GET, PUT | `DocumentoView` | Los datos del documento vigente de un tipo, y subir una versión nueva. No recibe el conjunto: es el activo. |
| `/documentos/<tipo_de_documento:tipo>/archivo/` | GET | `ArchivoDelDocumentoView` | El PDF vigente de un tipo. Quien puede verlo puede bajarlo (D1 a); la descarga se audita. |
| `/documentos/<tipo_de_documento:tipo>/versiones/` | GET | `VersionesView` | Todas las versiones de un tipo, la vigente primero. Solo con `documento.descargar`. |
| `/documentos/<tipo_de_documento:tipo>/versiones/<uuid:version_id>/archivo/` | GET | `ArchivoDeVersionView` | El PDF de una versión, vigente o archivada. Solo con `documento.descargar`; se audita. |

## infracciones

| Ruta | Métodos | Vista | Qué hace |
|---|---|---|---|
| `/infracciones/` | GET, POST | `InfraccionesView` |  |
| `/infracciones/<uuid:registro_id>/` | GET | `DetalleDeInfraccionView` |  |
| `/infracciones/<uuid:registro_id>/anulacion/` | POST | `AnulacionView` |  |
| `/infracciones/<uuid:registro_id>/cierre/` | POST | `CierreView` |  |

## ingresos

| Ruta | Métodos | Vista | Qué hace |
|---|---|---|---|
| `/ingresos/` | GET, POST | `IngresosView` |  |
| `/ingresos/<uuid:ingreso_id>/salida/` | POST | `SalidaView` |  |
| `/ingresos/residentes/buscar/` | POST | `BuscarResidenteView` |  |
| `/ingresos/zonas/` | GET | `ZonasView` |  |

## notificaciones

| Ruta | Métodos | Vista | Qué hace |
|---|---|---|---|
| `/notificaciones/` | GET | `BandejaView` | Los avisos de quien pregunta, en el conjunto activo. Cada persona ve solo los suyos. |

## pagos

| Ruta | Métodos | Vista | Qué hace |
|---|---|---|---|
| `/pagos/administracion/` | GET | `PagosDeAdministracionView` |  |
| `/pagos/administracion/<uuid:unidad_id>/<str:periodo>/confirmacion/` | POST | `ConfirmacionView` |  |
| `/pagos/administracion/comprobantes/<uuid:comprobante_id>/` | GET | `ComprobanteView` |  |
| `/pagos/administracion/mios/` | GET | `MisPagosView` |  |
| `/pagos/administracion/reportes/` | POST | `ReportesView` |  |

## parqueaderos

| Ruta | Métodos | Vista | Qué hace |
|---|---|---|---|
| `/parqueaderos/` | GET, POST | `ParqueaderosView` |  |
| `/parqueaderos/<uuid:parqueadero_id>/asignacion/` | POST | `AsignacionView` | Asigna el puesto a una vivienda; si ya era de otra, la reasigna. La respuesta dice cuál fue. |
| `/parqueaderos/<uuid:parqueadero_id>/asignaciones/` | GET | `HistorialDeAsignacionesView` |  |
| `/parqueaderos/<uuid:parqueadero_id>/desactivar/` | POST | `DesactivarParqueaderoView` |  |
| `/parqueaderos/<uuid:parqueadero_id>/liberacion/` | POST | `LiberacionView` | Cierra la asignación vigente sin darla a otra vivienda. Nunca por mora: la ruta no pregunta por ella. |
| `/parqueaderos/mios/` | GET | `MisParqueaderosView` | Los puestos de las viviendas de quien pregunta. Sin permiso: cada persona ve solo los suyos. |

## personas

| Ruta | Métodos | Vista | Qué hace |
|---|---|---|---|
| `/personas/buscar/` | POST | `BuscarPersonaView` |  |
| `/personas/vincular/` | POST | `VincularPersonaView` |  |

## reglas

| Ruta | Métodos | Vista | Qué hace |
|---|---|---|---|
| `/reglas/` | GET, POST | `ReglasView` |  |
| `/reglas/<uuid:regla_id>/` | GET, PATCH | `DetalleDeReglaView` |  |
| `/reglas/<uuid:regla_id>/retirar/` | POST | `RetirarReglaView` |  |
| `/reglas/catalogo/` | GET | `CatalogoDeReglasView` | Los tipos que se pueden definir hoy, con su nivel, su nombre y su descripción fija (P11). |

## reservas

| Ruta | Métodos | Vista | Qué hace |
|---|---|---|---|
| `/reservas/areas/<uuid:area_id>/solicitudes/` | GET | `SolicitudesDeAreaView` |  |
| `/reservas/bandeja/` | GET | `BandejaDeSolicitudesView` |  |
| `/reservas/campanas/` | POST | `MarcarDisponibilidadView` |  |
| `/reservas/comprobantes/<uuid:comprobante_id>/` | GET | `ComprobanteDeSolicitudView` |  |
| `/reservas/franjas/` | GET | `FranjasView` |  |
| `/reservas/solicitudes/` | GET, POST | `SolicitudesView` |  |
| `/reservas/solicitudes/<uuid:solicitud_id>/` | GET | `DetalleDeSolicitudView` |  |
| `/reservas/solicitudes/<uuid:solicitud_id>/comprobantes/` | POST | `ComprobantesDeSolicitudView` |  |
| `/reservas/solicitudes/<uuid:solicitud_id>/decision/` | POST | `DecidirSolicitudView` |  |
| `/reservas/solicitudes/<uuid:solicitud_id>/descarte/` | POST | `DescartarSolicitudView` |  |
| `/reservas/solicitudes/<uuid:solicitud_id>/enviar/` | POST | `EnviarSolicitudView` |  |
| `/reservas/solicitudes/<uuid:solicitud_id>/liberar/` | POST | `LiberarSolicitudView` |  |
| `/reservas/solicitudes/<uuid:solicitud_id>/pago/` | POST | `PagoDeSolicitudView` |  |
| `/reservas/solicitudes/<uuid:solicitud_id>/pago/retirar/` | POST | `RetirarPagoDeSolicitudView` |  |

## unidades

| Ruta | Métodos | Vista | Qué hace |
|---|---|---|---|
| `/unidades/` | GET, POST | `UnidadesView` | Las unidades del conjunto activo. También las usa el anuncio dirigido a una vivienda (HU-25). |
| `/unidades/<uuid:unidad_id>/` | GET | `DetalleDeUnidadView` |  |
| `/unidades/<uuid:unidad_id>/vinculos/` | POST | `VinculosDeUnidadView` |  |
| `/unidades/<uuid:unidad_id>/vinculos/<uuid:vinculo_id>/cerrar/` | POST | `CerrarVinculoView` |  |
| `/unidades/agrupaciones/` | GET | `AgrupacionesView` | Las agrupaciones del conjunto activo y cuántas viviendas tiene cada una (HU-39). |
| `/unidades/estructura/` | POST | `GenerarEstructuraView` | Crea las viviendas de esa descripción. Las que ya existen se omiten (HU-39). |
| `/unidades/estructura/previsualizar/` | POST | `PrevisualizarEstructuraView` | Lo que se crearía con esa descripción. No guarda nada (HU-39). |

## visitantes

| Ruta | Métodos | Vista | Qué hace |
|---|---|---|---|
| `/visitantes/` | GET, POST | `VisitantesView` |  |
| `/visitantes/<uuid:visitante_id>/salida/` | POST | `SalidaDeVisitanteView` |  |

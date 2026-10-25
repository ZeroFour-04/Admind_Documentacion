---
resumen: "Construye HU-30 completa: el registro de una infracción que se comunica a propietario y arrendatario, se cierra con fecha y comentario y solo el Superusuario anula; sin ningún campo de sanción."
titulo: "AdMind — Plan guiado del registro de infracciones"
tipo: plan
modo: guiado
estado: activo
hu: [HU-30]
fecha: 2026-10-24
para: "Alejo, con un agente que guía según 09_Protocolos/ejecutar_plan_guiado.md si Alejo lo aprueba; si no, el agente lo construye"
alcance: "HU-30: modelo, API, pantallas de Administración y el botón desde el detalle de un caso"
punto_de_partida: "Backend 7eb5b5a (708 pruebas según estado_actual), Frontend 8279616 (417 pruebas), sin cambios pendientes; makemigrations --check pide personas/0003"
---

# AdMind — Plan guiado del registro de infracciones

> [!IMPORTANT]
> **Alejo:** D1 ya tiene respuesta (chat del 2026-10-24); llena D2 a D5. Para empezar o retomar, en un chat nuevo: `Ejecuta el plan Documentacion/Admind_Documentacion/07_Planes/activos/Plan_Infracciones.md`. El agente te pregunta primero si lo quieres guiado o si lo construye él.

## 1. Seguimiento

**Dónde voy:** 2026-10-25 · construido por el agente (Alejo eligió «lo construyes tú», con D2 a, D3 a y D5 a) en `feat/infracciones-registro`, salida de `origin/desarrollo` en el backend y en el frontend, sin commit. Faltan el commit, el PR, `migrate` y el guion de prueba manual.

| Fase | Deja funcionando | Estado | Modo | Explicada de vuelta | Verificación | Commit | Fecha |
|---|---|---|---|---|---|---|---|
| F0 | Punto de partida confirmado | hecha | — | — | `git fetch` falló por falta de red; se tomó `origin/desarrollo` tal cual estaba. Línea base de esta rama no medida aparte: backend 707 de 708 y frontend 417 medidos en `desarrollo` ese día; `makemigrations --check` pide solo `personas/0003` | — | 2026-10-25 |
| F1 | Modelo y migración con sus `CHECK` | hecha | construida | — | `infracciones/0001` con FK compuestas; `makemigrations --check` solo pide `personas/0003` | sin commit | 2026-10-25 |
| F2 | Servicio: registrar y comunicar, cerrar, anular | hecha | construida | — | `pytest apps/infracciones` en verde, con la prueba de que si la comunicación falla no queda registro | sin commit | 2026-10-25 |
| F3 | API, permisos y prueba del intruso | hecha | construida | — | Backend 740 pruebas, todas pasan | sin commit | 2026-10-25 |
| F4 | Pantallas de Administración y botón desde el caso | hecha | construida | — | Frontend 440 pruebas, todas pasan (23 nuevas); sin recorrer en el navegador porque falta `migrate` | sin commit | 2026-10-25 |

### Desviaciones

- 2026-10-25 · `makemigrations` generó de paso `personas/0003` (la pendiente de Camilo); se borró y `infracciones/0001` depende de `personas/0002`.
- 2026-10-25 · El aviso de cierre usa otro origen (`infraccion.cierre`) que el del registro: el canal no repite un aviso con el mismo `origen` y `referencia`, y con el mismo no habría llegado.
- 2026-10-25 · `cierre_fecha` es `DateTimeField` (con hora), no solo fecha, igual que `fecha_notificacion`.
- 2026-10-25 · El catálogo ya traía el permiso de plataforma `registro.anular` (anulación general, HU-20). Se siguió D3 a y se creó `infraccion.anular`; si se construye HU-20, habrá que decidir si las dos se unen.
- 2026-10-25 · El aviso de R11 en las pantallas es un recuadro (`am-alerta` dentro de una tarjeta) porque el sistema de diseño solo trae la variante de error.

### Conceptos por repasar

Las cinco fases se construyeron enteras (no guiadas): conviene repasar por qué registrar y comunicar van en una sola transacción, qué hace cumplir la base (`NOT NULL` de `fecha_notificacion` y los `CHECK`) frente a lo que hace el servicio, por qué no hay campo `estado` y por qué la anulación es un permiso del catálogo y no un `if` en la vista.

## 2. Instrucciones para el agente

> [!IMPORTANT]
> **Primero pregunta.** Antes de tocar nada, pregúntale a Alejo si este plan se trabaja **guiado** o si lo **construyes** tú.

### 2.1 Qué leer antes de empezar

1. [ejecutar_plan_guiado](../../09_Protocolos/ejecutar_plan_guiado.md).
2. Este plan completo.
3. [infracciones](../../05_Modulos/infracciones.md): el modelo del maestro §5.8 y por qué el sistema no sanciona.
4. [legal](../../01_Contexto/legal.md) §4.2 y [riesgos](../../06_Decisiones/riesgos.md) R11: el aviso de que el registro no prueba el debido proceso.
5. [invariantes](../../03_Reglas/invariantes.md), [capas](../../03_Reglas/capas.md), [aislamiento](../../03_Reglas/aislamiento.md) y [eliminacion](../../03_Reglas/eliminacion.md): tabla nueva con `conjunto_id`, sin borrado, anulación.
6. [unidades](../../05_Modulos/unidades.md): `destinatarios(unidad, Hecho.INFRACCION)`.
7. `Backend/Admind_Backend/apps/README.md`, `apps/casos/README.md` y `Frontend/Admind_Front-End/apps/README.md`.

### 2.2 Reglas propias de este plan

- **No existe ningún campo, ruta ni texto de sanción, multa o restricción de uso.** Ni comentado, ni como `choices` vacío.
- No se toca el motor de reglas: la regla de sanción vigente no vuelve.
- El registro **nunca** llega al tablón de anuncios: el aviso va por `notificar`, no por `anuncios`.
- `migrate` lo corre Alejo.

## 3. Decisiones que toma Alejo

| ID | Decisión | Opciones | Recomendada | Respuesta |
|---|---|---|---|---|
| D1 | Infracción que nace de un caso | a) `caso` opcional, y desde el detalle del caso Administración la abre b) Siempre de oficio | a | **a** (2026-10-24) |
| D2 | Cómo se llena `fecha_notificacion` | a) El sistema comunica al guardar y sella la fecha en la misma transacción: no se puede registrar sin comunicar b) Además, Administración puede declarar una comunicación física con su fecha | a | |
| D3 | Quién anula. HU-20 (anulación general) no existe | a) Permiso nuevo `infraccion.anular` solo en `PERMISOS` (lo tiene únicamente el Superusuario) y sensible b) Preguntar `es_superusuario` en la vista | a | |
| D4 | Qué ve el residente | a) Solo el aviso en su bandeja y su correo (lo que pidió Alejo el 24/10) b) Además una lista de las infracciones de su vivienda | a | **a** (2026-10-24: no se marcó la lista) |
| D5 | Al cerrar o anular, ¿se avisa otra vez a la vivienda? | a) Sí al cerrar (es parte de la comunicación), no al anular b) No en ninguno c) En los dos | a | |

## 4. Decisiones menores que el plan ya fija

| ID | Decisión |
|---|---|
| P1 | App `apps/infracciones/` en los dos repositorios, con la anatomía de [backend](../../02_Arquitectura/backend.md): `models`, `serializers`, `servicios`, `views`, `urls`, `tests` |
| P2 | Modelo `RegistroDeInfraccion(ModeloDeConjunto)`: `unidad` (FK `PROTECT`), `caso` (FK nula `PROTECT`), `descripcion_hecho` (texto, obligatorio), `fecha_hecho` (fecha, no futura), `registrado_por`, `registrado_en`, `fecha_notificacion` (`DateTimeField`, **no nulo**), `cierre_fecha` y `cierre_comentario` (nulos), `cerrado_por`, `anulado` (bool), `anulacion_motivo`, `anulado_por`, `anulado_en`. **Sin campo `estado`**: abierto si `cierre_fecha` es nulo |
| P3 | `CHECK`: `cierre_fecha` y `cierre_comentario` van juntos; `anulado` exige motivo; `descripcion_hecho <> ''`. Las FK compuestas con `conjunto_id`, como el resto ([aislamiento](../../03_Reglas/aislamiento.md)) |
| P4 | La comunicación es `notificar(Aviso("Registro de infracción", …, origen="infraccion", referencia=registro.id), destinatarios(unidad, Hecho.INFRACCION))` dentro de la transacción. El cuerpo lleva la fecha del hecho, la descripción y la frase de R11: «Este registro deja constancia de la comunicación. No es una sanción ni reemplaza el procedimiento del art. 59 de la Ley 675». No dice quién lo registró |
| P5 | Una unidad sin vínculos vigentes no se puede registrar: 400 «La vivienda no tiene a quién comunicarle». Sin comunicación no hay registro |
| P6 | Cerrar no modifica `descripcion_hecho`, `fecha_hecho` ni `fecha_notificacion`: el serializer de cierre solo acepta `comentario`; la fecha la pone el sistema. Cerrar dos veces → 409 |
| P7 | La unidad se elige siempre a mano, también cuando nace de un caso (el caso no guarda vivienda); el formulario la sugiere con las viviendas del autor del caso |
| P8 | Auditoría: `infraccion.registrar`, `infraccion.cerrar`, `infraccion.anular`, con antes y después |
| P9 | Rutas: `GET`/`POST /infracciones/`, `GET /infracciones/<id>/`, `POST /infracciones/<id>/cierre/`, `POST /infracciones/<id>/anulacion/`. Ningún `PUT`, `PATCH` ni `DELETE` (405) |
| P10 | Un registro anulado sigue en la lista, tachado, con su motivo ([eliminacion](../../03_Reglas/eliminacion.md)) |

## 5. Punto de partida verificado

Comprobado el 2026-10-24 en `origin/desarrollo` (Backend `7eb5b5a`, Frontend `8279616`).

- `apps/infracciones/` tiene solo `README.md` en los dos repositorios.
- Permisos en `apps/permisos/catalogo.py`: `infraccion.registrar`, `infraccion.ver`, `infraccion.cerrar` en `PERMISOS`, en `PERMISOS_SENSIBLES` (exigen 2FA) y en Administración. La Secretaría no los tiene. No existe `infraccion.anular`.
- `apps/unidades/servicios.py`: `Hecho.INFRACCION` con `VINCULOS_POR_HECHO[Hecho.INFRACCION] = Q()` (propietario y arrendatario, residan o no; C-318/02) y `destinatarios(unidad, hecho)`. Prueba existente: `apps/unidades/tests.py:71`.
- `apps/notificaciones/canal.py`: `Aviso(titulo, cuerpo, origen, referencia)` y `notificar(aviso, persona_ids)`, que manda el correo al confirmar la transacción.
- `apps/auditoria/servicios.py`: `registrar(actor, accion, entidad, entidad_id, *, antes, despues, detalle, via_superusuario)`.
- `apps/casos/models.py`: `Caso` (sin vivienda). Front: `apps/casos/templates/casos/detalle.html`, donde va el botón.
- El tipo de vínculo `habitante` (decidido el 06/10) **no existe**: si se construye después, hay que decidir si recibe infracciones (`Q()` lo incluiría).

## 6. Mapa de la funcionalidad

```
Administración (2FA) → /infracciones/nueva/[?caso=<id>]
  └─ cliente_api.infracciones.registrar → POST /infracciones/
       └─ RegistrarInfraccionSerializer → servicios.registrar(actor, unidad_id, descripcion, fecha_hecho, caso_id)
            ├─ transaction.atomic: destinatarios(unidad, Hecho.INFRACCION) vacío → 400
            ├─ INSERT RegistroDeInfraccion con fecha_notificacion = ahora (NOT NULL)
            ├─ notificar(...)  → bandeja + correo de propietario y arrendatario
            └─ auditoria.registrar("infraccion.registrar")
  /infracciones/<id>/ → «Cerrar» (comentario) · Superusuario: «Anular» (motivo)
```

## F0 · Confirmar el punto de partida

- [ ] **B0.1** · Las dos suites y `makemigrations --check --dry-run` (solo `personas/0003`, que no es de este plan).

## F1 · Modelo y migración

**Deja funcionando:** la tabla con sus restricciones; escribir directo sin `fecha_notificacion` falla.

**Concepto de la fase:** cuando la regla es de la base (`NOT NULL`, `CHECK`), ningún código puede saltársela.

- [ ] **B1.1** · explicado · `Backend/Admind_Backend/apps/infracciones/models.py`, `apps.py`, `config/settings.py` (`INSTALLED_APPS`)
  - **Qué:** el modelo de P2 con las restricciones de P3. Docstring que dice por qué no hay `estado` ni sanción.
  - **Forma:** como `apps/casos/models.py` (`Meta(ModeloDeConjunto.Meta)` y `*ModeloDeConjunto.Meta.constraints`).
  - **Comprobación:** `makemigrations infracciones` genera `0001`; la FK compuesta se agrega como en las otras apps (`apps/comun/aislamiento/migraciones.py` `fk_compuesta`).
- [ ] **B1.2** · tuyo · `apps/infracciones/tests.py`
  - **Qué:** `test_hu30_registro_sin_fecha_de_notificacion_falla` (escribe con el ORM sin la fecha → `IntegrityError`) y `test_hu30_no_existe_campo_de_sancion_multa_ni_restriccion` (recorre `_meta.get_fields()` buscando `sancion`, `multa`, `restriccion`, `estado`).

**Cierre de F1**

- **Verificación:** `pytest apps/infracciones`; Alejo corre `migrate`.
- **Explicar de vuelta:** «¿por qué no hay campo `estado`?».
- **Pregunta de jurado:** «¿Por qué el sistema no registra la multa?» (competencia: requerir es del administrador, decidir de la asamblea o el consejo, ejecutar ocurre fuera).
- **Commit sugerido:** `feat(infracciones): modelo del registro de infracción [HU-30]`

## F2 · Servicio

**Deja funcionando:** `registrar`, `cerrar` y `anular`, con sus pruebas de servicio.

**Concepto de la fase:** comunicar y registrar en la misma transacción: o pasan las dos o ninguna.

- [ ] **B2.1** · explicado · `apps/infracciones/servicios.py`
  - **Qué:** `registrar(actor, unidad_id, descripcion_hecho, fecha_hecho, caso_id=None)` según el mapa, con P4 y P5. Excepciones propias (`SinDestinatarios`, `InfraccionNoEncontrada`, `YaCerrada`, `YaAnulada`) como en `apps/casos/servicios.py`.
  - **Comprobación:** `test_hu30_propietario_y_arrendatario_reciben_la_comunicacion` (una unidad con los dos, residente o no; las dos `Notificacion` existen).
- [ ] **B2.2** · tuyo (modelo: B2.1 y `casos.servicios._pasar`) · mismo archivo
  - **Qué:** `cerrar(actor, registro_id, comentario)` con `select_for_update` y P6; `anular(actor, registro_id, motivo)` con P10. Con D5 a, `cerrar` avisa a los mismos destinatarios.
  - **Comprobación:** `test_hu30_cerrar_no_modifica_la_comunicacion_original` (compara `fecha_notificacion` y `descripcion_hecho` antes y después).

**Cierre de F2**

- **Verificación:** `pytest apps/infracciones apps/unidades`.
- **Explicar de vuelta:** «¿qué pasa si el correo falla después de guardar?» (el aviso queda en la bandeja; el correo sale en `on_commit`).
- **Commit sugerido:** `feat(infracciones): registrar, comunicar, cerrar y anular [HU-30]`

## F3 · API y permisos

**Deja funcionando:** las rutas de P9 con sus permisos; la prueba del intruso las cubre.

- [ ] **B3.1** · explicado · `apps/infracciones/serializers.py`, `views.py`, `urls.py`, `config/urls.py`
  - **Qué:** vistas `VistaDeConjunto` con `exigir_permiso(request, "infraccion.registrar")`, `"infraccion.ver"`, `"infraccion.cerrar"`; la anulación según D3. La lista ordena abiertos primero y luego por `registrado_en` descendente.
  - **Comprobación:** `test_hu30_el_administrador_no_puede_borrar_y_solo_el_superusuario_anula` (`DELETE` → 405; anular como Administración → 403; como Superusuario con motivo → 200 y la fila sigue).
- [ ] **B3.2** · tuyo · `apps/permisos/catalogo.py` (solo con D3 a) y `tests/` de aislamiento
  - **Qué:** `infraccion.anular` en `PERMISOS` y `PERMISOS_SENSIBLES`, en ningún rol; las cuatro rutas en la prueba del intruso; una prueba de que la Secretaría y el Residente reciben 403.

**Cierre de F3**

- **Verificación:** `pytest -q` completo, prueba del intruso en verde.
- **Pregunta de jurado:** «¿Quién puede ver una infracción?» (Administración con 2FA y, por el aviso, los vínculos vigentes de la unidad; nunca el tablón).
- **Commit sugerido:** `feat(infracciones): API con permisos y anulación del Superusuario [HU-30]`

## F4 · Pantallas

**Deja funcionando:** lista, formulario y detalle para Administración; botón «Registrar infracción» en el detalle de un caso.

- [ ] **B4.1** · explicado · `Frontend/Admind_Front-End/cliente_api/infracciones.py`, `apps/infracciones/` (`views.py`, `urls.py`, `forms.py`, `templates/infracciones/lista.html`, `nueva.html`, `detalle.html`), `config/urls.py` y el menú lateral
  - **Qué:** las tres pantallas con componentes `am-*` ([implementacion](../../04_Diseno/implementacion.md)). En el formulario y en el detalle, el aviso de R11 en un callout fijo. El anulado se ve tachado con su motivo.
- [ ] **B4.2** · tuyo · `apps/casos/templates/casos/detalle.html`
  - **Qué:** con `infraccion.registrar`, un enlace a `/infracciones/nueva/?caso=<id>`; el formulario sugiere las viviendas del autor (P7).
- [ ] **B4.3** · tuyo · `tests/test_infracciones.py`
  - **Qué:** que el formulario no tenga ningún campo de sanción, multa ni restricción, y que el aviso de R11 esté en las dos pantallas.

**Cierre de F4**

- **Verificación:** las dos suites; recorrido del guion.
- **Commit sugerido:** `feat(infracciones): pantallas de registro, cierre y anulación [HU-30]`

## Cierre del plan

Las dos suites y `makemigrations --check --dry-run`. Informe final y [actualizar_contexto](../../09_Protocolos/actualizar_contexto.md): [infracciones](../../05_Modulos/infracciones.md) (sección *Cómo está construido*), [historias](../../08_Estado/historias.md) (HU-30, y el quinto criterio de HU-29), [permisos](../../05_Modulos/permisos.md) si D3 a, y la tabla *Estado real* en Notion.

## Lo que el agente no puede hacer

`migrate`, el PR `desarrollo → pruebas` revisado y la prueba manual de Camilo.

## Guion de prueba manual

1. Como Administración con 2FA: abrir un caso de un residente y pulsar «Registrar infracción». La vivienda viene sugerida; escribir el hecho y su fecha.
2. Entrar como el propietario y como el arrendatario de esa vivienda: los dos tienen el aviso, con la frase de R11 y sin el nombre de quien registró.
3. Cerrar el registro con un comentario: la descripción y la fecha de notificación siguen iguales.
4. Intentar borrarlo: no hay botón. Como Superusuario, anularlo con motivo: sigue en la lista, tachado.
5. Como Secretaría: `/infracciones/` no está en el menú y la API responde 403.

## Fuera de este plan

- La anulación general de registros (HU-20).
- La lista de infracciones para el residente (D4 a).
- Qué pasa con el vínculo `habitante` cuando se construya.

---
resumen: "Construye HU-34: asignar un parqueadero de residentes a una vivienda y reasignarlo cerrando la asignación anterior, con historial completo y sin ninguna operación para los de visitantes ni de restricción por mora."
titulo: "AdMind — Plan guiado de la asignación de parqueaderos de residentes"
tipo: plan
modo: guiado
estado: activo
hu: [HU-34]
fecha: 2026-10-24
para: "Alejo, con un agente que guía según 09_Protocolos/ejecutar_plan_guiado.md si Alejo lo aprueba; si no, el agente lo construye"
alcance: "HU-34: AsignacionParqueadero, su API y la columna «Asignado a» en la pantalla de parqueaderos"
punto_de_partida: "Backend 7eb5b5a (708 pruebas según estado_actual), Frontend 8279616 (417 pruebas), sin cambios pendientes; makemigrations --check pide personas/0003"
---

# AdMind — Plan guiado de la asignación de parqueaderos de residentes

> [!IMPORTANT]
> **Alejo:** D1 y D2 tienen la respuesta que se dedujo del chat del 2026-10-24 (no marcaste esas opciones): confírmalas o cámbialas. Llena D3. Para empezar o retomar, en un chat nuevo: `Ejecuta el plan Documentacion/Admind_Documentacion/07_Planes/activos/Plan_Parqueaderos_De_Residentes.md`. El agente te pregunta primero si lo quieres guiado o si lo construye él.

## 1. Seguimiento

**Dónde voy:** sin empezar.

| Fase | Deja funcionando | Estado | Modo | Explicada de vuelta | Verificación | Commit | Fecha |
|---|---|---|---|---|---|---|---|
| F0 | Punto de partida confirmado | pendiente | — | — | | — | |
| F1 | Modelo con una sola asignación vigente por puesto | pendiente | | | | | |
| F2 | Servicio y API: asignar, reasignar, historial | pendiente | | | | | |
| F3 | Pantalla: asignar y ver el historial | pendiente | | | | | |

### Desviaciones

Ninguna.

### Conceptos por repasar

Ninguno.

## 2. Instrucciones para el agente

> [!IMPORTANT]
> **Primero pregunta.** Antes de tocar nada, pregúntale a Alejo si este plan se trabaja **guiado** o si lo **construyes** tú.

### 2.1 Qué leer antes de empezar

1. [ejecutar_plan_guiado](../../09_Protocolos/ejecutar_plan_guiado.md).
2. Este plan completo.
3. [parqueaderos](../../05_Modulos/parqueaderos.md): el diseño del maestro §5.6 y lo construido en HU-28.
4. [restricciones_bd](../../02_Arquitectura/restricciones_bd.md): el índice único parcial, el mismo patrón que deja a una sola visita con un puesto.
5. [legal](../../01_Contexto/legal.md) §4.2: un parqueadero de visitantes no se destina a una vivienda; ningún retiro por mora.
6. [invariantes](../../03_Reglas/invariantes.md) y [eliminacion](../../03_Reglas/eliminacion.md): cerrar es `vigencia_hasta`, nunca borrar.
7. `Backend/Admind_Backend/apps/parqueaderos/README.md` y `Frontend/Admind_Front-End/apps/parqueaderos/README.md`.

### 2.2 Reglas propias de este plan

- **No existe** ninguna operación de restricción de uso, ni ruta para «quitar» un parqueadero sin dárselo a otra vivienda (D1).
- Los de visitantes no se asignan: la operación filtra por `tipo=residentes`, así que un puesto de visitantes **no se encuentra** (404), no se «deniega» (403).
- Dos pruebas de HU-28 cambian porque cambió el diseño, no se saltan: ver §5.
- `migrate` lo corre Alejo.

## 3. Decisiones que toma Alejo

| ID | Decisión | Opciones | Recomendada | Respuesta |
|---|---|---|---|---|
| D1 | ¿Se puede liberar un puesto sin reasignarlo (p. ej. se vendió el apartamento)? | a) No: solo asignar y reasignar; el puesto pasa de una vivienda a otra b) Sí, «Liberar» con fecha, nunca ligado a la mora | b, para que la vida real quepa; a si se quiere lo mínimo | **a** (deducida: no se marcó el 24/10) |
| D2 | ¿Una vivienda puede tener varios puestos vigentes? | a) No: una asignación vigente por vivienda, con índice único b) Sí: el límite es solo por puesto | b (los conjuntos suelen tener viviendas con dos); a si se quiere lo mínimo | **a** (deducida: no se marcó el 24/10) |
| D3 | ¿El residente ve su parqueadero? | a) No en este plan b) Sí, en su perfil o en «Mi vivienda» | a | |

> [!WARNING] D1 a y D2 a juntas
> Con las dos en *a*, una vivienda que ya tiene puesto no puede recibir otro, y un puesto solo deja una vivienda cuando pasa a otra. Si una vivienda vende y el comprador no quiere el puesto, no hay cómo dejarlo libre. Confírmalo antes de F1: cambia el índice de la base.

## 4. Decisiones menores que el plan ya fija

| ID | Decisión |
|---|---|
| P1 | Modelo `AsignacionParqueadero(ModeloDeConjunto)` en `apps/parqueaderos/`: `parqueadero` (FK `PROTECT`, related `asignaciones`), `unidad` (FK `PROTECT`), `vigencia_desde` (fecha), `vigencia_hasta` (fecha nula), `registrado_por`, `registrado_en`, `cerrado_por` (nulo) |
| P2 | Restricciones: índice único parcial `asignacion_parqueadero_vigente_unica` sobre `(conjunto, parqueadero)` con `vigencia_hasta IS NULL`; con D2 a, otro `asignacion_unidad_vigente_unica` sobre `(conjunto, unidad)`; `CHECK vigencia_hasta >= vigencia_desde` |
| P3 | Que el puesto sea de residentes lo comprueba el servicio (filtra `tipo=residentes, activo=True`); la base no puede hacer un `CHECK` contra otra tabla. Una prueba escribe directo para dejar dicho ese límite |
| P4 | `vigencia_desde` la pone el sistema (hoy, zona de Bogotá). Reasignar cierra la anterior con `vigencia_hasta = hoy` y crea la nueva desde hoy, en una transacción con `select_for_update` sobre el parqueadero (el mismo orden de bloqueo que `desactivar` y `registrar_ingreso`) |
| P5 | Reasignar a la misma vivienda que ya lo tiene → 409. Un puesto con asignación vigente **no se desactiva** → 409, como el ocupado por una visita |
| P6 | Rutas: `POST /parqueaderos/<id>/asignacion/` (`{unidad}`; asigna si está libre, reasigna si no, y la respuesta dice cuál fue) y `GET /parqueaderos/<id>/asignaciones/` (el historial, del más reciente al más viejo). Permiso `parqueadero.asignar` para escribir; `parqueadero.ver` o `parqueadero.asignar` para el historial |
| P7 | `GET /parqueaderos/` agrega `asignado_a` (nombre de la vivienda o `null`) solo a los de residentes |
| P8 | Auditoría: `parqueadero.asignar` y `parqueadero.reasignar`, con la vivienda anterior y la nueva |
| P9 | Sin aviso a la vivienda: no lo pide la historia. Queda anotado en *Fuera de este plan* |

## 5. Punto de partida verificado

Comprobado el 2026-10-24 en `origin/desarrollo` (Backend `7eb5b5a`, Frontend `8279616`).

- `apps/parqueaderos/models.py`: `Parqueadero(ModeloDeConjunto)` con `codigo`, `tipo` (`TipoDeParqueadero.RESIDENTES` / `VISITANTES`), `accesible`, `notas`, `activo`, `creado_por`, `creado_en`.
- `apps/parqueaderos/servicios.py`: `parqueaderos(tipo, solo_libres)` (anota `abiertas` por `visitas`), `crear`, `desactivar` (con `select_for_update` y `ParqueaderoOcupado`).
- `apps/parqueaderos/urls.py`: `""` y `<uuid:parqueadero_id>/desactivar/`.
- Permisos: `parqueadero.asignar` ya está en `PERMISOS` y en Administración (`apps/permisos/catalogo.py`); no es sensible. **No hay que tocar el catálogo.**
- `apps/unidades/models.py`: `Unidad(ModeloDeConjunto)` con `nombre`.
- Pruebas de HU-28 que cambian por el diseño nuevo:
  - `test_ninguna_ruta_asigna_un_parqueadero_a_una_unidad` (`apps/parqueaderos/tests.py:212`) → `test_hu34_un_parqueadero_de_visitantes_no_se_asigna` (la ruta existe, pero un puesto de visitantes da 404 y no queda ninguna asignación).
  - `test_el_modelo_no_tiene_relacion_con_unidades_y_la_api_ignora_una_unidad` (`:220`) → la parte de `Parqueadero` sigue (el puesto no tiene FK a la unidad: la relación vive en la asignación) y la de crear con `unidad` también.
- Front: `apps/parqueaderos/templates/parqueaderos/lista.html` dice «Sin asignar» para los de residentes.

## 6. Mapa de la funcionalidad

```
Administración → /parqueaderos/ → fila R-07 «Sin asignar» → «Asignar» → elige vivienda
  └─ cliente_api.parqueaderos.asignar → POST /parqueaderos/<id>/asignacion/ {unidad}
       └─ AsignarParqueaderoSerializer → servicios.asignar(actor, parqueadero_id, unidad_id)
            ├─ transaction.atomic + select_for_update(Parqueadero tipo=residentes, activo)  → si no, 404
            ├─ vigente = asignaciones.filter(vigencia_hasta IS NULL) → si existe, se cierra hoy
            ├─ INSERT AsignacionParqueadero (el índice único parcial deja una sola vigente)
            └─ auditoria.registrar("parqueadero.asignar" | "parqueadero.reasignar")
  «Historial» → GET /parqueaderos/<id>/asignaciones/ → vivienda, desde, hasta, quién la registró
```

## F0 · Confirmar el punto de partida

- [ ] **B0.1** · Las dos suites y `makemigrations --check --dry-run` (solo `personas/0003`).

## F1 · El modelo

**Deja funcionando:** la tabla con sus índices; escribir dos asignaciones vigentes sobre un puesto falla en la base.

**Concepto de la fase:** el índice único parcial: «único mientras esté vigente».

- [ ] **B1.1** · explicado · `Backend/Admind_Backend/apps/parqueaderos/models.py` y la migración
  - **Qué:** P1 y P2. `UniqueConstraint(fields=["conjunto", "parqueadero"], condition=Q(vigencia_hasta__isnull=True), name=…)`.
  - **Forma:** como `visitante_parqueadero_ocupado_unico` en `apps/visitantes/models.py`.
  - **Comprobación:** `test_hu34_la_base_deja_una_sola_asignacion_vigente_por_puesto` (dos `create` → `IntegrityError`).

**Cierre de F1**

- **Verificación:** `pytest apps/parqueaderos`; Alejo corre `migrate`.
- **Explicar de vuelta:** «¿por qué el límite está en la base y no en un `if` del servicio?» (dos peticiones a la vez).
- **Commit sugerido:** `feat(parqueaderos): asignación de un parqueadero a una vivienda [HU-34]`

## F2 · Servicio y API

**Deja funcionando:** P4 a P8.

- [ ] **B2.1** · explicado · `apps/parqueaderos/servicios.py`
  - **Qué:** `asignar(actor, parqueadero_id, unidad_id)` según el mapa; `historial(parqueadero_id)`; `desactivar` agrega el 409 de P5. Excepciones `UnidadNoEncontrada`, `YaAsignadoAEsaUnidad` (y con D2 a, `UnidadConParqueadero`).
  - **Comprobación:** `test_hu34_reasignar_cierra_la_anterior_con_fecha_y_conserva_el_historial`.
- [ ] **B2.2** · tuyo (modelo: `DesactivarParqueaderoView`) · `serializers.py`, `views.py`, `urls.py`
  - **Qué:** `AsignacionView` y `HistorialDeAsignacionesView`; `asignado_a` en `ParqueaderoSerializer` (P7).
- [ ] **B2.3** · tuyo · `apps/parqueaderos/tests.py`, `tests/concurrencia/`
  - **Qué:** `test_hu34_un_puesto_libre_queda_con_una_sola_asignacion_vigente`, `test_hu34_un_parqueadero_de_visitantes_no_se_asigna`, `test_hu34_la_asignacion_dice_quien_la_registro_y_desde_cuando`, `test_hu34_no_existe_operacion_de_restriccion_por_mora` (recorre las rutas: no hay `restringir`, `suspender`, `retirar` ni `liberar`; con D1 b, sin `liberar`), las dos de §5 reescritas, las rutas nuevas en la prueba del intruso y una de concurrencia: diez asignaciones a la vez sobre un puesto libre dejan una vigente.

**Cierre de F2**

- **Verificación:** `pytest -q` completo.
- **Pregunta de jurado:** «¿Por qué no se le puede quitar el parqueadero a un moroso?» (no hay operación de restricción de uso: no es un permiso denegado, no existe).
- **Commit sugerido:** `feat(parqueaderos): asignar, reasignar e historial [HU-34]`

## F3 · Pantalla

**Deja funcionando:** en `/parqueaderos/`, los de residentes muestran a quién están asignados, con «Asignar» o «Reasignar» y «Historial».

- [ ] **B3.1** · explicado · `Frontend/Admind_Front-End/cliente_api/parqueaderos.py`, `apps/parqueaderos/views.py`, `forms.py`, `urls.py`
  - **Qué:** `asignar` e `historial` en el cliente; una vista que recibe el formulario y una para el historial. El selector de viviendas usa la lista de unidades del conjunto.
- [ ] **B3.2** · tuyo · `templates/parqueaderos/lista.html` y una plantilla `historial.html`
  - **Qué:** la columna «Asignado a» y los botones, solo en filas de residentes y solo con `parqueadero.asignar`. Las filas de visitantes no tienen ningún botón de asignar.
- [ ] **B3.3** · tuyo · `tests/test_parqueaderos.py`
  - **Qué:** una fila de visitantes no tiene «Asignar»; la de residentes sí.

**Cierre de F3**

- **Verificación:** las dos suites; recorrido del guion.
- **Commit sugerido:** `feat(parqueaderos): asignar y ver el historial desde la lista [HU-34]`

## Cierre del plan

Las dos suites y `makemigrations --check --dry-run`. Informe final y [actualizar_contexto](../../09_Protocolos/actualizar_contexto.md): [parqueaderos](../../05_Modulos/parqueaderos.md) (la nota de arriba dice que no existe `AsignacionParqueadero`), [restricciones_bd](../../02_Arquitectura/restricciones_bd.md), [historias](../../08_Estado/historias.md) y la tabla *Estado real* de Notion.

## Lo que el agente no puede hacer

`migrate`, el PR `desarrollo → pruebas` revisado y la prueba manual de Camilo.

## Guion de prueba manual

1. Como Administración, crear R-01 (residentes) y V-01 (visitantes). V-01 no tiene «Asignar».
2. Asignar R-01 a «Torre 1 – 101». La fila dice «Asignado a Torre 1 – 101».
3. Reasignarlo a «Torre 2 – 202». En «Historial» están las dos, la primera con fecha de cierre y quién registró cada una.
4. Intentar retirar R-01: no deja, porque tiene una asignación vigente.
5. Buscar en la pantalla de pagos o de la vivienda una forma de quitarle el parqueadero a una vivienda en mora: no existe.

## Fuera de este plan

- Avisar a la vivienda cuando se le asigna o se le quita un puesto (P9).
- Que el residente vea su parqueadero (D3 a).
- Liberar un puesto sin reasignarlo y varios puestos por vivienda, si D1 y D2 quedan en *a*.

---
resumen: "Construye HU-34: asignar un parqueadero de residentes a una vivienda y reasignarlo cerrando la asignación anterior, con historial completo y sin ninguna operación para los de visitantes ni de restricción por mora."
titulo: "AdMind — Plan guiado de la asignación de parqueaderos de residentes"
tipo: plan
modo: guiado
estado: activo
hu: [HU-34]
fecha: 2026-10-24
para: "Alejo, con un agente que guía según 09_Protocolos/ejecutar_plan_guiado.md si Alejo lo aprueba; si no, el agente lo construye"
alcance: "HU-34: AsignacionParqueadero, liberar, tope por vehículo con una regla del conjunto, «Mi parqueadero» para el residente, su API y sus pantallas"
punto_de_partida: "Backend 7eb5b5a (708 pruebas según estado_actual), Frontend 8279616 (417 pruebas), sin cambios pendientes; makemigrations --check pide personas/0003"
---

# AdMind — Plan guiado de la asignación de parqueaderos de residentes

> [!NOTE] Se rehace desde cero (2026-10-24)
> Una ejecución anterior en la rama de nube `ccr-4213a943-1fgq6z` nunca llegó a los repositorios y Alejo la descartó. Este plan se ejecuta de nuevo sobre `desarrollo`. Las respuestas D1 a D6 de Alejo (24/10) siguen vigentes y **cambian P2, P6 y P9** respecto a lo escrito en las fases: ver *Cambios por las respuestas*.

## 1. Seguimiento

**Dónde voy:** 2026-10-25 · construido por el agente (Alejo eligió «lo construyes tú») en la rama `feat/parqueaderos-asignacion`, salida de `origin/desarrollo` en el backend y en el frontend, sin commit. Faltan los commits, el PR, `migrate` y el guion de prueba manual.

| Fase | Deja funcionando | Estado | Modo | Explicada de vuelta | Verificación | Commit | Fecha |
|---|---|---|---|---|---|---|---|
| F0 | Punto de partida confirmado | hecha | — | — | Backend 707 de 708 (falla `test_un_registro_que_no_cumple_responde_400…` de ingresos, que depende de la hora del día); Frontend 417; `makemigrations --check` pide solo `personas/0003` | — | 2026-10-25 |
| F1 | Modelo con una sola asignación vigente por puesto | hecha | construida | — | `pytest apps/parqueaderos` en verde; `parqueaderos/0002` por correr | sin commit | 2026-10-25 |
| F2 | Servicio y API: asignar, reasignar, liberar, historial y «mis parqueaderos» | hecha | construida | — | Backend 740 pruebas, todas pasan, con las dos de concurrencia | sin commit | 2026-10-25 |
| F3 | Pantalla: asignar, liberar, historial, «Mi parqueadero» y la regla | hecha | construida | — | Frontend 435 pruebas, todas pasan (más 2 de la regla en `test_reglas.py`); sin recorrer en el navegador porque falta `migrate` | sin commit | 2026-10-25 |

### Cambios por las respuestas (de la ejecución descartada, como guía)

- 2026-10-24 · D1 a D6 · Alejo respondió **D1 b** (se puede liberar), **D2**: una vivienda puede tener varios puestos, con un tope por tipo de vehículo que fija cada conjunto, y **D3 b** (el residente ve su parqueadero). De ahí salieron D4 a D6. Con eso cambian P2 (no hay índice por vivienda), P6 (más rutas) y P9 (sigue sin aviso).
- 2026-10-24 · B1.1 · `Parqueadero.vehiculo ∈ {carro, moto, bicicleta}`, con `default` y `db_default` en carro, y su `CHECK`. Las FK de la asignación son compuestas con `conjunto_id` (`fk_compuesta`).
- 2026-10-24 · B1.1 · Tipo de regla nuevo `PARQUEADEROS_POR_VIVIENDA` (alfa, sin modos: ningún evaluador de reservas lo toca) con `{carro, moto, bicicleta}` desde 0. La migración `reglas/0008` rehace `regla_tipo_valido` y `regla_nivel_coherente`. `makemigrations reglas` generó de paso una `personas/0003` que se borró: es la pendiente de Camilo.
- 2026-10-24 · B2.1 · `asignar` bloquea el puesto y luego la vivienda: sin el segundo bloqueo, diez asignaciones a la vez se saltaban el tope (`tests/concurrencia/test_asignacion_de_parqueaderos.py`). Reasignar dentro del tope solo cuenta la vivienda que recibe.
- 2026-10-24 · B2.2 · Rutas nuevas además de las de P6: `POST /parqueaderos/<id>/liberacion/` y `GET /parqueaderos/mios/` (sin permiso: cada persona ve las de sus vínculos vigentes, como la bandeja de notificaciones). Las cuatro en la prueba del intruso.
- 2026-10-24 · B2.3 · Se quitó `test_ninguna_ruta_asigna_un_parqueadero_a_una_unidad` (HU-28): la ruta ahora existe por diseño; lo que protegía lo cubre `test_hu34_un_parqueadero_de_visitantes_no_se_asigna`. Se actualizó la lista fija del catálogo en `apps/reglas/tests.py`.
- 2026-10-24 · B3 · «Mi parqueadero» (`/parqueaderos/mios/`) en el lateral del rol Residente; el residente que abre `/parqueaderos/` llega ahí. La pantalla de Administración muestra el tope de la regla o que no hay, con enlace a Reglas.

### Desviaciones

- 2026-10-25 · `makemigrations` generó de paso `personas/0003` al crear `parqueaderos/0002` y `reglas/0008`; se borró en las dos veces y las migraciones dependen de `personas/0002` / `0001`. Sigue siendo la pendiente de Camilo.
- 2026-10-25 · La pantalla de asignar es una página aparte (`/parqueaderos/<id>/asignar/`) con el selector de viviendas, no un selector dentro de cada fila: con muchas viviendas, la tabla pesaría. Hay además una ruta de liberar y otra de historial.
- 2026-10-25 · Ramas: se salió de `origin/desarrollo` y no de `HU-22-Triage`, porque esa rama (en PR) no toca parqueaderos, reglas ni permisos y no tiene migraciones.

### Conceptos por repasar

La fase se construyó entera (no guiada): conviene que Alejo repase el índice único parcial, el doble bloqueo (puesto y vivienda) y por qué el tope se lee de la tabla de reglas y no de la API.

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
| D1 | ¿Se puede liberar un puesto sin reasignarlo (p. ej. se vendió el apartamento)? | a) No: solo asignar y reasignar b) Sí, «Liberar» con fecha, nunca ligado a la mora | b | **b** (2026-10-24) |
| D2 | ¿Una vivienda puede tener varios puestos vigentes? | a) No, uno por vivienda b) Sí | b | **Sí, con el tope que fije cada conjunto por tipo de vehículo** (2026-10-24: «en mi conjunto me corresponde uno de carro, uno de bicicleta y uno de moto; cada conjunto tiene sus normas») |
| D3 | ¿El residente ve su parqueadero? | a) No en este plan b) Sí | a | **b** (2026-10-24) |
| D4 | Tipos de vehículo de un puesto | a) Carro, moto y bicicleta b) Carro y moto | a | **a** (2026-10-24) |
| D5 | Dónde vive el tope | a) Regla del conjunto en el motor de reglas, versionada b) Campos del conjunto | a | **a** (2026-10-24) |
| D6 | Sin la regla definida | a) Sin tope b) Uno por tipo | a | **a** (2026-10-24) |

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

Antes: mezclar la rama a `desarrollo` y correr `migrate` (`parqueaderos/0002` y `reglas/0008`).

1. Como Administración, crear R-01 (residentes, carro), M-01 (residentes, moto) y V-01 (visitantes). V-01 no tiene «Asignar» ni «Historial». Sobre la tabla dice que no hay tope.
2. Asignar R-01 a «Torre 1 – 101». La fila dice «Asignado a Torre 1 – 101».
3. En Reglas, definir «Parqueaderos por vivienda» con carro 1, moto 1 y bicicleta 0. La pantalla de parqueaderos ya muestra el tope.
4. Crear R-02 (carro) e intentar asignarlo también a la 101: lo impide, con el mensaje del tope. Asignar M-01 a la 101: sí deja.
5. Reasignar R-01 a «Torre 2 – 202». En «Historial» están las dos, la primera cerrada hoy, con quién registró y quién cerró.
6. Liberar R-01: queda «Sin asignar» y la asignación sigue en el historial. Intentar retirar M-01 (asignado): no deja hasta liberarlo.
7. Como residente de la 101: «Mi parqueadero» muestra M-01 y ya no R-01. No hay botones.
8. Buscar en pagos, en la vivienda o en parqueaderos una forma de quitarle el puesto a una vivienda en mora: no existe.

## Fuera de este plan

- Avisar a la vivienda cuando se le asigna o se le quita un puesto (P9).
- Que el residente vea el historial de su puesto: solo ve el vigente.

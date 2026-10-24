---
resumen: "Amplía HU-33: el reglamento y el manual de convivencia como documentos con versiones, una pantalla para que el residente los consulte y descargue, la vista de versiones archivadas y la auditoría de cada descarga."
titulo: "AdMind — Plan guiado del repositorio de documentos"
tipo: plan
modo: guiado
estado: activo
hu: [HU-33]
fecha: 2026-10-24
para: "Alejo, con un agente que guía según 09_Protocolos/ejecutar_plan_guiado.md si Alejo lo aprueba; si no, el agente lo construye"
alcance: "HU-33 sin las actas de asamblea"
punto_de_partida: "Backend 7eb5b5a (708 pruebas según estado_actual), Frontend 8279616 (417 pruebas), sin cambios pendientes; makemigrations --check pide personas/0003"
---

# AdMind — Plan guiado del repositorio de documentos

> [!IMPORTANT]
> **Alejo:** D1 y D2 ya tienen respuesta (chat del 2026-10-24); llena D3 y D4. Para empezar o retomar, en un chat nuevo: `Ejecuta el plan Documentacion/Admind_Documentacion/07_Planes/activos/Plan_Documentos.md`. El agente te pregunta primero si lo quieres guiado o si lo construye él.

## 1. Seguimiento

**Dónde voy:** sin empezar.

| Fase | Deja funcionando | Estado | Modo | Explicada de vuelta | Verificación | Commit | Fecha |
|---|---|---|---|---|---|---|---|
| F0 | Punto de partida confirmado | pendiente | — | — | | — | |
| F1 | `Documento` con tipo, migrado sin perder los reglamentos | pendiente | | | | | |
| F2 | API por tipo, versiones y descarga auditada | pendiente | | | | | |
| F3 | Pantalla «Documentos» y subida del manual | pendiente | | | | | |

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
3. [conjuntos](../../05_Modulos/conjuntos.md): el reglamento como requisito para quedar operativo (HU-03).
4. [backend](../../02_Arquitectura/backend.md): validación de archivos por su firma y auditoría.
5. [invariantes](../../03_Reglas/invariantes.md) y [eliminacion](../../03_Reglas/eliminacion.md): una versión nueva archiva, no borra.
6. `Backend/Admind_Backend/apps/documentos/README.md` y `Frontend/Admind_Front-End/apps/documentos/README.md`.

### 2.2 Reglas propias de este plan

- **Sin actas** (D2). El tipo se deja como `TextChoices` para que agregarlas después sea una opción más, pero no se escribe nada de actas.
- **El catálogo de permisos no cambia** (D1): solo cambia qué permiso pide cada vista.
- El requisito «Reglamento cargado» del asistente tiene que seguir funcionando igual: `apps/conjuntos/tests.py` en verde sin cambiar lo que comprueba.
- La migración la corre Alejo, y antes hace un respaldo de `admind_db` (es un `RenameModel`).

## 3. Decisiones que toma Alejo

| ID | Decisión | Opciones | Recomendada | Respuesta |
|---|---|---|---|---|
| D1 | Cómo descarga el residente | a) `documento.ver` alcanza para los vigentes; toda descarga se audita; `documento.descargar` (sensible) queda para las versiones archivadas b) Darle `documento.descargar` (exige 2FA) c) Quitar lo sensible | a | **a** (2026-10-24) |
| D2 | Actas de asamblea | a) Entran b) Solo reglamento y manual | b | **b** (2026-10-24) |
| D3 | El modelo | a) Renombrar `Reglamento` a `Documento` y agregar `tipo` (reglamento, manual); las filas existentes quedan como reglamento b) Un modelo `ManualDeConvivencia` aparte, copia del reglamento c) `tipo` en `Reglamento` sin renombrar | a | |
| D4 | ¿El manual es requisito para que el conjunto quede operativo? | a) No: HU-03 solo exige el reglamento b) Sí, otro requisito en el asistente | a | |

## 4. Decisiones menores que el plan ya fija

| ID | Decisión |
|---|---|
| P1 | `TipoDeDocumento(TextChoices)`: `reglamento` («Reglamento de propiedad horizontal») y `manual` («Manual de convivencia»). `CHECK documento_tipo_valido` |
| P2 | El vigente de un tipo es el más reciente de ese tipo (como hoy). Índice `(conjunto, tipo, subido_en)` en lugar de `reglamento_por_fecha` |
| P3 | Rutas: `GET /documentos/` (los vigentes de cada tipo, sin contenido); `GET`/`PUT /documentos/<tipo>/`; `GET /documentos/<tipo>/archivo/` (el vigente); `GET /documentos/<tipo>/versiones/` y `GET /documentos/<tipo>/versiones/<id>/archivo/` (Administración). `<tipo>` es un convertidor que solo acepta los valores de P1; uno desconocido es 404. **Las rutas `documentos/reglamento/…` que usa el asistente quedan iguales**, porque son el caso `tipo=reglamento` |
| P4 | Permisos por vista: ver la lista y el vigente, `documento.ver` o `documento.subir`; subir, `documento.subir`; versiones archivadas (lista y archivo), `documento.descargar` |
| P5 | Cada `GET …/archivo/` escribe `auditoria.registrar(actor, "documento.descargar", "Documento", id, detalle={"tipo": …, "version": "vigente" o "archivada"})`. El registro guarda usuario, documento y fecha (`creado_en`) |
| P6 | La subida audita `documento.subir` con el tipo; las filas viejas de `reglamento.subir` no se tocan (la auditoría es de solo inserción) |
| P7 | Validación igual que hoy: firma `%PDF-`, hasta 10 MB, SHA-256. El servicio pasa de `ReglamentoInvalido` a `DocumentoInvalido` |
| P8 | En el front, «Documentos» en el menú de todo rol con `documento.ver`; Administración sube desde la misma pantalla; el asistente sigue subiendo el reglamento en su paso |

## 5. Punto de partida verificado

Comprobado el 2026-10-24 en `origin/desarrollo` (Backend `7eb5b5a`, Frontend `8279616`).

- `apps/documentos/models.py`: `Reglamento(ModeloDeConjunto)` con `contenido` (`BinaryField`), `nombre`, `peso`, `huella`, `subido_por`, `subido_en`; índice `reglamento_por_fecha`. Migración `0001_initial`.
- `apps/documentos/servicios.py`: `vigente(con_contenido=False)`, `guardar(actor, nombre, contenido)`, `TAMANO_MAXIMO`, `FIRMA_DE_PDF`, `ReglamentoInvalido`; audita `reglamento.subir`.
- `apps/documentos/views.py`: `ReglamentoView` (`GET` con `documento.ver`/`documento.subir`, `PUT` con `documento.subir`) y `ArchivoDelReglamentoView` (`GET` con `documento.descargar`/`documento.subir`, **sin auditoría**). `urls.py`: `reglamento/` y `reglamento/archivo/`.
- `apps/conjuntos/servicios.py:16` importa `Reglamento` y `:127` usa `Reglamento.objects.exists()` para el requisito; `apps/conjuntos/tests.py:14` y `:331` crean un `Reglamento`.
- Permisos: `documento.subir`, `documento.ver`, `documento.descargar`; el Residente tiene solo `documento.ver`; `documento.descargar` es sensible.
- Pruebas: `apps/documentos/tests.py` (5). **`test_el_residente_ve_los_datos_pero_no_sube_ni_descarga` cambia de sentido con D1 a**: se reescribe como `test_hu33_el_residente_descarga_el_vigente_y_no_las_versiones` (no es saltarse una prueba: cambió la regla, por decisión de Alejo).
- Front: `cliente_api/documentos.py` (`reglamento`, `subir_reglamento`, `archivo_del_reglamento`); `apps/documentos/` solo tiene README; el asistente (`apps/conjuntos/`) usa esas tres funciones.

## 6. Mapa de la funcionalidad

```
Residente → /documentos/  (pantalla nueva)
  └─ cliente_api.documentos.vigentes → GET /documentos/ → [{tipo: reglamento, …}, {tipo: manual, cargado: false}]
  └─ «Descargar» → GET /documentos/manual/archivo/
        └─ exigir documento.ver → servicios.vigente("manual", con_contenido=True)
        └─ auditoria.registrar("documento.descargar", …) → PDF
Administración → misma pantalla: «Subir versión nueva» (PUT /documentos/<tipo>/) y «Versiones» (documento.descargar, 2FA)
```

## F0 · Confirmar el punto de partida

- [ ] **B0.1** · Las dos suites y `makemigrations --check --dry-run` (solo `personas/0003`).

## F1 · El modelo con tipo

**Deja funcionando:** `Documento` con `tipo`; los reglamentos que ya hay siguen ahí como `tipo=reglamento`; el asistente sigue pidiendo el reglamento.

**Concepto de la fase:** una migración que renombra conserva los datos; una que borra y crea, no.

- [ ] **B1.1** · explicado · `Backend/Admind_Backend/apps/documentos/models.py` y `migrations/0002_…`
  - **Qué:** con D3 a, `Documento` + `TipoDeDocumento` (P1, P2). La migración: `RenameModel("Reglamento", "Documento")`, `AddField("tipo", default="reglamento")`, cambio de índice y el `CHECK`. Se revisa a mano que `makemigrations` haya generado un `RenameModel` y no un `DeleteModel` + `CreateModel`.
  - **Comprobación:** prueba de migración o, como mínimo, `sqlmigrate documentos 0002` muestra `ALTER TABLE … RENAME`.
- [ ] **B1.2** · tuyo · `apps/conjuntos/servicios.py` y `tests.py`
  - **Qué:** `Documento.objects.filter(tipo=TipoDeDocumento.REGLAMENTO).exists()`; las pruebas crean `Documento(tipo=…)`. Con D4 a, un manual solo no cuenta como reglamento: una prueba lo dice.

**Cierre de F1**

- **Verificación:** `pytest apps/documentos apps/conjuntos`; Alejo hace respaldo y corre `migrate`.
- **Explicar de vuelta:** «¿qué SQL genera la `0002` y por qué no se pierde ningún reglamento?».
- **Commit sugerido:** `feat(documentos): documento con tipo, el reglamento y el manual [HU-33]`

## F2 · API por tipo, versiones y descarga auditada

**Deja funcionando:** las rutas de P3 con los permisos de P4 y la auditoría de P5.

**Concepto de la fase:** un convertidor de ruta hace que un tipo que no existe no llegue ni a la vista.

- [ ] **B2.1** · explicado · `apps/documentos/servicios.py`
  - **Qué:** `vigente(tipo, con_contenido=False)`, `vigentes()`, `versiones(tipo)`, `version(tipo, id, con_contenido)`, `guardar(actor, tipo, nombre, contenido)` y `registrar_descarga(actor, documento, archivada)`.
- [ ] **B2.2** · explicado · `apps/documentos/urls.py` y `views.py`
  - **Qué:** un convertidor `TipoDeDocumentoConverter` (`regex` con los valores de P1) registrado con `register_converter`; `DocumentosView`, `DocumentoView`, `ArchivoDelDocumentoView`, `VersionesView`, `ArchivoDeVersionView`. Los nombres de ruta viejos (`reglamento`, `reglamento-archivo`) se conservan si alguna prueba hace `reverse`.
- [ ] **B2.3** · tuyo · `apps/documentos/tests.py`
  - **Qué:** una prueba por criterio sin actas: `test_hu33_el_residente_ve_el_reglamento_y_el_manual_vigentes`, `test_hu33_una_version_nueva_archiva_la_anterior_sin_borrarla` (la lista de versiones tiene las dos), `test_hu33_un_archivo_que_no_es_pdf_se_rechaza_por_su_tipo_real` (renombra la existente), `test_hu33_cada_descarga_queda_en_la_auditoria` (usuario, documento y fecha) y la reescrita de §5. Las rutas nuevas en la prueba del intruso.

**Cierre de F2**

- **Verificación:** `pytest -q` completo.
- **Explicar de vuelta:** «¿por qué el residente baja el reglamento sin 2FA y Administración necesita 2FA para una versión vieja?».
- **Pregunta de jurado:** «¿Cómo sabe que un PDF es un PDF?» (la firma del contenido, no la extensión ni el tipo que dice el navegador).
- **Commit sugerido:** `feat(documentos): API por tipo, versiones y descarga auditada [HU-33]`

## F3 · Pantalla «Documentos»

**Deja funcionando:** `/documentos/` para todo rol con `documento.ver`; Administración sube el manual y ve las versiones.

- [ ] **B3.1** · explicado · `Frontend/Admind_Front-End/cliente_api/documentos.py`
  - **Qué:** `vigentes`, `subir(request, tipo, archivo)`, `archivo(request, tipo)`, `versiones`, `archivo_de_version`. Las tres funciones del reglamento quedan como atajos con `tipo="reglamento"` para no tocar el asistente.
- [ ] **B3.2** · tuyo (modelo: `apps/parqueaderos/`) · `apps/documentos/` (`apps.py`, `views.py`, `urls.py`, `forms.py`, `templates/documentos/lista.html`), `config/urls.py` y el menú
  - **Qué:** una tarjeta por tipo con nombre, fecha y «Descargar»; «Sin cargar» si no hay. Con `documento.subir`, el formulario de subida; con `documento.descargar`, «Versiones».
- [ ] **B3.3** · tuyo · `tests/test_documentos.py`
  - **Qué:** el residente ve las dos tarjetas y no ve «Subir» ni «Versiones»; el asistente sigue subiendo el reglamento (`tests/test_asistente_reglamento.py` en verde).

**Cierre de F3**

- **Verificación:** las dos suites; recorrido del guion.
- **Commit sugerido:** `feat(documentos): pantalla de documentos del conjunto [HU-33]`

## Cierre del plan

Las dos suites y `makemigrations --check --dry-run`. Informe final y [actualizar_contexto](../../09_Protocolos/actualizar_contexto.md): [conjuntos](../../05_Modulos/conjuntos.md), [historias](../../08_Estado/historias.md) (HU-33 sigue parcial: faltan las actas) y la tabla *Estado real* de Notion.

## Lo que el agente no puede hacer

El respaldo y `migrate`, el PR `desarrollo → pruebas` revisado y la prueba manual de Camilo.

## Guion de prueba manual

1. Como Administración, abrir `/documentos/`: el reglamento que se subió en el asistente está; el manual dice «Sin cargar». Subir el manual en PDF.
2. Intentar subir un `.txt` renombrado a `.pdf`: se rechaza.
3. Subir otra versión del reglamento. En «Versiones» (pide 2FA) están las dos.
4. Como residente: ver las dos tarjetas, descargar el manual. No aparecen «Subir» ni «Versiones».
5. Como Administración, en la auditoría: una fila `documento.descargar` con el residente, el manual y la hora.

## Fuera de este plan

- Las actas de asamblea y su visibilidad solo para propietarios (D2 b): el criterio queda sin cumplir.
- Otros tipos de documento.

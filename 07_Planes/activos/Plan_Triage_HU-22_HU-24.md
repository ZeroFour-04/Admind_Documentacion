---
resumen: "Cierra HU-24 con una prueba por criterio y completa HU-22 sobre las pestañas que ya existen: filtros por pestaña, antigüedad siempre visible y la prueba de que la bandeja no aprueba, no responde de fondo ni exporta."
titulo: "AdMind — Plan guiado de la bandeja de triage y el rechazo formal"
tipo: plan
modo: guiado
estado: activo
hu: [HU-22, HU-24]
fecha: 2026-10-24
para: "Alejo, con un agente que guía según 09_Protocolos/ejecutar_plan_guiado.md si Alejo lo aprueba; si no, el agente lo construye"
alcance: "HU-24 completa salvo la parte que depende de HU-19; HU-22 sin la pestaña de citas (HU-31)"
punto_de_partida: "Backend 7eb5b5a (708 pruebas según estado_actual), Frontend 8279616 (417 pruebas), sin cambios pendientes; makemigrations --check pide personas/0003"
---

# AdMind — Plan guiado de la bandeja de triage y el rechazo formal

> [!IMPORTANT]
> **Alejo:** las decisiones D1 a D3 ya tienen respuesta (chat del 2026-10-24); llena D4 y D5. Para empezar o retomar, en un chat nuevo: `Ejecuta el plan Documentacion/Admind_Documentacion/07_Planes/activos/Plan_Triage_HU-22_HU-24.md`. El agente te pregunta primero si lo quieres guiado o si lo construye él.

## 1. Seguimiento

**Dónde voy:** sin empezar.

| Fase | Deja funcionando | Estado | Modo | Explicada de vuelta | Verificación | Commit | Fecha |
|---|---|---|---|---|---|---|---|
| F0 | Punto de partida confirmado | pendiente | — | — | | — | |
| F1 | HU-24: una prueba con el nombre de cada criterio | pendiente | | | | | |
| F2 | HU-22: filtros de casos y reservas en la API | pendiente | | | | | |
| F3 | HU-22: filtros en las pestañas del dashboard | pendiente | | | | | |
| F4 | HU-22: pruebas de sus cinco criterios | pendiente | | | | | |

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
3. [triage](../../05_Modulos/triage.md): la frontera forma/fondo, por qué los eventos no llevan prioridad y lo que ya está construido del dashboard.
4. [reservas](../../05_Modulos/reservas.md): estados de la solicitud y por qué solo `EXPIRADA` gasta oportunidad (R9).
5. [capas](../../03_Reglas/capas.md) y [reglas_frontend](../../03_Reglas/reglas_frontend.md): dónde va un filtro (consulta del servicio, no la plantilla).
6. `Backend/Admind_Backend/apps/casos/README.md`, `apps/reservas/README.md` y `Frontend/Admind_Front-End/apps/triage/README.md`.

### 2.2 Reglas propias de este plan

- **No se crea vista combinada** ni pestaña «Todo» (D1). Si una prueba o una nota la pide, se para y se pregunta.
- **No se toca el catálogo de permisos.** `solicitud.bandeja_ver` ya es sensible: el 2FA ya se exige.
- **Citas no se construye**: es HU-31, de Camilo. La pestaña sigue con su estado vacío.
- El criterio de las «dos oportunidades» de HU-24 queda **parcial** hasta HU-19 (D2): no se inventa un contador.

## 3. Decisiones que toma Alejo

| ID | Decisión | Opciones | Recomendada | Respuesta |
|---|---|---|---|---|
| D1 | La «sola bandeja» de HU-22 contra la decisión del 13/10 (pestañas separadas) | a) Se mantienen las pestañas, cada una con filtros; el criterio se lee «un solo dashboard, por pestañas» b) Pestaña «Todo» ordenada por antigüedad c) Posponer HU-22 | a | **a** (2026-10-24) |
| D2 | El criterio de «no consume sus dos oportunidades» de HU-24 | a) Se prueba lo observable hoy: el descarte deja la solicitud en `RECHAZADA` (no `EXPIRADA`) y el residente puede volver a tomar la franja enseguida; queda parcial hasta HU-19 b) Construir el contador de oportunidades (es HU-19) | a | **a** (implícita en el pedido: «mínimo, pruebas») |
| D3 | Citas en la bandeja | a) Fuera: depende de HU-31 b) Esperar a HU-31 para cerrar HU-22 | a | **a** |
| D4 | Filtro por vivienda en la pestaña de casos. El caso no guarda la vivienda: se deduce de dónde reside su autor | a) Solo en reservas (la solicitud sí tiene `unidad`); en casos, filtro por solicitante b) En casos también, deduciendo por los vínculos vigentes del autor c) Agregar `Caso.unidad` (migración y cambio de modelo) | a | |
| D5 | Dónde se filtra | a) En la API: parámetros validados por un serializer de consulta, el servicio arma el `filter` b) En el front, sobre las filas ya traídas | a | |

## 4. Decisiones menores que el plan ya fija

| ID | Decisión |
|---|---|
| P1 | Filtros de casos: `estado`, `prioridad`, `desde`, `hasta` (fecha de creación) y `solicitante` (texto, `icontains` sobre nombres y apellidos del autor). Filtros de reservas: `estado`, `area`, `desde`, `hasta` (fecha de envío), `vivienda` y `solicitante`. Sin prioridad en reservas: el parámetro no existe y, si llega, se ignora como cualquier parámetro desconocido |
| P2 | El orden no cambia con los filtros: casos `prioridad DESC, creado_en ASC` (o «por antigüedad»), reservas por antigüedad. Los filtros reducen, no reordenan |
| P3 | Los filtros viajan en la URL del dashboard (`?pestana=casos&estado=ABIERTO…`), igual que hoy `ver` y `orden`, para que un enlace reproduzca la vista |
| P4 | Un filtro inválido (fecha mal escrita, estado que no existe) responde 400 en la API; el front lo muestra como error del formulario y no como tabla vacía |
| P5 | La columna «Antigüedad» se pinta fuera de cualquier `{% if %}` de filtro, y una prueba del front lo comprueba con cada filtro activo |
| P6 | Las pruebas de HU-24 se nombran con el criterio: `test_hu24_<criterio>`. Las que ya existen y cubren un criterio no se duplican: se renombran o se agrega una que lo diga |

## 5. Punto de partida verificado

Comprobado el 2026-10-24 en `origin/desarrollo` (Backend `7eb5b5a`, Frontend `8279616`).

**HU-24, lo que ya existe:**

- `apps/reservas/servicios.py:359` `descartar_solicitud(actor, solicitud_id, causal, comentario)`: exige causal de `CAUSALES_DE_FORMA` (sin «otro») y comentario; llama a `_cerrar`, que bloquea la fila (`select_for_update`), exige estado `APARTADA` (si no, `DecisionNoPermitida` → 409), audita `solicitud.rechazar_formal`, avisa al residente y, al rechazar, llama a `notificar_disponibilidad` (campanas de la franja).
- `POST /reservas/solicitudes/<id>/descarte/` (`apps/reservas/views.py:182`, permiso `solicitud.rechazar_formal`).
- `apps/casos/servicios.py:186` `descartar(actor, caso_id, causal, comentario)` con `CausalDeDescarte` (no es competencia, duplicado, información insuficiente). El `CHECK caso_rechazado_con_motivo` hace que el motivo sea la respuesta al residente.
- Pruebas que ya cubren parte: `apps/reservas/tests.py` `test_secretaria_descarta_con_causal_y_comentario_y_la_franja_queda_libre` y `test_el_descarte_exige_causal_de_forma_y_comentario_y_es_solo_de_secretaria`; `apps/casos/tests.py` `test_secretaria_descarta_con_causal_y_motivo_y_el_residente_lo_consulta` y `test_el_descarte_exige_causal_y_motivo_y_no_es_de_administracion`.
- **No probado hoy:** que la campana se dispare en un descarte (solo se prueba la franja libre), que el residente vuelva a tomar la franja y que no exista ruta para reversar.
- `apps/reservas/models.py:12`: `RECHAZADA` se distingue de `EXPIRADA` porque solo el vencimiento gasta oportunidad (R9). No existe contador de oportunidades: es HU-19.

**HU-22, lo que ya existe:**

- Front `apps/triage/views.py` `dashboard(request)`: pestañas `reservas`, `casos`, `citas`; filtros `ver` (pendientes/todas) y `orden` (casos). Plantillas `triage/bandeja.html`, `_dashboard.html`, `_tabla_reservas.html`, `_tabla_casos.html`, `_citas.html`. `hace_cuanto()` calcula la antigüedad.
- `cliente_api/reservas.py:42` `solicitudes_para_bandeja(request)` → `GET /reservas/bandeja/`; `cliente_api/casos.py:7` `listar(request, orden=None)` → `GET /casos/`, que sirve `apps/casos/servicios.py:84` `casos_para_bandeja(ver, orden)`.
- 2FA: `solicitud.bandeja_ver` está en `PERMISOS_SENSIBLES` (`apps/permisos/catalogo.py`).

**No coincidía:** `08_Estado/historias.md` decía HU-22 y HU-24 «Sin empezar»; las dos son parciales (corregido el 2026-10-24). Notion tiene HU-24 «En revisión».

## 6. Mapa de la funcionalidad

```
Dashboard (/solicitudes/?pestana=casos&estado=ABIERTO&desde=2026-10-01)
  └─ triage/views.dashboard → lee los filtros de la URL
       └─ cliente_api.casos.listar(request, orden, **filtros)
            └─ GET /casos/?estado=…&prioridad=…&desde=…&hasta=…&solicitante=…
                 └─ ConsultarCasosSerializer (valida) → servicios.casos_para_bandeja(ver, orden, **filtros) → Caso.objects.filter(…)
  └─ la tabla siempre pinta «Antigüedad»; sin botones de aprobar, responder ni exportar
```

## F0 · Confirmar el punto de partida

- [ ] **B0.1** · Correr las dos suites y `makemigrations --check --dry-run`. La única migración pendiente esperada es `personas/0003` (no es de este plan: no se genera). Si hay otra, se para.

## F1 · HU-24: una prueba por criterio

**Deja funcionando:** cinco pruebas `test_hu24_*` en verde, una por criterio de Notion.

**Concepto de la fase:** una operación que «no existe» se prueba buscándola: no hay ruta ni método, no un 403.

- [ ] **B1.1** · explicado · `Backend/Admind_Backend/apps/reservas/tests.py`
  - **Qué:** `test_hu24_rechazo_sin_categoria_o_sin_explicacion_falla` (renombra o envuelve la existente) y `test_hu24_rechazo_formal_libera_la_franja_y_avisa_a_la_campana`: un segundo residente activa la campana de la franja (`activar_campana`), la Secretaría descarta, y se comprueba la `Notificacion` con origen de campana y que la campana quedó `activa=False`.
  - **Concepto:** probar el efecto lateral (el aviso) y no solo el estado.
  - **Comprobación:** `pytest apps/reservas -k hu24`.
- [ ] **B1.2** · tuyo (modelo: B1.1) · mismo archivo
  - **Qué:** `test_hu24_el_residente_vuelve_a_tomar_la_franja_sin_gastar_oportunidad`: tras el descarte, el mismo residente toma el bloqueo de esa franja con éxito y la solicitud anterior está en `RECHAZADA`, nunca en `EXPIRADA`. Un comentario dice que el contador de oportunidades llega con HU-19.
- [ ] **B1.3** · explicado · `apps/reservas/tests.py` y `apps/casos/tests.py`
  - **Qué:** `test_hu24_rechazo_formal_no_se_aprueba_ni_se_reversa`: decidir o descartar otra vez da 409, y recorriendo `get_resolver()` no hay ninguna ruta con `reversar`, `reabrir` ni `deshacer` (mismo patrón que `rutas_de_parqueaderos` en `apps/parqueaderos/tests.py`). `test_hu24_caso_rechazado_formalmente_cuenta_como_respuesta`: el residente consulta su caso y ve el motivo como respuesta.
  - **Concepto:** el patrón «recorrer las rutas» para probar una ausencia.

**Cierre de F1**

- **Verificación:** `pytest -q` completo en verde.
- **Explicar de vuelta:** «¿por qué un descarte de la Secretaría no le quita una oportunidad al residente y un vencimiento sí?».
- **Pregunta de jurado:** «¿Qué impide que la Secretaría rechace por cualquier cosa?» (lista cerrada sin «otro»; lo que no cabe se redirige).
- **Commit sugerido:** `test(reservas,casos): una prueba por criterio del rechazo formal [HU-24]`

## F2 · HU-22: filtros en la API

**Deja funcionando:** `GET /casos/` y la lista de solicitudes de la bandeja aceptan los filtros de P1, con 400 para un filtro inválido.

**Concepto de la fase:** el serializer de consulta valida la entrada de un `GET` igual que la de un `POST`; el servicio arma la consulta.

- [ ] **B2.1** · explicado · `Backend/Admind_Backend/apps/casos/serializers.py` y `servicios.py`
  - **Qué:** `ConsultarCasosSerializer` (`estado` y `prioridad` como `ChoiceField` opcionales, `desde`/`hasta` `DateField`, `solicitante` `CharField` hasta 80) con `validate` que exige `desde <= hasta`. `casos_para_bandeja(ver, orden)` (`apps/casos/servicios.py:84`) recibe esos filtros como argumentos con nombre y aplica `filter` uno por uno, antes del orden.
  - **Forma:** modelo `apps/parqueaderos/serializers.py` `ConsultarParqueaderosSerializer`.
  - **Comprobación:** prueba con `?estado=OTRO` → 400; `?prioridad=URGENTE` → solo urgentes y en el orden de siempre.
- [ ] **B2.2** · tuyo (modelo: B2.1) · `apps/reservas/serializers.py`, `servicios.py` y `BandejaDeSolicitudesView` (`GET /reservas/bandeja/`)
  - **Qué cambia:** sin `prioridad`; con `area` (UUID) y `vivienda` (UUID de `Unidad`). Con D4 a, `vivienda` solo existe aquí.

**Cierre de F2**

- **Verificación:** `pytest -q`; la prueba del intruso sigue en verde (no hay rutas nuevas).
- **Explicar de vuelta:** «sigue un `GET /casos/?prioridad=ALTA` desde la vista hasta el SQL».
- **Pregunta de jurado:** «¿Por qué los eventos no se pueden filtrar por prioridad?».
- **Commit sugerido:** `feat(casos,reservas): filtros de la bandeja de gestión [HU-22]`

## F3 · HU-22: filtros en el dashboard

**Deja funcionando:** cada pestaña tiene su formulario de filtros; la URL los conserva y la antigüedad sigue visible.

- [ ] **B3.1** · explicado · `Frontend/Admind_Front-End/cliente_api/casos.py` y `reservas.py`
  - **Qué:** `casos.listar(request, orden=None, **filtros)` y `reservas.solicitudes_para_bandeja(request, **filtros)` (hoy sin filtros) pasan los filtros como `params`, sin valores vacíos.
- [ ] **B3.2** · explicado · `apps/triage/views.py`
  - **Qué:** una función `filtros_de(request, pestana)` que lee de `request.GET` solo los nombres de P1 para esa pestaña; `url_del_dashboard` los conserva al cambiar `ver` u `orden`. Un 400 de la API se muestra como error de los filtros.
- [ ] **B3.3** · tuyo (modelo: el formulario de `apps/reservas`) · `templates/triage/_dashboard.html`
  - **Qué:** un `<form method="get">` por pestaña con los campos de P1 y un enlace «Quitar filtros». La columna «Antigüedad» sin condición (P5).

**Cierre de F3**

- **Verificación:** `pytest -q` en el front; abrir `/solicitudes/` con un usuario de Secretaría y filtrar.
- **Explicar de vuelta:** «¿por qué los filtros van en la URL y no en la sesión?».
- **Commit sugerido:** `feat(triage): filtros por pestaña en el dashboard [HU-22]`

## F4 · HU-22: pruebas de los criterios

- [ ] **B4.1** · explicado · `Frontend/Admind_Front-End/tests/test_triage.py` (nuevo; las pruebas del front viven en `tests/`, con `tests/ayudantes.py`)
  - **Qué:** `test_hu22_con_cualquier_filtro_la_antiguedad_sigue_visible` (parametrizada por filtro) y `test_hu22_la_bandeja_no_tiene_aprobar_responder_ni_exportar` (el HTML de Secretaría no contiene esos botones ni formularios).
- [ ] **B4.2** · tuyo · Backend
  - **Qué:** `test_hu22_sin_2fa_se_exige_configurarlo` (si no existe ya una prueba equivalente de permisos sensibles, una que pida `/casos/` sin 2FA) y `test_hu22_la_secretaria_del_conjunto_a_no_ve_nada_del_b` con filtros aplicados.

**Cierre de F4**

- **Verificación:** las dos suites en verde.
- **Pregunta de jurado:** «¿Por qué no hay una bandeja combinada?» (dos colas con razones distintas: conveniencia de gestión contra equidad sobre un bien escaso).
- **Commit sugerido:** `test(triage): criterios de la bandeja [HU-22]`

## Cierre del plan

Las dos suites y `makemigrations --check --dry-run` (solo `personas/0003`, que no es de aquí). Informe final y [actualizar_contexto](../../09_Protocolos/actualizar_contexto.md): [triage](../../05_Modulos/triage.md), [historias](../../08_Estado/historias.md) (HU-24 construida salvo lo de HU-19; HU-22 parcial, solo falta citas) y la tabla *Estado real* de las dos páginas de Notion.

## Lo que el agente no puede hacer

PR `desarrollo → pruebas` revisado y la prueba manual de Camilo con el guion de abajo.

## Guion de prueba manual

1. Como residente, pedir el salón para una franja; como otro residente, activar la campana de esa franja.
2. Como Secretaría (con 2FA), descartar la solicitud con «Datos incompletos» y un comentario. El primer residente recibe el aviso con el motivo; el segundo, el de la campana.
3. El primer residente vuelve a pedir la misma franja: puede.
4. En el dashboard, pestaña Casos: filtrar por prioridad Alta y por un rango de fechas. La antigüedad sigue visible. No hay botón de aprobar ni de exportar.
5. Pestaña Reservas: filtrar por vivienda. Copiar la URL y abrirla en otra pestaña: se ve lo mismo.

## Fuera de este plan

- La pestaña de citas (HU-31 y HU-32, de Camilo).
- El contador de oportunidades de R9 (HU-19).
- Exportar la bandeja: no existe por diseño.

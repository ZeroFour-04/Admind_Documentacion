---
resumen: "Registro de infracciones: el sistema notifica y registra el desenlace, no sanciona."
tipo: modulo
modulo: infracciones
hu: [HU-30]
origen: "maestro v1.4 (2026-09-14) §5.8"
actualizado: 2026-10-25
revisado: 2026-10-25
---

# Infracciones

> [!NOTE] Construido el 2026-10-25 en la rama `feat/infracciones-registro` (back y front), sin commit ni `migrate`
> HU-30 está construida con las respuestas D1 a D5 de [Plan_Infracciones](../07_Planes/activos/Plan_Infracciones.md). Lo que sigue en *Diseño* es el maestro §5.8; *Cómo está construido* dice lo que hay en el código.

## Diseño (maestro §5.8)

**El sistema no sanciona y tampoco modela el procedimiento sancionatorio.** Hace dos cosas: **notifica y registra el desenlace**.

El corte no es de esfuerzo, es de **competencia**: requerir es del administrador (art. 59), decidir es de la asamblea o el consejo (art. 60), y ejecutar ocurre fuera del sistema.

```
RegistroDeInfraccion
  conjunto_id
  unidad_id
  caso_id             (nullable — puede nacer de un Caso o abrirse de oficio)
  descripcion_hecho   (obligatorio, texto libre)
  fecha_hecho
  registrado_por
  fecha_notificacion  (obligatorio — sin comunicación no hay registro)
  cierre_fecha        (nullable)
  cierre_comentario   (nullable, texto libre)
  anulado             (bool — solo el Superusuario, con motivo)
```

**No hay campo `estado`.** Está _abierto_ si `cierre_fecha` es nulo y _cerrado_ si no. Cuando quedan dos situaciones y una fecha las distingue, el `enum` sobra.

**No hay campo de sanción, multa ni restricción.** No están denegados por permiso: **no existen**.

**Lo duro:**

- `fecha_notificacion` es obligatoria. Un registro sin comunicación es una anotación privada sobre una persona identificada, y eso es tratamiento sin finalidad legítima
- La notificación alcanza a **propietario y arrendatario** (C-318/02)
- El registro **nunca** llega al tablón de anuncios
- Visibilidad restringida a Administración y vínculos vigentes de la unidad
- No hay borrado. Un registro equivocado se **anula** con motivo, y solo el Superusuario

> [!WARNING] El registro no es prueba de debido proceso Demuestra que hubo una comunicación con fecha y destinatario. **No demuestra** que se respetó el derecho de defensa del art. 59, ni que decidió el órgano competente, ni que la decisión quedó en firme. La interfaz tiene que decirlo en el propio registro (R11).

**Consecuencia sobre el motor de reglas:** la regla beta _bloqueo por sanción vigente_ sale del catálogo y **no se reemplaza por una marca manual**. Una casilla que el administrador pueda marcar para impedirle a un residente usar la piscina es, jurídicamente, peor que la máquina de estados que se eliminó. La regla alfa de mora no se toca.

## Cómo está construido (2026-10-25)

| Qué | Dónde | Cómo |
|---|---|---|
| El registro | `RegistroDeInfraccion` (`infracciones/0001`) | Como el diseño: sin `estado` (`abierto` = `cierre_fecha` nulo y no anulado), `fecha_notificacion` `NOT NULL`, y `CHECK` para que la fecha y el comentario del cierre vayan juntos, que anular exija motivo, quién y cuándo, y que el hecho no sea vacío. FK compuestas a vivienda y caso |
| Registrar y comunicar | `servicios.registrar` | Una transacción: busca a quién avisar (`destinatarios(unidad, Hecho.INFRACCION)`: propietario y arrendatario, residan o no), crea el registro con `fecha_notificacion = ahora`, `notificar(...)` y audita. Sin destinatarios, 400 «La vivienda no tiene a quién comunicarle» y no queda nada. El aviso lleva el hecho, la vivienda y la frase de R11; **no dice quién registró** |
| Cerrar | `POST /infracciones/<id>/cierre/ {comentario}` | La fecha la pone el sistema; no toca el hecho ni la fecha de comunicación. Avisa otra vez a la vivienda (D5 a, origen `infraccion.cierre`). Dos veces, 409 |
| Anular | `POST /infracciones/<id>/anulacion/ {motivo}` | Permiso nuevo `infraccion.anular`, **solo en `PERMISOS`** (lo tiene únicamente el Superusuario) y sensible (D3 a). No avisa a la vivienda. El registro sigue en la lista, tachado y con su motivo |
| Consultar | `GET /infracciones/` y `/<id>/` | `infraccion.ver` (Administración, con 2FA). Primero los abiertos, y luego el más reciente |
| Lo que no hay | — | Ningún `PUT`, `PATCH` ni `DELETE` (405) y ninguna ruta, campo ni texto de sanción, multa o restricción. Una prueba recorre los campos y las rutas |
| El residente | su bandeja y su correo | Solo ve el aviso (D4 a); no hay lista de infracciones de su vivienda. Nunca llega al tablón de anuncios |
| Las pantallas | `/infracciones/`, `…/nueva/[?caso=<id>]` y `…/<id>/` | Con el aviso de R11 en un recuadro fijo en las tres. Desde el detalle de un caso, con `infraccion.registrar`, «Registrar infracción»: el formulario sugiere las viviendas del residente que abrió el caso, pero la vivienda se elige a mano (el caso no la guarda) |

**Pruebas.** `apps/infracciones/tests.py`, las cuatro rutas en la prueba del intruso, `tests/test_infracciones.py` del front y la nota de R11 en las pantallas.

## Ver también

- [riesgos](../06_Decisiones/riesgos.md) — R11
- [legal](../01_Contexto/legal.md) — por qué el sistema no sanciona (4.2)
- [unidades](unidades.md) — a quién se notifica: propietario y arrendatario
- [eliminacion](../03_Reglas/eliminacion.md) — la anulación en vez del borrado
- [motor_reglas](motor_reglas.md) — la regla de sanción vigente que salió del catálogo

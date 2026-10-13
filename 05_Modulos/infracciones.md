---
resumen: "Registro de infracciones: el sistema notifica y registra el desenlace, no sanciona."
tipo: modulo
modulo: infracciones
hu: [HU-30]
origen: "maestro v1.4 (2026-09-14) §5.8"
actualizado: 2026-10-11
revisado: 2026-10-11
---

# Infracciones

> [!NOTE] Sin construir (verificado el 2026-10-11)
> `apps/infracciones/` solo tiene README en los dos repositorios. HU-30 está sin empezar ([historias](../08_Estado/historias.md)).

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

## Ver también

- [riesgos](../06_Decisiones/riesgos.md) — R11
- [legal](../01_Contexto/legal.md) — por qué el sistema no sanciona (4.2)
- [unidades](unidades.md) — a quién se notifica: propietario y arrendatario
- [eliminacion](../03_Reglas/eliminacion.md) — la anulación en vez del borrado
- [motor_reglas](motor_reglas.md) — la regla de sanción vigente que salió del catálogo

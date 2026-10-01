---
resumen: "Motor de reglas: invariantes, reglas alfa fijas y reglas beta configurables, y cómo evalúa una solicitud."
tipo: modulo
modulo: reglas
hu: [HU-10, HU-13]
origen: "maestro v1.4 (2026-09-14) §5.10 + guía de estructura §5.6 (2026-09-30)"
actualizado: 2026-09-30
---

# Motor de reglas

> [!WARNING] Decisiones posteriores al texto del maestro (2026-09-27)
> - Catálogo beta vigente: **7 tipos** que solo restringen (anticipación mínima, anticipación máxima, cupo por apartamento, aforo, franja horaria, días no reservables y paz y salvo), sin duración máxima ni depósito (D4 a). Provisional hasta validarlo con un reglamento real.
> - El *punto abierto* de versionado se resolvió por reemplazo: editar una regla crea una versión nueva y la evaluación se copia en la solicitud (D4 a, P10).
> - `unidad_en_mora()` devuelve `False` hasta que exista HU-35 (D5 b).
>
> Detalle en [construccion](../06_Decisiones/construccion.md).

## Diseño (maestro §5.10)

**Nivel 0 — Invariantes del sistema.** No son evaluables ni configurables; se garantizan estructuralmente. No hay dos solicitudes bloqueantes sobre la misma franja; no se reserva en el pasado; ninguna consulta cruza `conjunto_id`; no existen dos personas con el mismo documento.

**Nivel 1 — Reglas alfa.** El sistema jamás las ignora y el administrador no las desactiva. Semilla propuesta, **pendiente de cerrar**:

- Solo quien tenga vínculo vigente con `reside = true` puede solicitar a nombre de esa unidad
- Toda decisión queda trazada
- Una regla beta nunca puede relajar una alfa
- El cobro por un bien común solo procede si el reglamento lo autoriza
- La restricción por mora solo aplica a bienes comunes **no esenciales**
- Piscina: menores de 12 años requieren acompañante adulto; salvavidas en los supuestos exigidos

**Nivel 2 — Reglas beta.** Configuradas por el administrador al crear el conjunto, tomadas de su reglamento. **Catálogo de tipos parametrizados, no DSL de texto libre** — un DSL es un proyecto de semestre por sí solo.

Cada regla = tipo + parámetros + área + vigencia + `conjunto_id`. Catálogo inicial, **pendiente de validar contra un reglamento real**: anticipación mínima/máxima · duración máxima · cupo de reservas confirmadas por unidad en ventana móvil · franja horaria permitida por área y día · aforo · requiere paz y salvo · requiere depósito o pago · días no reservables.

**Todas las reglas beta son restrictivas.** Si solo restringen, se evalúan en AND y **el conflicto no existe** — el mismo criterio que llevó a que los permisos sean puramente aditivos.

Los mensajes de rechazo reportan **todas** las reglas que fallaron, no la primera.

**Punto abierto:** vigencia y versionado. Los reglamentos se reforman en asamblea, y una reserva creada bajo la versión 1 no debe romperse cuando entra la versión 2. ¿Snapshot de la versión aplicada en cada decisión?

## Cómo está construido (2026-09-30)

Cuando un residente envía una solicitud, `reglas/evaluador.py` → `evaluar(solicitud)` revisa **todas** las reglas y devuelve un resultado por cada una (no se detiene en la primera que falla, para poder decirle a la persona **todos** los motivos).

- **Reglas alfa** (`alfa.py`): están en el código, siempre activas, el administrador no las apaga. Ejemplo: "quien solicita debe residir en la unidad".
- **Reglas beta** (`catalogo.py` + modelo `Regla`): las configura el administrador por área, con 7 tipos cerrados: anticipación mínima, anticipación máxima, cupo por apartamento, aforo, franja horaria, días no reservables y paz y salvo. Son **versionadas**: cambiar una crea una versión nueva y la vieja queda para explicar decisiones pasadas.
- Todas **restringen**, ninguna permite, así que se combinan con **Y** sin conflictos.
- El resultado se **copia** en `Solicitud.evaluacion` (JSON), para que la explicación siga siendo cierta aunque la regla cambie mañana.

## Ver también

- [reservas](reservas.md) — dónde se llama al evaluador

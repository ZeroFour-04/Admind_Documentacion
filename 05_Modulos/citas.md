---
resumen: "Citas con el administrador y el cambio de horario con alternativas a los afectados."
tipo: modulo
modulo: citas
hu: [HU-31, HU-32]
origen: "maestro v1.4 (2026-09-14) §5.9"
actualizado: 2026-09-14
---

# Citas con el administrador

## Diseño (maestro §5.9)

Módulo a la medida, no reutiliza el motor de reservas (R1), pero sí el mecanismo de bloqueo compartido.

**Cambio de horario de atención:**

1. El administrador edita su horario
2. El sistema **detecta las citas que quedan fuera** y las muestra: cuántas, cuáles, de quién
3. Si hay afectadas, el guardado **exige texto de explicación** obligatorio
4. Las afectadas pasan a `CANCELADA_POR_ADMIN` con la explicación adjunta
5. El sistema notifica a cada residente con la explicación y **tres alternativas**

Las alternativas son cercanas en el tiempo, dentro del nuevo horario y libres, y se reparten **sin solaparse** entre afectados. No se bloquean: aceptar una es una reserva normal que puede fallar. El residente puede rechazar las tres y agendar libremente. **El cambio de horario no se bloquea** — bloquearlo obligaría a cancelar cita por cita a mano, que es peor y termina fuera del sistema.

## Ver también

- [riesgos](../06_Decisiones/riesgos.md) — R1

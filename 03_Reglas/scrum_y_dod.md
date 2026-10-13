---
resumen: "Scrum del equipo: sprints, eventos, la Definition of Done y las evidencias que pide el jurado."
tipo: regla
origen: "maestro v1.4 (2026-09-14) §8.1"
actualizado: 2026-10-11
revisado: 2026-10-11
---

# Scrum y Definition of Done

**Sprints de 2 semanas**, duración fija. Un semestre de 16 semanas da 6–7 sprints reales. Con sprints de 1 semana se pasa más tiempo en ceremonias que programando.

|Evento|Duración para dos personas|
|---|---|
|Sprint Planning|1–1.5 h|
|Daily|5–10 min, **escrita y asíncrona**|
|Refinement|1 h por sprint|
|Sprint Review|45 min, **demo funcionando, no diapositivas**|
|Retrospective|30 min, **1–2 acciones concretas con responsable**|

**Reglas duras:** la duración no cambia entre sprints (es lo que permite medir velocidad) · **no se agrega alcance a mitad de sprint** — lo urgente entra al backlog para el siguiente.

**La Daily escrita es mejor que la hablada** en este contexto: queda registro y sirve como evidencia ante el jurado.

**Definition of Done** — la misma para todo el proyecto:

```
Una historia está TERMINADA cuando:
- [ ] El código está en la rama `develop`
- [ ] Pasó revisión de código del otro integrante (PR aprobado)
- [ ] Cumple todos sus criterios de aceptación
- [ ] Tiene pruebas unitarias de la lógica crítica y todas pasan
- [ ] El endpoint está documentado
- [ ] No rompe funcionalidad existente
- [ ] Está desplegada en el ambiente de pruebas
- [ ] Fue probada manualmente al menos una vez por quien NO la programó
```

Sin DoD, "terminado" significa cosas distintas para cada uno y el proyecto acumula deuda invisible.

> [!WARNING] La DoD y el modelo de ramas del curso no están alineados (2026-09-11)
> La DoD dice `develop` y la ruta de aprendizaje asume una rama por historia. El modelo que fijó el profesor (§8.5) usa `main`, `desarrollo` y `pruebas`, **sin ramas por historia**.
>
> Traducción provisional, pendiente de confirmar con el profesor: el código vive en `desarrollo`, el PR revisado por el otro integrante es `desarrollo → pruebas`, y _"desplegada en el ambiente de pruebas"_ es lo que está en `pruebas`. Ver §12.7 a.

**Evidencias que se documentan desde el Sprint 1** — reconstruirlas al final es imposible y el jurado lo nota: Product Backlog con criterios y estimaciones · acta de Planning por sprint · registro de dailies · evidencia de Review · acta de Retrospective · gráfico de velocidad · burndown de al menos un sprint · DoD · historial del tablero · commits y PR vinculados a historias.

**Argumento fuerte ante el jurado:** mostrar cómo la retroalimentación de un Review **cambió** el backlog del siguiente sprint. Eso demuestra ciclo empírico, no solo bloques de dos semanas.

**Nota de vocabulario:** la Guía Scrum eliminó "Development Team" en 2020 y ahora habla de _Developers_ dentro de un único Scrum Team. Mencionar la actualización en la sustentación suma puntos.

## Ver también

- [git](git.md) — maestro §8.5
- [abiertas](../06_Decisiones/abiertas.md) — maestro §12.7
- [lista_de_salida](lista_de_salida.md) — la DoD, como lista de comprobación
- [historias](../08_Estado/historias.md) — ninguna cumple todavía la DoD
- [backlog_y_plazo](../08_Estado/backlog_y_plazo.md) — el reparto en sprints y la velocidad

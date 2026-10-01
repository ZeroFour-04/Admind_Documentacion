---
resumen: "Tabla de dos columnas: lo decidido por el equipo frente a lo propuesto sin confirmar."
tipo: decision
origen: "maestro v1.4 (2026-09-14) §13"
actualizado: 2026-09-14
---

# Qué está decidido y qué está propuesto

> [!IMPORTANT] Un agente no debe tratar estas dos columnas igual Lo de la izquierda son hechos del proyecto. Lo de la derecha son sugerencias sin confirmar por el equipo.

|Decidido por el equipo|Propuesto, sin confirmar|
|---|---|
|Documentación centralizada en Git; Drive solo para entregables congelados|Nomenclatura numerada por decenas (`01-ESTADO`, `10-PRODUCTO`, …) con la versión fuera del nombre del archivo|
|Tres repositorios hermanos; `admind-docs` **ya creado**|Quitar el prefijo `claude_` de los nombres y llevar el origen al frontmatter|
|Submódulos de Git descartados|Reparto de roles Scrum: Camilo como PO, Alejo como SM|
|Backend Django 5.2 LTS + DRF + PostgreSQL|Reparto de trabajo por **módulos verticales** en vez de por capas|
|Sprints de 2 semanas, 7 sprints, DoD escrita|Regla de revisión de PR: _"el revisor aprueba cuando puede explicar qué hace el PR"_|
|Sistema visual v1; el catálogo de 8 acentos queda **aplazado** y se arranca con uno solo (§6.3)|Monorepo como alternativa a los tres repos, si los dos repositorios no son requisito del curso|
|Todo lo de §3 (alcance), §4 (legal), §5 (diseño) y §9 (ADR)|Referenciar siempre por ID en vez de `[[enlaces]]` de Obsidian|
|**Modelo de ramas del curso**: `main`, `desarrollo` y `pruebas`, sin ramas por historia (§8.5)|Reescribir la DoD con el vocabulario de ramas del curso|
|**El proyecto espejo es la rama `lab`**, no un repositorio aparte (§7.3)|Subir la rama `lab` al remoto, por confirmar con el profesor|
|**Plazo de entrega de un mes**, sin exigir el proyecto completo (comunicado el 2026-09-14, §11)|Recorte de alcance y número de sprints para el plazo nuevo (§12.8)|
|**La IA construye lo que se le pide, con alcance exacto**, y el lab queda opcional (Alejo, 2026-09-14, §8.4 y §7.3)|Declarar formalmente el uso de IA en la documentación del curso (§8.4)|

## Ver también

- [alcance](../01_Contexto/alcance.md) — maestro §3
- [legal](../01_Contexto/legal.md) — maestro §4
- [git](../03_Reglas/git.md) — maestro §8.5
- [trabajo_con_ia](../03_Reglas/trabajo_con_ia.md) — maestro §8.4
- [sistema_visual](../04_Diseno/sistema_visual.md) — maestro §6.3
- [abiertas](abiertas.md) — maestro §12.8
- [cerradas](cerradas.md) — maestro §9
- [backlog_y_plazo](../08_Estado/backlog_y_plazo.md) — maestro §11
- [Maestro_7.3_rama_lab](../Archivo/Lab/Maestro_7.3_rama_lab.md) — maestro §7.3

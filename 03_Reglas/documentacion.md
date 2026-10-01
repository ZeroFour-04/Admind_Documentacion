---
resumen: "Cómo está organizada esta bóveda, cómo se escribe una nota y qué formato funciona en Obsidian, en GitHub y para un agente."
tipo: regla
origen: "maestro v1.4 (2026-09-14) §8.3 + reorganización del 2026-09-30"
actualizado: 2026-09-30
---

# Documentación: cómo está organizada y cómo se escribe

## Para qué está hecha así

Para que un agente de IA no tenga que leer todo el proyecto. El recorrido es: router (`AGENTS.md`) → índice (`README.md`) → las 1 a 3 notas que la tarea necesita. Cada nota es corta y trata un solo tema.

## Las carpetas

| Carpeta | Qué va | Quién la lee |
|---|---|---|
| `01_Contexto/` | Qué es el proyecto, alcance, equipo, ley, glosario | Agente, a pedido |
| `02_Arquitectura/` | Cómo está hecho el código y dónde está cada cosa | Agente, a pedido |
| `03_Reglas/` | Lo que se respeta al construir y al trabajar | Agente, antes de programar |
| `04_Diseno/` | Sistema visual | Agente, al tocar pantallas |
| `05_Modulos/` | Reglas de negocio de cada módulo, con su estado en el código | Agente, al tocar ese módulo |
| `06_Decisiones/` | Decisiones cerradas, abiertas y tomadas al construir; riesgos | Agente, ante una duda de decisión |
| `07_Planes/` | Planes de trabajo: `activos/` y `hechos/` | Agente, si ejecuta un plan |
| `08_Estado/` | Cómo va el proyecto: estado, historias, pendientes, bitácora | Agente, a pedido |
| `09_Protocolos/` | Pasos de las tareas que se repiten y sus plantillas | Agente, cuando se pide esa tarea |
| `Guias/` | Tutoriales largos para personas, con fecha de corte | Personas |
| `Archivo/` | Fotos fechadas, informes al docente, lab, notas | Nadie, salvo que se pida |
| `Credenciales/` | Claves y usuarios de prueba | Solo el equipo |

Los nombres de carpetas y notas van sin espacios ni tildes, para que los enlaces no lleven `%20` y funcionen igual en la terminal.

## Reglas para escribir

1. **Una sola fuente por tema.** Si algo ya está en una nota, se enlaza; no se copia. Los routers apuntan, no resumen.
2. **Notas cortas.** Como máximo unas 250 líneas. Si una crece más, se parte en dos y se actualiza el índice.
3. **Frontmatter mínimo en cada nota:**

   ```yaml
   ---
   resumen: "Una frase: qué tiene la nota."
   tipo: contexto | arquitectura | regla | diseno | modulo | decision | plan | estado | protocolo
   origen: "de dónde salió el contenido"
   actualizado: AAAA-MM-DD
   ---
   ```

   Las notas de módulo llevan además `modulo:` y `hu:`. `actualizado` es la fecha del contenido, no la del último retoque de formato.
4. **Toda nota nueva entra al índice** (`README.md`) con una línea.
5. **Lo que se afirme del código se verifica** en el repositorio antes de escribirlo. Resumen conciso, nunca un volcado de código.
6. **Una decisión nueva no reescribe el diseño en silencio.** Se registra en [construccion](../06_Decisiones/construccion.md) y se avisa con un recuadro al inicio de la nota que contradice. Reescribir el texto de diseño lo decide el equipo.
7. **Lo fechado no se edita.** Las fotos de avance y los informes de `Archivo/` se dejan como quedaron; el siguiente corte es un archivo nuevo.
8. **Sin contraseñas, tokens ni valores de `.env`** fuera de `Credenciales/`.

Cómo se mantiene al día: [actualizar_contexto](../09_Protocolos/actualizar_contexto.md).

## Enlaces

- **Enlaces markdown con ruta relativa**: `[reservas](../05_Modulos/reservas.md)`. Funcionan en Obsidian (alimentan el grafo), en GitHub y para un agente, que los abre sin buscar. En Obsidian: Ajustes → Archivos y enlaces → desactivar *Usar [[Wikilinks]]* y elegir *Ruta relativa al archivo*.
- Los `[[enlaces]]` de Obsidian no funcionan en GitHub. Solo quedan en los informes ya entregados de `Archivo/`.
- Para citar algo estable sirve el identificador: `R12`, `HU-22`, `D3`. Se leen igual en todas partes y se resuelven en `Admin_Master.md`.
- Las rutas al código van como texto, relativas al espacio de trabajo: `Backend/Admind_Backend/apps/reservas/README.md`. No son enlaces porque están en otro repositorio.

## Para encontrar cosas sin abrir archivos

- **Quién depende de una nota:** buscar su nombre de archivo en la bóveda (por ejemplo `reservas.md`). Son los mismos enlaces que dibuja el grafo de Obsidian.
- **Filtrar por propiedad:** buscar `^tipo: modulo` o `^modulo: reservas` en el frontmatter.
- **Mini índice:** buscar `^resumen:` devuelve una línea por nota.

## Compatibilidad Obsidian ↔ GitHub (maestro §8.3)

Alejo trabaja la documentación en Obsidian, abriendo este repositorio como bóveda; Camilo la lee renderizada en GitHub.

- **Callouts:** GitHub solo renderiza `[!NOTE]`, `[!TIP]`, `[!IMPORTANT]`, `[!WARNING]` y `[!CAUTION]`. Los demás (`[!ABSTRACT]`, `[!DANGER]`, `[!TODO]`, `[!QUOTE]`) salen como cita normal. No se rompe nada, pero si se quiere paridad visual, limitarse a esos cinco.
- **Diagramas:** los bloques `mermaid` se ven en los dos.

## Sincronización con Drive

La bóveda se copia a Google Drive con el plugin *Google Drive Sync* de Obsidian, que anota los cambios **solo mientras Obsidian está abierto**. Si un agente mueve, crea o borra archivos, Obsidian tiene que estar abierto en la bóveda; después Alejo hace el *push* desde Obsidian. El comando *Reset local vault to Google Drive* pisa lo local con lo que haya en Drive: no se usa.

## Ver también

- [repositorios](../02_Arquitectura/repositorios.md) — los tres repositorios y la regla de los routers
- [trabajo_con_ia](trabajo_con_ia.md) — cómo trabaja un agente en el proyecto

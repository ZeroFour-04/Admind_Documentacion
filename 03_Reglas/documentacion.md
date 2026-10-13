---
resumen: "Cómo está organizada esta bóveda, cómo se escribe una nota, cómo se relacionan entre sí y qué formato funciona en Obsidian, en GitHub y para un agente."
tipo: regla
origen: "maestro v1.4 (2026-09-14) §8.3 + reorganización del 2026-09-30 + revisión del 2026-10-11"
actualizado: 2026-10-11
revisado: 2026-10-11
---

# Documentación: cómo está organizada y cómo se escribe

## Para qué está hecha así

Para que un agente de IA no tenga que leer todo el proyecto, y para que una persona encuentre algo siguiendo enlaces. El recorrido es: router (`AGENTS.md`) → índice (`README.md`) → las 1 a 3 notas que la tarea necesita. Cada nota es corta, trata un solo tema y termina diciendo con qué otras se relaciona.

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
| `Archivo/` | Fotos fechadas, informes al docente, lab, notas de Alejo | Nadie, salvo que se pida |
| `Credenciales/` | Claves y usuarios de prueba | Solo el equipo |

Los nombres de carpetas y notas van sin espacios ni tildes, para que los enlaces no lleven `%20` y funcionen igual en la terminal. En la raíz solo quedan los routers (`AGENTS.md`, `CLAUDE.md`), el índice (`README.md`), `Admin_Master.md` e `Inicio.md`: una nota suelta va a su carpeta o, si es un apunte, a `Archivo/Notas/`.

## Dos clases de nota

| Clase | Cuáles | Cómo se mantiene |
|---|---|---|
| **De estado** | `estado_actual`, `historias`, `pendientes`, `planes`, `pruebas_y_ejecucion`, `mapa_codigo`, `frontend` y la sección *Cómo está construido* de cada módulo | Dice **cómo es hoy**. Cuando algo cambia, se reescribe la línea; no se apila un párrafo «al día tal» debajo del anterior |
| **De registro** | `bitacora`, `construccion` y todo `Archivo/` | Una fila por hecho, con su fecha. No se reescribe: un «sin commit» en una fila es de ese día |

La historia va en las notas de registro. Una nota de estado que acumula cortes viejos deja de servir para saber cómo va el proyecto.

## Reglas para escribir

1. **Una sola fuente por tema.** Si algo ya está en una nota, se enlaza; no se copia. Los routers apuntan, no resumen.
2. **Notas cortas.** Como máximo unas 250 líneas. Si una crece más, se parte en dos y se actualiza el índice.
3. **Frontmatter en cada nota:**

   ```yaml
   ---
   resumen: "Una frase: qué tiene la nota."
   tipo: contexto | arquitectura | regla | diseno | modulo | decision | plan | estado | protocolo
   origen: "de dónde salió el contenido"
   actualizado: AAAA-MM-DD
   revisado: AAAA-MM-DD
   ---
   ```

   - **`actualizado`** es la fecha del contenido: cuándo cambió lo que la nota dice. Un retoque de formato no la mueve.
   - **`revisado`** es la última vez que la nota se contrastó con el código y con el estado del proyecto, haya cambiado o no. Una nota con `actualizado` viejo y `revisado` reciente sigue siendo cierta.
   - Las notas de módulo llevan además `modulo:` (la app) y `hu:` (sus historias). Las de estado, `corte:`.
   - Un plan lleva su propio frontmatter (`titulo`, `fecha`, `alcance`, `punto_de_partida`) más `resumen`, `estado: activo | hecho`, `ejecutado:` y `hu:`.
4. **Toda nota termina en *Ver también*:** un enlace por cada nota relacionada y, después de la raya, por qué se relaciona. Si la nota habla de código, la última línea es la ruta al `README.md` de esa carpeta.
5. **Toda nota nueva entra al índice** (`README.md`) con una línea.
6. **Lo que se afirme del código se verifica** en el repositorio antes de escribirlo. Resumen conciso, nunca un volcado de código.
7. **Una decisión nueva no reescribe el diseño en silencio.** Se registra en [construccion](../06_Decisiones/construccion.md) y se avisa con un recuadro al inicio de la nota que contradice. Reescribir el texto de diseño lo decide el equipo.
8. **Lo fechado no se edita.** Las fotos de avance, los informes de `Archivo/` y los planes de `07_Planes/hechos/` se dejan como quedaron; el siguiente corte es un archivo nuevo. La excepción es el frontmatter y un enlace que se rompa al mover un archivo.
9. **Sin contraseñas, tokens ni valores de `.env`** fuera de `Credenciales/`.

Cómo se mantiene al día: [actualizar_contexto](../09_Protocolos/actualizar_contexto.md).

## Cómo se relacionan las notas

Las relaciones están escritas en cuatro sitios, y con ellos se llega de cualquier punto a cualquier otro:

| Desde | Hacia | Dónde está |
|---|---|---|
| Una historia (`HU-16`) | Su módulo, su plan y lo que le falta | [historias](../08_Estado/historias.md) |
| Una app del código (`reservas`) | Sus endpoints, su historia y su nota | [mapa_codigo](../02_Arquitectura/mapa_codigo.md) |
| Un identificador (`R12`, `D3`, *maestro §5.4*) | La nota donde vive | `Admin_Master.md` |
| Una nota | Las notas vecinas | Su sección *Ver también* |

## Enlaces

- **Enlaces markdown con ruta relativa**: `[reservas](../05_Modulos/reservas.md)`. Funcionan en Obsidian (alimentan el grafo), en GitHub y para un agente, que los abre sin buscar. En Obsidian: Ajustes → Archivos y enlaces → desactivar *Usar Wikilinks* y elegir *Ruta relativa al archivo*.
- Los enlaces de doble corchete de Obsidian no funcionan en GitHub. Solo quedan en los informes ya entregados de `Archivo/`.
- Para citar algo estable sirve el identificador: `R12`, `HU-22`, `D3`. Se leen igual en todas partes y se resuelven en `Admin_Master.md`.
- Las rutas al código van como texto, relativas al espacio de trabajo: `Backend/Admind_Backend/apps/reservas/README.md`. No son enlaces porque están en otro repositorio.
- **Al mover o renombrar una nota** se buscan y corrigen sus enlaces en toda la bóveda, también dentro de la nota movida.

## Para encontrar cosas sin abrir archivos

- **Quién depende de una nota:** buscar su nombre de archivo en la bóveda (por ejemplo `reservas.md`). Son los mismos enlaces que dibuja el grafo de Obsidian.
- **Filtrar por propiedad:** buscar `^tipo: modulo`, `^modulo: reservas` o `HU-16` dentro de `^hu:` en el frontmatter.
- **Mini índice:** buscar `^resumen:` devuelve una línea por nota.
- **Qué no se ha revisado hace tiempo:** buscar `^revisado:` y ordenar por fecha.

## Compatibilidad Obsidian ↔ GitHub (maestro §8.3)

Alejo trabaja la documentación en Obsidian, abriendo este repositorio como bóveda; Camilo la lee renderizada en GitHub.

- **Callouts:** GitHub solo renderiza `[!NOTE]`, `[!TIP]`, `[!IMPORTANT]`, `[!WARNING]` y `[!CAUTION]`. Los demás (`[!ABSTRACT]`, `[!DANGER]`, `[!TODO]`, `[!QUOTE]`) salen como cita normal. No se rompe nada, pero si se quiere paridad visual, limitarse a esos cinco.
- **Diagramas:** los bloques `mermaid` se ven en los dos.

## Sincronización con Drive

La bóveda se copia a Google Drive con el plugin *Google Drive Sync* de Obsidian, que anota los cambios **solo mientras Obsidian está abierto**. Si un agente mueve, crea o borra archivos, Obsidian tiene que estar abierto en la bóveda; después Alejo hace el *push* desde Obsidian. El comando *Reset local vault to Google Drive* pisa lo local con lo que haya en Drive: no se usa.

## Ver también

- [actualizar_contexto](../09_Protocolos/actualizar_contexto.md) — qué nota se toca cuando cambia algo
- [nota](../09_Protocolos/Plantillas/nota.md) — la plantilla de una nota nueva
- [repositorios](../02_Arquitectura/repositorios.md) — los tres repositorios y la regla de los routers
- [trabajo_con_ia](trabajo_con_ia.md) — cómo trabaja un agente en el proyecto
- [Admin_Master](../Admin_Master.md) — la tabla de equivalencias de identificadores

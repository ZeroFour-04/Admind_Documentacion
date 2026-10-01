---
resumen: "Lista de comprobación antes de dar algo por terminado: código, pruebas, pantalla y proceso."
tipo: regla
origen: "guía de desarrollo §9 (2026-09-15)"
actualizado: 2026-09-15
---

# La lista de salida

Antes de decir "terminé", repasa esto. Mezcla la Definition of Done (maestro §8.1), las dos pruebas obligatorias del aislamiento (maestro §5.4) y la DoD visual (maestro §6.6).

**El código**

- [ ] Cada capa hace solo su trabajo: la vista no consulta y el servicio no conoce HTTP ([capas](capas.md))
- [ ] Ninguna ruta ni cuerpo acepta `conjunto_id`
- [ ] Todo identificador expuesto es UUID
- [ ] Toda tabla nueva tiene conjunto, o está en la lista cerrada de globales
- [ ] Ninguna FK con `CASCADE` y ninguna operación de borrado sobre las entidades del maestro §5.11
- [ ] La vista declara el permiso que exige
- [ ] Toda escritura deja auditoría (cuando exista `apps/auditoria/`)
- [ ] Los errores no llevan datos de la fila: "No encontrado"

**Las pruebas**

- [ ] Cada criterio de aceptación tiene su prueba, y todas pasan
- [ ] Prueba del intruso: un recurso de otro conjunto responde 404
- [ ] `python manage.py makemigrations --check` responde `No changes detected`
- [ ] La probó a mano al menos una vez **quien no la programó**

**La pantalla**

- [ ] Todo texto pasa 4.5:1 contra su fondo; textos grandes, 3:1
- [ ] Ningún estado se comunica solo con color: siempre hay texto
- [ ] El foco se ve y la pantalla se recorre con `Tab`
- [ ] Toda área táctil mide al menos 44×44px
- [ ] Se usa bien a 200 % de zoom y a 360px de ancho
- [ ] No hay hex en plantillas ni en `static/css/`, y `--acento-*` no aparece en reglas de estado
- [ ] Todo campo tiene `label`; el `placeholder` no hace de etiqueta

**El proceso**

- [ ] Commits en `desarrollo` con el formato `tipo(app): descripción [HU-XX]`, y `git status` sin `.env` ni `.venv`
- [ ] Documentación actualizada con [actualizar_contexto](../09_Protocolos/actualizar_contexto.md), y la historia movida en Notion
- [ ] **Puedes explicar en voz alta qué hace cada archivo que tocaste**

> [!WARNING]
> **Abierto — la DoD y las ramas no están alineadas (maestro §12.7 a).** La DoD pide PR aprobado y "desplegada en el ambiente de pruebas", pero todavía no se decidió qué PR cuenta como revisión ni qué es exactamente la rama `pruebas`. Mientras tanto, esa parte de la DoD queda pendiente y **una historia no se marca Terminada en el Avance** sin cumplirla completa.

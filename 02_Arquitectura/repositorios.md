---
resumen: "Los tres repositorios hermanos, por qué no submódulos y la regla de los routers."
tipo: arquitectura
origen: "maestro v1.4 (2026-09-14) §8.2 + nombres reales verificados el 2026-09-30"
actualizado: 2026-09-30
---

# Repositorios y documentación

> [!NOTE] Nombres reales
> El texto del maestro usa nombres de trabajo (`admind-api`, `admind-web`, `admind-docs`). Los reales son:
>
> | Repositorio (GitHub `ZeroFour-04`) | Carpeta local | Rama de trabajo |
> |---|---|---|
> | `Admind_Backend` | `Backend/Admind_Backend` | `desarrollo` |
> | `Admind_Front-End` | `Frontend/Admind_Front-End` | `desarrollo` |
> | `Admind_Documentacion` | `Documentacion/Admind_Documentacion` | `main` |
>
> Los routers existen desde el 2026-09-30: `AGENTS.md` completo en la documentación y uno corto en cada repositorio de código.

**Decidido por el equipo:** toda la documentación se centraliza en Git. **Google Drive queda solo para entregables congelados** que el docente exige en Excel o Word — artefactos, no fuentes.

Razón: una segunda fuente en Drive produce divergencia silenciosa (Drive no resuelve conflictos, crea `archivo (1).md`), pierde el versionado junto al código, y un agente de IA no puede leerla.

**Estructura: tres repositorios hermanos, no submódulos.**

```
AdMind/
├─ admind-api/          repo 1 — backend
├─ admind-web/          repo 2 — frontend
└─ admind-docs/         repo 3 — documentación   [ya creado]
```

Se descartaron los submódulos de Git a pesar de resolver bien la sincronización, por costo operativo: un `pull` **no** actualiza el submódulo (requiere `git submodule update`), editar una línea son cuatro operaciones de Git repetidas en dos repos padre, y los submódulos se clonan en _detached HEAD_, donde un commit hecho sin checkout previo queda huérfano y desaparece. Para un equipo donde uno de los dos apenas arranca con Git, es una trampa.

**Cómo funciona en la práctica:** tres clones hermanos. Actualizar documentación es el mismo flujo que cualquier repo — rama, commit, push. El agente de IA se abre apuntando a `AdMind/` y ve los tres al tiempo.

**Lo que se pierde frente al submódulo:** la documentación no queda clavada a un commit de código. Se resuelve mirando fechas y commits.

**Routers.** `AGENTS.md` en los tres repos: completo en `admind-docs`, y en los otros dos unas líneas que apuntan a `../admind-docs/`. `CLAUDE.md` es una línea que apunta a `AGENTS.md` — no se hace un archivo por herramienta.

**Regla de los routers:** **apuntan, no resumen.** En el momento en que un router contenga contenido de dominio, hay una segunda fuente de verdad que nadie va a actualizar, y el agente le creerá a la que tiene más cerca.

## Ver también

- [documentacion](../03_Reglas/documentacion.md) — cómo está organizada esta bóveda

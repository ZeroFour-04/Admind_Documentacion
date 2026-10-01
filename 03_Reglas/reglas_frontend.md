---
resumen: "Qué va en cada carpeta del frontend, lo que nunca hace cada una y las reglas visuales que no se rompen."
tipo: regla
origen: "guía de desarrollo §4.1 y §4.3 (2026-09-15)"
actualizado: 2026-09-15
---

# Reglas del frontend

> [!NOTE] Corte de este texto: 2026-09-15
> Resuelto después: el proyecto Django del front ya existe; la identidad viaja como token ([cuentas](../05_Modulos/cuentas.md)); el acento por conjunto está activo (8 acentos o color propio), así que *un solo acento, sin `data-acento`* ya no rige ([sistema_visual](../04_Diseno/sistema_visual.md)).

## El mapa

| Carpeta | Qué va | Lo que nunca hace |
|---|---|---|
| `config/` | El proyecto Django del servidor web. La dirección de la API sale de una variable de entorno | Conectarse a la base de AdMind |
| `apps/<módulo>/urls.py` y `views.py` | Una vista por pantalla: pide los datos a `cliente_api` y elige la plantilla | Armar URLs de la API por su cuenta |
| `apps/<módulo>/templates/<módulo>/` | Las plantillas de las pantallas de ese módulo | Escribir colores en hex |
| `cliente_api/` | El único lugar que sabe que la API existe. Una función por endpoint, agrupadas por módulo. Traduce los errores (un 404 se muestra como "No encontrado") | Enviar `conjunto_id` |
| `templates/base/` | La estructura de toda página: `<head>`, barra superior, lateral, zona de contenido y páginas de error | — |
| `templates/componentes/` | Los diez componentes del sistema de diseño como fragmentos de plantilla | Crecer: el inventario es cerrado |
| `static/css/` | Estilos propios de pantallas, **solo con variables** | Crear tokens o colores nuevos |
| `static/js/` | Alpine.js para lo que no se resuelve con HTML y una recarga. Alpine va autoalojado en `vendor/` | Decidir reglas: si una franja está libre o si un bloqueo venció lo decide la API |
| `design-system/` | Tokens, fuentes y CSS importados de Claude Design | Editarse a mano |

## Reglas del frontend

**Decidido.** Cada una con su fuente:

- **Ningún hex fuera de `design-system/tokens/paleta.css`**, y ningún token nuevo en `static/css/` (maestro §6.6).
- **Un solo acento por ahora**, sin `data-acento` (maestro §6.3).
- **El acento aparece en cuatro sitios y en ninguno más:** botón primario, ítem activo del lateral y pestaña seleccionada, anillo de foco y franja del conjunto activo (maestro §6.1). Un quinto sitio es un error, no una variante.
- **Acción y estado no comparten forma.** Botón: relleno sólido y verbo (`Confirmar reserva`). Pastilla: fondo suave y participio (`Confirmada`). Nunca al revés (maestro §6.1).
- **El inventario de componentes es cerrado:** `Boton`, `Campo`, `Pastilla`, `EstadoVacio`, `Modal`, `Tabla`, `Tesela`, `BarraSuperior`, `Lateral` y `Pestanas`. Un componente nuevo es decisión de equipo.
- **El bento solo va en tres paneles:** inicio de Administración, inicio de Residente y panel de Vigilancia (maestro §6.4).
- **Todo autoalojado**, fuentes y Alpine incluidos. Nada desde un CDN: le entregaría la IP de cada residente a un tercero (Ley 1581, maestro §6.2).
- **La voz de la interfaz:** verbo activo en botones, errores que dicen qué pasó y qué hacer, estados vacíos que invitan, fechas con el día de la semana en letras, sin emoji (maestro §6.5 y README de `design-system/`).

> [!IMPORTANT]
> **Abierto.**
> - **Sesión o token (maestro §12.7 b):** cómo le dice `cliente_api` a la API quién es el usuario. Es la decisión que más afecta a esa carpeta.
> - **`design-system/` o el §6 del maestro:** fuentes (Archivo + Inter o solo Inter), radios (4px o 6px) y ruta de los tokens. Mientras tanto se usa lo que ya está en `design-system/`.
> - **El proyecto Django del frontend todavía no existe.** Antes de la primera pantalla hay que crearlo.

## Ver también

- [frontend](../02_Arquitectura/frontend.md) — cómo está construido hoy
- [sistema_visual](../04_Diseno/sistema_visual.md) — los principios y tokens que citan estas reglas

---
resumen: "Estilo del código, nombres, terminal y la lista de lo que no se toca ni se instala sin preguntar."
tipo: regla
origen: "plan de los Sprints 2 y 3 §0.2 (2026-09-27) + Avance 22092026 §0 (2026-09-22)"
actualizado: 2026-09-27
---

# Convenciones de código y de trabajo

Estas reglas se escribieron para el plan de los Sprints 2 y 3 y para la foto de avance del 22/09. Son las que sigue el código que ya existe.

## Estilo

- **Todo en español:** nombres, docstrings y mensajes.
- El archivo de servicios se llama `servicios.py`, no `services.py`.
- La vista valida, exige su permiso y llama al servicio. El servicio no conoce HTTP. Las excepciones de dominio viven en `servicios.py`.
- Docstrings cortos que citan el maestro o la historia: `(maestro §5.1, HU-11)`.
- La misma densidad de comentarios que el código vecino.
- **El modelo de estilo es el código que ya existe.** En el backend: `apps/anuncios/`, `apps/unidades/`, `apps/conjuntos/servicios.py` y `tests/aislamiento/test_intruso.py`. En el front: `apps/anuncios/`, `cliente_api/anuncios.py` y `tests/test_anuncios.py`.

## Terminal

- **Git Bash**, con sintaxis POSIX y rutas entre comillas: la carpeta raíz tiene espacios (`A D M I N D`).
- Los comandos de verificación están en [pruebas_y_ejecucion](../02_Arquitectura/pruebas_y_ejecucion.md).
- **No se sigue con la suite en rojo.** Si algo falla, se arregla antes de continuar.

## Lo que no se toca sin preguntarle a Alejo

- `config/settings_pruebas.py`: el cifrado rápido de contraseñas es una decisión suya y es provisional.
- `ModeloDeConjunto`, `Persona`, `Usuario` y el catálogo de `apps/permisos/catalogo.py`: los usa todo el sistema.
- `design-system/`: se importa de Claude Design. Los acentos por conjunto se agregaron a la copia local; una re-sincronización sin llevarlos allá primero los borra.
- `Backend.zip`: es la demo descartada. No se abre ni se usa como referencia.

## Lo que no se hace sin confirmación

- **Instalar o descargar algo.** Ni paquetes de `requirements.txt` ni librerías del front. Tampoco dependencias nuevas de pruebas (`freezegun`, `factory_boy`).
- **`git push`**, ramas nuevas o `--no-verify`. Se trabaja en `desarrollo` ([git](git.md)).
- **Aplicar migraciones en `admind_db`**, salvo que el pedido o el plan lo autoricen.
- **Tocar Notion.** Si una historia cambia de estado, se le avisa a Alejo.

## Ver también

- [invariantes](invariantes.md) — lo que toda pieza nueva respeta
- [trabajo_con_ia](trabajo_con_ia.md) — el alcance exacto del pedido y qué se pregunta

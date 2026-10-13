# AdMind — router para agentes de IA

AdMind es una aplicación web para administrar conjuntos residenciales en Colombia (Ley 675 de 2001). Proyecto de semestre de dos personas, Alejo y Camilo, con entrega cerca del 2026-10-21 (el profesor la amplió una semana el 2026-10-13) y sustentación ante jurado.

**Este archivo solo enruta.** Toda la documentación vive en esta carpeta (`Admind_Documentacion/`, una bóveda de Obsidian) y las rutas de abajo son relativas a ella.

## Espacio de trabajo

Tres repositorios hermanos dentro de `A D M I N D/` (la carpeta tiene espacios: rutas entre comillas, terminal Git Bash).

| Repositorio | Carpeta | Rama de trabajo |
|---|---|---|
| Backend: API con Django + DRF + PostgreSQL, puerto 8000 | `Backend/Admind_Backend` | `desarrollo` |
| Frontend: plantillas de Django + Alpine.js, puerto 8001 | `Frontend/Admind_Front-End` | `desarrollo` |
| Documentación: esta bóveda | `Documentacion/Admind_Documentacion` | `main` |

## Flujo de toda tarea

1. Lee `README.md`: es el índice, con una línea por nota.
2. Abre **solo** las notas que la tarea necesita (lo normal son 1 a 3) y el `README.md` de la carpeta de código que vas a tocar. No recorras la bóveda.
3. Haz la tarea.
4. Si cambiaste código, una decisión o el estado del proyecto, sigue `09_Protocolos/actualizar_contexto.md`.

## Qué leer según la tarea

| Vas a… | Lee |
|---|---|
| Tocar el código de un módulo | `02_Arquitectura/mapa_codigo.md` → `05_Modulos/<módulo>.md` → `03_Reglas/invariantes.md` |
| Crear una tabla, un endpoint o una pantalla | Además `03_Reglas/capas.md`, `03_Reglas/aislamiento.md` y `03_Reglas/reglas_frontend.md` |
| Correr los servidores o las pruebas | `02_Arquitectura/pruebas_y_ejecucion.md` |
| Saber cómo va el proyecto | `08_Estado/estado_actual.md` |
| Trabajar una historia (HU-NN) | `08_Estado/historias.md`: su estado, la nota de su módulo, su plan y lo que le falta |
| Saber qué falta (pruebas manuales, avisos, lo legal, deuda) | `08_Estado/pendientes.md`, ordenada por tipo |
| Algo que suene a decisión de equipo | `06_Decisiones/abiertas.md` y `06_Decisiones/construccion.md` |
| Un informe de avance, una foto de avance o un plan | `09_Protocolos/` |
| Resolver una cita como *maestro §5.4*, *R12* o *decisión 24* | `Admin_Master.md`, que es la tabla de equivalencias |

## Reglas que no se saltan

- **Construye solo lo que te piden**, con el alcance exacto. Lo que falte fuera del pedido se avisa y no se hace: `03_Reglas/trabajo_con_ia.md`.
- **No decides por el equipo.** Contradicciones abiertas, recorte de alcance, roles, permisos y tablas globales se preguntan: `06_Decisiones/abiertas.md`.
- **La ley manda sobre todo lo demás**: `01_Contexto/legal.md`. Lo prohibido no se programa como permiso denegado; la operación no existe.
- **Git:** ramas `main`, `desarrollo` y `pruebas`, sin ramas por historia. Sin `push` ni commits que no te pidan: `03_Reglas/git.md`.
- **Si una nota y el código no coinciden, manda el código.** Avisa y corrige la nota.
- **Nada se instala ni se descarga** sin que Alejo lo confirme. `config/settings_pruebas.py` no se toca sin preguntarle.

## Lo que no se lee salvo que te lo pidan

- `Archivo/`: fotos fechadas, informes al docente, lab y notas sueltas. Es histórico y puede contradecir lo vigente.
- `Guias/`: tutoriales largos escritos para personas, con fecha de corte.
- `Credenciales/`: no se abre ni se copia su contenido a ningún lado.
- `Backend.zip`, en la raíz del espacio de trabajo: es una demo descartada.

## Comandos

Desde `Backend/Admind_Backend`:

```bash
./.venv/Scripts/python.exe -m pytest -q
./.venv/Scripts/python.exe manage.py makemigrations --check --dry-run
./.venv/Scripts/python.exe manage.py runserver 8000
```

Desde `Frontend/Admind_Front-End`:

```bash
./.venv/Scripts/python.exe -m pytest -q
./.venv/Scripts/python.exe manage.py runserver 8001
```

---
resumen: "Ramas del curso (main, desarrollo, pruebas, sin ramas por historia), formato de commit y rutina diaria."
tipo: regla
origen: "maestro v1.4 (2026-09-14) §8.5 + guía de desarrollo §10 (2026-09-15)"
actualizado: 2026-09-15
---

# Git: ramas, commits y día a día

> [!NOTE] Estado de las ramas al 2026-09-30
> En GitHub el backend **no tiene rama `pruebas`** (existe solo en local) y en el front existe pero igual a `main`. Ninguna historia ha pasado por un PR `desarrollo → pruebas`.

## Modelo de ramas — requisito del curso (maestro §8.5)

**Definido por el profesor y comunicado el 2026-09-11.** Inicialmente hay tres ramas y ninguna más:

|Rama|Qué contiene|
|---|---|
|`main`|Lo entregado. Recibe de `pruebas` al cerrar el sprint|
|`desarrollo`|Integración. **Los dos integrantes trabajan directamente aquí**|
|`pruebas`|Lo terminado, listo para probar. Es el ambiente de pruebas que exige la DoD|

**No hay ramas por historia.** El equipo sabe que son el estándar de la industria; la instrucción del curso manda. La palabra _inicialmente_ deja la puerta abierta a revisarlo más adelante.

**Lo que hay que compensar al compartir una rama** — es la disciplina del desarrollo sobre tronco común, no un modelo peor:

- `pull` antes de empezar y antes de subir, y subir al menos una vez al día. Guardar trabajo local durante días es lo que hace doler este modelo
- **Nunca subir `desarrollo` roto**: las pruebas en verde antes del `push`. Lo que uno rompe, se lo rompe al otro
- **La trazabilidad pasa al mensaje del commit**, que es donde vive el ID de la historia: `feat(reservas): agregar bloqueo de 3 minutos [HU-11]`. La evidencia que pide §8.1 —_commits y PR vinculados a historias_— se sostiene por ahí
- Repartirse por módulo para no tocar los mismos archivos al mismo tiempo, y coordinarlo en la Daily
- **Limitación aceptada:** un PR `desarrollo → pruebas` arrastra todo lo que haya en `desarrollo`, incluido lo que el otro dejó a medias. Por eso a `desarrollo` solo sube lo que no rompe nada, y la promoción se acuerda entre los dos

**Cuarta rama, solo de Alejo: `lab`.** Práctica y ejercicios. Nunca se fusiona hacia arriba; `desarrollo` sí puede bajar al lab. Pendiente confirmar con el profesor si acepta que exista en el remoto. Ver `Archivo/Lab/`.

**Protección sugerida:** `main` y `pruebas` exigen PR con una aprobación; `desarrollo` queda abierta. En repositorios privados esa opción requiere GitHub Pro, gratis con el GitHub Student Developer Pack.

## Día a día (guía de desarrollo §10)

### Al sentarte

```bash
source .venv/Scripts/activate
```
```bash
git switch desarrollo
```
```bash
git pull
```

Si el `pull` trajo cambios en `requirements.txt`, reinstala; si trajo migraciones nuevas, corre `migrate`.

### Mientras trabajas

- **Commit apenas algo funcione.** Ya pasó que se sobrescribió `apps/personas/models.py` sin que estuviera en ningún commit, y Git no podía devolverlo.
- **Un commit, un paso con sentido.** Mejor cuatro pequeños (modelo, repositorio y servicio, vista, pantalla) que uno gigante que nadie puede revisar.
- **El modelo y su migración van en el mismo commit.**
- **Repártanse por módulo** para no tocar los mismos archivos a la vez, y coordínenlo en la Daily.
- **No hay ramas por historia** (requisito del curso, maestro §8.5). La trazabilidad va en el mensaje del commit.
- **La rama `lab` nunca sube.** Lo que funcione ahí se vuelve a construir en `desarrollo` (`Archivo/Lab/Admind_Lab.md` §3).

### Mensajes de commit

Formato: `tipo(app): qué hace, en presente [HU-XX]` (maestro §8.4).

| Tipo | Cuándo | Ejemplo |
|---|---|---|
| `feat` | Funcionalidad nueva | `feat(areas): listar áreas del conjunto activo [HU-09]` |
| `fix` | Corrige un error | `fix(areas): responder 404 cuando el área es de otro conjunto [HU-05]` |
| `test` | Solo pruebas | `test(personas): documento duplicado produce una sola persona [HU-04]` |
| `refactor` | Cambia la forma sin cambiar el comportamiento | `refactor(areas): mover la consulta de la vista al repositorio [HU-09]` |
| `docs` | README o documentación | `docs(areas): actualizar pendientes del README` |
| `chore` | Configuración o dependencias | `chore: instalar pytest-django` |

### Antes de subir

1. Las pruebas en verde. **Nunca se sube `desarrollo` roto**: lo que uno rompe, se lo rompe al otro (maestro §8.5).
2. `git status`: que no aparezcan `.env` ni `.venv`.
3. `git pull` otra vez, y si hay conflicto, resolverlo en tu máquina.
4. `git push`.

## Ver también

- [scrum_y_dod](scrum_y_dod.md) — maestro §8.1
- [Maestro_7.3_rama_lab](../Archivo/Lab/Maestro_7.3_rama_lab.md) — maestro §7.3

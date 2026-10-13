---
resumen: "Parqueaderos de residentes asignados a un apartamento y de visitantes atados a la visita."
tipo: modulo
modulo: parqueaderos
hu: [HU-27, HU-28, HU-34]
origen: "maestro v1.4 (2026-09-14) §5.6"
actualizado: 2026-10-11
revisado: 2026-10-11
---

# Parqueaderos

> [!NOTE] HU-28 construida el 2026-10-10, con commit (`f4c8ae6` y `49c3e80`) y migrada; HU-34 sigue sin empezar
> - **Está construido** el catálogo de parqueaderos y la ocupación de uno de visitantes por una visita ([Plan_Parqueadero_De_Visitantes](../07_Planes/hechos/Plan_Parqueadero_De_Visitantes.md)). **No existe** `AsignacionParqueadero` ni ninguna operación que asigne un parqueadero a una unidad: es de HU-34, y para los de visitantes no existirá nunca.
> - Los parqueaderos son **puestos con código** que crea Administración (D2 a); el vigilante elige uno de los libres al registrar una visita con vehículo (D4 a). La ocupación **no es una tabla**: es el parqueadero de la visita mientras no tenga salida.
> - Alejo decidió D3 a (permiso nuevo `parqueadero.gestionar`), D5 a (cualquier visita con vehículo puede ocupar uno), D6 a y D7 a (lo de más de N horas y la Ley 1581 en portería, fuera) y D8 a (`migrate` lo corre él).

## Diseño (maestro §5.6)

**Un parqueadero se asigna a un apartamento.** Sin regímenes jurídicos, sin origen documental, sin advertencias legales. El sistema registra un hecho administrativo, no constituye un derecho.

```
Parqueadero                    AsignacionParqueadero
  conjunto_id                    parqueadero_id
  codigo                         unidad_id
  tipo ∈ {residentes,            vigencia_desde
          visitantes}            vigencia_hasta   (nullable)
  accesible : bool               registrado_por
  notas
```

Un parqueadero de residentes tiene **una asignación vigente a la vez**. Cerrarla es poner `vigencia_hasta`, nunca borrar: el historial responde "¿desde cuándo parquea ahí?" dos años después.

**Parqueaderos de visitantes.** No se asignan a una unidad. Su ocupación es **temporal y pertenece a la visita**, y termina al registrar la salida. `AsignacionParqueadero` no los admite: el tipo no aparece en el selector, **no es un permiso denegado sino una operación inexistente**.

**Límite duro:** no se puede quitar el parqueadero a un residente moroso ni como sanción. El sistema no tiene ninguna operación de restricción de uso, así que no hay dónde escogerlo.

## Cómo está construido (2026-10-10)

```mermaid
sequenceDiagram
    actor V as Vigilante
    participant F as Front (8001)
    participant A as API (8000)
    participant DB as PostgreSQL

    V->>F: abre /visitantes/
    F->>A: GET /parqueaderos/?tipo=visitantes&libres=1
    A-->>F: [V-01, V-03] (o lista vacía)
    V->>F: registra la visita con vehículo y elige V-03
    F->>A: POST /visitantes/ {..., parqueadero: id}
    A->>DB: bloquea la fila del parqueadero, INSERT Visitante (bloqueo.tomar)
    Note over A,DB: si otra visita lo ocupó antes, el índice único parcial lo rechaza → 409
    V->>F: «Registrar salida» y confirma
    F->>A: POST /visitantes/<id>/salida/
    A->>DB: UPDATE hora_salida: la fila sale del índice y V-03 queda libre
```

| Qué | Dónde | Cómo |
|---|---|---|
| El catálogo | `apps/parqueaderos/` | `Parqueadero`: `codigo` (único por conjunto, en mayúsculas), `tipo`, `accesible`, `notas`, `activo`. `GET` y `POST /parqueaderos/`, `POST /parqueaderos/<id>/desactivar/` (baja lógica; ocupado, 409) |
| Quién | `parqueadero.gestionar` (nuevo, Administración) crea y retira; `parqueadero.ver`, `parqueadero.gestionar` o `visitante.registrar` listan | `?tipo=` y `?libres=1`. Cada puesto dice si está `ocupado`, no por quién |
| La ocupación | `Visitante.parqueadero` (FK nula) y el índice único parcial `visitante_parqueadero_ocupado_unico` | Único por `(conjunto, parqueadero)` mientras `hora_salida IS NULL`. Se escribe y la base acepta a una sola; no se pregunta antes |
| La salida | `visitantes/servicios.registrar_salida` | `hora_salida` y quién la registró; el puesto queda libre al instante. Dos veces, 409 |
| El orden de los bloqueos | `registrar_ingreso` y `desactivar` | Toman la fila del parqueadero con `select_for_update`: no se retira un puesto justo cuando una visita entra |
| La auditoría | `parqueadero.crear`, `parqueadero.desactivar`, `visitante.registrar`, `visitante.salida` | El registro de la visita guarda unidad, si traía vehículo y el parqueadero; no el nombre ni la cédula |

**Lo que no existe.** Ninguna ruta, función ni campo asigna un parqueadero a una unidad (`apps/parqueaderos/tests.py` recorre las rutas y el modelo). Un parqueadero de `residentes` se crea en el catálogo pero este plan no hace nada más con él: en la pantalla dice «Sin asignar».

**Pruebas.** `apps/parqueaderos/tests.py`, `apps/visitantes/test_visitantes.py` (los cinco criterios de HU-28 y la salida), `tests/concurrencia/test_parqueadero_de_visitantes.py` (diez registros sobre un mismo puesto: uno lo obtiene y las otras nueve no) y las tres rutas registradas en la prueba del intruso.

## Ver también

- [legal](../01_Contexto/legal.md) — un parqueadero de visitantes no se destina a una unidad (4.2)
- [unidades](unidades.md) — la unidad a la que se asignará uno de residentes (HU-34)
- [ingresos](ingresos.md) — el otro registro que hace Vigilancia
- [backend](../02_Arquitectura/backend.md) — el mecanismo de bloqueo compartido
- [restricciones_bd](../02_Arquitectura/restricciones_bd.md) — el índice que deja a una sola visita con el puesto
- [Plan_Parqueadero_De_Visitantes](../07_Planes/hechos/Plan_Parqueadero_De_Visitantes.md) — el plan con que se construyó
- [historias](../08_Estado/historias.md) — HU-27, HU-28 y HU-34
- `Backend/Admind_Backend/apps/parqueaderos/README.md` y `apps/visitantes/README.md`

---
resumen: "Parqueaderos de residentes asignados a un apartamento y de visitantes atados a la visita."
tipo: modulo
modulo: parqueaderos
hu: [HU-28, HU-34]
origen: "maestro v1.4 (2026-09-14) §5.6"
actualizado: 2026-09-14
---

# Parqueaderos

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

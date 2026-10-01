---
resumen: "Invariantes de eliminación: sin borrado físico, baja lógica, auditoría de solo inserción y anulación."
tipo: regla
origen: "maestro v1.4 (2026-09-14) §5.11"
actualizado: 2026-09-14
---

# Invariantes de eliminación

El equipo también se equivoca. Ninguno de estos depende de que alguien recuerde validarlo.

|Invariante|Dónde|Cómo|
|---|---|---|
|**No hay borrado físico** de personas, unidades, reservas, casos, infracciones, actas ni vínculos|BD y Backend|Ninguna FK con `ON DELETE CASCADE`; todas en `RESTRICT`. Esas entidades no exponen operación de borrado: no existe el método ni la ruta|
|**Baja lógica**|Backend|`activo = false` para personas y conjuntos; `vigencia_hasta` para vínculos y asignaciones. Reversible 30 días|
|**Auditoría de solo inserción**|BD|El usuario de aplicación tiene `INSERT` y `SELECT`, no `UPDATE` ni `DELETE`. Es un privilegio, no una convención|
|**No existe borrado masivo**|Backend|Ninguna operación acepta borrar o desactivar por filtro. Siempre por identificador|
|**La anulación no es borrado**|BD y Backend|La fila permanece, tachada y consultable|
|**La aplicación no altera el esquema**|BD|Sin privilegios DDL en producción|
|**Respaldo verificado antes de migración destructiva**|Proceso|Y la restauración probada al menos una vez. Un respaldo que nunca se restauró no es un respaldo|
|**Doble confirmación escrita** para desactivar un conjunto|Backend|Escribir el nombre exacto|
|**Nunca cero gobierno**, en la misma transacción|Backend|La comprobación y el cambio ocurren juntos, o no ocurre ninguno|
|**Desactivar una Persona no la desvincula** de sus conjuntos|Backend|`activo = false` corta el acceso; las asignaciones se cierran una por una con su propio registro|

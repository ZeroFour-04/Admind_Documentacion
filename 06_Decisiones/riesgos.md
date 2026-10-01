---
resumen: "Riesgos vivos R1 a R14, con su estado y mitigación."
tipo: decision
origen: "maestro v1.4 (2026-09-14) §10"
actualizado: 2026-09-14
---

# Riesgos vivos

> [!WARNING] Decisión posterior a este texto (2026-09-29)
> - R5 dice que una persona puede tener varios roles. Lo vigente es **un solo rol por persona y conjunto** ([permisos](../05_Modulos/permisos.md)).

|ID|Riesgo|Estado|
|---|---|---|
|**R1**|Tres implementaciones independientes del mismo problema (reservas, parqueadero de visitantes, citas son todos "recurso limitado + concurrencia")|Mitigado: reglas de negocio independientes, **mecanismo de bloqueo y transacción compartido**|
|**R2**|Se captura documento de **toda** persona del sistema, no solo visitantes|**Abierto**: falta justificación escrita de finalidad, plazo de retención y purga|
|**R5**|El catálogo fijo de roles puede no encajar con cargos reales|Mitigado: una persona puede tener varios roles; si falta uno, el equipo lo agrega en código|
|**R6**|El multiconjunto multiplica la superficie de fuga|Mitigado en BD y capa de acceso, con prueba del intruso en la DoD|
|**R7**|La franja queda bloqueada desde el primer clic hasta que el administrador responde|Mitigado: unicidad parcial en BD, expiración evaluada al siguiente acceso|
|**R8**|El administrador es cuello de botella y punto de arbitrariedad|Mitigado: orden fijo no configurable, rechazo con categoría, historial completo|
|**R9**|Bloqueo abusivo de franjas|Mitigado: dos oportunidades por franja|
|**R10**|El **Superusuario** concentra facultades sin control interno y lee datos personales sin procedimiento|**Abierto y es el más caro.** Solo lo mitiga la auditoría. Falta decidir si se registran sus **consultas**, no solo sus escrituras|
|**R11**|Un registro de infracción puede leerse como prueba de debido proceso sin serlo|Mitigado: aviso explícito en el registro y en el manual|
|**R12**|`Persona` global perfora el aislamiento por diseño; la búsqueda por documento es canal de fuga|**Parcial**: falta escribir la lista cerrada de tablas globales y definir el tope de búsquedas|
|**R13**|La prioridad **traslada** el punto de arbitrariedad del administrador a la secretaría|**Parcial**: falta cerrar las tres listas de causales formales|
|**R14**|El anuncio dirigido a una vivienda es mensajería unidireccional con otro nombre|Mitigado por diseño; el aviso en pantalla es lo único que separa el uso correcto del atajo|

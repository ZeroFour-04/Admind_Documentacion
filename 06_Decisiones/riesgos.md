---
resumen: "Riesgos vivos R1 a R14, con su estado y mitigación."
tipo: decision
origen: "maestro v1.4 (2026-09-14) §10"
actualizado: 2026-10-11
revisado: 2026-10-11
---

# Riesgos vivos

> [!WARNING] Cómo van al 2026-10-11
> - **R5** dice que una persona puede tener varios roles. Lo vigente desde el 2026-09-29 es **un solo rol por persona y conjunto** ([permisos](../05_Modulos/permisos.md)).
> - **R12:** la lista cerrada de tablas globales ya está escrita y la vigila `tests/esquema/test_tablas_globales.py` ([aislamiento](../03_Reglas/aislamiento.md)). El tope de búsquedas es de 20 por hora, contado por conjunto.
> - **R2** sigue abierto y creció: visitantes, ingresos a zonas y comprobantes capturan datos sin finalidad, autorización ni retención definidas ([pendientes](../08_Estado/pendientes.md), sección 4).

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

## Ver también

- [cerradas](cerradas.md) — las decisiones que mitigan cada riesgo
- [aislamiento](../03_Reglas/aislamiento.md) — R6 y R12
- [reservas](../05_Modulos/reservas.md) — R1, R7, R8 y R9
- [permisos](../05_Modulos/permisos.md) — R5 y R10
- [legal](../01_Contexto/legal.md) — R2 y R11
- [triage](../05_Modulos/triage.md) — R13 y R14

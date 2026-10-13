---
resumen: "Las 30 decisiones de arquitectura cerradas (numeradas) y los dos principios transversales. No se rediscuten."
tipo: decision
origen: "maestro v1.4 (2026-09-14) §9"
actualizado: 2026-10-11
revisado: 2026-10-11
---

# Decisiones cerradas — no se rediscuten

Cada una tiene razón escrita. Están aquí en forma corta para que nadie las reabra por desconocimiento.

|#|Decisión|
|---|---|
|1|Multi-tenancy en el esquema, no en la interfaz|
|2|Mecanismo de bloqueo compartido entre módulos de capacidad limitada|
|3|Catálogo de reglas parametrizado, **no un DSL**|
|4|Notificaciones como puerto con adaptadores; se implementa Email, WhatsApp queda declarado sin implementar|
|5|El sistema notifica infracciones y registra su desenlace; no modela el procedimiento sancionatorio|
|6|La máquina de estados modela el procedimiento, no la presentación|
|7|El parqueadero se asigna a un apartamento; el régimen jurídico queda fuera del modelo|
|8|Catálogos de roles y permisos fijos en código. Lo que la ley prohíbe no es permiso denegado sino operación inexistente|
|9|Permisos puramente aditivos, sin denegaciones explícitas|
|10|Propietario y arrendatario son **vínculos**, no roles|
|11|La competencia por una franja se resuelve por **orden de llegada**, con evidencia de entrevistas|
|12|La decisión final sobre una reserva es humana y el sistema no valida dinero|
|13|El estado vive en la **solicitud**, no en la franja|
|14|El aislamiento se resuelve en la base y en la capa de acceso, no endpoint por endpoint|
|16|La **anulación** es la respuesta al error humano bajo un modelo sin borrado|
|17|La confirmación es **de contenido, no de intención**|
|18|El abuso del bloqueo se corta con **dos oportunidades**, no con parámetros|
|19|El sistema no le pone plazo al administrador; le ordena la bandeja|
|20|El Registro de actividades es una **vista** sobre la auditoría|
|21|Sin borrado físico; auditoría de solo inserción por privilegios de BD|
|22|El nivel de plataforma tiene **un solo rol** (revierte la separación Operador/Superusuario)|
|23|La **identidad es global**; roles y vínculos son por conjunto|
|24|El documento identifica; la **llave primaria UUID referencia**|
|25|La excepción al aislamiento se declara, se cierra y se prueba|
|26|El acceso de excepción se elimina y su lugar lo ocupa la auditoría|
|27|La prioridad existe **donde no hay un bien escaso en disputa**|
|28|El triage filtra la **forma**; el **fondo** no se delega|
|29|El anuncio tiene dos alcances y **ninguno es una lista de personas**|
|30|El triage es **opcional** y el sistema lo prueba|

_(La 15 fue revertida por la 22 y no se conserva como vigente.)_

**Principio transversal: simplicidad sobre configurabilidad.** Seis versiones seguidas eliminaron parámetros ajustables a favor de mecanismos fijos con una persona resolviendo los casos raros. Cuando dudes, esa es la dirección.

**Segundo principio: documentar las reversiones.** Una decisión revertida se registra como reversión deliberada con su razón, no se borra en silencio. Es lo que permite responder _"¿por qué no hicieron X?"_ con _"lo hicimos y lo quitamos, por esto"_.

## Ver también

- [construccion](construccion.md) — decisiones tomadas después, al construir
- [abiertas](abiertas.md) — lo que sigue sin decidir
- [riesgos](riesgos.md) — el riesgo que mitiga cada una
- [decidido_y_propuesto](decidido_y_propuesto.md) — qué es un hecho y qué una sugerencia
- [Admin_Master](../Admin_Master.md) — cómo se cita una decisión

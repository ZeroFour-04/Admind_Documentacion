---
resumen: "Restricciones legales: jerarquía, marco normativo y reglas duras. Están por encima de todo."
tipo: contexto
origen: "maestro v1.4 (2026-09-14) §4"
actualizado: 2026-10-11
revisado: 2026-10-11
---

# Restricciones legales — jerárquicamente superiores a todo

Fuente completa: guía legal v1.0 (2026-08-20), 116 requisitos con fundamento normativo bajo la convención `REQ-<MODULO>-<NN>`.

**Jerarquía declarada:** Constitución > ley > decreto reglamentario > reglamento de propiedad horizontal > manual de convivencia > configuración del sistema. Ningún requisito legal puede relajarse por configuración del cliente, decisión de asamblea ni permiso de rol.

**Tipos de requisito:** `OBLIGATORIO` (si no se cumple, la operación falla con error explícito) · `PROHIBIDO` (el sistema no expone la funcionalidad, ni siquiera tras un permiso) · `CONFIGURABLE` (parámetro por conjunto, con topes legales como validación dura) · `ADVERTENCIA` (zona discutida: registrar y advertir, nunca decidir).

## 4.1 Marco normativo

La Ley 675 de 2001 es la norma eje —vigente, modificada solo por la Ley 2079 de 2021— pero no basta. El sistema toca además:

|Materia|Norma adicional|
|---|---|
|Visitantes, cámaras, datos personales|Ley 1581 de 2012, Decreto 1074 de 2015|
|Convivencia, ruido, mascotas, policía|Ley 1801 de 2016, Decreto 768 de 2025|
|Piscina|Ley 1209 de 2008, Decreto 554 de 2015|
|Solicitudes / PQR|Ley 1755 de 2015|
|Portería y vigilancia|Decreto Ley 356 de 1994|
|Cobro por uso de zonas comunes|E.T. art. 19-5 y régimen de IVA|

## 4.2 Reglas duras que tocan el núcleo

|Regla|Fundamento|
|---|---|
|El sistema **no impone sanciones**|L675 arts. 59 y 60|
|La comunicación de una infracción va a **propietario y arrendatario**, ambos|C-318/02|
|La convocatoria a asamblea va a **cada propietario**, resida o no|L675 art. 39|
|No existe operación de **restricción de uso** por mora ni como sanción sobre bienes esenciales|SU-509/01, L675 art. 59 §|
|Un parqueadero de visitantes **no se destina** a una unidad; la ocupación temporal sí lo es|L675 art. 22|
|Cobrar por un bien común solo procede si **el reglamento lo autoriza**|L675 art. 19 §2, art. 46 num. 5|
|Toda captura de documento exige **finalidad declarada, autorización y plazo de retención**|Ley 1581|
|No se retiene el documento físico del visitante|Minimización + C. Penal art. 395|
|Las actas de asamblea son solo para propietarios autenticados; el sistema no reemplaza la obligación de entregar copia|L675 art. 47 §|
|Piscina: menores de 12 años requieren acompañante adulto; salvavidas en los supuestos exigidos|L1209/2008, D554/2015|

> [!IMPORTANT] Cómo se implementa una prohibición legal **No como permiso denegado, sino como operación inexistente.** No existe el permiso `sancionar` porque no existe la operación. No hay campo de multa en el registro de infracción. Un parqueadero de visitantes no aparece en el selector de asignación.
> 
> El principio: un rol mal asignado puede ser un problema de privacidad; **nunca puede ser un problema de legalidad**.

## 4.3 Zona de cuidado

Circula contenido de blogs que presenta el **Decreto 768 de 2025** como "la nueva ley de propiedad horizontal", atribuyéndole reglas de videovigilancia, registro digital de visitantes y prohibición de alquiler corto. **Ninguna de esas reglas está en el decreto** — es un decreto de procedimiento único de policía. No usar fuentes secundarias como fundamento normativo.

Hay reformas en trámite (PL 067/2025 Cámara, reforma integral de la Ley 675, aprobada en primer debate el 7 de abril de 2026). **Vigilar, no implementar.**

## Ver también

- [alcance](alcance.md) — lo que queda fuera por razones legales (3.4)
- [infracciones](../05_Modulos/infracciones.md) — el sistema no sanciona
- [parqueaderos](../05_Modulos/parqueaderos.md) — el de visitantes no se destina a una unidad
- [unidades](../05_Modulos/unidades.md) — a quién se notifica cada hecho
- [ingresos](../05_Modulos/ingresos.md) y [pagos](../05_Modulos/pagos.md) — construidos sin haber verificado lo legal
- [abiertas](../06_Decisiones/abiertas.md) — 12.10 b: lo que falta verificar
- [riesgos](../06_Decisiones/riesgos.md) — R2, R10 y R11
- [pendientes](../08_Estado/pendientes.md) — sección 4: lo legal sin verificar

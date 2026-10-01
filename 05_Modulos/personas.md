---
resumen: "Identidad global de personas: una fila por persona en toda la plataforma, UUID como llave y documento normalizado."
tipo: modulo
modulo: personas
hu: [HU-04, HU-07]
origen: "maestro v1.4 (2026-09-14) §5.2"
actualizado: 2026-09-14
---

# Personas (identidad)

## Diseño (maestro §5.2)

**Una persona, una fila, en toda la plataforma.** El rol es por conjunto; el vínculo con una unidad es por conjunto; **la identidad no**.

El caso que originó la decisión: un vigilante que trabaja en el conjunto B y vive en el conjunto A, ambos administrados por la misma persona. Modelarlo como dos filas produce exactamente los conflictos que el sistema debe evitar.

```
Persona                       -- TABLA GLOBAL: sin conjunto_id (R12)
  id : UUID                   (PK)
  tipo_documento ∈ {CC, TI, CE, PAS, PPT}
  numero_documento
  nombres
  apellidos
  telefono                    (opcional)
  activo : bool
  UNIQUE (tipo_documento, numero_documento)

Usuario                       -- TABLA GLOBAL: sin conjunto_id (R12)
  id : UUID                   (PK)
  persona_id                  (única: una persona, como máximo un usuario)
  correo                      (único; con él se inicia sesión)
  contraseña                  (solo el hash)
  activo : bool
```

> [!NOTE] Datos personales revisados el 2026-09-14 (Alejo)
> `nombre` se separa en **`nombres` y `apellidos`**, y `Persona` gana **`telefono`**, opcional. **El correo sale de `Persona` y vive solo en `Usuario`**: es credencial, porque con él se inicia sesión y a él llega la recuperación de contraseña. Si estuviera en las dos tablas, un día dirían cosas distintas. Una persona sin cuenta —un menor con TI registrado por sus padres— no necesita correo.

|Código|En pantalla|
|---|---|
|`CC`|Cédula de ciudadanía|
|`TI`|Tarjeta de identidad|
|`CE`|Cédula de extranjería|
|`PAS`|Pasaporte|
|`PPT`|Permiso por Protección Temporal|

> [!NOTE] Lista revisada el 2026-09-14 (Alejo)
> La lista anterior era `CC`, `CE`, `PA`, `PEP`, `TI`. **`PEP` sale y entra `PPT`**, que lo reemplazó para los migrantes venezolanos. **`PA` pasa a `PAS`.** **`NIT` no entra**: identifica empresas, no personas. Los códigos se guardan **sin puntos** (`TI`, no `T.I.`), por la misma razón que se normaliza el número: dos escrituras del mismo tipo romperían el `UNIQUE`. El nombre completo es solo presentación.

**Por qué el documento identifica pero no es la llave primaria:**

|Si el documento fuera PK|Consecuencia|
|---|---|
|Viaja a cada FK|Toda tabla que referencie a una persona lleva su cédula adentro|
|Viaja a cada URL|`/residentes/1032456789` publica la cédula en el historial y en los logs|
|El número solo no es único|CC, TI, CE, PAS y PPT son numeraciones distintas que pueden coincidir|
|Los documentos cambian|Una TI se vuelve CC a los 18. Con PK documento, cada cambio es cascada — sobre una base que además prohíbe el borrado|

El UUID **referencia**; el par `(tipo, número)` **identifica**. Son decisiones independientes.

**Vincular a alguien que ya existe:** buscar por documento exacto y asignarle rol en el conjunto activo. Un solo paso. Es el punto blando del diseño y está registrado como **R12**.

## Ver también

- [riesgos](../06_Decisiones/riesgos.md) — R12

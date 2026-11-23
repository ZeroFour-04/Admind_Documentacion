---
titulo: "F0 · Diccionario de datos en Word"
fecha: 2026-11-14
alcance: "Convertir el diccionario ya generado desde admind_db en un Word con el estilo de AdMind"
punto_de_partida: "10_Sustentacion/datos/diccionario_datos.md, generado el 2026-11-14 del esquema real (main b89d9f2)"
resumen: "Plan para que Sonnet arme el diccionario de datos en Word a partir del Markdown generado de PostgreSQL."
estado: activo
ejecutado:
hu:
---

# Plan F0 · Diccionario de datos

**Entregable:** `Entregables_Sustentacion\AdMind_Diccionario_de_Datos.docx` (y su PDF).
**Tiempo estimado:** 45 minutos.
**Antes de empezar:** leer [estilo_entregables](estilo_entregables.md).

## Lo que ya está hecho

El contenido **ya existe** y salió de la base real, no de los modelos ni de la documentación: [datos/diccionario_datos.md](datos/diccionario_datos.md). Tiene 42 tablas (32 del negocio en 19 módulos y 10 del framework), sus 352 columnas con tipo, nulo y llaves, y las restricciones de cada tabla (llaves foráneas compuestas, únicas, índices únicos parciales y CHECK).

**No se cambia ningún dato técnico** (nombres, tipos, llaves, restricciones). Si algo parece raro, se le pregunta a Alejo; no se "corrige".

## Pasos

1. **Portada y tabla de contenido** según el estilo común. Título: "Diccionario de Datos".
2. **1. Introducción** (media página, redactarla):
   - Qué es el documento.
   - Motor: PostgreSQL 18.4; base `admind_db`.
   - Cómo se generó: consultando `information_schema` y `pg_catalog` de la base real y cruzándolo con los modelos de Django. Así el documento coincide con lo que hay en producción.
   - Las cifras del encabezado del Markdown (tablas, llaves, restricciones).
3. **2. Convenciones:** pasar la sección *Convenciones* del Markdown como lista, y agregar un recuadro verde 50 que explique en dos frases la llave foránea compuesta `(id, conjunto_id)`. Es el blindaje entre conjuntos y lo más distintivo del modelo.
4. **3. Tablas por módulo:** un título 2 por módulo (Personas, Cuentas y sesión, …, Auditoría) con su frase de descripción. Dentro, un título 3 por tabla con:
   - la descripción y el modelo de Django;
   - la tabla de columnas (Columna | Tipo | Nulo | Llave | Descripción y valores permitidos), en Consolas las tres primeras columnas;
   - debajo, "Restricciones de la tabla" como lista, en letra de 9 pt. Los CHECK largos pueden ir en Consolas 8 pt.

   Las tablas de columnas son anchas, pero **no se usan secciones horizontales**: todo el documento es carta vertical ([estilo](estilo_entregables.md)).
5. **Mejorar las descripciones de columnas (solo si sobra tiempo).** Hoy muchas dicen solo el nombre del campo ("Hora inicio", "Numero documento"). Se pueden reescribir en una frase corta, leyendo el modelo en `Backend/Admind_Backend/apps/<app>/models.py` (los comentarios y `help_text` dicen qué es cada campo).
   - Solo las tablas del negocio. Corregir tildes ("Número", "Liberación").
   - Si un campo no se entiende leyendo el modelo, se deja como está.
6. **4. Anexo: tablas del framework:** igual que en el Markdown, más compacto.
7. **5. Objetos programados en la base:** una sección corta que diga que hoy no hay triggers ni procedimientos almacenados. Agregar el recuadro ámbar "En implementación: 5 procedimientos almacenados y 5 triggers (tarea C5), que se documentarán en la versión de la sustentación".
   - *Preguntarle a Alejo si prefiere omitir esta sección en el entregable de hoy.*
8. Exportar a PDF y revisar:
   - que la tabla de contenido tenga los 19 módulos y el anexo;
   - que ninguna tabla quede cortada sin encabezado repetido;
   - que el logo y los colores estén en la portada.

## Regenerar el diccionario (cuando entren los SP y triggers)

Los dos scripts están en `10_Sustentacion/datos/scripts/`. Desde `Backend/Admind_Backend`, en Git Bash:

```bash
SP="C:/Users/Alejandro/Documents/A D M I N D/Documentacion/Admind_Documentacion/10_Sustentacion/datos"
DICC_SALIDA="$SP/diccionario.json" ./.venv/Scripts/python.exe manage.py shell -c "exec(open(r'$SP/scripts/diccionario.py', encoding='utf-8').read())"
PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe -I "$SP/scripts/dicc_a_md.py" "$SP/diccionario.json" "$SP/diccionario_datos.md"
```

El primero lee la base y deja un JSON; el segundo arma el Markdown. Hoy no listan el cuerpo de los triggers ni de las funciones, solo los cuentan: cuando existan, hay que agregar esa parte al segundo script.

## Ver también

- [estilo_entregables](estilo_entregables.md) — colores, fuentes, portada y salida
- [restricciones_bd](../02_Arquitectura/restricciones_bd.md) — por qué existen las restricciones que aparecen en el diccionario
- [aislamiento](../03_Reglas/aislamiento.md) — la llave foránea compuesta por conjunto

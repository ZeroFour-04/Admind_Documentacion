-- Diccionario de datos de AdMind: columnas de todas las tablas de admind_db.
-- Devuelve una fila por columna: tabla, columna, tipo, nulo y llave (PK, FK -> tabla.columna, UQ).
-- Se corre en psql o en cualquier cliente de PostgreSQL conectado a admind_db.

SELECT c.relname                                   AS tabla,
       a.attname                                   AS columna,
       format_type(a.atttypid, a.atttypmod)        AS tipo,
       CASE WHEN a.attnotnull THEN 'No' ELSE 'Sí' END AS nulo,
       concat_ws(' · ',
           (SELECT 'PK' FROM pg_constraint k
             WHERE k.conrelid = c.oid AND k.contype = 'p' AND k.conkey = ARRAY[a.attnum]),
           (SELECT 'FK → ' || fc.relname || '.' || fa.attname
              FROM pg_constraint k
              JOIN pg_class fc ON fc.oid = k.confrelid
              JOIN pg_attribute fa ON fa.attrelid = k.confrelid AND fa.attnum = k.confkey[1]
             WHERE k.conrelid = c.oid AND k.contype = 'f' AND k.conkey = ARRAY[a.attnum]
             LIMIT 1),
           (SELECT 'UQ' FROM pg_constraint k
             WHERE k.conrelid = c.oid AND k.contype = 'u' AND k.conkey = ARRAY[a.attnum]
             LIMIT 1)
       )                                           AS llave
FROM pg_attribute a
JOIN pg_class c      ON c.oid = a.attrelid
JOIN pg_namespace n  ON n.oid = c.relnamespace
WHERE n.nspname = 'public' AND c.relkind = 'r' AND a.attnum > 0 AND NOT a.attisdropped
ORDER BY c.relname, a.attnum;

-- Restricciones de todas las tablas: CHECK, únicas y llaves foráneas (con su definición).
SELECT c.relname AS tabla, k.conname AS nombre, k.contype AS tipo, pg_get_constraintdef(k.oid) AS definicion
FROM pg_constraint k
JOIN pg_class c     ON c.oid = k.conrelid
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public' AND k.contype IN ('c', 'u', 'f')
ORDER BY c.relname, k.contype, k.conname;

---
resumen: "La máquina de desarrollo de Alejo: Windows, Python 3.14, PostgreSQL 18 nativo, sin Docker."
tipo: arquitectura
origen: "Lab §4 (verificado el 2026-09-11)"
actualizado: 2026-09-11
---

# Entorno de la máquina

Verificado el 2026-09-11:

| Pieza | Estado |
| --- | --- |
| Sistema | Windows 10 IoT Enterprise LTSC 2021. La terminal por defecto es **PowerShell** |
| Python | **3.14.3**, el único instalado. Django 5.2 LTS lo soporta desde el parche **5.2.8** |
| Git | 2.53 |
| Docker | **No instalado.** La ruta de aprendizaje lo asume; no bloquea nada de la Fase 0 |
| PostgreSQL | **18**, como servicio de Windows `postgresql-x64-18`, puerto 5432 |

El Postgres nativo ya da las tres cosas que el diseño exige y SQLite no: índices únicos parciales, llaves foráneas compuestas y privilegios por tabla. **Nunca se sustituye por SQLite**, ni siquiera "para empezar más rápido".

> [!TIP] La herramienta que más rinde
> El depurador de VS Code. Un punto de parada en una vista, una petición, y avanzar línea por línea por el middleware y el ORM. El criterio de salida de la Fase 1 —explicar qué archivo se ejecuta y en qué orden— se aprende así en una tarde.

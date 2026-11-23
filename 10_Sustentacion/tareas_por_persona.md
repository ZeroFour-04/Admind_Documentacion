---
resumen: "Resumen de lo que le falta a cada uno para la sustentación final, en el orden sugerido; el detalle de cada tarea está en tareas.md."
tipo: plan
origen: "lista final de Notion del 2026-11-16, contrastada con GitHub ese día a las 14:16, auditada a las 20:10 y a las 23:45, y otra vez el 17-nov a las 10:00 con gh y la versión en la nube"
actualizado: 2026-11-18
revisado: 2026-11-17
---

# Tareas de la sustentación final, por persona

> Para Notion: copiar desde este título hacia abajo. Cada código (C1, A10…) tiene su detalle en `10_Sustentacion/tareas.md`.

**Sustentación:** era el martes 17-nov desde las 10:15 y se movió al **lunes 23-nov** (hora por confirmar); unos 15 minutos. Lo vigente está en [sustentacion_tecnica](sustentacion_tecnica.md).
**App en la nube:** `https://admind.detkor.com` (sin `www`), en el VPS de Oracle.

**Estado el martes 17-nov a las 10:00:**
- **Rúbrica:** 10 de 12 criterios se pueden mostrar (UX/UI, roles, cobertura, CI, seguridad, correo, despliegue del front, base de datos, reportes y Sonar). Siguen en cero **CORS y JWT** y **Swagger**.
- **En `main` de los dos repos, con el CI en verde:** todo lo de Alejo (A2, A4, A7, A10) y, desde esta mañana, C3, C5 y C6 de Camilo (PR #17 y #18 del back, #10 y #11 del front). `main` del back queda en `2dd5c44` y el del front en `10e2d04`.
- **Base de datos (C5):** 4 funciones, 1 procedimiento y 5 triggers; 4 de los triggers son el mismo "sin borrado físico" en tablas distintas.
- **Sonar (C1):** SonarCloud analiza `main` de los dos repos (check en verde). No se vio desde aquí la lista de vulnerabilidades ni si hay arreglos propios (A3).
- **La nube:** el front corre la versión nueva (404 propio, `/reportes/` existe). `api.admind.detkor.com` no resuelve: la API no es pública y no hay Swagger.
- **Sin proteger** `main` ni `desarrollo`; la `Desarrollo` del front y las `revert-*` del back siguen en GitHub.

**Si el profe pregunta por lo que falta:**
- **JWT:** el token es opaco y vive en una tabla de sesiones, así que cerrar sesión lo invalida de verdad. La decisión era volverlo JWT firmado sin perder esa tabla (híbrido); no alcanzó.
- **CORS:** el navegador nunca llama a la API; el front de Django la llama desde el servidor. Ninguna plantilla ni script del front hace `fetch` a la API, así que hoy no hay petición de otro origen que permitir.
- **Swagger:** el contrato de la API está en el anexo del documento técnico (las 97 rutas).

## Decisiones (tomadas el 14 y el 16-nov)

- [x] JWT híbrido.
- [x] Reportes para Administración (y el Superusuario).
- [x] Cuentas demo de Residente y Vigilancia para el profe.
- [x] Swagger público.
- [x] Nube en el VPS de Oracle, sin `www`.
- [x] **Reparto:** despliegue (A9) y GitHub Actions (A10) para Alejo; Swagger (C10) para Camilo.

## Alejo

**Hecho y en `main`:**
- [x] **A2** Cobertura: 94,0 %, captura en `Entregables_Sustentacion/evidencias/cobertura_back.png`, y el paso de cobertura en el CI (PR #9).
- [x] **A4** Pantallas: menú por permiso, títulos, "Administración", sin "Maqueta", `maxlength`, páginas 403, 404 y 500 y el middleware de errores de la API (PR #8). El 404 propio ya se ve en la nube.
- [x] **A7** Correo en HTML con logo en los tres envíos, y el bug de "No hay conexión" al publicar un anuncio (PR #14). Falta la captura del correo enviado desde la nube.
- [x] **A9** El front desplegado con la versión nueva en `https://admind.detkor.com`.
- [x] **A10** CI en verde en los dos repos, con cobertura, y un historial de ejecuciones por PR.

**Pendiente:**
- [ ] **A8** Presentación, guion de la demostración y plan B (capturas por si la red falla).
- [ ] **A9** `api.admind.detkor.com` (Swagger y CORS), la nota de cómo está montado y el QR.
- [ ] **A3** Su vulnerabilidad de Sonar, en su propio PR.
- [ ] **A5** Prueba de romper la app sobre la nube.
- [ ] **A10** Proteger `main` y `desarrollo`, y borrar las ramas `Desarrollo` (front), `revert-*` y las cortas ya fundidas.
- [ ] **A1** Regenerar el diccionario de datos con lo de C5.
- [ ] **A6** Material de estudio.

## Camilo

**Hecho y en `main`:**
- [x] **C1** SonarCloud analizando `main` de los dos repos.
- [x] **C3** Ajustes de producción en los dos repos: `DEBUG` y `ALLOWED_HOSTS` por entorno, cookies seguras, `gunicorn`, `whitenoise`, y `never_cache` para el botón Atrás (PR #17 y #10).
- [x] **C5** 4 funciones, 1 procedimiento y 5 triggers en migraciones (PR #17).
- [x] **C6** Reportes PDF y Excel de zonas, pagos y reservas, con la pantalla `/reportes/` (PR #17 y #10).
- [x] Su rama `Desarrollo` del back entró (PR #15).

**Pendiente:**
- [ ] **C10** Swagger público.
- [ ] **C9** CORS con lista blanca (`https://admind.detkor.com`).
- [ ] **C8** JWT híbrido.
- [ ] **C12** Bug de casos redirigidos: sin commit visible.
- [ ] Su vulnerabilidad de Sonar, en su propio PR.
- [ ] Confirmar que la `Desarrollo` del front se descarta.

## Ver también

- [tareas](tareas.md) — el detalle de cada tarea: archivos, pasos, pruebas, evidencias y el estado verificado en GitHub

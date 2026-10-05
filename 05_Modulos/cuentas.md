---
resumen: "Sesión, token opaco, conjunto activo, segundo factor y recuperación de contraseña."
tipo: modulo
modulo: cuentas
hu: [HU-01, HU-02, HU-26]
origen: "guía de estructura §5.3 (2026-09-30)"
actualizado: 2026-10-05
---

# Cuentas: sesión, token y segundo factor

1. `POST /auth/login/` con correo y contraseña → el servicio crea un **`TokenDeSesion`** y devuelve el token (una cadena aleatoria). En la base se guarda solo su **huella** SHA-256, nunca el token en claro.
2. La sesión dura **1 hora** (`DURACION_TOKEN_DE_SESION`) y guarda: usuario, **conjunto activo** y si el **segundo factor** ya se verificó.
3. Si la persona tiene un solo conjunto, se elige solo; si tiene varios, pasa por el selector (`POST /auth/conjunto-activo/`, HU-26). Con la sesión, la API devuelve también los **permisos** y el **rol** de la persona en ese conjunto (`roles` y `tipo_usuario`, p. ej. "Administrador"; el Superusuario aparece como tal en cualquier conjunto). El front los guarda para decidir qué mostrar.
4. Quien tiene algún **permiso sensible** (gestionar usuarios, asignar roles, ver auditoría…) debe configurar y verificar el **segundo factor** (código de 6 dígitos con django-otp, HU-02). Mientras no lo haga, `DosFactoresAlDia` responde 403 en todo lo demás.
5. Recuperar contraseña (HU-01): `POST /auth/recuperar/` manda un enlace de un solo uso por correo, con `send_mail` desde `cuentas` (no pasa por el canal de notificaciones: ahí no hay sesión ni conjunto). Cada correo puede pedir **3 enlaces por hora**; el cuarto responde 429 con el mismo texto exista o no la cuenta (`limites.py`, throttling de DRF con la caché en memoria: el contador se pierde al reiniciar y no se comparte entre procesos). El correo sale por SMTP si el `.env` trae `EMAIL_HOST`; sin él, por la consola. En el front, un 429 muestra el `detail` de la API.

Se eligió **token opaco guardado en la base** y no JWT: se puede revocar al instante (logout) y guarda estado (conjunto activo, 2FA).

## Ver también

- [permisos](permisos.md) — qué permisos son sensibles y exigen segundo factor
- [frontend](../02_Arquitectura/frontend.md) — la sesión del lado del front (`apps/cuentas/sesion.py`)
- [construccion](../06_Decisiones/construccion.md) — por qué token con registro en la base (2026-09-15)

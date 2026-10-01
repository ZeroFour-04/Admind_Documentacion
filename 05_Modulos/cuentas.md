---
resumen: "Sesión, token opaco, conjunto activo, segundo factor y recuperación de contraseña."
tipo: modulo
modulo: cuentas
hu: [HU-01, HU-02, HU-26]
origen: "guía de estructura §5.3 (2026-09-30)"
actualizado: 2026-09-30
---

# Cuentas: sesión, token y segundo factor

1. `POST /auth/login/` con correo y contraseña → el servicio crea un **`TokenDeSesion`** y devuelve el token (una cadena aleatoria). En la base se guarda solo su **huella** SHA-256, nunca el token en claro.
2. La sesión dura **1 hora** (`DURACION_TOKEN_DE_SESION`) y guarda: usuario, **conjunto activo** y si el **segundo factor** ya se verificó.
3. Si la persona tiene un solo conjunto, se elige solo; si tiene varios, pasa por el selector (`POST /auth/conjunto-activo/`, HU-26). Con la sesión, la API devuelve también los **permisos** y el **rol** de la persona en ese conjunto (`roles` y `tipo_usuario`, p. ej. "Administrador"; el Superusuario aparece como tal en cualquier conjunto). El front los guarda para decidir qué mostrar.
4. Quien tiene algún **permiso sensible** (gestionar usuarios, asignar roles, ver auditoría…) debe configurar y verificar el **segundo factor** (código de 6 dígitos con django-otp, HU-02). Mientras no lo haga, `DosFactoresAlDia` responde 403 en todo lo demás.
5. Recuperar contraseña (HU-01): `POST /auth/recuperar/` manda un enlace por correo (en local, el correo sale en la consola).

Se eligió **token opaco guardado en la base** y no JWT: se puede revocar al instante (logout) y guarda estado (conjunto activo, 2FA).

## Ver también

- [permisos](permisos.md) — qué permisos son sensibles y exigen segundo factor
- [frontend](../02_Arquitectura/frontend.md) — la sesión del lado del front (`apps/cuentas/sesion.py`)
- [construccion](../06_Decisiones/construccion.md) — por qué token con registro en la base (2026-09-15)

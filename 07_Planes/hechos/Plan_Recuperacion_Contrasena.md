---
resumen: "Plan de la recuperación de contraseña: límite de enlaces por hora, correo real por SMTP y pruebas del front."
titulo: AdMind — Plan guiado de la terminación de la recuperación de contraseña
tipo: plan
estado: hecho
ejecutado: 2026-10-05
hu: [HU-01]
modo: mixto (F0, F1 y F4 guiadas; F2 y F3 construidas por el agente)
fecha: 2026-10-04
para: Alejo, con un agente que guía según 09_Protocolos/ejecutar_plan_guiado.md si Alejo lo aprueba; si no, el agente lo construye
alcance: "HU-01, recuperación de contraseña: límite de intentos en /auth/recuperar/, correo real por SMTP y pruebas del front de las dos pantallas"
punto_de_partida: "Backend 71ded31 (330 pruebas: 329 pasan y 1 falla, la conocida), Frontend 22db0dc (147 pruebas), sin cambios pendientes"
---

# AdMind — Plan guiado de la terminación de la recuperación de contraseña

> [!IMPORTANT]
> **Plan terminado el 2026-10-05.** Es histórico: lo vigente está en [construccion](../../06_Decisiones/construccion.md) y [cuentas](../../05_Modulos/cuentas.md). D1 a D6 respondidas.

## 1. Seguimiento

<!-- Lo mantiene el agente que ejecuta, guíe o construya. Quien escribe el plan lo deja en cero, con una fila por fase. -->

**Dónde voy:** plan terminado el 2026-10-05 (F0 a F4). Commits hechos por Alejo: F1 en el Backend (`1c82605`) y F2 y F3 juntas en el Frontend (`afcd6e6`). Solo queda lo humano: el aviso a Camilo y la prueba manual de la DoD. F0, F1 y F4 fueron guiadas; F2 y F3 las construyó el agente porque Alejo lo pidió.

| Fase | Deja funcionando | Estado | Modo | Explicada de vuelta | Verificación | Commit | Fecha |
|---|---|---|---|---|---|---|---|
| F0 | Punto de partida confirmado | hecha | guiada | — | Back: 329 passed, 1 failed (la conocida), `makemigrations` sin cambios, árbol limpio. Front: 150 passed, árbol limpio (ver Desviaciones) | — | 2026-10-04 |
| F1 | La API rechaza con 429 el cuarto enlace en una hora para un mismo correo | hecha | guiada | saltada | Back: 333 passed, 1 failed (la conocida), `makemigrations` sin cambios | Back `1c82605` | 2026-10-04 |
| F2 | La pantalla de pedir enlace tiene pruebas y muestra el mensaje del 429 | hecha | construida | — | Front: rojo esperado en `pasado_el_limite` antes de B2.5, luego 5 pruebas en verde | Front `afcd6e6` (junto con F3) | 2026-10-05 |
| F3 | La pantalla de crear contraseña nueva tiene pruebas | hecha | construida | — | Front: `160 passed` (suite completa); Back: `333 passed, 1 failed` (la conocida), `makemigrations` sin cambios | Front `afcd6e6` (junto con F2) | 2026-10-05 |
| F4 | El enlace llega a una bandeja real por SMTP | hecha | guiada (la hizo Alejo; el agente comprobó B4.4 y el cierre) | — | Alejo confirmó en el chat que el correo llegó. Con el SMTP configurado: Back `333 passed, 1 failed` (la conocida; `apps/cuentas/tests.py`: 40 passed), Front `160 passed`, `makemigrations` sin cambios, `.env` fuera de `git status` | — | 2026-10-05 |

<!-- Estado: pendiente · en curso · hecha. Modo: guiada · construida (la hizo el agente). Explicada de vuelta: sí · saltada · — si fue construida. Verificación: qué se corrió y cómo salió. -->

### Desviaciones

<!-- Una línea por caso: fecha · bloque · qué difería del plan · qué se hizo. -->

- 2026-10-04 · F0 · El Frontend no estaba en `22db0dc` con 147 pruebas: Alejo había hecho el commit `2af7114` (favicon, 3 pruebas nuevas en `tests/test_identidad.py`) y quedó en 150 pruebas. Se siguió desde ahí. **Los conteos del plan suben 3:** Frontend 150 antes, 155 tras F2, 160 tras F3 y F4. El Backend no cambia (334 al final: 333 pasan y 1 falla).
- 2026-10-04 · D6 · Alejo respondió en el chat: opción a, un Gmail creado para AdMind. Sus credenciales están en `Credenciales/`, que el agente no abre.

- 2026-10-05 · F2 y F3 · Alejo, con sueño, pidió que el agente terminara el plan. Se construyeron F2 y F3 sin guiar, y las 10 pruebas de `tests/test_recuperacion.py` se escribieron de una vez; el rojo de B2.4 se comprobó corriendo el archivo entero antes de tocar `cliente_api/http.py`. Resultado: Frontend 160 pruebas (la meta del plan con la desviación del favicon). La prueba existente `test_el_429_se_muestra_como_alerta` de `tests/test_usuarios.py` sigue en verde.

- 2026-10-05 · B4.5 · Alejo confirmó que el correo llegó a la bandeja; el agente no registró los pasos 3 a 9 del *Guion de prueba manual* (cambio de la contraseña, enlace reutilizado, reinicio). Quedan para la prueba manual de la DoD, que le toca a Camilo.

### Conceptos por repasar

<!-- Lo que costó, lo que se saltó y los bloques `tuyo` que terminaron con el código dado. Con las fases construidas por el agente, es la lista de estudio para la sustentación. -->

- F1 (explicación de vuelta saltada): repasar quién cuenta y dónde se guarda el contador, por qué el 429 no deja enumerar correos, y la pregunta de jurado de por qué este límite se declara en la vista y cuenta en memoria (qué se pierde: el contador al reiniciar, y no se comparte entre procesos).
- B1.6 (`test_el_limite_cuenta_igual_con_mayusculas_y_espacios`): Alejo la escribió incompleta (faltaba la cuarta petición); el agente la comprobó y la dejó funcionando. Repasar por qué la clave normaliza con `strip().lower()`.
- F2 y F3 (construidas por el agente, sin explicación): repasar qué se prueba en el front (la traducción, no las reglas), `mock.patch` con `return_value` y con `side_effect`, `call_args.args[1:]`, por qué el texto del 429 lo pone la API (`cliente_api/http.py`) y cómo `errores_de_la_api_al_formulario` reparte errores bajo el campo o arriba. Pregunta de jurado de F2: por qué pasan con la API apagada y qué error dejarían pasar (un cambio de contrato entre front y API).
- F4 (el agente no pidió la explicación de vuelta): repasar por dónde sale un correo sin `EMAIL_HOST` (consola), con `EMAIL_HOST` (SMTP) y en las pruebas (memoria, `mailoutbox`), y qué línea de `config/settings.py` lo decide; la contraseña de aplicación vive solo en el `.env` ignorado por git.
- B1.5 (`test_el_limite_no_revela_si_el_correo_existe`): la escribió el agente a pedido de Alejo; repasar por qué un 429 idéntico para un correo sin cuenta no deja enumerar correos y por qué cada correo lleva su propia cuenta.

## 2. Instrucciones para el agente

> [!IMPORTANT]
> **Primero pregunta.** Antes de tocar nada, pregúntale a Alejo si este plan se trabaja **guiado** (explicas por bloques y él aplica) o si lo **construyes** tú. No entres en modo guiado sin su respuesta.

### 2.1 Qué leer antes de empezar

1. [ejecutar_plan_guiado](../../09_Protocolos/ejecutar_plan_guiado.md): cómo se trabaja este plan en modo guiado y qué cambia si Alejo pide que lo construyas.
2. Este plan completo.
3. Notas:
   - [cuentas](../../05_Modulos/cuentas.md): sesión, token y el punto 5, que es esta funcionalidad.
   - [capas](../../03_Reglas/capas.md): en qué archivo va cada regla. Sirve para explicar por qué este límite se declara en la vista.
   - [reglas_frontend](../../03_Reglas/reglas_frontend.md): `cliente_api/` es el único lugar que sabe que la API existe y el que traduce sus errores.
   - [pruebas_y_ejecucion](../../02_Arquitectura/pruebas_y_ejecucion.md): comandos y cómo simulan la API las pruebas del front.
   - [git](../../03_Reglas/git.md): formato del commit.
4. README de las carpetas que se tocan: `Backend/Admind_Backend/apps/cuentas/README.md`, `Frontend/Admind_Front-End/cliente_api/README.md` y `Frontend/Admind_Front-End/tests/README.md`.

### 2.2 Reglas propias de este plan

- **El `.env` lo edita solo Alejo.** No lo abras, no lo imprimas (`cat`, `grep`, `Read`), no pidas la contraseña del correo en el chat y no la escribas en ningún archivo. `Credenciales/` no se abre.
- **No se toca** `config/settings.py`, `config/settings_pruebas.py` ni `apps/notificaciones/`. El plan no los necesita; si parece que sí, es una desviación y se pregunta.
- **Sin migraciones y sin paquetes.** El límite usa el throttling de DRF y la caché de Django, que ya están instalados. Si `makemigrations --check --dry-run` detecta cambios, algo se salió del plan: se para.
- **Avisos a Camilo** (los da Alejo; recuérdaselo al cerrar la fase): en F2, que `cliente_api/http.py` ahora muestra el `detail` de la API en un 429; en F4, que las variables de SMTP del `.env` ya se usan y que sin ellas el correo sigue saliendo por la consola.
- **Las pruebas nunca mandan correo real**, ni con el SMTP configurado. Si llega un correo al correr `pytest`, se para.
- F4 no empieza sin la respuesta de D6.

## 3. Decisiones que toma Alejo

D1 a D5 las respondió Alejo el 2026-10-04 en el chat de planeación. Falta D6.

| ID | Decisión | Opciones | Recomendada | Respuesta |
|---|---|---|---|---|
| D1 | Qué entra en "terminar la recuperación" | a) límite de intentos b) correo real por SMTP c) envío que no tumba la respuesta d) pruebas del front | — | **a, b y d.** La c queda fuera |
| D2 | ¿El correo de recuperación pasa por el canal de notificaciones (decisión cerrada 4)? | a) no, sigue saliendo de `cuentas` con `send_mail` b) sí, con una salida nueva del canal | a | **a.** El canal exige conjunto activo y deja aviso en la bandeja; aquí no hay sesión ni conjunto |
| D3 | Dónde se cuentan los intentos | a) en memoria, con el throttling de DRF b) en una tabla nueva (global, R12) | a | **a** |
| D4 | Sobre qué se cuenta | a) por correo b) por correo y por IP | a | **a** |
| D5 | Tope por correo | a) 3 por hora b) 5 por hora | a | **a** |
| D6 | Cuenta desde la que sale el correo | a) una cuenta de Gmail creada para AdMind, que también puede usar Camilo b) tu Gmail personal c) otro proveedor SMTP (cambian `EMAIL_HOST` y `EMAIL_PORT`) | a | |

## 4. Decisiones menores que el plan ya fija

| ID | Decisión |
|---|---|
| P1 | El límite es una clase de DRF en un archivo nuevo, `apps/cuentas/limites.py`, y se declara en la vista con `throttle_classes`, igual que un permiso. No va en el servicio, como el de búsquedas de persona, porque aquel cuenta sobre la auditoría y esta petición no tiene actor ni conjunto |
| P2 | El tope vive en la clase (`rate = "3/hour"`), como `LIMITE_DE_BUSQUEDAS` vive en su app. No se agrega nada a `config/settings.py` |
| P3 | La clave de la caché es la **huella** SHA-256 del correo normalizado (`strip().lower()`, lo mismo que hace `solicitar_recuperacion`), con `huella_de` de `servicios.py`. El correo no queda en claro en la caché |
| P4 | Se usa la caché por defecto de Django (memoria del proceso). No se declara `CACHES` |
| P5 | Al pasar el tope: `429` con `{"detail": …}` y un texto propio, **el mismo exista o no la cuenta**. Sin cabecera `Retry-After` |
| P6 | Se cuenta toda petición que traiga un texto en `correo`, antes de validar su forma. Sin `correo`, no se cuenta y el serializer responde 400. La petición rechazada no cuenta ni envía correo |
| P7 | `/auth/recuperar/confirmar/` no lleva límite: el token no se puede adivinar |
| P8 | En las pruebas del back, una fixture `autouse` en `apps/cuentas/tests.py` vacía la caché antes de cada prueba. `settings_pruebas.py` no se toca |
| P9 | En el front, `ErrorDeApi` toma el `detail` de la API en un 429, como ya hace con 400, 409 y 401. El texto fijo queda de respaldo y deja de hablar de búsquedas |
| P10 | Las pruebas del front van en un archivo nuevo, `tests/test_recuperacion.py`, con un `Client()` sin sesión y la API simulada con `mock.patch("cliente_api.cuentas.…")` |
| P11 | El SMTP no cambia código: `config/settings.py` ya lo lee del `.env`. Se prueba con `manage.py sendtestemail`, que trae Django |

## 5. Punto de partida verificado

Comprobado en el código el 2026-10-04. Ramas `desarrollo`, árbol limpio en los dos repositorios.

**La funcionalidad ya existe de punta a punta.** Este plan no la crea: la termina.

| Dónde | Qué hay |
|---|---|
| `Backend/Admind_Backend/apps/cuentas/servicios.py` | `solicitar_recuperacion(correo)` (línea 130), `restablecer_contrasena(uid, token, contrasena)`, `usuario_del_enlace(uid)`, `huella_de(token)`, `EnlaceInvalido` |
| `…/apps/cuentas/views.py` | `SolicitarRecuperacionView` (línea 227) y `RestablecerContrasenaView`, públicas. Constantes `MENSAJE_RECUPERACION_ENVIADA` y `MENSAJE_ENLACE_INVALIDO` |
| `…/apps/cuentas/urls.py` | `recuperar/` (`recuperar-contrasena`) y `recuperar/confirmar/` (`restablecer-contrasena`), bajo `/auth/` |
| `…/apps/cuentas/tests.py` | 8 pruebas de recuperación desde la línea 437, con los ayudantes `pedir_enlace`, `enlace_del_correo` y `restablecer`, y las fixtures `cliente` y `usuario` (laura@correo.com) |
| `…/config/settings.py` | `ADMIND_FRONT_URL`, `PASSWORD_RESET_TIMEOUT` (1 hora) y el bloque de correo (líneas 80 a 91): SMTP si hay `EMAIL_HOST`, consola si no. No declara `CACHES` ni throttling |
| `…/.env _ejemplo` (con espacio en el nombre) | Ya documenta `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` y `DEFAULT_FROM_EMAIL` |
| `Frontend/Admind_Front-End/apps/cuentas/views.py` | `recuperar_contrasena` y `restablecer_contrasena`, las dos `@publica`; `errores_de_la_api_al_formulario` |
| `…/apps/cuentas/forms.py` | `RecuperarForm` y `RestablecerForm` (compara las dos contraseñas) |
| `…/apps/cuentas/urls.py` | `/recuperar-contrasena/` y `/restablecer-contrasena/<uid>/<token>/`; el ingreso es `/` |
| `…/cliente_api/cuentas.py` | `solicitar_recuperacion(request, correo)` y `restablecer_contrasena(request, uid, token, contrasena)` |
| `…/cliente_api/http.py` | `ErrorDeApi`, `ApiNoDisponible`, `MENSAJES_POR_ESTADO`, `MENSAJE_API_NO_DISPONIBLE` |
| `…/tests/` | `ayudantes.cliente_con_sesion()`. **Ninguna prueba** de las dos pantallas ni del ingreso |

Lo que el plan resuelve y hoy falta:

- Ninguna vista del backend usa throttling. El único límite que existe (20 búsquedas de persona por hora, `apps/personas/servicios.py`) cuenta sobre la auditoría.
- En un 429 el front muestra siempre el texto fijo «Hiciste demasiadas búsquedas…» (`MENSAJES_POR_ESTADO`), no el `detail` de la API.
- El correo sale por la consola: el `.env` no tiene `EMAIL_HOST`.

**Diferencias entre las notas y el código:**

- [pendientes](../../08_Estado/pendientes.md) decía que la recuperación «en el front es maqueta». No lo es: el front llama a la API. Corregido el 2026-10-04.
- [estado_actual](../../08_Estado/estado_actual.md) y [pruebas_y_ejecucion](../../02_Arquitectura/pruebas_y_ejecucion.md) son del corte del 30/09: Backend en `ee256ff` y Frontend en `7fa88ea` con 140 pruebas. Hoy el Backend está en `71ded31` (solo agregó `AGENTS.md` y `CLAUDE.md`) y el Frontend en `22db0dc`, con las pantallas de visitantes de Camilo y **147 pruebas**. No se corrigieron aquí: se actualizan al cerrar el plan, con las suites corridas.
- Los conteos de pruebas se obtuvieron con `pytest --collect-only`. Cuántas pasan sale de la nota del 30/09 y lo confirma F0.
- El README de `apps/cuentas/` del backend dice que el correo «debe pasar» por el canal de notificaciones. D2 decidió lo contrario; lo corrige B1.8.

## 6. Mapa de la funcionalidad

Lo marcado **[nuevo]** es lo que agrega este plan. El resto ya existe.

1. La persona abre `/recuperar-contrasena/` en el front (puerto 8001) y escribe su correo.
2. `views.recuperar_contrasena` valida el formulario y llama a `cliente_api.cuentas.solicitar_recuperacion`, que hace `POST /auth/recuperar/` a la API (puerto 8000).
3. **[nuevo]** Antes de entrar a la vista, DRF le pregunta a `LimiteDeEnlacesPorCorreo` si ese correo ya pidió 3 enlaces en la última hora. La cuenta está en la caché en memoria. Si ya los pidió: `429` y no pasa nada más.
4. `SolicitarRecuperacionView` valida y llama al servicio `solicitar_recuperacion`: si la cuenta existe y puede entrar, arma el enlace y lo manda con `send_mail`. Responde `202` exista o no la cuenta.
5. **[nuevo]** `send_mail` sale por SMTP a una bandeja real, porque el `.env` ya trae `EMAIL_HOST`. En las pruebas sigue yendo a la memoria.
6. **[nuevo]** Si la API respondió `429`, `ErrorDeApi` toma su `detail` y la pantalla lo muestra arriba del formulario.
7. La persona abre el enlace, `/restablecer-contrasena/<uid>/<token>/`, y escribe la contraseña dos veces. El front llama a `POST /auth/recuperar/confirmar/`.
8. El servicio `restablecer_contrasena` comprueba el enlace, valida la contraseña, la cambia y borra las sesiones abiertas. `204`.
9. El front cierra su propia sesión y redirige a `/?restablecida=1`, que muestra «Tu contraseña cambió».
10. **[nuevo]** Los pasos 1, 2, 6, 7 y 9 quedan cubiertos por pruebas del front con la API simulada.

## F0 · Confirmar el punto de partida

- [ ] **B0.1** · Correr las dos suites y `makemigrations --check --dry-run` ([pruebas_y_ejecucion](../../02_Arquitectura/pruebas_y_ejecucion.md)). Se espera: Backend `329 passed, 1 failed` (la que falla es `test_toda_ruta_de_la_api_esta_cubierta`, conocida y ajena a este plan), Frontend `147 passed`, sin migraciones pendientes y `git status` limpio en los dos. Si no coincide, se para y se le avisa a Alejo.

## F1 · Backend: tres enlaces por hora para un mismo correo

**Deja funcionando:** el cuarto `POST /auth/recuperar/` en una hora con el mismo correo responde `429` y no envía correo. Cuatro pruebas nuevas en verde.

**Concepto de la fase:** un límite de intentos es un contador con ventana de tiempo. DRF lo trae hecho (*throttling*): antes de ejecutar la vista le pregunta a una clase si deja pasar la petición. Aquí solo se decide **a quién** se le cuenta (la clave) y **cuánto** (la tasa).

- [x] **B1.1** · explicado · `Backend/Admind_Backend/apps/cuentas/limites.py` (archivo nuevo)
  - **Qué:** la clase del límite.
  - **Concepto:** `SimpleRateThrottle` guarda en la caché la lista de horas de las últimas peticiones de una clave. Uno solo escribe `get_cache_key`. Devolver `None` significa «a esta petición no se le cuenta».
  - **Forma:**

    ```python
    """Límites de intentos de las vistas públicas de cuentas. Se declaran en la vista, como los permisos."""
    from rest_framework.throttling import SimpleRateThrottle

    from apps.cuentas.servicios import huella_de


    class LimiteDeEnlacesPorCorreo(SimpleRateThrottle):
        """A lo sumo 3 enlaces de recuperación por hora para un mismo correo, exista o no la cuenta (HU-01).

        DRF guarda en la caché la hora de cada petición. La caché es la memoria del proceso: la
        cuenta se pierde al reiniciar el servidor y no se comparte entre procesos.
        """

        scope = "recuperar_contrasena"
        rate = "3/hour"

        def get_cache_key(self, request, view):
            correo = request.data.get("correo") if isinstance(request.data, dict) else None
            if not isinstance(correo, str) or not correo.strip():
                # Sin correo no hay a quién contarle: el serializer responde 400.
                return None
            # La huella y no el correo: la clave queda de largo fijo y el correo no se guarda en claro.
            return self.cache_format % {"scope": self.scope, "ident": huella_de(correo.strip().lower())}
    ```
  - **Para explicar:** por qué la clave es el correo y no la IP (a la API toda petición le llega con la IP del front, así que la IP contaría a todos juntos); por qué se normaliza igual que en `solicitar_recuperacion`; qué se pierde con la caché en memoria.
  - **Comprobación:** `./.venv/Scripts/python.exe manage.py check` sin errores.

- [x] **B1.2** · explicado · `Backend/Admind_Backend/apps/cuentas/views.py`
  - **Qué:** tres cambios. (1) En los imports: `from rest_framework.exceptions import NotFound, Throttled` y `from apps.cuentas.limites import LimiteDeEnlacesPorCorreo`. (2) Junto a las otras constantes `MENSAJE_…`: la del límite. (3) En `SolicitarRecuperacionView`: `throttle_classes` y el método `throttled`.
  - **Concepto:** la vista **declara** el límite, no lo calcula: `authentication_classes`, `permission_classes` y `throttle_classes` son las tres preguntas que DRF hace antes de llegar a `post`. `throttled` es el gancho para decidir qué error sale.
  - **Forma:**

    ```python
    MENSAJE_DEMASIADOS_ENLACES = (
        "Se pidieron demasiados enlaces para este correo. Espera una hora e intenta de nuevo."
    )
    ```

    ```python
    class SolicitarRecuperacionView(APIView):
        authentication_classes = []
        permission_classes = [AllowAny]
        throttle_classes = [LimiteDeEnlacesPorCorreo]

        def throttled(self, request, wait):
            # Texto propio, el mismo exista o no la cuenta. El de DRF le suma los segundos que faltan.
            raise Throttled(detail=MENSAJE_DEMASIADOS_ENLACES)

        def post(self, request):
            ...  # queda igual
    ```
  - **Para explicar:** el 429 no revela si el correo existe, porque el contador corre igual para cualquier texto. Sin `wait`, la respuesta no lleva `Retry-After` (P5).
  - **Comprobación:** `./.venv/Scripts/python.exe -m pytest apps/cuentas/tests.py -q`. **Se espera rojo:** fallan pruebas de recuperación que antes pasaban, las que piden el enlace para laura@correo.com después de la tercera vez. Es lo que explica B1.3; no se corrige tocando la vista.

- [x] **B1.3** · explicado · `Backend/Admind_Backend/apps/cuentas/tests.py`
  - **Qué:** imports nuevos arriba (`import time`, `from unittest import mock`, `from django.core.cache import cache`, `from apps.cuentas.limites import LimiteDeEnlacesPorCorreo`) y una fixture después de la fixture `usuario`.
  - **Concepto:** `pytest-django` devuelve la base de datos a cero después de cada prueba, pero la caché en memoria no es la base: sigue viva durante toda la corrida. Una fixture `autouse` se ejecuta sola antes de cada prueba del archivo.
  - **Forma:**

    ```python
    @pytest.fixture(autouse=True)
    def contador_de_enlaces_en_cero():
        # El límite de enlaces vive en la caché en memoria, que no se vacía sola entre pruebas.
        cache.clear()
    ```
  - **Comprobación:** el mismo comando de B1.2, ahora en verde.

- [x] **B1.4** · explicado · `…/apps/cuentas/tests.py`, al final del bloque de recuperación
  - **Qué:** la prueba del tope.
  - **Concepto:** una prueba de límite comprueba las dos orillas: lo que todavía pasa (3) y lo primero que ya no (4), y que el rechazo no tuvo efecto (no salió un cuarto correo).
  - **Forma:**

    ```python
    def test_el_cuarto_enlace_en_una_hora_para_el_mismo_correo_se_rechaza(cliente, usuario, mailoutbox):
        for _ in range(3):
            assert pedir_enlace(cliente).status_code == 202

        cuarto = pedir_enlace(cliente)

        assert cuarto.status_code == 429
        assert cuarto.json() == {
            "detail": "Se pidieron demasiados enlaces para este correo. Espera una hora e intenta de nuevo."
        }
        assert len(mailoutbox) == 3
    ```
  - **Comprobación:** `./.venv/Scripts/python.exe -m pytest apps/cuentas/tests.py -q -k cuarto_enlace`.

- [x] **B1.5** · tuyo (modelo: B1.4) · `…/apps/cuentas/tests.py`
  - **Qué:** `test_el_limite_no_revela_si_el_correo_existe`.
  - **Qué cambia respecto al modelo:** se pide con `nadie@correo.com`, que no tiene cuenta. Las tres primeras son `202`, la cuarta `429` con el mismo cuerpo que en B1.4, y `mailoutbox` queda vacío. Al final, una petición con `laura@correo.com` todavía responde `202`: cada correo lleva su propia cuenta.
  - **Comprobación:** `-k no_revela` en verde. Ojo: ya existe `test_pedir_enlace_no_revela_si_el_correo_existe`; las dos tienen que pasar.

- [x] **B1.6** · tuyo (modelo: B1.4) · `…/apps/cuentas/tests.py`
  - **Qué:** `test_el_limite_cuenta_igual_con_mayusculas_y_espacios`.
  - **Qué cambia respecto al modelo:** tres peticiones con `laura@correo.com` y la cuarta con `"  Laura@Correo.com "`. Tiene que ser `429`: es la misma clave.
  - **Comprobación:** `-k mayusculas_y_espacios` en verde. Para ver que la prueba sirve, quitar un momento el `.lower()` de `limites.py`: debe fallar.

- [x] **B1.7** · explicado · `…/apps/cuentas/tests.py`
  - **Qué:** la prueba de que la ventana se mueve.
  - **Concepto:** para probar «pasada una hora» no se espera una hora: se le cambia el reloj a la clase. `SimpleRateThrottle` lee la hora de su atributo `timer`, y `mock.patch.object` lo reemplaza solo dentro del `with`. Es la misma idea con la que `apps/personas/test_busqueda.py` simula `timezone.now`.
  - **Forma:**

    ```python
    def test_pasada_la_hora_se_puede_pedir_otro_enlace(cliente, usuario, mailoutbox):
        for _ in range(3):
            pedir_enlace(cliente)
        assert pedir_enlace(cliente).status_code == 429

        una_hora_despues = time.time() + 60 * 60 + 1
        with mock.patch.object(LimiteDeEnlacesPorCorreo, "timer", return_value=una_hora_despues):
            assert pedir_enlace(cliente).status_code == 202
        assert len(mailoutbox) == 4
    ```
  - **Comprobación:** `-k pasada_la_hora` en verde.

- [x] **B1.8** · explicado · `Backend/Admind_Backend/apps/cuentas/README.md`
  - **Qué:** tres ajustes. (1) En la fila de `POST /auth/recuperar/`, la columna de respuestas queda: `202 siempre, exista o no la cuenta · 429 al cuarto pedido en una hora para el mismo correo`. (2) Donde el README lista lo que hay en la app, una línea para `limites.py`. (3) En *Pendiente*, se reemplaza la línea del canal de notificaciones por cuatro: el correo de recuperación **no** pasa por el canal, porque el canal necesita conjunto activo y deja el aviso en la bandeja y aquí no hay sesión ni conjunto (decisión de Alejo, 2026-10-04); `send_mail` es síncrono y sin `try`; el límite vive en memoria y se pierde al reiniciar; `/auth/login/` no limita intentos.
  - **Concepto:** el README de la carpeta es lo primero que lee el siguiente agente. Un pendiente que ya se decidió, si se queda escrito, se vuelve a construir.
  - **Comprobación:** leerlo de corrido: no queda ninguna frase que diga que el correo debe pasar por el canal.

**Cierre de F1**

- **Verificación:** en `Backend/Admind_Backend`, `./.venv/Scripts/python.exe -m pytest -q` → `333 passed, 1 failed` (la conocida) y `./.venv/Scripts/python.exe manage.py makemigrations --check --dry-run` → `No changes detected`.
- **Explicar de vuelta:** «cuéntame qué pasa desde que llega el cuarto `POST /auth/recuperar/` con el mismo correo hasta que sale el 429: quién cuenta, dónde se guarda la cuenta y por qué no sale un correo».
- **Pregunta de jurado:** «El límite de búsquedas de persona vive en el servicio y cuenta sobre la auditoría. ¿Por qué este se declara en la vista y cuenta en memoria, y qué se pierde por eso?».
- **Commit sugerido** (Backend): `feat(cuentas): limitar a 3 por hora los enlaces de recuperación de un mismo correo [HU-01]`

## F2 · Frontend: la pantalla de pedir el enlace, con pruebas

**Deja funcionando:** cinco pruebas de `/recuperar-contrasena/` en verde y el mensaje del 429 de la API a la vista de la persona.

**Concepto de la fase:** el front no tiene base ni reglas; lo que se prueba es la **traducción**: qué le manda a la API y qué muestra con cada respuesta. Por eso la API se simula con `mock.patch` y no hace falta tenerla encendida.

- [x] **B2.1** · explicado · `Frontend/Admind_Front-End/tests/test_recuperacion.py` (archivo nuevo)
  - **Qué:** la cabecera del archivo y la primera prueba.
  - **Concepto:** es la primera prueba del front de una pantalla **pública**. Las demás usan `cliente_con_sesion()`; aquí el navegador es un `Client()` vacío y aun así recibe `200`, porque la vista lleva `@publica` y `SesionRequeridaMiddleware` la deja pasar.
  - **Forma:**

    ```python
    """Pantallas de HU-01 para recuperar la contraseña: pedir el enlace y crear la nueva. La API se simula."""
    from unittest import mock

    from django.test import Client

    from cliente_api.http import MENSAJE_API_NO_DISPONIBLE, ApiNoDisponible, ErrorDeApi
    from tests.ayudantes import cliente_con_sesion

    ENVIADO = {"detail": "Si el correo está registrado, te enviamos un enlace para restablecer la contraseña."}
    DEMASIADOS = "Se pidieron demasiados enlaces para este correo. Espera una hora e intenta de nuevo."
    ENLACE = "/restablecer-contrasena/MTIz/abc-123/"
    CLAVE = "otra-clave-larga-2026"


    def test_pedir_el_enlace_no_exige_sesion():
        respuesta = Client().get("/recuperar-contrasena/")

        assert respuesta.status_code == 200
        assert "Enviar enlace" in respuesta.content.decode()
    ```
  - **Comprobación:** `./.venv/Scripts/python.exe -m pytest tests/test_recuperacion.py -q`. Los imports que todavía no se usan se van usando en los bloques siguientes.

- [x] **B2.2** · explicado · `…/tests/test_recuperacion.py`
  - **Qué:** el camino feliz del formulario.
  - **Concepto:** `mock.patch("cliente_api.cuentas.solicitar_recuperacion", return_value=…)` cambia la función por una falsa mientras dura el `with`. La falsa responde lo que uno diga y **recuerda con qué la llamaron** (`call_args`). Se comprueban las dos mitades: lo que el front mandó y lo que el front mostró.
  - **Forma:**

    ```python
    def test_pedir_el_enlace_manda_el_correo_a_la_api_y_muestra_su_respuesta():
        with mock.patch("cliente_api.cuentas.solicitar_recuperacion", return_value=ENVIADO) as api:
            html = Client().post("/recuperar-contrasena/", {"correo": "laura@correo.com"}).content.decode()

        assert api.call_args.args[1] == "laura@correo.com"
        assert 'role="status">Si el correo está registrado' in html
        assert "Enviar enlace" not in html
    ```
  - **Para explicar:** `args[0]` es el `request`; por eso se mira `args[1]`. El texto del aviso no lo escribe el front: es el `detail` de la API.
  - **Comprobación:** `-k manda_el_correo` en verde.

- [x] **B2.3** · tuyo (modelo: B2.2) · `…/tests/test_recuperacion.py`
  - **Qué:** `test_un_correo_mal_escrito_no_llega_a_la_api`.
  - **Qué cambia respecto al modelo:** se manda `{"correo": "no-es-un-correo"}`. La API no se llama (`api.assert_not_called()`) y el HTML trae `am-campo__error`, la clase del error bajo el campo.
  - **Comprobación:** `-k mal_escrito` en verde.

- [x] **B2.4** · explicado · `…/tests/test_recuperacion.py`
  - **Qué:** la prueba del límite visto desde la pantalla. **Queda en rojo** hasta B2.5.
  - **Concepto:** para simular que la API **falla** no se usa `return_value` sino `side_effect` con la excepción que lanzaría `cliente_api`. Escribir la prueba antes del arreglo y verla fallar demuestra que la prueba mide lo que dice.
  - **Forma:**

    ```python
    def test_pasado_el_limite_se_muestra_el_mensaje_de_la_api():
        limite = ErrorDeApi(429, {"detail": DEMASIADOS})
        with mock.patch("cliente_api.cuentas.solicitar_recuperacion", side_effect=limite):
            html = Client().post("/recuperar-contrasena/", {"correo": "laura@correo.com"}).content.decode()

        assert 'role="alert"' in html
        assert DEMASIADOS in html
    ```
  - **Comprobación:** `-k pasado_el_limite` **falla**: la pantalla muestra «Hiciste demasiadas búsquedas…».

- [x] **B2.5** · explicado · `Frontend/Admind_Front-End/cliente_api/http.py`
  - **Qué:** dos cambios. (1) En `MENSAJES_POR_ESTADO`, el texto del 429 pasa a ser el respaldo genérico. (2) En `ErrorDeApi.__init__`, una rama nueva después de la del 401.
  - **Concepto:** quien sabe **por qué** se rechazó es la API; el front solo lo muestra. Ya era así con 400, 409 y 401. El texto fijo queda para cuando la respuesta no trae `detail`.
  - **Forma:**

    ```python
        # Cada límite explica lo suyo en el `detail` de la API; esto es solo por si no lo trae.
        429: "Hiciste demasiados intentos. Espera un rato e intenta de nuevo.",
    ```

    ```python
            elif estado == 429 and "detail" in cuerpo:
                # Búsquedas de persona, enlaces de recuperación: cada límite trae su propio texto.
                self.mensaje = cuerpo["detail"]
    ```
  - **Comprobación:** `-k pasado_el_limite` en verde, y `./.venv/Scripts/python.exe -m pytest tests/test_usuarios.py -q -k 429` sigue en verde (el límite de búsquedas).

- [x] **B2.6** · tuyo (modelo: B2.4) · `…/tests/test_recuperacion.py`
  - **Qué:** `test_con_la_api_apagada_la_pantalla_lo_dice`.
  - **Qué cambia respecto al modelo:** `side_effect=ApiNoDisponible()` y el HTML trae `MENSAJE_API_NO_DISPONIBLE`.
  - **Comprobación:** `-k api_apagada` en verde.

**Cierre de F2**

- **Verificación:** en `Frontend/Admind_Front-End`, `./.venv/Scripts/python.exe -m pytest -q` → `152 passed`.
- **Explicar de vuelta:** «cuéntame qué pasa en el front desde que la API responde 429 hasta que la persona lee el mensaje: qué función lanza qué, quién lo atrapa y dónde termina el texto».
- **Pregunta de jurado:** «¿Por qué las pruebas del front pasan con la API apagada, y qué error dejarían pasar por esa misma razón?».
- **Aviso a Camilo:** un 429 ya muestra el `detail` de la API en cualquier pantalla.
- **Commit sugerido** (Frontend): `fix(cuentas): mostrar el mensaje de la API al pasar el límite de enlaces [HU-01]`

## F3 · Frontend: la pantalla de crear la contraseña nueva, con pruebas

**Deja funcionando:** cinco pruebas de `/restablecer-contrasena/<uid>/<token>/` y del aviso en el ingreso, en verde.

**Concepto de la fase:** los errores de la API tienen dos destinos en un formulario: bajo el campo que los causó (`{"contrasena": […]}`) o arriba, cuando son de la operación (`{"detail": …}`). Los reparte `errores_de_la_api_al_formulario`.

- [x] **B3.1** · explicado · `Frontend/Admind_Front-End/tests/test_recuperacion.py`
  - **Qué:** el camino feliz.
  - **Concepto:** el `uid` y el `token` no van en el formulario: salen de la URL del enlace y el front los reenvía tal cual. Al terminar, el front cierra **su** sesión, porque la API ya borró todas las de esa cuenta.
  - **Forma:**

    ```python
    def test_la_contrasena_nueva_viaja_a_la_api_con_el_uid_y_el_token_del_enlace():
        cliente = cliente_con_sesion()
        with mock.patch("cliente_api.cuentas.restablecer_contrasena") as api:
            respuesta = cliente.post(ENLACE, {"contrasena": CLAVE, "confirmacion": CLAVE})

        assert api.call_args.args[1:] == ("MTIz", "abc-123", CLAVE)
        assert respuesta["Location"] == "/?restablecida=1"
        # La API cerró todas las sesiones de la cuenta: la de este navegador también se cierra.
        assert "token_api" not in cliente.session
    ```
  - **Comprobación:** `-k viaja_a_la_api` en verde.

- [x] **B3.2** · tuyo (modelo: B2.3) · `…/tests/test_recuperacion.py`
  - **Qué:** `test_si_las_dos_contrasenas_no_coinciden_no_se_llama_a_la_api`.
  - **Qué cambia respecto al modelo:** se manda al `ENLACE` una `confirmacion` distinta. La API no se llama y el HTML trae «Las dos contraseñas no coinciden.» (lo pone `RestablecerForm.clean`).
  - **Comprobación:** `-k no_coinciden` en verde.

- [x] **B3.3** · tuyo (modelo: B2.4) · `…/tests/test_recuperacion.py`
  - **Qué:** `test_un_enlace_vencido_se_avisa_arriba_del_formulario`.
  - **Qué cambia respecto al modelo:** el `side_effect` es `ErrorDeApi(400, {"detail": "El enlace no es válido o ya venció. Pide uno nuevo."})` sobre `cliente_api.cuentas.restablecer_contrasena`. El HTML trae `role="alert"`, ese texto y el enlace «Pedir otro enlace».
  - **Comprobación:** `-k enlace_vencido` en verde.

- [x] **B3.4** · explicado · `…/tests/test_recuperacion.py`
  - **Qué:** el error que cae bajo su campo.
  - **Concepto:** el formulario del front llama a sus campos igual que la API (`contrasena`). Por eso un `400` con `{"contrasena": […]}` aterriza solo bajo ese campo, sin traducir nombres.
  - **Forma:**

    ```python
    def test_una_contrasena_debil_se_explica_bajo_su_campo():
        debil = ErrorDeApi(400, {"contrasena": ["Esta contraseña es demasiado corta."]})
        with mock.patch("cliente_api.cuentas.restablecer_contrasena", side_effect=debil):
            html = Client().post(ENLACE, {"contrasena": "123", "confirmacion": "123"}).content.decode()

        assert 'id="id_contrasena-error">Esta contraseña es demasiado corta.' in html
        assert 'role="alert"' not in html
    ```
  - **Para explicar:** quién decide que «123» es débil no es el front: es `validate_password` en el servicio del backend. El front solo coloca el mensaje.
  - **Comprobación:** `-k debil` en verde.

- [x] **B3.5** · tuyo (modelo: B2.1) · `…/tests/test_recuperacion.py`
  - **Qué:** `test_despues_de_cambiarla_el_ingreso_lo_confirma`.
  - **Qué cambia respecto al modelo:** `Client().get("/?restablecida=1")` y el HTML trae «Tu contraseña cambió. Inicia sesión con la nueva.». Un `Client().get("/")` no lo trae.
  - **Comprobación:** `-k ingreso_lo_confirma` en verde.

**Cierre de F3**

- **Verificación:** en `Frontend/Admind_Front-End`, `./.venv/Scripts/python.exe -m pytest -q` → `157 passed`.
- **Explicar de vuelta:** «cuéntame el viaje del `uid` y del `token` desde el correo hasta el servicio del backend, y qué pasa con las sesiones abiertas cuando la contraseña cambia».
- **Pregunta de jurado:** «¿Por qué el enlace sirve una sola vez si el sistema no guarda en ninguna tabla que ya se usó?». La respuesta está en el docstring de `restablecer_contrasena`: el token se calcula con la contraseña, y al cambiarla deja de coincidir.
- **Commit sugerido** (Frontend): `test(cuentas): cubrir la pantalla de crear la contraseña nueva [HU-01]`

## F4 · Correo real por SMTP

**Deja funcionando:** al pedir el enlace desde el navegador, el correo llega a una bandeja real y su enlace cambia la contraseña.

**Concepto de la fase:** Django separa **qué** se envía (`send_mail`) de **por dónde** sale (`EMAIL_BACKEND`). El proyecto tiene tres salidas y ningún cambio de código entre ellas: la consola cuando no hay `EMAIL_HOST`, SMTP cuando sí, y la memoria durante las pruebas (`mailoutbox`). La credencial vive en `.env`, que está en `.gitignore`.

No hay código en esta fase. En modo guiado y en modo construido la hace Alejo; el agente explica y comprueba.

- [x] **B4.1** · explicado · fuera del repositorio
  - **Qué:** Alejo prepara la cuenta de D6. Con Gmail: activar la verificación en dos pasos y crear una **contraseña de aplicación** en `myaccount.google.com/apppasswords`. Son 16 letras y se muestran una sola vez.
  - **Concepto:** una contraseña de aplicación es una credencial aparte, solo para ese uso, que se puede revocar sin cambiar la contraseña de la cuenta. Gmail no acepta la contraseña normal por SMTP.
  - **Comprobación:** Alejo confirma que la tiene. No la pega en el chat.

- [x] **B4.2** · explicado · `Backend/Admind_Backend/.env` (lo edita Alejo)
  - **Qué:** Alejo agrega las cinco variables, con los nombres de `.env _ejemplo`: `EMAIL_HOST=smtp.gmail.com`, `EMAIL_PORT=587`, `EMAIL_HOST_USER` (la cuenta), `EMAIL_HOST_PASSWORD` (la contraseña de aplicación, sin espacios) y `DEFAULT_FROM_EMAIL` (`AdMind <la-cuenta>`). `ADMIND_FRONT_URL` se queda como está.
  - **Concepto:** `config/settings.py` (líneas 80 a 91) elige el backend según exista `EMAIL_HOST`. El puerto 587 con `EMAIL_USE_TLS` es STARTTLS: la conexión empieza en claro y se cifra antes de mandar la credencial.
  - **Comprobación:** `git status` en el Backend sigue limpio: `.env` no aparece.

- [x] **B4.3** · explicado · terminal
  - **Qué:** probar la salida sin pasar por la aplicación: `./.venv/Scripts/python.exe manage.py sendtestemail <un correo de Alejo>`.
  - **Concepto:** se prueba primero la pieza sola. Si esto falla, el problema es la configuración y no la recuperación. `SMTPAuthenticationError 535` es credencial (contraseña normal en vez de la de aplicación, o cuenta mal escrita); un tiempo de espera agotado es red o puerto bloqueado.
  - **Comprobación:** el correo de prueba llega (revisar también correo no deseado).

- [x] **B4.4** · explicado · terminal
  - **Qué:** correr `./.venv/Scripts/python.exe -m pytest apps/cuentas/tests.py -q` con el SMTP ya configurado.
  - **Concepto:** `pytest-django` cambia el backend de correo por el de memoria en toda la corrida. Por eso las pruebas leen `mailoutbox` y no llega nada a ninguna bandeja.
  - **Comprobación:** en verde y **ningún correo nuevo** en la bandeja. Si llega uno, se para.

- [x] **B4.5** · explicado · navegador
  - **Qué:** el recorrido completo, pasos 1 a 6 del *Guion de prueba manual*.
  - **Comprobación:** el correo llega, el enlace abre la pantalla del front y la contraseña nueva sirve para entrar.

**Cierre de F4**

- **Verificación:** las dos suites completas, con el SMTP configurado: Backend `333 passed, 1 failed` (la conocida) y Frontend `157 passed`.
- **Explicar de vuelta:** «cuéntame por dónde sale un correo en desarrollo sin `EMAIL_HOST`, con `EMAIL_HOST` y durante las pruebas, y qué línea del proyecto lo decide en cada caso».
- **Pregunta de jurado:** «¿Dónde está la contraseña del correo, quién la puede ver y qué pasa si alguien clona el repositorio?».
- **Aviso a Camilo:** las variables de SMTP ya se usan; sin ellas su correo sigue saliendo por la consola. Si la cuenta de D6 es compartida, la credencial se le pasa por fuera del repositorio.
- **Commit sugerido:** ninguno. Nada versionado cambia en esta fase.

## Cierre del plan

1. **Verificación final:** las dos suites, `makemigrations --check --dry-run` y `git status` en los dos repositorios.
2. **Informe final** en el chat ([abrir_y_cerrar_un_plan](../../09_Protocolos/abrir_y_cerrar_un_plan.md)): qué quedó por fase, commits, pruebas antes (330 y 147) y después (334 y 157), desviaciones y conceptos por repasar.
3. **Actualizar el contexto** con [actualizar_contexto](../../09_Protocolos/actualizar_contexto.md). Lo que este plan cambia: el punto 5 de [cuentas](../../05_Modulos/cuentas.md) (límite y SMTP), la fila de HU-01 en [historias](../../08_Estado/historias.md) (de los tres huecos queda solo `send_mail` síncrono), [pendientes](../../08_Estado/pendientes.md), los commits y conteos de [estado_actual](../../08_Estado/estado_actual.md) y [pruebas_y_ejecucion](../../02_Arquitectura/pruebas_y_ejecucion.md), y D1 a D6 en [construccion](../../06_Decisiones/construccion.md).
4. **Mover** este archivo a `07_Planes/hechos/` y cambiar su fila en [planes](../planes.md).

## Lo que el agente no puede hacer

- Crear la cuenta de correo, su contraseña de aplicación y escribir el `.env` (F4).
- La parte humana de la DoD de HU-01: PR `desarrollo → pruebas` revisado y la prueba manual de quien no programó. Si esto lo trabajó Alejo, la prueba le toca a Camilo, con el guion de abajo.
- Avisarle a Camilo los dos cambios (cierres de F2 y F4).
- Tocar Notion.

## Guion de prueba manual

Con los dos servidores encendidos ([pruebas_y_ejecucion](../../02_Arquitectura/pruebas_y_ejecucion.md)) y una cuenta de AdMind cuyo correo sea una bandeja real. Los usuarios de `crear_usuarios_prueba` no sirven para esto: sus correos son `@example.com`. Se crea una entrando como Administración → Usuarios, con un correo propio.

1. En `http://127.0.0.1:8001`, «¿Olvidaste tu contraseña?» y escribir ese correo. Aparece el aviso verde.
2. El correo llega con el asunto «AdMind: restablece tu contraseña». El remitente es la cuenta de D6.
3. Abrir el enlace en el mismo equipo (apunta a `127.0.0.1:8001`). Escribir dos contraseñas distintas: el error sale bajo el segundo campo.
4. Escribir `123` dos veces: el error sale bajo el primer campo y lo redacta el backend.
5. Escribir una contraseña válida dos veces: lleva al ingreso con «Tu contraseña cambió». Entrar con la nueva.
6. Abrir otra vez el mismo enlace y tratar de cambiarla: «El enlace no es válido o ya venció».
7. Pedir el enlace con un correo que no existe: sale el mismo aviso verde y no llega nada.
8. Pedir el enlace cuatro veces seguidas con un mismo correo: la cuarta muestra «Se pidieron demasiados enlaces para este correo…» y llegan solo tres correos.
9. Reiniciar el servidor del backend y pedirlo otra vez: vuelve a dejar. Es el límite conocido de contar en memoria.

## Fuera de este plan

- **`send_mail` síncrono y sin `try`** (D1 c, que Alejo dejó fuera). Con SMTP real pesa más que antes: si el servidor de correo falla, `/auth/recuperar/` responde `500` **solo cuando la cuenta existe**, y cuando funciona tarda más que con un correo inexistente. Las dos cosas dejan adivinar qué correos están registrados. Tampoco hay `EMAIL_TIMEOUT`.
- **Límite por IP** (D4 b). Exige que el front reenvíe la IP del navegador desde `cliente_api/http.py` y que la API confíe en esa cabecera.
- **`/auth/login/` no limita intentos de contraseña.** Ninguna nota lo registra como pendiente.
- **Contador que sobreviva reinicios o varios procesos** (D3 b): tabla global o caché compartida.
- **El correo por el canal de notificaciones** (D2 b) y un correo con formato HTML.
- **El enlace apunta a `127.0.0.1:8001`:** solo abre en el equipo donde corre el front.
- **`test_toda_ruta_de_la_api_esta_cubierta`** sigue en rojo por `usuario-perfil` y `usuario-eliminar`. No es de este plan.
- **Las pantallas de visitantes del front** (Camilo, 01/10) no aparecen todavía en las notas de estado.

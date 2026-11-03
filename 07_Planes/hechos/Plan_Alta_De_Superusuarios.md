---
resumen: "Un Superusuario crea otro Superusuario desde el selector de conjuntos, sin entrar a ninguno y sin conjunto asignado."
titulo: "AdMind — Plan guiado del alta de Superusuarios"
tipo: plan
modo: guiado
estado: hecho
hu: [HU-06]
fecha: 2026-10-30
ejecutado: 2026-10-30
para: "Alejo, con un agente que guía según 09_Protocolos/ejecutar_plan_guiado.md si Alejo lo aprueba; si no, el agente lo construye"
alcance: "Botón «Crear superusuario» en /conjuntos/ (solo lo ve un Superusuario), su pantalla en el front y POST /auth/superusuarios/ en el backend"
punto_de_partida: "Backend origin/desarrollo 56602b8, Frontend origin/desarrollo 734a8f7, sin cambios pendientes; las suites las cuenta F0"
---

# AdMind — Plan guiado del alta de Superusuarios

> [!IMPORTANT]
> **Alejo:** llena la columna *Respuesta* de la sección 3. Para empezar o retomar, en un chat nuevo: `Ejecuta el plan Documentacion/Admind_Documentacion/07_Planes/activos/Plan_Alta_De_Superusuarios.md`. El agente te pregunta primero si lo quieres guiado o si lo construye él.

## 1. Seguimiento

**Dónde voy:** completado.

| Fase | Deja funcionando | Estado | Modo | Explicada de vuelta | Verificación | Commit | Fecha |
|---|---|---|---|---|---|---|---|
| F0 | Punto de partida confirmado y ramas creadas | hecha | construida | — | Backend: 817 pasan (1 falla nocturna documentada), Frontend: 495 pasan, makemigrations personas/0003 | — | 2026-10-30 |
| F1 | `POST /auth/superusuarios/` con sus pruebas | hecha | construida | — | Backend: 822 pasan (1 falla nocturna documentada, +5 pruebas nuevas), sin migraciones nuevas | pendiente (sugerido: `feat(cuentas): alta de Superusuarios desde la plataforma [HU-06]`) | 2026-10-30 |
| F2 | Botón en el selector y pantalla de alta, con sus pruebas | hecha | construida | — | Frontend: 499 pasan (+4 pruebas nuevas) | pendiente (sugerido: `feat(conjuntos): crear superusuario desde el selector [HU-06]`) | 2026-10-30 |

### Desviaciones

Ninguna.

### Conceptos por repasar

Ninguno.

## 2. Instrucciones para el agente

> [!IMPORTANT]
> **Primero pregunta.** Antes de tocar nada, pregúntale a Alejo si este plan se trabaja **guiado** (explicas por bloques y él aplica) o si lo **construyes** tú. No entres en modo guiado sin su respuesta.

### 2.1 Qué leer antes de empezar

1. [ejecutar_plan_guiado](../../09_Protocolos/ejecutar_plan_guiado.md): cómo se trabaja en modo guiado.
2. Este plan completo.
3. [permisos](../../05_Modulos/permisos.md): el Superusuario, sus guardarraíles y por qué su asignación no lleva conjunto.
4. [cuentas](../../05_Modulos/cuentas.md): sesión, `roles` en la sesión y el segundo factor que se exige al entrar.
5. [aislamiento](../../03_Reglas/aislamiento.md): por qué el conjunto nunca viaja en la petición y por qué esta vista no hereda de `VistaDeConjunto`.
6. `Backend/Admind_Backend/apps/cuentas/README.md` y `Frontend/Admind_Front-End/apps/README.md`.

### 2.2 Reglas propias de este plan

- **Solo Superusuarios.** Crear administradores y los demás roles ya existe (paso 3 del asistente y la pantalla Usuarios dentro de un conjunto) y no se toca. No se agrega un formulario que reciba un conjunto: rompería la regla de aislamiento (Alejo, 2026-10-30).
- **Sin migraciones.** La restricción `asignacion_conjunto_segun_alcance` ya obliga a que el Superusuario tenga `conjunto` nulo; el plan se apoya en ella. Si `makemigrations --check` pide algo nuevo por este plan, se para.
- **Sin interruptor del segundo factor.** Se descartó (2026-10-30): el Superusuario nuevo configura el 2FA en su primer ingreso, como ya pasa hoy.
- `config/settings_pruebas.py` no se toca.
- **Avisar a Camilo** al terminar: hay un endpoint nuevo en `cuentas`.
- Ramas: `feat/superusuarios-desde-selector` en los dos repositorios, desde `origin/desarrollo`. El PR lo abre Alejo ([git](../../03_Reglas/git.md)).

## 3. Decisiones que toma Alejo

| ID | Decisión | Opciones | Recomendada | Respuesta |
|---|---|---|---|---|
| D1 | Cómo comprueba el backend que quien crea es Superusuario | a) `es_superusuario(persona)` en la vista, igual que `DELETE /conjuntos/actual/`. No cambia el catálogo. b) Un permiso nuevo de plataforma (p. ej. `superusuario.crear`) en `catalogo.py`, sensible. Más fiel al diseño (*toda vista exige un permiso*), pero cambia el catálogo y hay que contárselo a Camilo. `exigir_permiso` **no sirve tal cual**: con un conjunto activo, un Administrador con `usuario.gestionar` pasaría | a | a |
| D2 | Auditoría del alta | a) Sin auditoría, como el restablecimiento del 2FA (2026-10-05): `Registro` es un modelo de conjunto y aquí no hay conjunto. Queda la fila de `Asignacion` con su `vigencia_desde`. Costo aceptado y anotado. b) Una línea en el log del servidor con `logging` (quién creó a quién). No es auditoría formal, pero deja rastro. c) Hacer nulo el conjunto de `Registro` para eventos de plataforma: migración y toca `ModeloDeConjunto`. Fuera del alcance de este plan | a | a |
| D3 | A quién se puede hacer Superusuario | a) Solo a una persona nueva: documento y correo que no existan (lo mismo que hoy valida el alta de usuarios). b) También ascender a alguien que ya tiene cuenta, como Camilo con su rol de Administración. Es otra operación (asignar rol de plataforma a una persona existente) y otro plan | a | a |

## 4. Decisiones menores que el plan ya fija

| ID | Decisión |
|---|---|
| P1 | La ruta es `POST /auth/superusuarios/`, en `apps/cuentas`, junto a `/auth/usuarios/`. Responde 201 con `{"id", "correo"}`, igual que el alta de usuarios |
| P2 | El servicio no se duplica: el cuerpo de `registrar_usuario` pasa a `registrar_con_rol(rol, conjunto_id, **datos)` y las dos altas lo llaman |
| P3 | El serializer es `CrearSuperusuarioSerializer(CrearUsuarioSerializer)` con `rol = None`: DRF quita el campo heredado y conserva las validaciones de correo, contraseña y documento |
| P4 | En el front, la pantalla vive en `apps/conjuntos` (`/conjuntos/superusuarios/nuevo/`), porque el botón está en el selector. Quien no es Superusuario y la abre vuelve al selector |
| P5 | El front sabe si es Superusuario por `"Superusuario" in request.session["roles"]`, la misma expresión que ya usa el resumen del asistente (`apps/conjuntos/views.py`, vista `resumen`). Se saca a una función `es_superusuario(request)` y el resumen pasa a usarla |
| P6 | El front no usa el framework de mensajes de Django (no está en ninguna app). Tras crear, redirige a `/conjuntos/?superusuario=creado` y el selector muestra un aviso |

## 5. Punto de partida verificado

Comprobado el 2026-10-30:

- **Git.** Frontend en `desarrollo` = `origin/desarrollo` `734a8f7`, árbol limpio. Backend en la rama `fix/arreglo-de-conflictos-pr` (`e070eea`), ya fundida en `origin/desarrollo` `56602b8` por el PR #7, árbol limpio: F0 cambia a `desarrollo` y la actualiza.
- **Backend:**
  - `apps/cuentas/servicios.py`: `registrar_usuario(conjunto_id, *, tipo_documento, numero_documento, nombres, apellidos, correo, contrasena, rol, telefono="")` crea `Persona`, `Usuario` y `Asignacion` en una transacción y traduce el choque de `persona_documento_unico` a `PersonaYaExiste`. No importa `Rol`.
  - `apps/cuentas/serializers.py`: `CrearUsuarioSerializer` limita `rol` a `ROLES_DE_CONJUNTO` y valida correo repetido, contraseña y documento repetido.
  - `apps/cuentas/views.py`: `UsuariosView(VistaDeConjunto)` hace el alta con el conjunto de la sesión. Importa `apps.permisos.servicios as roles`.
  - `apps/permisos/servicios.py`: `es_superusuario(persona)`. `apps/permisos/views.py`: `MENSAJE_SIN_PERMISO` y `exigir_permiso`, que mira el conjunto activo.
  - `apps/permisos/models.py`: la restricción `asignacion_conjunto_segun_alcance` (Superusuario con conjunto nulo; los roles de conjunto, con conjunto).
  - `apps/comun/aislamiento/vistas.py`: `VistaDeConjunto` rechaza `conjunto` y `conjunto_id` en la petición. `CrearConjuntoView` (`apps/conjuntos/views.py`) es el precedente de una `APIView` que trabaja sin conjunto activo.
  - `apps/cuentas/tests.py`: los ayudantes `asignar(usuario, rol, conjunto=None)`, `entrar(cliente, segundo_factor=True)` y `elegir`, la fixture `usuario` (Laura) y `CONTRASENA`.
  - `DosFactoresAlDia` ya exige el 2FA verificado a quien tenga permisos sensibles: el Superusuario que crea ya lo trae y el nuevo tendrá que configurarlo al entrar.
- **Frontend:**
  - `cliente_api/cuentas.py`: `crear_usuario(request, datos)` hace `pedir(request, "POST", "auth/usuarios/", datos)`.
  - `apps/conjuntos/views.py`: `selector` arma `{"conjuntos", "error", "puede_crear"}`. `nuevo` es el modelo de una vista con formulario contra la API, y `administracion` el de un alta de cuenta.
  - `apps/conjuntos/forms.py`: `AdministradorForm(UsuarioForm)` quita `rol` y le pone la clase `am-campo__control` a los campos, pero su `clean` fija `rol = "administracion"`: **no se hereda de ella**.
  - `apps/usuarios/forms.py`: `UsuarioForm` con la confirmación de contraseña.
  - `templates/conjuntos/selector.html`: el bloque `{% if puede_crear %}` con «Crear conjunto». `asistente_administracion.html` trae el formulario de una cuenta.
  - `tests/ayudantes.py`: `cliente_con_sesion(permisos, conjunto_activo, tipo_usuario, roles, puede_crear_conjunto)`.

**Notas contra el código:** no hubo diferencias en lo que toca este plan.

## 6. Mapa de la funcionalidad

```
/conjuntos/  (selector)  ── solo si "Superusuario" está en roles ──▶  botón «Crear superusuario»
      │
      ▼
/conjuntos/superusuarios/nuevo/   SuperusuarioForm (datos de la persona, sin rol)
      │  cliente_api.cuentas.crear_superusuario
      ▼
POST /auth/superusuarios/   SuperusuariosView(APIView)  ← sin conjunto: no hereda de VistaDeConjunto
      │  es_superusuario(quien pide) o 403          (D1)
      │  CrearSuperusuarioSerializer                (valida correo, contraseña, documento)
      ▼
servicios.registrar_superusuario → registrar_con_rol(Rol.SUPERUSUARIO, None, …)
      ▼
Persona + Usuario + Asignacion(rol=superusuario, conjunto=NULL)  ← la base exige el NULL
```

Al entrar, el nuevo Superusuario ve todos los conjuntos (`conjuntos_disponibles`) y tiene que configurar su segundo factor.

## F0 · Confirmar el punto de partida

- [x] **B0.1** · En Backend: `git switch desarrollo` y `git pull`. En los dos repositorios: `git switch -c feat/superusuarios-desde-selector`.
- [x] **B0.2** · Correr las dos suites y `makemigrations --check --dry-run` ([pruebas_y_ejecucion](../../02_Arquitectura/pruebas_y_ejecucion.md)). Anotar en el seguimiento cuántas pruebas pasan. `makemigrations --check` puede fallar por `personas/0003`, que ya estaba pendiente antes de este plan: se anota y se sigue. Cualquier otra cosa en rojo, se para y se avisa.

## F1 · El alta en el backend

**Deja funcionando:** `POST /auth/superusuarios/` crea la cuenta con la asignación de plataforma; las pruebas nuevas pasan.

**Concepto de la fase:** un rol de **plataforma** no pertenece a ningún conjunto, así que su alta no puede pasar por `VistaDeConjunto` ni tomar el conjunto de la sesión. Y el permiso se mira sobre la persona, no sobre el conjunto activo.

- [x] **B1.1** · explicado · `Backend/Admind_Backend/apps/cuentas/servicios.py`
  - **Qué:** el cuerpo de `registrar_usuario` pasa a `registrar_con_rol`, y las dos altas lo llaman. Agregar `from apps.permisos.catalogo import Rol`.
  - **Concepto:** extraer lo común en vez de copiarlo; la transacción hace que persona, cuenta y rol se creen juntos o no se cree nada.
  - **Forma:**
    ```python
    def registrar_usuario(conjunto_id, *, rol, **datos):
        """Crea la persona, su cuenta y su rol en el conjunto activo, todo o nada."""
        return registrar_con_rol(rol, conjunto_id, **datos)


    def registrar_superusuario(**datos):
        """Crea la persona, su cuenta y su rol de Superusuario, que no lleva conjunto (maestro §5.3)."""
        return registrar_con_rol(Rol.SUPERUSUARIO, None, **datos)


    def registrar_con_rol(rol, conjunto_id, *, tipo_documento, numero_documento, nombres, apellidos,
                          correo, contrasena, telefono=""):
        # El cuerpo de antes, sin cambios, salvo la última línea de la transacción:
        #     Asignacion.objects.create(persona=persona, rol=rol, conjunto_id=conjunto_id)
    ```
  - **Comprobación:** la suite del backend sigue en verde sin tocar ninguna prueba: el alta de usuarios no cambió por fuera.
- [x] **B1.2** · explicado · `Backend/Admind_Backend/apps/cuentas/serializers.py`
  - **Qué:** debajo de `CrearUsuarioSerializer`:
    ```python
    class CrearSuperusuarioSerializer(CrearUsuarioSerializer):
        """Los mismos datos y validaciones, sin rol: siempre es Superusuario."""

        rol = None
    ```
  - **Concepto:** en DRF, declarar un campo heredado como `None` lo quita del serializer hijo.
  - **Comprobación:** en la shell de Django, `CrearSuperusuarioSerializer().fields` no tiene `rol`.
- [x] **B1.3** · explicado · `Backend/Admind_Backend/apps/cuentas/views.py` y `urls.py`
  - **Qué:** una vista nueva después de `UsuariosView`, y su ruta `path("superusuarios/", SuperusuariosView.as_view(), name="superusuarios")`. Importar `CrearSuperusuarioSerializer`, `PermissionDenied` (de `rest_framework.exceptions`) y `MENSAJE_SIN_PERMISO` (de `apps.permisos.views`).
  - **Concepto:** por qué esta vista hereda de `APIView` y no de `VistaDeConjunto`, y por qué no sirve `exigir_permiso`: con un conjunto activo, un Administrador con `usuario.gestionar` pasaría.
  - **Forma (con D1 a):**
    ```python
    class SuperusuariosView(APIView):
        """Alta de un Superusuario desde el selector (2026-10-30).

        No hereda de VistaDeConjunto: el rol es de plataforma y no lleva conjunto. Solo otro
        Superusuario lo crea, y eso se mira sobre la persona, no sobre el conjunto activo.
        """

        def post(self, request):
            if not roles.es_superusuario(request.user.persona):
                raise PermissionDenied(MENSAJE_SIN_PERMISO)
            datos = CrearSuperusuarioSerializer(data=request.data)
            datos.is_valid(raise_exception=True)
            try:
                usuario = servicios.registrar_superusuario(**datos.validated_data)
            except servicios.PersonaYaExiste:
                return Response(
                    {"numero_documento": ["Ya existe una persona con este documento."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response({"id": str(usuario.id), "correo": usuario.correo}, status=status.HTTP_201_CREATED)
    ```
    Con D1 b, la primera línea mira el permiso nuevo con `permisos_efectivos(persona, None)` y el permiso se agrega a `catalogo.py` y a `PERMISOS_SENSIBLES`. Con D2 b, después de crear: `logger.info("Superusuario %s creado por %s", usuario.correo, request.user.correo)`.
  - **Comprobación:** las pruebas de B1.4.
- [x] **B1.4** · explicado (la primera) y tuyo (las demás) · `Backend/Admind_Backend/apps/cuentas/test_superusuarios.py` (nuevo; importa los ayudantes de `apps/cuentas/tests.py`)
  - **Qué:** cinco pruebas:
    1. Un Superusuario crea otro: 201, y la asignación nueva es `rol=superusuario` con `conjunto` nulo.
    2. Un Administrador, aun con su conjunto activo elegido, recibe 403 y no se crea nada.
    3. Un documento repetido responde 400 con el error en `numero_documento`.
    4. Si se manda `"rol": "residente"` en el cuerpo, igual queda Superusuario (el campo no existe).
    5. El nuevo inicia sesión y su `dos_factores.requerido` es verdadero.
  - **Concepto:** probar el permiso por los dos lados (quien sí puede y quien no) y que la base hace cumplir el conjunto nulo.
  - **Comprobación:** `./.venv/Scripts/python.exe -m pytest -q apps/cuentas/test_superusuarios.py`.

**Cierre de F1**

- **Verificación:** la suite completa del backend en verde, con cinco pruebas más que en F0.
- **Explicar de vuelta:** «cuéntame qué pasa desde que llega el POST a `/auth/superusuarios/` hasta que queda la fila en `Asignacion`, y por qué esta vista no hereda de `VistaDeConjunto`».
- **Pregunta de jurado:** «Si un Superusuario puede crear a otro, ¿qué impide que un administrador se cree uno?» (Respuesta: la vista mira el rol de plataforma de quien pide, no sus permisos en el conjunto activo, y la prueba 2 lo fija).
- **Commit sugerido:** `feat(cuentas): alta de Superusuarios desde la plataforma [HU-06]`

## F2 · El botón y la pantalla en el front

**Deja funcionando:** el Superusuario ve «Crear superusuario» en `/conjuntos/`, llena el formulario y vuelve al selector con un aviso; nadie más ve el botón ni abre la pantalla.

**Concepto de la fase:** el front esconde el botón por comodidad, pero **quien protege es la API**: aunque alguien escriba la URL a mano, el backend responde 403.

- [x] **B2.1** · tuyo (modelo: `crear_usuario`) · `Frontend/Admind_Front-End/cliente_api/cuentas.py`
  - **Qué:** `crear_superusuario(request, datos)` → `POST auth/superusuarios/`.
  - **Comprobación:** se importa sin error.
- [x] **B2.2** · tuyo (modelo: `AdministradorForm`) · `Frontend/Admind_Front-End/apps/conjuntos/forms.py`
  - **Qué:** `SuperusuarioForm(UsuarioForm)` con el mismo `__init__` que `AdministradorForm` (quita `rol`, pone la clase a los campos).
  - **Qué cambia respecto al modelo:** **sin** el `clean` que fija el rol. No hereda de `AdministradorForm` justamente por ese `clean`.
  - **Comprobación:** `SuperusuarioForm().fields` no tiene `rol`.
- [x] **B2.3** · explicado · `Frontend/Admind_Front-End/apps/conjuntos/views.py` y `urls.py`
  - **Qué:** la función `es_superusuario(request)` (P5), que pasa a usar también la vista `resumen`; la vista `nuevo_superusuario`; la ruta `path("superusuarios/nuevo/", views.nuevo_superusuario, name="superusuario-nuevo")`; y en `selector`, dos claves más en el contexto: `"es_superusuario": es_superusuario(request)` y `"superusuario_creado": request.GET.get("superusuario") == "creado"`.
  - **Concepto:** el mismo patrón de `nuevo` (formulario → cliente_api → errores de la API al formulario → redirect), más una guarda de entrada.
  - **Forma:**
    ```python
    def es_superusuario(request):
        return "Superusuario" in request.session.get("roles", [])


    @require_http_methods(["GET", "POST"])
    def nuevo_superusuario(request):
        """La cuenta de otro integrante del equipo, desde el selector. Solo la abre un Superusuario."""
        if not es_superusuario(request):
            return redirect("conjuntos:selector")
        formulario = SuperusuarioForm(request.POST or None)
        if request.method == "POST" and formulario.is_valid():
            try:
                api_cuentas.crear_superusuario(request, formulario.cleaned_data)
            except ApiNoDisponible:
                formulario.add_error(None, MENSAJE_API_NO_DISPONIBLE)
            except ErrorDeApi as error:
                errores_de_la_api_al_formulario(formulario, error)
            else:
                return redirect(f"{reverse('conjuntos:selector')}?superusuario=creado")
        return render(request, "conjuntos/superusuario_nuevo.html", {"formulario": formulario})
    ```
    Importar `reverse` si no está.
  - **Comprobación:** las pruebas de B2.5.
- [x] **B2.4** · tuyo (modelo: `asistente_administracion.html` y el bloque `puede_crear` de `selector.html`) · `templates/conjuntos/superusuario_nuevo.html` (nuevo) y `selector.html`
  - **Qué:** la pantalla con el formulario, un texto corto («La cuenta tendrá acceso a todos los conjuntos y deberá configurar la verificación en dos pasos al entrar») y un enlace para volver al selector. En el selector, dentro de `.acciones`, el botón «Crear superusuario» con `{% if es_superusuario %}`, y arriba, con `{% if superusuario_creado %}`, un `am-alerta` de éxito.
  - **Qué cambia respecto al modelo:** no lleva los pasos del asistente (`_pasos.html`) ni el resumen del conjunto, porque no hay conjunto.
  - **Comprobación:** abrir la pantalla en el navegador como Superusuario.
- [x] **B2.5** · explicado (la primera) y tuyo (las demás) · `Frontend/Admind_Front-End/tests/test_superusuarios.py` (nuevo)
  - **Qué:** con `cliente_con_sesion(conjunto_activo=None, roles=["Superusuario"], tipo_usuario="Superusuario")` y la API simulada con `mock.patch("cliente_api.cuentas.crear_superusuario")`:
    1. El selector muestra «Crear superusuario» a un Superusuario y no a un Administrador.
    2. Un Administrador que abre `/conjuntos/superusuarios/nuevo/` vuelve al selector.
    3. Un POST válido llama a la API sin `rol` y redirige a `/conjuntos/?superusuario=creado`.
    4. Un `ErrorDeApi` con `numero_documento` aparece en el formulario.
  - **Comprobación:** `./.venv/Scripts/python.exe -m pytest -q tests/test_superusuarios.py`.

**Cierre de F2**

- **Verificación:** la suite completa del front en verde, con cuatro pruebas más que en F0, y el guion de prueba manual de abajo.
- **Explicar de vuelta:** «¿qué pasa si un Administrador escribe a mano `/conjuntos/superusuarios/nuevo/`? ¿Y si se salta el front y hace el POST directo a la API?».
- **Pregunta de jurado:** «¿Por qué no dejaron que el Superusuario cree secretarías desde esta misma pantalla, escogiendo el conjunto?» (Respuesta: el conjunto nunca viaja en la petición; sale de la sesión. Para crear en un conjunto, el Superusuario entra a él).
- **Commit sugerido:** `feat(conjuntos): crear superusuario desde el selector [HU-06]`

## Cierre del plan

1. Las dos suites en verde y `makemigrations --check --dry-run` sin nada nuevo por este plan.
2. Informe final en el chat: qué se hizo por fase, desviaciones y conceptos por repasar.
3. [actualizar_contexto](../../09_Protocolos/actualizar_contexto.md): la decisión del 2026-10-30 y las respuestas D1 a D3 a [construccion](../../06_Decisiones/construccion.md); [permisos](../../05_Modulos/permisos.md) y [cuentas](../../05_Modulos/cuentas.md) con el endpoint nuevo; *falta contárselo a Camilo*.
4. Mover este plan a `hechos/` según [abrir_y_cerrar_un_plan](../../09_Protocolos/abrir_y_cerrar_un_plan.md).

## Lo que el agente no puede hacer

- Abrir los PR de `feat/superusuarios-desde-selector` a `desarrollo`: los hace Alejo.
- La prueba manual de quien no programó (Camilo), con el guion de abajo.

## Guion de prueba manual

1. Entrar como Superusuario. En `/conjuntos/` aparece «Crear superusuario».
2. Crear uno con documento y correo nuevos. Vuelve al selector con el aviso de éxito.
3. Intentar otro con el mismo documento: el error sale en el campo del documento.
4. Cerrar sesión y entrar con la cuenta nueva: pide configurar la verificación en dos pasos. Al terminar, ve todos los conjuntos, también los dados de baja.
5. Entrar como Administrador: el botón no aparece y `/conjuntos/superusuarios/nuevo/` devuelve al selector.
6. En `admind_db`: la asignación nueva tiene rol `superusuario` y `conjunto` vacío.

## Fuera de este plan

- Crear cuentas de conjunto desde el selector escogiendo el conjunto (descartado: rompe el aislamiento).
- Administrador sin conjunto que arranca vacío (descartado el 2026-10-30: necesitaría un rol nuevo y cambiar el diagrama de clases).
- Quitar o eximir el segundo factor (descartado el 2026-10-30). Para la sustentación, los jurados entran con cuentas de Residente o Vigilancia, que no exigen 2FA.
- Ascender a Superusuario a alguien que ya tiene cuenta (D3 b).
- Retirar el rol de Superusuario desde la interfaz. El guardarraíl *no puede revocarse a sí mismo el último rol de Superusuario* aplicará cuando exista.

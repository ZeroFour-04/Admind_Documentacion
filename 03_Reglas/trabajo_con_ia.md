---
resumen: "Cómo trabaja un agente de IA en AdMind: construir solo lo pedido, qué no hacer, qué preguntar en vez de decidir y cómo pedirle."
tipo: regla
origen: "maestro v1.4 (2026-09-14) cabecera y §8.4 + Lab §2, §8 y §9 (2026-09-14) + guía de desarrollo §11 y §12 (2026-09-15)"
actualizado: 2026-10-04
---

# Trabajo con agentes de IA

## Lo primero

1. Las **contradicciones abiertas** están en [abiertas](../06_Decisiones/abiertas.md). Si tu tarea toca alguna, **pregunta; no elijas por tu cuenta**.
2. [decidido_y_propuesto](../06_Decisiones/decidido_y_propuesto.md) separa lo decidido de lo propuesto. No trates una propuesta como un hecho.
3. Las **restricciones legales** ([legal](../01_Contexto/legal.md)) están por encima de todo. Un requisito prohibido no se implementa ni detrás de un permiso de administrador.
4. Las **decisiones de arquitectura** ([cerradas](../06_Decisiones/cerradas.md)) están cerradas con razón escrita. Si tu propuesta contradice una, dilo explícitamente en vez de reabrirla en silencio.
5. El criterio de corte del proyecto no es la funcionalidad, es la **defendibilidad en sustentación**. Ante dos soluciones, gana la que el equipo pueda explicar en voz alta.

## Disciplina de trabajo con IA (maestro §8.4)

> [!WARNING] Reversión deliberada — 2026-09-14
> Hasta esta fecha regía un **modo tutor estricto**: la IA explicaba, revisaba y ponía ejercicios, pero no escribía código del producto, y el filtro de abajo era de entrada al repositorio. **El plazo de entrega se redujo a un mes** y no hay que entregar el proyecto completo (§11). Con un equipo de dos que apenas está aprendiendo, ese modo no llega a tiempo, así que Alejo decidió que **la IA construya, pero solo lo que se le pide**. Django y las API se aprenden sobre la marcha. El protocolo operativo está más abajo, en *Cómo debe ayudar un agente*.

> [!TIP] El filtro de una sola pregunta **¿Puedo explicar esto ante el jurado?** Hasta el 2026-09-14, si la respuesta era no, no entraba al repositorio. Ahora puede entrar, pero lo que se vaya a defender se entiende antes de la sustentación.

- **La IA construye lo que se le pide, con el alcance exacto del pedido.** Lo que haga falta fuera de él lo avisa y no lo hace
- El diseño del motor de reglas se piensa en papel primero; la IA implementa lo ya especificado
- Las pruebas del núcleo las escribe o revisa el equipo línea por línea
- Bitácora de decisiones (ADR): qué se decidió, qué se descartó, por qué
- Commits pequeños con historial coherente. Conventional Commits con el ID de la historia: `feat(reservas): agregar bloqueo de 3 minutos [HU-11]`
- **Congelar el contrato de la API en el Planning**, antes de programar, para que ambos avancen sin bloquearse
- **Rotar** capas por sprint: si uno hace siempre lo mismo, termina el semestre sabiendo la mitad
- Declarar el uso de IA en la documentación si el curso lo permite. Desde el cambio del 2026-09-14 esto pesa más

**Lo que ayuda:** pedir piezas concretas en vez de módulos enteros · preguntar _por qué_ sobre lo que la IA entregó · pedir el concepto explicado de tres formas · pedir preguntas de jurado sobre el código propio. **Lo que lo arruina:** aceptar código que funciona sin abrirlo y seguir. Se siente como avanzar y llega a la sustentación sin poder explicarlo.

**El techo del proyecto no es cuánto código se puede generar, es cuánto se puede defender en la sustentación.**

## Cómo debe ayudar un agente (Lab §2)

> [!WARNING] Reversión deliberada — 2026-09-14
> Hasta esta fecha el agente solo orientaba: Alejo escribía todo el código, y el agente explicaba, revisaba sin corregir y ponía ejercicios. **El plazo de entrega se redujo a un mes** y no hay que entregar el proyecto completo. Con un equipo de dos que apenas está aprendiendo, ese modo no llega a tiempo, así que Alejo decidió dejarlo a un lado: **el agente construye, pero solo lo que Alejo le pide.** Queda escrito como reversión y no se borra, como pide el §9 del maestro.

> [!NOTE] Plan guiado — 2026-10-04
> Desde esta fecha las funcionalidades se trabajan con **planes guiados**: un chat de planeación escribe el plan ([Inicio](../Inicio.md)) y Alejo lo ejecuta en otro chat con un agente que **guía en vez de construir** ([ejecutar_plan_guiado](../09_Protocolos/ejecutar_plan_guiado.md)). El agente solo guía si el plan es guiado **y** Alejo lo aprueba cuando se lo pregunta; si no, vale lo de abajo.

### Construir a pedido — el modo por defecto

1. **Se construye exactamente lo pedido.** Ni un modelo, una vista, una prueba o un archivo de más. Nada de "de paso también arreglé…".
2. **Lo que haga falta fuera del pedido se avisa, no se hace.** Una dependencia, una migración, un error que se ve en código vecino, una carpeta que no existe: se dice en una línea y se espera respuesta.
3. **Si el alcance es ambiguo, se toma la lectura más estrecha y se dice cuál fue.** Se pregunta antes solo cuando las dos lecturas llevan a trabajos muy distintos.
4. **Al entregar, un resumen corto:** qué archivos se tocaron, qué hace cada pieza y qué decisión técnica hay ahí que el jurado podría preguntar. La explicación a fondo, solo si la pide.
5. **Construir no autoriza a decidir.** Siguen siendo preguntas las contradicciones del maestro (§12), el recorte de alcance para el plazo nuevo y todo lo de la sección *Lo que un agente debe preguntar en vez de decidir*.

### Orientar — cuando Alejo la pida

Alejo tiene que sustentar, así que va a seguir pidiendo orientación. Cuando la pida:

- Se explica en serio lo que pregunte, **incluido el código que escribió el agente**: qué hace, por qué así y qué se descartó
- Si pide preparar la sustentación, se ponen preguntas de jurado sobre ese código
- No se convierte cada entrega en un ejercicio ni se le pide que la reescriba él, salvo que lo pida

### El filtro, con el plazo nuevo

> [!TIP] ¿Puedo explicar esto ante el jurado?
> Hasta el 2026-09-14 era un filtro de entrada: si Alejo no podía explicar una línea, no entraba al repositorio. Ahora es una meta de sustentación: lo que construye el agente sí entra, y lo que se vaya a defender se entiende antes de llegar al jurado.

La tutoría dentro de un ejercicio del lab (pistas graduadas, sin dar la solución) sigue en `Archivo/Lab/Admind_Lab.md` §2.4.

## Lo que un agente no debe hacer (Lab §8)

- **Construir más de lo que Alejo pidió**, ni siquiera "de paso". Lo que falte se avisa.
- **Escribir el código de solución de un ejercicio del lab**, ni "para que lo uses de ejemplo". Fuera del lab, construir lo pedido sí es su trabajo.
- **Proponer ramas por historia.** El modelo de ramas es requisito del curso.
- **Subir código del lab a `desarrollo`**, por merge, *cherry-pick* o copia.
- **Usar `Backend.zip`** como referencia: es la demo descartada, hecha con IA.
- **Resolver las contradicciones abiertas del maestro (§12)**, en especial el stack del frontend (§12.1). Se pregunta.
- **Recortar alcance o repartir el mes en sprints** por su cuenta (maestro §12.8). Se pregunta.
- **Proponer Tailwind, Bootstrap o un framework de componentes.** El sistema visual es CSS propio sobre variables.
- **Sustituir PostgreSQL por SQLite** para simplificar.
- **Dar por cerrado un ejercicio** sin que Alejo responda las preguntas de jurado.

## Lo que un agente debe preguntar en vez de decidir (Lab §9)

Corte 2026-09-14. Cómo va cada pregunta hoy: [abiertas](../06_Decisiones/abiertas.md).

- ¿Cuál es la fecha exacta de entrega, y qué se entrega en ese mes? Hasta que se decida, se construye lo que Alejo pida.
- ¿Cuántos sprints caben en el mes y cuándo arranca el primero? El plan de siete sprints de dos semanas (maestro §11.2) ya no cabe.
- ¿Qué significa exactamente la rama `pruebas` para el profesor: ambiente de pruebas en una cadena `desarrollo → pruebas → main`, u otra cosa?
- ¿El stack de frontend ya se cerró (§12.1)? Sin eso no arranca el Sprint 1, pero **la Fase 0 no depende de esa decisión**.
- ¿La rama `lab` se sube al remoto o se queda local?
- ¿Cuál manda en lo visual: `design-system/` o el §6 del maestro? Por ahora se trabaja con **un solo acento**.

## Cuándo parar y preguntar (guía de desarrollo §11)

Construir no autoriza a decidir. Hay dos niveles:

**Preguntar antes de construir** (es decisión de equipo o del profesor):

- Todo lo que toque una **contradicción abierta del maestro §12**: el stack del frontend, sesión o token, "un solo bloqueo en todo el sistema" contra "toda clave única incluye el conjunto".
- Los **choques del esquema de referencia con el maestro** ([pendientes](../08_Estado/pendientes.md)): `asignacion.conjunto_id`, roles y permisos como tablas, estados de `reserva`, `clasificacion` de áreas, columnas `*_por` sin destino claro.
- **Alcance:** algo Condicional o Fuera de alcance (maestro §3.3 y §3.4), o qué entra en el mes (§12.8).
- **La ley** (maestro §4): si hay duda, no se implementa hasta resolverla.
- **Un permiso o un rol nuevo**, o un cambio al catálogo (maestro §5.3).
- **Una tabla global nueva** (R12).
- **Un componente, un token o un color nuevo**, o el acento en un quinto sitio (maestro §6).
- **Cambiar `Persona` o `Usuario`**: las usa todo el sistema.
- **Cualquier cosa que borre datos.**

**Avisar al otro integrante** (no es decisión, pero tiene que enterarse):

- Una migración nueva, sobre todo si es en una app que el otro también toca.
- Un paquete nuevo en `requirements.txt`.
- Un cambio en `apps/comun/` o en `config/`, que afecta a todas las apps.
- Un cambio en el contrato JSON de un endpoint que el otro ya está consumiendo.

## Cómo pedirle a un agente (guía de desarrollo §12)

**Decidido (maestro §8.4, Lab §2):** desde el 2026-09-14 la IA **construye lo que se le pide, con el alcance exacto**. Lo que haga falta fuera del pedido lo avisa y no lo hace.

**Cómo pedir bien:** historia, capa, archivo y criterio. Mientras más concreto, menos inventa.

| Pedido vago | Pedido concreto |
|---|---|
| "Hazme el módulo de reservas" | "Para HU-09, escribe en `apps/areas/repositories.py` y `services.py` el listado de áreas del conjunto activo, siguiendo la §3 de la Guía de desarrollo. Todavía sin vista" |
| "Arregla las pruebas" | "`pytest apps/personas` falla en `test_documento_con_puntos`. Este es el error completo: …" |
| "Haz la pantalla de áreas" | "Con el contrato JSON de la HU-09, crea la vista y la plantilla de `apps/areas/` en el frontend, usando `am-tabla` y el estado vacío" |

**Lo que conviene pedirle siempre:**

- Que lea `AGENTS.md`, las notas que apliquen y el README de la carpeta antes de empezar.
- Al terminar, un resumen: qué archivos tocó, qué hace cada pieza y qué decisión podría preguntar el jurado.
- "¿Por qué así y no de otra forma?" sobre lo que no entiendas. El jurado les va a preguntar a los dos.

**Lo que arruina el proyecto:** aceptar código que funciona sin abrirlo y seguir. Se siente como avanzar y llega a la sustentación sin poder explicarlo (maestro §8.4).

## Ver también

- [backlog_y_plazo](../08_Estado/backlog_y_plazo.md) — maestro §11

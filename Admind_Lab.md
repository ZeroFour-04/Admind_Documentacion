---
titulo: "AdMind — Lab: documento de contexto"
proyecto: "Proyecto de Ingeniería de Software II — Universidad de Cundinamarca, Facatativá"
fecha: 2026-09-11
proposito: "Contexto completo para cualquier agente de IA que acompañe a Alejo mientras aprende programando AdMind. Se lee entero antes de proponer nada."
---

# AdMind — Lab

> [!IMPORTANT] Si eres un agente de IA, lee esto primero
>
> 1. Lee este archivo completo y después `Admin_Master.md`, que está en esta misma carpeta. El maestro manda sobre el producto; este documento manda sobre **cómo se trabaja aquí**.
> 2. **Tu trabajo no es escribir el código. Es que Alejo lo escriba y lo entienda.** La sección 2 es una regla operativa, no una preferencia de estilo.
> 3. Si tu tarea toca una contradicción abierta del maestro (§12), **pregunta; no elijas por tu cuenta**.
> 4. Cuando dudes entre resolverle algo y hacerle una pregunta, haz la pregunta.

---

## 1. Qué es el lab y qué no

**El lab es el sitio donde Alejo aprende rompiendo cosas, dentro del repositorio real pero sin tocar lo que se entrega.**

- **Es** una rama `lab` en `Backend/Admind_Backend`, y más adelante otra en el repositorio del frontend.
- **Es** de una sola persona: Alejo. Camilo no lo usa, porque tiene más experiencia escribiendo código.
- **No es** el producto. Nada que se escriba aquí llega a `desarrollo` por merge, ni por *cherry-pick*, ni copiando y pegando.
- **No es** un curso ni un repositorio de ejemplos. Cada ejercicio existe porque una historia de AdMind lo va a necesitar.

**El objetivo, en una frase:** llegar a la sustentación pudiendo explicar cada línea del repositorio en voz alta, sin mirarla.

> [!NOTE] Por qué existe
> En septiembre se construyó una demo entera con IA y se descartó, porque el equipo no sabía cómo funcionaba. El techo de este proyecto no es cuánto código se puede generar: es cuánto se puede defender ante el jurado.

---

## 2. Cómo debe ayudar un agente

### 2.1 El ciclo, igual para cada cosa que se construya

1. **Antes de escribir código, Alejo explica el plan en 3 a 5 líneas.** El agente lo cuestiona. Aquí muere la mitad de los errores.
2. **Escribe Alejo.** Si se atasca, pelea 30 a 45 minutos de verdad (leer el error completo, leer la documentación) y después pide una pista.
3. **Las pruebas deciden si funciona**, no el agente. El ejercicio termina con `pytest` en verde.
4. **Revisión sin corrección.** El agente señala problemas con preguntas; Alejo los arregla.
5. **Preguntas de jurado antes de dar algo por terminado.** Tres a cinco preguntas sobre su propio código. Si no las responde, el ejercicio no está terminado.

### 2.2 Pistas graduadas

| Nivel | Qué da el agente |
| --- | --- |
| Pista 1 | Dónde mirar: el concepto, la sección de la documentación |
| Pista 2 | Qué está mal: la línea o la idea equivocada |
| Pista 3 | Un ejemplo parecido **en otro contexto**, nunca su código resuelto |
| Excepcional | La solución completa, explicada línea por línea. Entonces Alejo la borra y la reescribe sin mirar al día siguiente. Si no puede, no la entendió |

### 2.3 Reparto de quién escribe qué

- **El agente escribe las pruebas del ejercicio.** Son la especificación ejecutable: convierten el criterio de salida en un semáforo.
- **Alejo escribe el código que las pone en verde.**
- En el repositorio de producto la cosa se invierte: allí **las pruebas también las escribe Alejo**, y el agente solo revisa. Leer primero unas pruebas bien escritas es justamente el entrenamiento.

### 2.4 El filtro de una sola pregunta

> [!TIP] ¿Puedo explicar esta línea, en voz alta, sin mirarla?
> Si la respuesta es no, no entra al repositorio. Da igual que funcione.

---

## 3. Dónde vive el lab y cómo se mueve el código

**Modelo de ramas fijado por el profesor** (ver §8.5 del maestro). Inicialmente hay tres ramas y ninguna más:

```
main         lo entregado; recibe de pruebas al cerrar el sprint
desarrollo   integración; los dos integrantes trabajan directamente aquí
pruebas      lo terminado, listo para probar
lab          práctica de Alejo; cuarta rama, no oficial
```

**No hay ramas por historia.** El agente no debe proponerlas: es instrucción del curso. La trazabilidad entre código e historia va en el mensaje del commit: `feat(reservas): agregar bloqueo de 3 minutos [HU-11]`.

**Las tres reglas del lab:**

1. **`desarrollo` puede bajar al lab; el lab nunca sube.** Se trae el código real para practicar sobre él, y no vuelve nada.
2. **Lo que funcionó en el lab se reescribe desde cero** en `desarrollo`, sin mirar. Esa reescritura es la prueba de que se aprendió.
3. **Un ejercicio responde una sola pregunta.** Vive en su carpeta (`laboratorio/01-poo-persona/`, `laboratorio/02-sql-fk-compuesta/`, …) y dura de horas a un día.

**Pendiente:** confirmar con el profesor si acepta que la rama `lab` exista en GitHub. Si no, se queda solo en la máquina de Alejo.

---

## 4. Entorno de la máquina

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

---

## 5. El equipo y el contexto mínimo

**Dos personas.** **Alejo** (Manuel Alejandro Aldana Rincón) parte de Python básico, lidera la documentación y es quien recorre esta ruta. **Camilo** tiene más experiencia escribiendo código. La ruta de aprendizaje llama "Sergio" al compañero: es un error, es Camilo.

**AdMind en cinco líneas.** Aplicación web para administrar conjuntos residenciales bajo la Ley 675 de 2001, con una sola base de datos para todas las copropiedades. Cuatro pilares: multiconjunto con aislamiento estricto, motor de reglas configurable por copropiedad, reserva de zonas comunes por orden de llegada con bloqueo de 3 minutos y decisión humana, y un sistema que registra pero no decide. El detalle está en `Admin_Master.md`; **este resumen no sustituye leerlo**.

**Lo que hace difícil a AdMind**, y por lo tanto lo que el lab entrena:

1. Aislamiento entre conjuntos, en la base de datos y en la capa de acceso (R6)
2. Concurrencia real sobre una franja escasa: bloqueo exclusivo de 3 minutos (R1, R7, HU-11)
3. Auditoría de solo inserción, que no es código sino privilegios de PostgreSQL
4. 2FA para permisos sensibles

---

## 6. Catálogo de ejercicios

Tomados de la ruta de aprendizaje, que vive en
`G:\Mi unidad\U N I V E R S I D A D\SEXTO SEMESTRE\Ingles III\Tareas\Brochure\Ruta de aprendizaje - Desarrollo AdMind.md`.

### Fase 0 — los cimientos

| # | Ejercicio | Criterio de salida |
| --- | --- | --- |
| 0.1 | **Git.** Provocar un conflicto a propósito sobre la misma línea y resolverlo desde la terminal | Explicarle a Camilo, en voz alta y sin apuntes, qué pasó y por qué Git no pudo decidir solo |
| 0.2 | **POO.** `Persona`, `Conjunto` y `Asignacion` en Python puro, sin base de datos ni framework. `Persona` normaliza el documento al construirse | `Persona("CC", "1.032.456.789")` y `Persona("CC", "1032456789")` guardan el mismo número, y Alejo explica por qué la normalización ocurre al escribir y no al leer |
| 0.3 | **SQL.** Crear a mano `conjuntos`, `areas` y `reservas` en el Postgres local, con clave única `(id, conjunto_id)` en `areas` y una FK compuesta desde `reservas` | Insertar una reserva del conjunto 1 que apunte a un área del conjunto 2 y que **la base de datos la rechace**. Guardar la captura: es el blindaje de R6 funcionando y sirve en la sustentación |
| 0.4 | **HTTP.** Peticiones con `curl` contra una API pública; provocar un 404 y un 400 a propósito | Dibujar en papel el viaje completo desde "el residente oprime Reservar" hasta "la base de datos guarda la fila", nombrando cada pieza |
| 0.5 | **HTML y CSS.** Maquetar estática la pantalla de confirmación de contenido: área, **día de la semana en letras**, fecha, horario, asistentes, y los botones Corregir y Enviar | Se ve razonable en un teléfono y en un computador. Va en el lab del repositorio de frontend |

> [!NOTE] El 0.1 se va a dar solo
> Con `desarrollo` compartida entre dos personas, el primer conflicto real aparece al hacer `pull`. Cuando Git pida elegir entre *merge* y *rebase*, ese es el momento de aprender la diferencia, no de copiar el comando que aparezca primero.

### El spike de concurrencia — el ejercicio que importa

Corresponde a M3 y M4 del proyecto espejo y a HU-11, la historia de 7 SP que sirve de referencia de velocidad. **Si se resuelve en el lab, se resolvió la parte más difícil del proyecto antes de que llegue su sprint.**

Debe funcionar:

- Con dos navegadores abiertos sobre la misma franja, **solo uno** consigue el bloqueo
- Si vencen los 3 minutos sin enviar, la franja vuelve a estar libre **sin ningún proceso corriendo en segundo plano**
- N solicitudes simultáneas producen **exactamente un** bloqueo

> [!WARNING] Estas dos preguntas no se responden en este documento, a propósito
> - ¿Qué fila bloquea `select_for_update` cuando la franja está **libre**?
> - ¿Qué pasa con el índice único parcial cuando un bloqueo **ya venció** pero nadie lo ha vuelto a tocar?
>
> Son el centro del ejercicio. Un agente puede dar pistas de nivel 1 y 2; no la respuesta.

---

## 7. La bitácora de errores

Vive en el repositorio de documentación y se escribe **el mismo día**. Una entrada por error resuelto:

```
Fecha · Ejercicio
Síntoma:     qué vi en pantalla
Causa:       qué estaba pasando de verdad
Solución:    qué cambié
Aprendizaje: qué sé ahora que no sabía
Tiempo:      cuánto me tomó
```

Sirve para tres cosas a la vez: consolida lo aprendido, da el dato de "tiempo dedicado a aprender" que la retrospectiva del Sprint 1 necesita, y ante un jurado que sospeche de la IA es la prueba de autoría más fuerte que existe.

---

## 8. Lo que un agente no debe hacer

- **Escribir el código de solución** de un ejercicio, ni "para que lo uses de ejemplo".
- **Proponer ramas por historia.** El modelo de ramas es requisito del curso.
- **Subir código del lab a `desarrollo`**, por merge, *cherry-pick* o copia.
- **Usar `Backend.zip`** como referencia: es la demo descartada, hecha con IA.
- **Resolver las contradicciones abiertas del maestro (§12)**, en especial el stack del frontend (§12.1). Se pregunta.
- **Proponer Tailwind, Bootstrap o un framework de componentes.** El sistema visual es CSS propio sobre variables.
- **Sustituir PostgreSQL por SQLite** para simplificar.
- **Dar por cerrado un ejercicio** sin que Alejo responda las preguntas de jurado.

---

## 9. Lo que un agente debe preguntar en vez de decidir

- ¿Qué fecha arranca el Sprint 1? Condiciona todo el calendario de la Fase 0.
- ¿Qué significa exactamente la rama `pruebas` para el profesor: ambiente de pruebas en una cadena `desarrollo → pruebas → main`, u otra cosa?
- ¿El stack de frontend ya se cerró (§12.1)? Sin eso no arranca el Sprint 1, pero **la Fase 0 no depende de esa decisión**.
- ¿La rama `lab` se sube al remoto o se queda local?
- ¿Cuál manda en lo visual: `design-system/` o el §6 del maestro? Por ahora se trabaja con **un solo acento**.

---

## 10. Estado actual

**Al 2026-09-11:** cero líneas de código de producto. Sprint 1 sin iniciar. El repositorio `Backend/Admind_Backend` solo tiene dos commits de práctica y las ramas todavía no están creadas.

**Siguiente paso, en orden:**

1. Dejar `main` limpio con un commit, y crear `desarrollo`, `pruebas` y `lab`.
2. Proteger `main` y `pruebas` en GitHub exigiendo PR con una aprobación; `desarrollo` queda abierta.
3. Ejercicio 0.2 con el ciclo completo de la sección 2, para probar el método en algo pequeño.
4. Ejercicio 0.3, que es el de mayor rendimiento de toda la ruta.

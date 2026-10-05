---
resumen: "Cómo ejecuta un agente un plan guiado, solo si Alejo lo aprueba al preguntarle: explica por bloques, Alejo aplica el código, explica de vuelta cada fase y el avance se anota en el plan."
tipo: protocolo
origen: "proceso acordado con Alejo el 2026-10-04"
actualizado: 2026-10-04
---

# Protocolo: ejecutar un plan guiado

## Cuándo

Solo si se cumplen las dos cosas:

1. El plan que Alejo pide ejecutar lleva `modo: guiado` en el frontmatter.
2. **Alejo lo aprueba.** Pregúntaselo al empezar cada sesión, antes de hacer nada: «Este plan es guiado. ¿Lo trabajamos así, te explico por bloques y tú aplicas, o lo construyo yo?».

Sin las dos, construyes. No entras en este modo por tu cuenta, ni siquiera con un plan guiado delante: hay días en que Alejo necesita que el agente lo haga todo, por tiempo.

Cómo se escribe un plan guiado: [Inicio](../Inicio.md).

### Si Alejo dice que construyas

- El plan se ejecuta como cualquier otro: *Ejecutar* en [abrir_y_cerrar_un_plan](abrir_y_cerrar_un_plan.md) y *Construir a pedido* en [trabajo_con_ia](../03_Reglas/trabajo_con_ia.md). Los bloques `tuyo` también los construyes.
- El seguimiento se lleva igual, con `construida` en la columna *Modo*. Así Alejo sabe qué fases le falta estudiar.
- Al cerrar cada fase, el resumen corto de construir a pedido: archivos tocados, qué hace cada pieza y qué podría preguntar el jurado.

### Cambiar a mitad del plan

Alejo puede cambiar de modo cuando quiera: «el resto hazlo tú», «esta fase sí explícamela». El cambio vale desde ese punto y lo pide él. No lo propongas ni vuelvas a preguntar en cada fase.

## Qué cambia en modo guiado

Aquí **no construyes: guías**. Alejo aplica el código y tú te aseguras de que entienda lo que queda en el repositorio, porque lo va a sustentar ante un jurado. Tampoco es un curso: la entrega está cerca. La medida de cada fase es que Alejo pueda explicarla en voz alta.

| | Construir a pedido | Plan guiado |
|---|---|---|
| Quién edita el código | El agente | Alejo. El agente, solo si Alejo dice «aplícalo tú» para ese bloque |
| Cuándo se explica | Al entregar, en un resumen | Antes de aplicar, bloque por bloque |
| Una fase está hecha cuando | Pasan las pruebas | Pasan las pruebas y Alejo la explicó de vuelta |
| Commits | Solo si se piden | Los hace Alejo; el agente propone el mensaje |

## Antes de empezar

1. Pregunta el modo y espera la respuesta. Lo que sigue en esta nota vale si Alejo eligió guiado.
2. Lee el plan completo y lo que lista su sección 2.1. Nada más.
3. Mira la sección **Seguimiento**. Si ya hay avance, retoma donde dice; antes confirma con `git status` y las pruebas que el código está como el plan cree.
4. Si falta una *Respuesta* en la sección 3, pídesela a Alejo. No empieza una fase cuya decisión esté vacía.
5. Si el plan está sin empezar, explica el *Mapa de la funcionalidad* en menos de diez líneas y haz la fase F0.

## El ciclo de un bloque

Un bloque a la vez, en este orden. No muestres el siguiente hasta cerrar el actual.

1. **Anuncia** el bloque: archivo, para qué sirve y qué concepto trae. Dos líneas.
2. **Muestra** el código y el punto exacto donde va (después de qué función, dentro de qué clase).
3. **Explica** por partes, no línea por línea: qué hace, por qué se hizo así y no de otra forma, y qué regla del proyecto cumple, citando la nota. Lo que se lee en un minuto.
4. **Alejo lo aplica** y avisa. Si pregunta, se le responde en serio antes de seguir.
5. **Comprueba**: lee el archivo para ver que quedó como debía y corre la comprobación del bloque si la tiene.
6. **Marca la casilla** del bloque en el plan.

### Bloques `tuyo`

El patrón ya se explicó en otro bloque y este lo escribe Alejo.

- Dile cuál es el bloque modelo y qué cambia respecto a él. No des el código.
- Si se traba, pistas en tres niveles y solo hasta el que haga falta: la idea, la estructura (firma y pasos), el código.
- Revisa lo que escribió: señala qué falla y por qué. No lo reescribas en silencio.
- Si Alejo prefiere recibirlo hecho, se trata como un bloque explicado y se anota en *Conceptos por repasar*. Lo mismo si hizo falta el tercer nivel.

## Al cerrar una fase

1. **Verificación.** Corre los comandos del cierre de la fase. Con la suite en rojo no se sigue.
2. **Explicar de vuelta.** Pídele a Alejo que cuente en dos o tres frases qué hace la fase, con la consigna del plan. Corrige lo impreciso sin repetir la explicación entera. Después, la pregunta de jurado.
3. **Commit.** Propón el mensaje con el formato de [git](../03_Reglas/git.md). Lo hace Alejo. Sin `push`.
4. **Seguimiento.** Actualiza la fila de la fase y la línea *Dónde voy*.

Si Alejo quiere saltarse el paso 2, se salta sin insistir: la fila queda como `saltada` y el tema pasa a *Conceptos por repasar*.

## El ritmo lo pone Alejo

- «Más rápido»: explicaciones más cortas y bloques seguidos. El cierre de fase se mantiene.
- «Más despacio» o «no entendí»: otra explicación, desde otro ángulo o con un ejemplo con datos del proyecto. No la misma más larga.
- No conviertas en ejercicio lo que el plan no marcó como `tuyo`.

## Cuándo parar

- El plan nombra un archivo, una función o un campo que no existe o que ya cambió.
- Un paso toca una decisión abierta o algo de *Cuándo parar y preguntar* ([trabajo_con_ia](../03_Reglas/trabajo_con_ia.md)).
- Hace falta algo que el plan no trae: un paquete, una migración no prevista, otra pantalla.

En los tres casos: una línea en *Desviaciones*, se le pregunta a Alejo y no se improvisa. Si el desajuste cambia la forma del plan, Alejo vuelve al chat de planeación.

## Seguimiento

El avance vive en el plan y no en el chat, para que otra sesión pueda retomarlo.

| Qué | Cuándo se actualiza |
|---|---|
| Casilla del bloque | Al comprobarlo |
| Fila de la fase y *Dónde voy* | Al cerrar la fase y cuando Alejo corta la sesión |
| *Desviaciones* | Cuando algo no salió como decía el plan |
| *Conceptos por repasar* | Cuando algo costó o se saltó |

Es lo único del plan que editas, y sin pedir permiso. El resto no se corrige sobre la marcha: lo que cambió va a *Desviaciones*.

## Cerrar el plan

Los cuatro pasos de *Cerrar* en [abrir_y_cerrar_un_plan](abrir_y_cerrar_un_plan.md). El informe final agrega las desviaciones y los conceptos por repasar. Actualizar el contexto no es opcional: el siguiente plan se escribe confiando en las notas.

## Ver también

- [Inicio](../Inicio.md) — cómo escribe el plan el chat de planeación
- [plan_guiado](Plantillas/plan_guiado.md) — la plantilla, con la sección de seguimiento
- [lista_de_salida](../03_Reglas/lista_de_salida.md) — comprobación antes de dar algo por terminado

---
titulo: "AdMind — Plan guiado de <qué cubre>"
tipo: plan
modo: guiado
fecha: AAAA-MM-DD
para: "Alejo, con un agente que guía según 09_Protocolos/ejecutar_plan_guiado.md si Alejo lo aprueba; si no, el agente lo construye"
alcance: "Historia, sección o vista que cubre"
punto_de_partida: "Backend xxxxxxx (N pruebas), Frontend xxxxxxx (N pruebas), sin cambios pendientes"
---

# AdMind — Plan guiado de <qué cubre>

> [!IMPORTANT]
> **Alejo:** llena la columna *Respuesta* de la sección 3. Para empezar o retomar, en un chat nuevo: `Ejecuta el plan Documentacion/Admind_Documentacion/07_Planes/activos/<archivo>.md`. El agente te pregunta primero si lo quieres guiado o si lo construye él.

## 1. Seguimiento

<!-- Lo mantiene el agente que ejecuta, guíe o construya. Quien escribe el plan lo deja en cero, con una fila por fase. -->

**Dónde voy:** sin empezar.

| Fase | Deja funcionando | Estado | Modo | Explicada de vuelta | Verificación | Commit | Fecha |
|---|---|---|---|---|---|---|---|
| F0 | Punto de partida confirmado | pendiente | — | — | | — | |
| F1 | | pendiente | | | | | |

<!-- Estado: pendiente · en curso · hecha. Modo: guiada · construida (la hizo el agente). Explicada de vuelta: sí · saltada · — si fue construida. Verificación: qué se corrió y cómo salió. -->

### Desviaciones

<!-- Una línea por caso: fecha · bloque · qué difería del plan · qué se hizo. -->

Ninguna.

### Conceptos por repasar

<!-- Lo que costó, lo que se saltó y los bloques `tuyo` que terminaron con el código dado. Con las fases construidas por el agente, es la lista de estudio para la sustentación. -->

Ninguno.

## 2. Instrucciones para el agente

> [!IMPORTANT]
> **Primero pregunta.** Antes de tocar nada, pregúntale a Alejo si este plan se trabaja **guiado** (explicas por bloques y él aplica) o si lo **construyes** tú. No entres en modo guiado sin su respuesta.

### 2.1 Qué leer antes de empezar

1. [ejecutar_plan_guiado](../../09_Protocolos/ejecutar_plan_guiado.md): cómo se trabaja este plan en modo guiado y qué cambia si Alejo pide que lo construyas.
2. Este plan completo.
3. <!-- Las notas concretas de 05_Modulos/ y 03_Reglas/ que apliquen, enlazadas, con una frase de para qué sirve cada una. -->
4. <!-- Los README.md de las carpetas de código que se tocan, como ruta relativa al espacio de trabajo. -->

### 2.2 Reglas propias de este plan

<!-- Solo lo que este plan agrega al protocolo y a 03_Reglas/: qué no se toca, qué se avisa a Camilo. -->

## 3. Decisiones que toma Alejo

| ID | Decisión | Opciones | Recomendada | Respuesta |
|---|---|---|---|---|
| D1 | | a) … b) … | a | |

## 4. Decisiones menores que el plan ya fija

| ID | Decisión |
|---|---|
| P1 | |

## 5. Punto de partida verificado

<!-- Lo que se comprobó en el código el día de escribir el plan: commits, árbol limpio, y los archivos, clases y funciones que ya existen y que el plan usa, con su ruta. Aparte, lo que no coincidía entre las notas y el código. -->

## 6. Mapa de la funcionalidad

<!-- Qué va a existir al terminar y por dónde pasa una petición: pantalla → cliente_api → vista → servicio → repositorio → tabla. Diez líneas o un diagrama mermaid. -->

## F0 · Confirmar el punto de partida

- [ ] **B0.1** · Correr las dos suites y `makemigrations --check --dry-run` ([pruebas_y_ejecucion](../../02_Arquitectura/pruebas_y_ejecucion.md)). Tienen que coincidir con el frontmatter; si no, se para y se le avisa a Alejo.

## F1 · <fase>

**Deja funcionando:** <!-- lo que se puede comprobar al terminar -->

**Concepto de la fase:** <!-- la idea que Alejo tiene que poder explicar -->

- [ ] **B1.1** · explicado · `Backend/Admind_Backend/apps/<app>/<archivo>.py`
  - **Qué:** <!-- qué se agrega o cambia, y en qué punto del archivo -->
  - **Concepto:** <!-- lo que enseña este bloque -->
  - **Forma:** <!-- firma, contrato o código -->
  - **Comprobación:** <!-- cómo se ve que quedó bien -->
- [ ] **B1.2** · tuyo (modelo: B1.1) · `<ruta>`
  - **Qué:**
  - **Qué cambia respecto al modelo:**
  - **Comprobación:**

**Cierre de F1**

- **Verificación:** <!-- comando y prueba que tiene que pasar -->
- **Explicar de vuelta:** <!-- la consigna: «cuéntame qué pasa desde que… hasta que…» -->
- **Pregunta de jurado:**
- **Commit sugerido:** `feat(<app>): <qué> [HU-xx]`

## Cierre del plan

<!-- Comandos de verificación finales, informe final (qué se hizo por fase, desviaciones, conceptos por repasar) y actualización del contexto con 09_Protocolos/actualizar_contexto.md. -->

## Lo que el agente no puede hacer

<!-- La parte humana de la DoD: PR desarrollo → pruebas revisado y prueba manual de quien no programó. -->

## Guion de prueba manual

## Fuera de este plan

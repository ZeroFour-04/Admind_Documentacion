---
resumen: "El proyecto espejo: la rama lab, su alcance mínimo y los criterios M1 a M6."
tipo: archivo
origen: "maestro v1.4 (2026-09-14) §7.3"
actualizado: 2026-09-14
---

# El proyecto espejo — la rama `lab` (maestro §7.3)

**El repositorio aparte se descartó.** Su función la cumple una rama `lab` dentro del repositorio real, que **solo usa Alejo** y que **nunca se fusiona** hacia `desarrollo`. Lo que funciona en el lab no sube: se vuelve a construir en `desarrollo` (hasta el 2026-09-14 lo reescribía Alejo sin mirar, como prueba de que aprendió; ver la nota de abajo). El detalle operativo está en `Admind_Lab.md`, que es además lo que lee un agente de IA antes de trabajar en el proyecto.

La razón original sigue en pie —**aprender es romper cosas**, y romper cosas en el repositorio que se va a sustentar es mala idea—, pero una rama que nunca sube da la misma protección sin un tercer repositorio que mantener. Lo que se pierde: el lab arrastra la estructura del repositorio real, así que no es el lienzo en blanco que era MiniAdmind.

> [!NOTE] Desde el 2026-09-14 el lab es opcional
> Con el plazo reducido a un mes (§11), los ejercicios se hacen solo si hay tiempo. Lo que no se ensaye en el lab se construye directamente en el producto, y ya no hace falta reescribirlo sin mirar (§8.4).

Alcance, y no crece: un conjunto, dos usuarios, un área, franjas de una hora, el ciclo mínimo bloquear → solicitar → aprobar/rechazar. Sin correo, sin 2FA, sin auditoría, sin documentos, sin visitantes.

|#|Debe funcionar|
|---|---|
|M1|El residente ve el calendario con franjas libres y ocupadas|
|M2|"Reservar" toma un bloqueo exclusivo y arranca una cuenta de 3 minutos visible|
|M3|**Con dos navegadores abiertos, solo uno consigue el bloqueo**|
|M4|**Si vencen los 3 minutos, la franja se libera sin ningún proceso en segundo plano**|
|M5|El administrador ve la bandeja por antigüedad y aprueba o rechaza con categoría|
|M6|Aprobar exige escribir las condiciones y el texto queda congelado|

**M3 y M4 son el objetivo real.** Son la historia de 7 SP usada como referencia de velocidad. Si se resuelven en el lab, se resolvió la parte más difícil antes de que el sprint que la contiene llegue. Los demás criterios (M1, M2, M5 y M6) son CRUD corriente: se construyen directamente en el producto y no se ensayan aparte.

# 6. Revisar una guía que el alumno ya completó

Una guía o lista que el alumno respondió a mano puede tener respuestas incorrectas. Antes de usarla como material de estudio, revísala.

## Con el kit (sin IA)

Escribe las respuestas en `respostas.json` así: `{"f1": "Estroma", "r2": "Oxígeno"}` (id de la pregunta → respuesta dada)
y ejecuta `python3 -m estudo respostas respostas.json`. El kit muestra lo que no coincide con la fuente, junto con el fragmento.

## En el chat (para una guía que aún no está en el kit)

---

Esta es una guía de estudio que [nombre] completó (foto adjunta) y esta es la fuente (adjunta).
Antes de usarla para estudiar, compara cada respuesta con la fuente.
Por cada respuesta que no coincida, muestra: la pregunta, la respuesta dada, lo que dice la fuente (con el fragmento) y pregúntame qué
hacer. No corrijas nada por tu cuenta ni uses nada que no esté en la fuente.
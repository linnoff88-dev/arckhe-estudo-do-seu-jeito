# 3. Construir con el kit (Claude Code o Codex, dentro de la carpeta del kit)

Abre Claude Code (o Codex) en la carpeta de `estudo-do-seu-jeito` y pega el texto. Pega el `plano.md` justo debajo.

---

Lee el README.md y el skill/estudo-do-seu-jeito/SKILL.md de este kit y sigue la fórmula de 8 pasos.
El plan que definí en el chat está abajo. Los archivos de las fuentes están en [ruta de las fotos/PDF].

1. Crea la materia con `python3 -m estudo nova "[nombre de la materia]"` y completa el nombre del profesor y del estudiante según el plan.
2. Transcribe cada fuente a texto en fontes/ (solo lo que está escrito, sin completar).
3. Escribe los objetivos en objetivos.json con el formato del kit; cada pregunta debe incluir la fuente y el fragmento copiado de la fuente.
4. Ejecuta `python3 -m estudo adicionar objetivos.json`. Si el kit rechaza alguna pregunta, corrige el fragmento o quita la pregunta; nunca inventes una fuente.
5. Para cada objetivo, ejecuta `python3 -m estudo proximo --objetivo <id> --anotar` y muéstrame el método y el porqué.
6. Genera la guía con `python3 -m estudo guia` y dime dónde está el archivo.
7. Al final, ejecuta `python3 -m estudo passos` y muéstrame qué falta.

[Pega aquí el plano.md]
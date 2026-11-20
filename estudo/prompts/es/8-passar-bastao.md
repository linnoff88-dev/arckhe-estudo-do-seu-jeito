# 8. Pasar la posta (el alumno lo usa por su cuenta)

El objetivo final es que quien enseña deje de estar en medio. Cuando el alumno ya usa la guía sin ayuda, puede encargarse de la semana por su cuenta.
Pega esto en Claude Code (o Codex), en la carpeta del kit; quien lo pega es el alumno.

---

Soy [nombre del alumno] y, a partir de hoy, me encargaré de mi guía de estudio por mi cuenta. Lee skill/estudo-do-seu-jeito/SKILL.md.
1. Ejecuta `python3 -m estudo passos` y explícame en 3 líneas en qué punto estoy.
2. Te enviaré las fotos de la clase de esta semana: transcríbelas en fontes/, crea los objetivos y ejecuta `adicionar`.
3. Importa mis resultados con `python3 -m estudo importar resultados.json` y muéstrame el marcador de los métodos.
4. Para cada objetivo que aún no domine, ejecuta `python3 -m estudo proximo --objetivo <id> --anotar` y dime por qué.
5. Genera la nueva guía. No inventes contenido fuera de las fuentes.
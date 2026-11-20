# 5. Cada semana: el material nuevo se incorpora como fuente y se convierte en objetivo (chat o Claude Code)

Después de cada clase, el estudiante fotografía sus apuntes y envía la guía del profesor.

## 5a. Transcribir (una foto o un PDF por vez)

---

Transcribe el texto de esta foto exactamente como aparece, en texto simple. No corrijas el contenido, no completes
frases ni agregues nada. Donde no se pueda leer, escribe [ilegible]. Dibujo o esquema: descríbelo en una línea
entre corchetes, ej.: [esquema: glucosa → piruvato, con flecha].

---

Guarda como `fontes/<aula>.txt` y ejecuta `python3 -m estudo semana fontes/<aula>.txt`.

## 5b. Transformar la fuente en objetivos (formato del kit)

---

Basándote solo en las fuentes adjuntas, escribe los objetivos de esta semana en JSON, con este formato:

{"objetivos": [{"id": "curto-sem-espaco", "titulo": "...", "topicos": ["..."], "fontes": ["arquivo.txt"],
  "leitura": "explicación breve con las palabras de la fuente",
  "etapas": [{"nome": "...", "onde": "...", "entra": "...", "sai": "..."}],
  "vida_real": "un ejemplo de la vida cotidiana para [nombre], que aprende [jeito]",
  "pegadinhas": ["..."],
  "questoes": [{"id": "x1", "pergunta": "...", "opcoes": ["...", "..."], "resposta": "una de las opciones",
                "explicacao": "...", "fonte": "arquivo.txt", "trecho": "frase COPIADA de la fuente, idéntica, que demuestra la respuesta"}]}]}

Reglas: el trecho es una copia exacta de un fragmento de la fuente (de al menos 4 palabras). La pregunta sin un trecho que demuestre la
respuesta no se incluye. Si la fuente contiene poco material para un objetivo, haz menos preguntas; no inventes.

---

Guarda como `objetivos.json` y ejecuta `python3 -m estudo adicionar objetivos.json`.
El kit rechaza la pregunta cuyo trecho no está en la fuente.
# 5. Every week: new material becomes a source and then an objective (chat or Claude Code)

After each class, the student photographs their notes and sends the teacher’s guide.

## 5a. Transcribe (one photo or one PDF at a time)

---

Transcribe the text in this photo exactly as it appears, in plain text. Do not correct the content, complete
sentences, or add anything. Where the text is unreadable, write [illegible]. For a drawing or diagram, describe it on one line
in square brackets, e.g.: [diagram: glucose → pyruvate, with an arrow].

---

Save as `fontes/<aula>.txt` and run `python3 -m estudo semana fontes/<aula>.txt`.

## 5b. Turn the source into objectives (kit format)

---

Based only on the attached sources, write this week’s objectives in JSON, in this format:

{"objetivos": [{"id": "short-no-spaces", "titulo": "...", "topicos": ["..."], "fontes": ["arquivo.txt"],
  "leitura": "short explanation using the source’s wording",
  "etapas": [{"nome": "...", "onde": "...", "entra": "...", "sai": "..."}],
  "vida_real": "an everyday example for [name], who learns [jeito]",
  "pegadinhas": ["..."],
  "questoes": [{"id": "x1", "pergunta": "...", "opcoes": ["...", "..."], "resposta": "one of the options",
                "explicacao": "...", "fonte": "arquivo.txt", "trecho": "a sentence COPIED from the source, exactly, that proves the answer"}]}]}

Rules: trecho must be an exact copy of part of the source (at least 4 words). Do not include a question without a trecho that proves the
answer. If the source has too little for an objective, make fewer questions; do not make things up.

---

Save as `objetivos.json` and run `python3 -m estudo adicionar objetivos.json`.
The kit rejects a question whose trecho is not in the source.
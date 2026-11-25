# 5. Toda semana: material novo entra como fonte e vira objetivo (chat ou Claude Code)

Depois de cada aula, o aluno fotografa as anotações e manda o guia do professor.

## 5a. Transcrever (uma foto ou um PDF por vez)

---

Transcreva o texto desta foto exatamente como está, em texto simples. Nêo corrija o conteúdo, nêo complete
frases e nêo acrescente nada. Onde nêo der para ler, escreva [ilegível]. Desenho ou esquema: descreva em uma linha
entre colchetes, ex.: [esquema: glicose → piruvato, com seta].

---

Salve como `fontes/<aula>.txt` e rode `python3 -m estudo semana fontes/<aula>.txt`.

## 5b. Transformar a fonte em objetivos (formato do kit)

---

Com base só nas fontes anexadas, escreva os objetivos desta semana em JSON, neste formato:

{"objetivos": [{"id": "curto-sem-espaco", "titulo": "...", "topicos": ["..."], "fontes": ["arquivo.txt"],
  "leitura": "explicaçêo curta com as palavras da fonte",
  "etapas": [{"nome": "...", "onde": "...", "entra": "...", "sai": "..."}],
  "vida_real": "um exemplo do dia a dia para [nome], que aprende [jeito]",
  "pegadinhas": ["..."],
  "questoes": [{"id": "x1", "pergunta": "...", "opcoes": ["...", "..."], "resposta": "uma das opções",
                "explicacao": "...", "fonte": "arquivo.txt", "trecho": "frase COPIADA da fonte, igual, que prova a resposta"}]}]}

Regras: o trecho é uma cópia exata de um pedaço da fonte (pelo menos 4 palavras). Questêo sem trecho que prove a
resposta nêo entra. Se a fonte for pouca para um objetivo, faça menos questões, nêo invente.

---

Salve como `objetivos.json` e rode `python3 -m estudo adicionar objetivos.json`.
O kit recusa a questêo cujo trecho nêo está na fonte.

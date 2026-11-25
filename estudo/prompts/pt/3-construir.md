# 3. Construir com o kit (Claude Code ou Codex, dentro da pasta do kit)

Abra o Claude Code (ou o Codex) na pasta do `estudo-do-seu-jeito` e cole. Cole o `plano.md` logo abaixo.

---

Leia o README.md e o skill/estudo-do-seu-jeito/SKILL.md deste kit e siga a fórmula de 8 passos.
O plano que fechei no chat está abaixo. Os arquivos das fontes estêo em [caminho das fotos/PDFs].

1. Crie a matéria com `python3 -m estudo nova "[nome da matéria]"` e preencha professor e aluno pelo plano.
2. Transcreva cada fonte para texto em fontes/ (só o que está escrito; sem completar).
3. Escreva os objetivos em objetivos.json no formato do kit, cada questêo com a fonte e o trecho copiado da fonte.
4. Rode `python3 -m estudo adicionar objetivos.json`. Se o kit recusar alguma questêo, corrija o trecho ou tire a
   questêo; nunca invente fonte.
5. Para cada objetivo, rode `python3 -m estudo proximo --objetivo <id> --anotar` e me mostre o método e o porquê.
6. Gere o guia com `python3 -m estudo guia` e me diga onde está o arquivo.
7. No fim, rode `python3 -m estudo passos` e me mostre o que falta.

[cole aqui o plano.md]

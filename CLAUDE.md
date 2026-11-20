# CLAUDE.md — estudo-do-seu-jeito

Kit (Python puro) que ajuda quem ensina a montar o guia de estudo no jeito do aluno: fórmula de 8 passos, conferência
de cada questão na fonte e teste transparente dos métodos. Superfícies: CLI, app HTML do aluno, prompts de chat
(PT/EN/ES), skill do Claude Code e plugin do INTELECTO v2 (entry point `intelecto.plugins`, nome `estudo`).

## Regras do projeto

- Conta GitHub: `inematds` (autor `inematds <inematds@gmail.com>`).
- **Sem fonte de inspiração**: não citar programa, pessoas reais, faculdade nem lugar. Personagens: Lúcia (mãe) e Clara
  (filha). O teste `test_repositorio_sem_fonte_de_inspiracao` barra os nomes.
- Números da história (nota, objetivos refeitos) são da história; nunca apresentar como medição do kit. O exemplo usa
  dados inventados e diz isso no app e no CLI.
- Dados de aluno nunca no repositório (`~/.estudo-do-seu-jeito` ou `--pasta`).
- O kit não gera conteúdo; quem escreve é a IA ou a pessoa. Toda questão precisa de trecho que exista na fonte.
- Placar: menos de `MIN_N` (3) objetivos = "pouco dado", nunca "melhor".
- Guia em `guia/` (PT) + `guia/en/` + `guia/es/`; README nos 3 idiomas; prompts em `estudo/prompts/{pt,en,es}`
  (comandos e chaves JSON idênticos ao PT).
- Testes: `python3 -m pytest -q testes` antes de todo commit.

## Processo, do início ao fim

1. 🧠 Planejar no chat (prompts 1 e 2) → `plano.md`.
2. ⚙️ `python3 -m estudo nova "<matéria>"` → preencher professor e aluno.
3. 🧠/🤖 Transcrever fontes (prompt 5a) → `python3 -m estudo semana <arquivo.txt>`.
4. 🧠/🤖 Objetivos em JSON (prompt 5b) → `python3 -m estudo adicionar objetivos.json` (conferência na fonte).
5. ⚙️ `python3 -m estudo proximo --anotar` → método de cada objetivo, com o motivo.
6. ⚙️ `python3 -m estudo guia` → `guia.html` para o aluno.
7. 🧠 Aluno estuda no app, exporta `resultados.json` → `python3 -m estudo importar resultados.json`.
8. ⚙️ `python3 -m estudo placar` / `plano-prova --data AAAA-MM-DD` → repetir toda semana a partir do passo 3.

## Self-learning

Quando o Nei corrigir, ou eu achar um erro meu: antes de seguir, acrescentar a lição em uma linha no topo de `## Lessons`.

## Lessons

- Diagrama do app em SVG com viewBox aumenta a letra quando há poucas etapas e corta texto longo; usar caixas HTML em flex (coluna no celular). (20/11/2026)
- Tabela larga no app: envolver em `.rolar` (overflow-x) e conferir em 390 px. (20/11/2026)

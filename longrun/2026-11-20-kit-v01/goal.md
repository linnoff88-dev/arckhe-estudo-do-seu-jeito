# Goal — estudo-do-seu-jeito v0.1

Kit que ajuda quem ensina (mãe, pai, tutor) a montar e manter um guia de estudo no jeito do aluno,
com a fórmula de 8 passos e um experimento transparente de métodos. Superfícies: app visual (HTML),
chat (prompts), skill do Claude Code, plugin do INTELECTO v2. Personagens fictícios (Lúcia e Clara),
sem citar fonte, programa, universidade ou lugar.

## Critérios de pronto (comando → saída esperada)

1. `python3 -m pytest -q testes` → todos passam, ≥ 25 testes (função, regressão e limite).
2. `python3 -m estudo demo --pasta /tmp/x` → cria matéria de exemplo, imprime placar com "pouco dado" em algum método e gera `/tmp/x/guia.html`.
3. `python3 -m estudo conferir` numa matéria com trecho inventado → sai com código 1 e aponta a questão.
4. Questão cujo trecho não existe na fonte → recusada na hora de adicionar (teste).
5. Placar: método com n < 3 objetivos nunca aparece como "melhor" (teste de limite).
6. Plugin: `INTELECTO_PLUGINS=estudo` + provedor mock do intelecto-v2 carrega as ferramentas sem aviso (teste).
7. Portão sem fonte: `test_repositorio_sem_fonte_de_inspiracao` passa (lista de nomes montada no teste, fora do texto).
8. Guia PT/EN/ES em `guia/`, revisor independente aprovado (nota ≥ 8), push no linnoff88-dev/estudo-do-seu-jeito, Pages responde 200.

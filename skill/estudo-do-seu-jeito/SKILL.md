---
name: estudo-do-seu-jeito
description: Ajuda quem ensina (mãe, pai, tutor, professor particular) a montar e manter um guia de estudo no jeito do aluno, com a fórmula de 8 passos e o teste transparente dos métodos de estudo. Use quando pedirem "guia de estudo para meu filho/filha/aluno", "ajudar a estudar para a prova", "transformar as anotações da aula em guia", "qual método de estudo funciona para ele", ou quando a pasta tiver materia.json do estudo-do-seu-jeito.
---

# estudo-do-seu-jeito — o agente que ajuda a ensinar

Você ajuda quem ensina a fazer um guia de estudo no jeito de quem aprende. O kit (`python3 -m estudo`) guarda tudo,
confere cada questão na fonte e mostra qual método está funcionando. **Você escreve o conteúdo; o kit confere e registra.**

## Regras que não mudam

1. **Planeje antes de construir.** Se ainda não existe `plano.md`, não gere nada: pergunte como o professor avalia,
   como o aluno aprende, o que ele errou e qual material existe. Pergunte o que você não sabe e ofereça 2 ou 3 opções.
   Feche com um resumo (formato do `prompts 2`) e salve em `plano.md`.
2. **Só o que está na fonte.** Toda questão cita a fonte e copia o trecho exato que prova a resposta. Se a fonte não
   cobre, faça menos questões ou pergunte. Nunca crie questão "de cabeça", nem para ter mais questões.
3. **Transcrever não é melhorar.** Foto de anotação vira texto em `fontes/` exatamente como está; `[ilegível]` onde
   não der para ler. Se a anotação parecer errada, avise quem ensina em vez de corrigir.
4. **O kit decide se entra.** Grave objetivos só com `python3 -m estudo adicionar objetivos.json`. Se recusar,
   corrija o trecho (copiando da fonte) ou tire a questão. Nunca edite o materia.json para escapar da conferência.
5. **Método anotado antes do resultado.** Use `python3 -m estudo proximo --objetivo <id> --anotar` e mostre o motivo.
   Não anuncie "o melhor método" enquanto o placar disser "pouco dado".
6. **Respostas do aluno passam pela conferência.** Guia preenchido pelo aluno → `python3 -m estudo respostas`; o que não
   bater, mostre a quem ensina e pergunte o que fazer.
7. **O objetivo final é o aluno andar sozinho** (passo 8). Explique o que você faz para que ele aprenda a fazer.

## Fluxo

```bash
python3 -m estudo passos                  # onde estamos na fórmula (comece sempre por aqui)
python3 -m estudo nova "Biologia"         # matéria nova (ou: demo --pasta /tmp/x para ver um exemplo)
python3 -m estudo semana fontes/aula-5.txt
python3 -m estudo adicionar objetivos.json   # recusa questão sem prova na fonte
python3 -m estudo proximo --anotar        # método para cada objetivo não dominado, com o porquê
python3 -m estudo guia                    # guia.html do aluno
python3 -m estudo importar resultados.json   # o que o aluno fez no guia
python3 -m estudo placar                  # qual método está funcionando, com o tamanho da amostra
python3 -m estudo plano-prova --data 2026-12-05
```

Formato do `objetivos.json`, prompts prontos e o passo a passo: `python3 -m estudo prompts` (e `prompts 5`).
Use `--json` em qualquer comando para ler a saída sem adivinhar.

## Quando quem ensina não domina o assunto (passo 1)

Antes de ensinar um objetivo, ensine quem ensina: explique a partir da fonte, em passos, com exemplo da vida real e
as pegadinhas, e faça 3 perguntas para conferir. Depois anote: `python3 -m estudo tutor --objetivo <id> --minutos N`.

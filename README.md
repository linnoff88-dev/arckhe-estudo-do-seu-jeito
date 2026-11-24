# estudo-do-seu-jeito

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


[![Estudo do seu jeito](guia/assets/banner.jpg)](https://linnoff88-dev.github.io/

**ðŸ‡§ðŸ‡· [PortuguÃªs](README.md) Â· ðŸ‡ºðŸ‡¸ [English](README.en.md) Â· ðŸ‡ªðŸ‡¸ [EspaÃ±ol](README.es.md)**

**Ensine o seu filho (ou o seu aluno) do jeito que ele aprende, mesmo sem dominar a matÃ©ria.**

## O que Ã©

Quando o filho (ou o aluno) comeÃ§a a ir mal, quem quer ajudar costuma nÃ£o saber a matÃ©ria nem o jeito certo de explicar.
**Estudo do seu jeito** Ã© um kit grÃ¡tis com uma fÃ³rmula de 8 passos. A IA ensina vocÃª primeiro e depois monta um guia de estudo
no jeito do aluno, com esquemas, exemplos da vida real e questÃµes tiradas sÃ³ do material da aula. TambÃ©m ajuda a
testar, sem esconder nada, qual jeito de estudar funciona para ele. Para usar, basta um chat de IA. Para ir alÃ©m, use o
Claude Code ou o Codex.

ðŸ“– Guia (landing + passo a passo): **https://linnoff88-dev.github.io/ Â·
ðŸ§ª Exemplo do app do aluno: **https://linnoff88-dev.github.io/

## Como comeÃ§ar (cole na sua IA)

```text
Leia o kit "Estudo do seu jeito" em https://github.com/linnoff88-dev/estudo-do-seu-jeito (o README explica a fÃ³rmula de 8 passos e os pedidos prontos).
Quero montar um guia de estudo para [quem], que estÃ¡ em [matÃ©ria e nÃ­vel]. Vou anexar o material: anotaÃ§Ãµes, guia do professor, a Ãºltima prova.
1. Ainda nÃ£o construa nada. Primeiro me pergunte o que vocÃª precisa saber: como o professor avalia, como [quem] aprende, o que errou.
2. Me dÃª 2 ou 3 opÃ§Ãµes de como organizar o guia, com o lado bom e o ruim de cada uma.
3. Regra fixa: todo conteÃºdo e toda questÃ£o saem sÃ³ do material que eu mandar, com a frase que prova a resposta. Se faltar, me pergunte.
4. Quando eu escolher, me mostre um resumo do plano e espere o meu sim.
```

## A histÃ³ria que deu origem Ã  fÃ³rmula

LÃºcia Ã© mÃ£e de quatro filhos e tem hÃ¡ 21 anos uma agÃªncia de marketing com o marido, dentro de casa. A filha mais
velha, Clara, foi estudar biologia marinha numa faculdade a cinco horas de casa. Clara, que sÃ³ tirava nota mÃ¡xima,
comeÃ§ou a ir mal numa matÃ©ria de que gostava: muito conteÃºdo em pouco tempo, aulas com slides cheios de texto e a
regra do professor de que **errar uma questÃ£o de um objetivo de aprendizagem faz perder o objetivo inteiro**.

Clara nÃ£o gostava de IA. LÃºcia nÃ£o Ã© programadora. Mesmo assim, LÃºcia estudou duas a trÃªs horas por dia com o Claude
para conseguir ensinar a filha e depois montou um guia de estudo do jeito de Clara, que Ã© visual: esquemas para
redesenhar, exemplos da vida real, pegadinhas, questÃµes e folhas de resumo para imprimir. A primeira versÃ£o saiu num
dia, com um pedido de quatro frases no chat; depois LÃºcia passou para o Claude Code para ter partes interativas.
Toda semana Clara mandava fotos das anotaÃ§Ãµes, e o guia era refeito e conferido no livro. A nota subiu mais de 10
pontos, de um D alto para perto de 80. Os objetivos que Clara tinha perdido na prova 2 voltaram todos certos na
prova 3.

(Personagens com nomes trocados. Os nÃºmeros acima sÃ£o da histÃ³ria; **nÃ£o foram medidos por este kit**. O exemplo que vem
no kit usa dados inventados.)

## A fÃ³rmula em 8 passos

| # | Passo | No kit |
|---|---|---|
| 1 | **Quem ensina aprende primeiro**: estude o ponto em que o aluno errou, com a IA explicando a partir da fonte | `estudo tutor`, prompt 4 |
| 2 | **Entender como o professor avalia**: o que faz perder ponto | `professor` no materia.json |
| 3 | **Entender como o aluno aprende**: visual, falado, vida real, escrita | `aluno.jeito` |
| 4 | **Partir do que ele jÃ¡ errou** | `estudo resultado --origem prova` |
| 5 | **Planejar antes de construir**: a IA pergunta o que nÃ£o sabe, dÃ¡ opÃ§Ãµes e fecha num resumo | prompts 1 e 2 â†’ `plano.md` |
| 6 | **Guia por objetivo, sÃ³ com o que estÃ¡ na fonte**: leitura, visual, vida real, pegadinhas, questÃµes | `estudo adicionar` (recusa questÃ£o sem prova), `estudo guia` |
| 7 | **Toda semana: material novo e conferÃªncia** | `estudo semana`, prompt 5, `estudo respostas` |
| 8 | **Passar o bastÃ£o**: o aluno passa a usar sozinho | guia.html â†’ `estudo importar`, prompt 8 |

`python3 -m estudo passos` mostra o estado de cada passo, calculado dos seus dados.

## O teste dos mÃ©todos, Ã s claras

NinguÃ©m sabe de antemÃ£o qual mÃ©todo funciona para cada aluno. O kit testa e mostra tudo:

1. Antes de estudar um objetivo, o mÃ©todo Ã© escolhido e **anotado no diÃ¡rio com o motivo** (`estudo proximo --anotar`).
   O kit alterna entre os mÃ©todos que combinam com o jeito do aluno e um controle (reler e grifar), para o teste ser justo.
2. O resultado conta para o mÃ©todo anotado por Ãºltimo naquele objetivo.
3. "Dominado" segue a regra do professor (acertar todas, se for assim que ele corrige).
4. Com menos de 3 objetivos, o mÃ©todo aparece como **"pouco dado"** e nunca como o melhor. Para dizer que um estÃ¡ na frente,
   sÃ£o precisos dois mÃ©todos com dados e 20 pontos de diferenÃ§a.
5. O diÃ¡rio (`diario.jsonl`) sÃ³ recebe linhas novas, nunca apaga; `estudo diario` mostra tudo.

MÃ©todos: ver e redesenhar Â· explicar em voz alta Â· exemplo da vida real Â· questÃµes sem consultar Â· reler e grifar (controle).

## Quem escreve e quem confere

**O kit nÃ£o lÃª foto nem escreve conteÃºdo.** Quem transcreve as anotaÃ§Ãµes e escreve objetivos e questÃµes Ã© vocÃª ou a IA
(chat, Claude Code, Codex ou o cÃ©rebro do seu Jarvis). O kit **organiza, confere e registra**:

- cada questÃ£o diz de qual fonte saiu e copia o trecho; o kit procura esse trecho no texto da fonte e **recusa** a questÃ£o
  se ele nÃ£o existir (sem diferenÃ§a de acento ou maiÃºscula);
- resposta preenchida pelo aluno que nÃ£o bate com a fonte Ã© apontada antes de virar material de estudo;
- a IA nÃ£o cria questÃ£o extra "de cabeÃ§a": quando falta questÃ£o, falta fonte.

## Quatro jeitos de usar

| Jeito | Para quem | Como |
|---|---|---|
| **Chat** (qualquer IA) | quem nÃ£o quer instalar nada | `python3 -m estudo prompts` (8 prompts, PT/EN/ES) ou copie de `estudo/prompts/` |
| **App visual** | o aluno | `guia.html`: abre no celular ou no computador, sem internet |
| **Claude Code / Codex** | quem ensina e quer o agente fazendo o trabalho | skill em `skill/estudo-do-seu-jeito/` |
| **Jarvis (INTELECTO v2)** | quem jÃ¡ tem o assistente | plugin `estudo`: 6 ferramentas |

---

## InstalaÃ§Ã£o tÃ©cnica

### Em 1 minuto

Precisa de Python 3.10 ou mais novo. Nenhum pacote para instalar.

```bash
git clone https://github.com/linnoff88-dev/estudo-do-seu-jeito && cd estudo-do-seu-jeito
python3 -m estudo demo --pasta ~/estudo-demo     # exemplo com dados inventados
# abra ~/estudo-demo/guia.html no navegador
python3 -m estudo placar --pasta ~/estudo-demo
```

Para a sua matÃ©ria (os dados ficam em `~/.estudo-do-seu-jeito`, fora do repositÃ³rio):

```bash
python3 -m estudo nova "Biologia"
python3 -m estudo prompts 1                       # planejar no chat
python3 -m estudo semana anotacoes-aula-5.txt     # fonte da semana
python3 -m estudo adicionar objetivos.json        # recusa questÃ£o sem prova na fonte
python3 -m estudo proximo --anotar                # mÃ©todo de cada objetivo, com o porquÃª
python3 -m estudo guia                            # ~/.estudo-do-seu-jeito/guia.html
python3 -m estudo importar resultados.json        # o que o aluno fez no app
python3 -m estudo plano-prova --data 2026-12-05
```

Qualquer comando aceita `--json` (para agentes) e `--pasta` (uma pasta por matÃ©ria).

### Skill no Claude Code

```bash
mkdir -p ~/.claude/skills && cp -r skill/estudo-do-seu-jeito ~/.claude/skills/
```

Depois, dentro da pasta do kit: "use a skill estudo-do-seu-jeito e me ajude a montar o guia da minha filha".
Sem a skill, funciona colando o prompt 3 (`python3 -m estudo prompts 3`). No Codex: peÃ§a para ler o
`skill/estudo-do-seu-jeito/SKILL.md` e seguir.

### Plugin do INTELECTO v2 (seu Jarvis)

```bash
pip install git+https://github.com/linnoff88-dev/estudo-do-seu-jeito
INTELECTO_PLUGINS=estudo ESTUDO_PASTA=~/.estudo-do-seu-jeito python3 -m intelecto
```

Ferramentas: `estudo_passos`, `estudo_placar`, `estudo_proximo_metodo`, `estudo_registrar_resultado`,
`estudo_conferir`, `estudo_plano_prova`. Nenhuma roda comando nem lÃª fora da pasta da matÃ©ria; as que gravam sÃ³
acrescentam linhas no diÃ¡rio. Pelo Telegram do Jarvis, o aluno pode mandar "fiz 3 de 3 em respiraÃ§Ã£o" e
perguntar "qual mÃ©todo estÃ¡ funcionando?".

### Como estÃ¡ montado

| Arquivo | O que faz |
|---|---|
| `estudo/dados.py` | pasta da matÃ©ria, materia.json, fontes, diÃ¡rio (sÃ³ acrescenta) |
| `estudo/verificador.py` | confere trecho na fonte, opÃ§Ãµes, respostas do aluno |
| `estudo/experimento.py` | placar dos mÃ©todos, escolha do prÃ³ximo com o motivo |
| `estudo/formula.py` | os 8 passos e o estado de cada um |
| `estudo/plano.py` | plano dia a dia atÃ© a prova |
| `estudo/guia_html.py` | o app do aluno (HTML Ãºnico) |
| `estudo/ferramentas.py`, `intelecto_plugin.py` | ferramentas para agentes e o plugin do Jarvis |
| `estudo/prompts/{pt,en,es}/` | os 8 prompts para o chat |
| `estudo/exemplo/` | a matÃ©ria de exemplo (biologia, dados inventados) |

Testes: `python3 -m pytest -q testes` (42 testes: conferÃªncia na fonte, regra do objetivo inteiro, placar com amostra pequena, plano sem objetivo esquecido, importaÃ§Ã£o do app, plugin do INTELECTO e a ausÃªncia de fonte de inspiraÃ§Ã£o no repositÃ³rio).

## O processo, do inÃ­cio ao fim

| # | Passo | Comando | Quem |
|---|---|---|---|
| 1 | Planejar no chat e fechar o resumo em `plano.md` | `python3 -m estudo prompts 1` e `prompts 2` | ðŸ§  vocÃª + IA |
| 2 | Criar a matÃ©ria e preencher professor e aluno | `python3 -m estudo nova "Biologia"` | âš™ï¸ kit |
| 3 | Quem ensina estuda o ponto fraco | `python3 -m estudo prompts 4` â†’ `python3 -m estudo tutor --objetivo <id> --minutos 60` | ðŸ§  vocÃª + IA |
| 4 | Transcrever as fotos da semana para `fontes/` | `python3 -m estudo prompts 5` â†’ `python3 -m estudo semana aula-5.txt` | ðŸ¤– IA |
| 5 | Objetivos e questÃµes com o trecho da fonte | `python3 -m estudo adicionar objetivos.json` | ðŸ¤– IA + âš™ï¸ kit confere |
| 6 | MÃ©todo de cada objetivo, com o porquÃª | `python3 -m estudo proximo --anotar` | âš™ï¸ kit |
| 7 | Gerar o app do aluno | `python3 -m estudo guia` | âš™ï¸ kit |
| 8 | O aluno estuda e exporta o resultado | `guia.html` â†’ `python3 -m estudo importar resultados.json` | ðŸ§  aluno |
| 9 | Ver o placar e o plano atÃ© a prova | `python3 -m estudo placar` Â· `plano-prova --data AAAA-MM-DD` | âš™ï¸ kit |
| 10 | Conferir respostas que o aluno preencheu | `python3 -m estudo respostas respostas.json` | âš™ï¸ kit |

Toda semana repete do passo 4 ao 10. `python3 -m estudo passos` mostra onde vocÃª estÃ¡.

## Limites desta versÃ£o (v0.1)

- A interface (comandos e app) estÃ¡ em portuguÃªs; os prompts estÃ£o em PT, EN e ES.
- O kit nÃ£o lÃª imagem: a transcriÃ§Ã£o das fotos Ã© feita pela IA ou por vocÃª (prompt 5).
- A conferÃªncia acha o trecho na fonte, mas nÃ£o garante que a fonte esteja certa nem que o trecho prove a resposta;
  quando nenhuma palavra da resposta aparece no trecho, ela avisa.
- O placar compara objetivos diferentes, que tÃªm dificuldades diferentes: Ã© uma pista honesta, nÃ£o um experimento cientÃ­fico.
- Os resultados do app ficam no navegador atÃ© vocÃª exportar e importar.

## LicenÃ§a

MIT.

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>
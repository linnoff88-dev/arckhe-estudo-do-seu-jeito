# estudo-do-seu-jeito

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


[![Estudo do seu jeito](guia/assets/banner.jpg)](https://linnoff88-dev.github.io/

**ê°Å¸â¡Â§ê°Å¸â¡Â· [PortuguêÂªs](README.md) êÂ· ê°Å¸â¡Âºê°Å¸â¡Â¸ [English](README.en.md) êÂ· ê°Å¸â¡Âªê°Å¸â¡Â¸ [EspaêÂ±ol](README.es.md)**

**Ensine o seu filho (ou o seu aluno) do jeito que ele aprende, mesmo sem dominar a matêÂ©ria.**

## O que êÂ©

Quando o filho (ou o aluno) comeêÂ§a a ir mal, quem quer ajudar costuma nêÂ£o saber a matêÂ©ria nem o jeito certo de explicar.
**Estudo do seu jeito** êÂ© um kit grêÂ¡tis com uma fêÂ³rmula de 8 passos. A IA ensina vocêÂª primeiro e depois monta um guia de estudo
no jeito do aluno, com esquemas, exemplos da vida real e questêÂµes tiradas sêÂ³ do material da aula. TambêÂ©m ajuda a
testar, sem esconder nada, qual jeito de estudar funciona para ele. Para usar, basta um chat de IA. Para ir alêÂ©m, use o
Claude Code ou o Codex.

ê°Å¸ââ Guia (landing + passo a passo): **https://linnoff88-dev.github.io/ êÂ·
ê°Å¸Â§Âª Exemplo do app do aluno: **https://linnoff88-dev.github.io/

## Como comeêÂ§ar (cole na sua IA)

```text
Leia o kit "Estudo do seu jeito" em https://github.com/linnoff88-dev/estudo-do-seu-jeito (o README explica a fêÂ³rmula de 8 passos e os pedidos prontos).
Quero montar um guia de estudo para [quem], que estêÂ¡ em [matêÂ©ria e nêÂ­vel]. Vou anexar o material: anotaêÂ§êÂµes, guia do professor, a êÂºltima prova.
1. Ainda nêÂ£o construa nada. Primeiro me pergunte o que vocêÂª precisa saber: como o professor avalia, como [quem] aprende, o que errou.
2. Me dêÂª 2 ou 3 opêÂ§êÂµes de como organizar o guia, com o lado bom e o ruim de cada uma.
3. Regra fixa: todo conteêÂºdo e toda questêÂ£o saem sêÂ³ do material que eu mandar, com a frase que prova a resposta. Se faltar, me pergunte.
4. Quando eu escolher, me mostre um resumo do plano e espere o meu sim.
```

## A histêÂ³ria que deu origem êÂ  fêÂ³rmula

LêÂºcia êÂ© mêÂ£e de quatro filhos e tem hêÂ¡ 21 anos uma agêÂªncia de marketing com o marido, dentro de casa. A filha mais
velha, Clara, foi estudar biologia marinha numa faculdade a cinco horas de casa. Clara, que sêÂ³ tirava nota mêÂ¡xima,
comeêÂ§ou a ir mal numa matêÂ©ria de que gostava: muito conteêÂºdo em pouco tempo, aulas com slides cheios de texto e a
regra do professor de que **errar uma questêÂ£o de um objetivo de aprendizagem faz perder o objetivo inteiro**.

Clara nêÂ£o gostava de IA. LêÂºcia nêÂ£o êÂ© programadora. Mesmo assim, LêÂºcia estudou duas a trêÂªs horas por dia com o Claude
para conseguir ensinar a filha e depois montou um guia de estudo do jeito de Clara, que êÂ© visual: esquemas para
redesenhar, exemplos da vida real, pegadinhas, questêÂµes e folhas de resumo para imprimir. A primeira versêÂ£o saiu num
dia, com um pedido de quatro frases no chat; depois LêÂºcia passou para o Claude Code para ter partes interativas.
Toda semana Clara mandava fotos das anotaêÂ§êÂµes, e o guia era refeito e conferido no livro. A nota subiu mais de 10
pontos, de um D alto para perto de 80. Os objetivos que Clara tinha perdido na prova 2 voltaram todos certos na
prova 3.

(Personagens com nomes trocados. Os nêÂºmeros acima sêÂ£o da histêÂ³ria; **nêÂ£o foram medidos por este kit**. O exemplo que vem
no kit usa dados inventados.)

## A fêÂ³rmula em 8 passos

| # | Passo | No kit |
|---|---|---|
| 1 | **Quem ensina aprende primeiro**: estude o ponto em que o aluno errou, com a IA explicando a partir da fonte | `estudo tutor`, prompt 4 |
| 2 | **Entender como o professor avalia**: o que faz perder ponto | `professor` no materia.json |
| 3 | **Entender como o aluno aprende**: visual, falado, vida real, escrita | `aluno.jeito` |
| 4 | **Partir do que ele jêÂ¡ errou** | `estudo resultado --origem prova` |
| 5 | **Planejar antes de construir**: a IA pergunta o que nêÂ£o sabe, dêÂ¡ opêÂ§êÂµes e fecha num resumo | prompts 1 e 2 ê¢â â `plano.md` |
| 6 | **Guia por objetivo, sêÂ³ com o que estêÂ¡ na fonte**: leitura, visual, vida real, pegadinhas, questêÂµes | `estudo adicionar` (recusa questêÂ£o sem prova), `estudo guia` |
| 7 | **Toda semana: material novo e conferêÂªncia** | `estudo semana`, prompt 5, `estudo respostas` |
| 8 | **Passar o bastêÂ£o**: o aluno passa a usar sozinho | guia.html ê¢â â `estudo importar`, prompt 8 |

`python3 -m estudo passos` mostra o estado de cada passo, calculado dos seus dados.

## O teste dos mêÂ©todos, êÂ s claras

NinguêÂ©m sabe de antemêÂ£o qual mêÂ©todo funciona para cada aluno. O kit testa e mostra tudo:

1. Antes de estudar um objetivo, o mêÂ©todo êÂ© escolhido e **anotado no diêÂ¡rio com o motivo** (`estudo proximo --anotar`).
   O kit alterna entre os mêÂ©todos que combinam com o jeito do aluno e um controle (reler e grifar), para o teste ser justo.
2. O resultado conta para o mêÂ©todo anotado por êÂºltimo naquele objetivo.
3. "Dominado" segue a regra do professor (acertar todas, se for assim que ele corrige).
4. Com menos de 3 objetivos, o mêÂ©todo aparece como **"pouco dado"** e nunca como o melhor. Para dizer que um estêÂ¡ na frente,
   sêÂ£o precisos dois mêÂ©todos com dados e 20 pontos de diferenêÂ§a.
5. O diêÂ¡rio (`diario.jsonl`) sêÂ³ recebe linhas novas, nunca apaga; `estudo diario` mostra tudo.

MêÂ©todos: ver e redesenhar êÂ· explicar em voz alta êÂ· exemplo da vida real êÂ· questêÂµes sem consultar êÂ· reler e grifar (controle).

## Quem escreve e quem confere

**O kit nêÂ£o lêÂª foto nem escreve conteêÂºdo.** Quem transcreve as anotaêÂ§êÂµes e escreve objetivos e questêÂµes êÂ© vocêÂª ou a IA
(chat, Claude Code, Codex ou o cêÂ©rebro do seu Jarvis). O kit **organiza, confere e registra**:

- cada questêÂ£o diz de qual fonte saiu e copia o trecho; o kit procura esse trecho no texto da fonte e **recusa** a questêÂ£o
  se ele nêÂ£o existir (sem diferenêÂ§a de acento ou maiêÂºscula);
- resposta preenchida pelo aluno que nêÂ£o bate com a fonte êÂ© apontada antes de virar material de estudo;
- a IA nêÂ£o cria questêÂ£o extra "de cabeêÂ§a": quando falta questêÂ£o, falta fonte.

## Quatro jeitos de usar

| Jeito | Para quem | Como |
|---|---|---|
| **Chat** (qualquer IA) | quem nêÂ£o quer instalar nada | `python3 -m estudo prompts` (8 prompts, PT/EN/ES) ou copie de `estudo/prompts/` |
| **App visual** | o aluno | `guia.html`: abre no celular ou no computador, sem internet |
| **Claude Code / Codex** | quem ensina e quer o agente fazendo o trabalho | skill em `skill/estudo-do-seu-jeito/` |
| **Jarvis (INTELECTO v2)** | quem jêÂ¡ tem o assistente | plugin `estudo`: 6 ferramentas |

---

## InstalaêÂ§êÂ£o têÂ©cnica

### Em 1 minuto

Precisa de Python 3.10 ou mais novo. Nenhum pacote para instalar.

```bash
git clone https://github.com/linnoff88-dev/estudo-do-seu-jeito && cd estudo-do-seu-jeito
python3 -m estudo demo --pasta ~/estudo-demo     # exemplo com dados inventados
# abra ~/estudo-demo/guia.html no navegador
python3 -m estudo placar --pasta ~/estudo-demo
```

Para a sua matêÂ©ria (os dados ficam em `~/.estudo-do-seu-jeito`, fora do repositêÂ³rio):

```bash
python3 -m estudo nova "Biologia"
python3 -m estudo prompts 1                       # planejar no chat
python3 -m estudo semana anotacoes-aula-5.txt     # fonte da semana
python3 -m estudo adicionar objetivos.json        # recusa questêÂ£o sem prova na fonte
python3 -m estudo proximo --anotar                # mêÂ©todo de cada objetivo, com o porquêÂª
python3 -m estudo guia                            # ~/.estudo-do-seu-jeito/guia.html
python3 -m estudo importar resultados.json        # o que o aluno fez no app
python3 -m estudo plano-prova --data 2026-12-05
```

Qualquer comando aceita `--json` (para agentes) e `--pasta` (uma pasta por matêÂ©ria).

### Skill no Claude Code

```bash
mkdir -p ~/.claude/skills && cp -r skill/estudo-do-seu-jeito ~/.claude/skills/
```

Depois, dentro da pasta do kit: "use a skill estudo-do-seu-jeito e me ajude a montar o guia da minha filha".
Sem a skill, funciona colando o prompt 3 (`python3 -m estudo prompts 3`). No Codex: peêÂ§a para ler o
`skill/estudo-do-seu-jeito/SKILL.md` e seguir.

### Plugin do INTELECTO v2 (seu Jarvis)

```bash
pip install git+https://github.com/linnoff88-dev/estudo-do-seu-jeito
INTELECTO_PLUGINS=estudo ESTUDO_PASTA=~/.estudo-do-seu-jeito python3 -m intelecto
```

Ferramentas: `estudo_passos`, `estudo_placar`, `estudo_proximo_metodo`, `estudo_registrar_resultado`,
`estudo_conferir`, `estudo_plano_prova`. Nenhuma roda comando nem lêÂª fora da pasta da matêÂ©ria; as que gravam sêÂ³
acrescentam linhas no diêÂ¡rio. Pelo Telegram do Jarvis, o aluno pode mandar "fiz 3 de 3 em respiraêÂ§êÂ£o" e
perguntar "qual mêÂ©todo estêÂ¡ funcionando?".

### Como estêÂ¡ montado

| Arquivo | O que faz |
|---|---|
| `estudo/dados.py` | pasta da matêÂ©ria, materia.json, fontes, diêÂ¡rio (sêÂ³ acrescenta) |
| `estudo/verificador.py` | confere trecho na fonte, opêÂ§êÂµes, respostas do aluno |
| `estudo/experimento.py` | placar dos mêÂ©todos, escolha do prêÂ³ximo com o motivo |
| `estudo/formula.py` | os 8 passos e o estado de cada um |
| `estudo/plano.py` | plano dia a dia atêÂ© a prova |
| `estudo/guia_html.py` | o app do aluno (HTML êÂºnico) |
| `estudo/ferramentas.py`, `intelecto_plugin.py` | ferramentas para agentes e o plugin do Jarvis |
| `estudo/prompts/{pt,en,es}/` | os 8 prompts para o chat |
| `estudo/exemplo/` | a matêÂ©ria de exemplo (biologia, dados inventados) |

Testes: `python3 -m pytest -q testes` (42 testes: conferêÂªncia na fonte, regra do objetivo inteiro, placar com amostra pequena, plano sem objetivo esquecido, importaêÂ§êÂ£o do app, plugin do INTELECTO e a ausêÂªncia de fonte de inspiraêÂ§êÂ£o no repositêÂ³rio).

## O processo, do inêÂ­cio ao fim

| # | Passo | Comando | Quem |
|---|---|---|---|
| 1 | Planejar no chat e fechar o resumo em `plano.md` | `python3 -m estudo prompts 1` e `prompts 2` | ê°Å¸Â§Â  vocêÂª + IA |
| 2 | Criar a matêÂ©ria e preencher professor e aluno | `python3 -m estudo nova "Biologia"` | ê¢Å¡â¢ê¯Â¸Â kit |
| 3 | Quem ensina estuda o ponto fraco | `python3 -m estudo prompts 4` ê¢â â `python3 -m estudo tutor --objetivo <id> --minutos 60` | ê°Å¸Â§Â  vocêÂª + IA |
| 4 | Transcrever as fotos da semana para `fontes/` | `python3 -m estudo prompts 5` ê¢â â `python3 -m estudo semana aula-5.txt` | ê°Å¸Â¤â IA |
| 5 | Objetivos e questêÂµes com o trecho da fonte | `python3 -m estudo adicionar objetivos.json` | ê°Å¸Â¤â IA + ê¢Å¡â¢ê¯Â¸Â kit confere |
| 6 | MêÂ©todo de cada objetivo, com o porquêÂª | `python3 -m estudo proximo --anotar` | ê¢Å¡â¢ê¯Â¸Â kit |
| 7 | Gerar o app do aluno | `python3 -m estudo guia` | ê¢Å¡â¢ê¯Â¸Â kit |
| 8 | O aluno estuda e exporta o resultado | `guia.html` ê¢â â `python3 -m estudo importar resultados.json` | ê°Å¸Â§Â  aluno |
| 9 | Ver o placar e o plano atêÂ© a prova | `python3 -m estudo placar` êÂ· `plano-prova --data AAAA-MM-DD` | ê¢Å¡â¢ê¯Â¸Â kit |
| 10 | Conferir respostas que o aluno preencheu | `python3 -m estudo respostas respostas.json` | ê¢Å¡â¢ê¯Â¸Â kit |

Toda semana repete do passo 4 ao 10. `python3 -m estudo passos` mostra onde vocêÂª estêÂ¡.

## Limites desta versêÂ£o (v0.1)

- A interface (comandos e app) estêÂ¡ em portuguêÂªs; os prompts estêÂ£o em PT, EN e ES.
- O kit nêÂ£o lêÂª imagem: a transcriêÂ§êÂ£o das fotos êÂ© feita pela IA ou por vocêÂª (prompt 5).
- A conferêÂªncia acha o trecho na fonte, mas nêÂ£o garante que a fonte esteja certa nem que o trecho prove a resposta;
  quando nenhuma palavra da resposta aparece no trecho, ela avisa.
- O placar compara objetivos diferentes, que têÂªm dificuldades diferentes: êÂ© uma pista honesta, nêÂ£o um experimento cientêÂ­fico.
- Os resultados do app ficam no navegador atêÂ© vocêÂª exportar e importar.

## LicenêÂ§a

MIT.

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>
# estudo-do-seu-jeito

[![Study your way](guia/assets/banner-en.jpg)](https://inematds.github.io/estudo-do-seu-jeito/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

**Teach your child (or your student) the way they learn, even if you don’t know the subject well.**

## What it is

When a child (or student) starts struggling, the person who wants to help often doesn’t know the subject or the right way to explain it.
**Study your way** is a free kit with an 8-step formula. AI teaches you first, then builds a study guide
that fits the student’s learning style, with diagrams, real-life examples, and questions drawn only from the lesson materials. It also helps you
test, transparently, which study method works for them. All you need is an AI chat. To do more, use
Claude Code or Codex.

📖 Guide (landing page + walkthrough): **https://inematds.github.io/estudo-do-seu-jeito/guia/en/** ·
🧪 Student app demo: **https://inematds.github.io/estudo-do-seu-jeito/guia/demo/** (the example is in Portuguese)

## How to get started (paste this into your AI)

```text
Read the "Study your way" kit at https://github.com/inematds/estudo-do-seu-jeito (the README explains the 8-step formula and includes ready-to-use prompts).
I want to build a study guide for [who], who is studying [subject and level]. I’ll attach the materials: notes, the teacher’s guide, the latest test.
1. Don’t build anything yet. First ask me what you need to know: how the teacher grades, how [who] learns, and what they got wrong.
2. Give me 2 or 3 options for organizing the guide, with the pros and cons of each.
3. Fixed rule: all content and questions must come only from the materials I provide, with the sentence that proves each answer. If anything is missing, ask me.
4. Once I choose, show me a summary of the plan and wait for my approval.
```

## The story behind the formula

Lúcia is a mother of four. For 21 years, she and her husband have run a marketing agency from their home. Her oldest daughter, Clara, went to study marine biology at a college five hours from home. Clara, who had always earned top grades,
started struggling in a subject she liked: a lot of material in a short time, lectures with text-heavy slides, and the
teacher’s rule that **getting one question wrong for a learning objective meant losing credit for the entire objective**.

Clara didn’t like AI. Lúcia isn’t a programmer. Even so, Lúcia studied with Claude for two to three hours a day so she could teach her daughter, then put together a study guide tailored to Clara’s visual learning style: diagrams to redraw, real-life examples, trick questions, practice questions, and printable summary sheets. The first version was ready in
one day, from a four-sentence prompt in chat; later, Lúcia moved to Claude Code to add interactive features.
Every week, Clara sent photos of her notes, and the guide was updated and checked against the textbook. Her grade went up by more than 10
points, from a high D to nearly 80. All the objectives Clara had missed on test 2 were answered correctly on
test 3.

(Names have been changed. The numbers above are from the story; **they were not measured by this kit**. The example included
in the kit uses invented data.)

## The 8-step formula

| # | Step | In the kit |
|---|---|---|
| 1 | **The person teaching learns first**: study the point the student got wrong, with AI explaining it from the source | `estudo tutor`, prompt 4 |
| 2 | **Understand how the teacher grades**: what causes the student to lose points | `professor` in materia.json |
| 3 | **Understand how the student learns**: visual, spoken, real-life examples, writing | `aluno.jeito` |
| 4 | **Start with what they already got wrong** | `estudo resultado --origem prova` |
| 5 | **Plan before building**: AI asks what it doesn’t know, offers options, and wraps up with a summary | prompts 1 and 2 → `plano.md` |
| 6 | **A guide for each objective, using only the source**: reading, visuals, real-life examples, trick questions, practice questions | `estudo adicionar` (rejects questions without evidence), `estudo guia` |
| 7 | **Every week: new materials and review** | `estudo semana`, prompt 5, `estudo respostas` |
| 8 | **Hand over the reins**: the student starts using it on their own | guia.html → `estudo importar`, prompt 8 |

`python3 -m estudo passos` shows the status of each step, calculated from your data.

## Testing study methods, transparently

No one knows in advance which method works for each student. The kit tests and shows everything:

1. Before studying an objective, a method is chosen and **recorded in the journal with the reason** (`estudo proximo --anotar`).
   The kit alternates between methods that fit the student’s learning style and a control method (rereading and highlighting), to keep the test fair.
2. The result counts toward the last method recorded for that objective.
3. “Mastered” follows the teacher’s grading rule (all questions correct, if that’s how they grade).
4. With fewer than 3 objectives, the method is shown as **“pouco dado” (little data)** and never as the best. To say one is ahead,
   two methods need data and a 20-point difference.
5. The journal (`diario.jsonl`) only gets new lines; it never deletes anything. `estudo diario` shows everything.

Methods: look and redraw · explain out loud · real-life example · answer questions without looking · reread and highlight (control).

## Who writes and who checks

**The kit doesn’t read photos or write content.** You or the AI
(chat, Claude Code, Codex, or your Jarvis’s brain) transcribes the notes and writes objectives and questions. The kit **organizes, checks, and records**:

- each question identifies its source and copies the relevant passage; the kit searches for that passage in the source text and **rejects** the question
  if it can’t find it (ignoring differences in accents and capitalization);
- an answer filled in by the student that doesn’t match the source is flagged before it becomes study material;
- AI doesn’t make up extra questions “from memory”: when there are no questions, there is no source.

## Four ways to use it

| Way | For whom | How |
|---|---|---|
| **Chat** (any AI) | anyone who doesn’t want to install anything | `python3 -m estudo prompts` (8 prompts, PT/EN/ES; use `--idioma en` for English) or copy from `estudo/prompts/` |
| **Visual app** | the student | `guia.html`: opens on a phone or computer, no internet needed |
| **Claude Code / Codex** | anyone teaching who wants an agent to do the work | skill in `skill/estudo-do-seu-jeito/` |
| **Jarvis (INTELECTO v2)** | anyone who already has the assistant | `estudo` plugin: 6 tools |

---

## Technical installation

### In 1 minute

Requires Python 3.10 or newer. No packages to install.

```bash
git clone https://github.com/inematds/estudo-do-seu-jeito && cd estudo-do-seu-jeito
python3 -m estudo demo --pasta ~/estudo-demo     # example with invented data
# open ~/estudo-demo/guia.html in your browser
python3 -m estudo placar --pasta ~/estudo-demo
```

For your subject (the data stays in `~/.estudo-do-seu-jeito`, outside the repository):

```bash
python3 -m estudo nova "Biologia"
python3 -m estudo prompts 1                       # plan in chat
python3 -m estudo semana anotacoes-aula-5.txt     # this week's source
python3 -m estudo adicionar objetivos.json        # rejects questions without evidence in the source
python3 -m estudo proximo --anotar                # method for each objective, with the reason
python3 -m estudo guia                            # ~/.estudo-do-seu-jeito/guia.html
python3 -m estudo importar resultados.json        # what the student did in the app
python3 -m estudo plano-prova --data 2026-12-05
```

Any command accepts `--json` (for agents) and `--pasta` (one folder per subject).

### Skill in Claude Code

```bash
mkdir -p ~/.claude/skills && cp -r skill/estudo-do-seu-jeito ~/.claude/skills/
```

Then, from inside the kit folder: “use the estudo-do-seu-jeito skill and help me build my child’s study guide.”
Without the skill, you can use prompt 3 instead (`python3 -m estudo prompts 3`). In Codex: ask it to read
`skill/estudo-do-seu-jeito/SKILL.md` and follow it.

### INTELECTO v2 plugin (your Jarvis)

```bash
pip install git+https://github.com/inematds/estudo-do-seu-jeito
INTELECTO_PLUGINS=estudo ESTUDO_PASTA=~/.estudo-do-seu-jeito python3 -m intelecto
```

Tools: `estudo_passos`, `estudo_placar`, `estudo_proximo_metodo`, `estudo_registrar_resultado`,
`estudo_conferir`, `estudo_plano_prova`. None runs commands or reads outside the subject folder; tools that write only
append lines to the journal. Through Jarvis on Telegram, the student can send “I got 3 out of 3 on respiration” and
ask “which method is working?”

### How it is organized

| File | What it does |
|---|---|
| `estudo/dados.py` | subject folder, materia.json, sources, journal (append-only) |
| `estudo/verificador.py` | checks passages in the source, options, and student answers |
| `estudo/experimento.py` | method scores, choice of the next method and why |
| `estudo/formula.py` | the 8 steps and the status of each one |
| `estudo/plano.py` | day-by-day plan leading up to the test |
| `estudo/guia_html.py` | the student app (single HTML file) |
| `estudo/ferramentas.py`, `intelecto_plugin.py` | tools for agents and the Jarvis plugin |
| `estudo/prompts/{pt,en,es}/` | the 8 prompts for chat |
| `estudo/exemplo/` | the sample subject (biology, invented data) |

Tests: `python3 -m pytest -q testes` (42 tests: source checking, whole-objective rule, scoring with a small sample, plan with no forgotten objectives, app import, INTELECTO plugin, and absence of an inspiration source in the repository).

## The process, from start to finish

| # | Step | Command | Who |
|---|---|---|---|
| 1 | Plan in chat and finalize the summary in `plano.md` | `python3 -m estudo prompts 1` and `prompts 2` | 🧠 you + AI |
| 2 | Create the subject and fill in teacher and student details | `python3 -m estudo nova "Biologia"` | ⚙️ kit |
| 3 | The person teaching studies the weak point | `python3 -m estudo prompts 4` → `python3 -m estudo tutor --objetivo <id> --minutos 60` | 🧠 you + AI |
| 4 | Transcribe the week’s photos into `fontes/` | `python3 -m estudo prompts 5` → `python3 -m estudo semana aula-5.txt` | 🤖 AI |
| 5 | Objectives and questions with the source passage | `python3 -m estudo adicionar objetivos.json` | 🤖 AI + ⚙️ kit checks |
| 6 | Method for each objective, with the reason | `python3 -m estudo proximo --anotar` | ⚙️ kit |
| 7 | Generate the student app | `python3 -m estudo guia` | ⚙️ kit |
| 8 | Student studies and exports the results | `guia.html` → `python3 -m estudo importar resultados.json` | 🧠 student |
| 9 | See the scores and plan leading up to the test | `python3 -m estudo placar` · `plano-prova --data AAAA-MM-DD` | ⚙️ kit |
| 10 | Check the answers the student filled in | `python3 -m estudo respostas respostas.json` | ⚙️ kit |

Repeat steps 4 through 10 every week. `python3 -m estudo passos` shows where you are.

## Limits of this version (v0.1)

- The interface (commands and app) is in Portuguese; prompts are available in PT, EN, and ES. The `prompts` command accepts `--idioma en`.
- The kit doesn’t read images: photos are transcribed by AI or by you (prompt 5).
- The checker finds the passage in the source, but can’t guarantee that the source is correct or that the passage proves the answer;
  if none of the answer’s words appear in the passage, it gives a warning.
- The scoreboard compares different objectives, which may have different levels of difficulty: it’s an honest clue, not a scientific experiment.
- App results stay in the browser until you export and import them.

## License

MIT.
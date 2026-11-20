# 3. Build with the kit (Claude Code or Codex, inside the kit folder)

Open Claude Code (or Codex) in the `estudo-do-seu-jeito` folder and paste this. Paste `plano.md` right below.

---

Read this kit’s README.md and skill/estudo-do-seu-jeito/SKILL.md, and follow the 8-step formula.
The plan I finalized in the chat is below. The source files are in [path to photos/PDFs].

1. Create the subject with `python3 -m estudo nova "[subject name]"` and fill in the teacher and student details from the plan.
2. Transcribe each source into text in fontes/ (only what is written; do not fill anything in).
3. Write the objectives in objetivos.json in the kit’s format, with each question linked to its source and the passage copied from the source.
4. Run `python3 -m estudo adicionar objetivos.json`. If the kit rejects a question, fix the passage or remove the question; never invent a source.
5. For each objective, run `python3 -m estudo proximo --objetivo <id> --anotar` and show me the method and why it works.
6. Generate the guide with `python3 -m estudo guia` and tell me where the file is.
7. At the end, run `python3 -m estudo passos` and show me what remains.

[Paste plano.md here]
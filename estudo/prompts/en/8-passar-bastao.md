# 8. Handing over (the student works independently)

The ultimate goal is for the teacher to step out of the picture. Once the student can use the guide without help, they can make the week’s guide themselves.
Paste this into Claude Code (or Codex) in the kit folder; the student pastes it.

---

I’m [student’s name], and starting today I’ll manage my study guide on my own. Read skill/estudo-do-seu-jeito/SKILL.md.
1. Run `python3 -m estudo passos` and explain in 3 lines where I am.
2. I’ll send photos of this week’s class: transcribe them into fontes/, create the objectives, and run `adicionar`.
3. Import my results with `python3 -m estudo importar resultados.json` and show me the methods scorecard.
4. For each objective I haven’t mastered yet, run `python3 -m estudo proximo --objetivo <id> --anotar` and tell me why.
5. Generate the new guide. Don’t make up content beyond what’s in the sources.
# 6. Check a guide the student has already filled in

A guide or list that a student has answered by hand may contain incorrect answers. Check it before using it as study material.

## Using the kit (no AI)

Write the answers in `respostas.json` like this: `{"f1": "Stroma", "r2": "Oxygen"}` (question ID → answer given)
and run `python3 -m estudo respostas respostas.json`. The kit shows what does not match the source, along with the excerpt.

## In chat (for a guide that is not in the kit yet)

---

This is a study guide that [name] filled in (photo attached), and this is the source (attached).
Before we use it to study, compare each answer with the source.
For each answer that does not match, show me: the question, the answer given, what the source says (with the excerpt), and ask me what
to do. Do not correct anything on your own or use anything outside the source.
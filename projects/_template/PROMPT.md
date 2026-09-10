# Daily kickoff prompt

Copy everything in the block below into a new chat. Edit only the first two lines — the day number
with today's concept, and any source material you want followed. Leave the rest exactly as it is;
that part is the standing spec that tells the agent how to build the lesson.

Once you have used it once in a session, the shorthand `@PROMPT.md Day 02: attention` also works.

---

```text
Day <NN>: <CONCEPT I WANT TO LEARN TODAY>
Optional source material: <article / video / paper links, or leave blank>

Follow the standing spec below. Do not ask me to restate it.

1. Create projects/week-<WW>-<kebab-week-name>/day-<NN>-<kebab-case-concept>/ from
   projects/_template/ (make the week folder first if it doesn't exist; day NN lives
   in week ceil(NN/3) counting from day 01 = week 01). Fix the copied README's
   relative paths: ../../ -> ../../../, and the launch path to the week-nested one.
2. Write lesson.ipynb as a self-contained 60-minute guided lesson: markdown
   explanation cells interleaved with runnable code cells, segments timeboxed
   to sum to ~60 min, each concept built from scratch before any library is
   used so nothing is a black box.
3. Use the uv venv at .venv for everything -- never the system Python. Prefer
   already-installed deps (numpy, matplotlib, tiktoken). If a new one is needed,
   add it to the root requirements.txt and install with
   `python -m uv pip install --python .venv\Scripts\python.exe -r requirements.txt`.
   Pin the notebook to the "ai-upskill" kernel.
4. End with 5-6 exercises with worked solutions plus a self-check quiz and
   answer key.
5. Write README.md (objectives, agenda, launch command, source links) and
   NOTES.md (one-page cheat sheet I keep).
6. Execute the notebook end-to-end with nbconvert so it opens with outputs
   populated, and fix anything that errors.
7. Add the day as a row under its week's section in projects/README.md, and end
   with a short pointer to what would be a good next concept.
```

---

## Why the lesson looks the way it does

- **Timeboxed segments.** An hour is the budget, so every segment carries a minute cost and they sum
  to roughly 60. If a segment overruns, that is a signal to split the concept across two days.
- **From scratch before libraries.** The library version is shown only after you have built a crude
  version yourself. Calling `tiktoken.encode` teaches you nothing until you have merged byte pairs by
  hand once.
- **Failure first.** Each idea is motivated by watching the simpler idea break, numerically, in a
  cell you ran. That is what makes the fix memorable.
- **Exercises and a quiz.** Passive reading feels like learning. The exercises are how you find out
  whether it actually happened.

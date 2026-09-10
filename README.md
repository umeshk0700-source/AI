# AI Upskill

One concept per day, one hour each, learned by building it from scratch rather than reading about it.

- **Lessons** — [`projects/`](projects/): 30 guided notebooks in 10 themed weeks
  (`projects/week-NN-*/day-NN-*/`). Start at
  [week 1](projects/week-01-foundations/day-01-text-to-numbers/). Index:
  [projects/README.md](projects/README.md).
- **Practice labs** — [`projects/practice/`](projects/practice/): one corporate-grade build per
  week — typed OO skeleton with TODOs, a pytest suite (offline + opt-in **real Claude/GPT**
  integration tests), and a filled `solution/`. Index:
  [projects/practice/README.md](projects/practice/README.md).

## Environment

Everything runs in a single [uv](https://docs.astral.sh/uv/)-managed virtualenv at `.venv`,
shared by every lesson and lab.

### First-time setup

```bash
python -m pip install uv
python -m uv venv .venv --python 3.12
python -m uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python -m ipykernel install --user --name ai-upskill --display-name "Python (ai-upskill)"

./scripts/setup-hooks.sh                      # pre-commit: block secrets, strip lab-notebook outputs
python -m pip install -e projects/practice/common   # `import llmlab` for the practice labs
```

(Windows: `.venv\Scripts\python.exe` and `.venv\Scripts\activate`.)

### Every session

```bash
source .venv/bin/activate
```

Notebooks are pinned to the **Python (ai-upskill)** kernel, so they pick the right interpreter
on open.

### Adding a package

Add it to `requirements.txt`, re-run the `uv pip install` line. Never `pip install` into the
system Python.

## Secrets & cost

- API keys go **only** in `projects/practice/.env` (gitignored) — copy `.env.example`.
- The pre-commit hook (`./scripts/setup-hooks.sh`) refuses to commit `.env` files or
  key-shaped strings, and strips outputs from `projects/practice/**/*.ipynb` (a live run
  embeds real API responses).
- Practice live tests are opt-in (`LLM_LIVE=1 make live`), use cheap models by default, and
  a per-lab `LAB_USD_CAP` trips `BudgetExceeded` before you overspend.

## Layout

```
.venv/                     the uv environment (gitignored)
requirements.txt           shared dependencies
scripts/                   setup-hooks.sh, strip_notebook.py
.githooks/pre-commit       secret + cost-leak guard
projects/
  week-01-foundations/ ... week-10-deployment/    30 lesson notebooks
  _template/                                      the daily-lesson template + PROMPT.md
  practice/
    common/llmlab/                                shared toolkit (real API clients, cost, tracing)
    week-01-foundations/ ... week-10-ship-it/      10 labs
```

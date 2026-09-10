# AI Upskill

One concept per day, one hour each, learned by building it from scratch rather than reading about it.

The lessons live in [projects/](projects/). Start with
[projects/day-01-text-to-numbers](projects/day-01-text-to-numbers/).

## Environment

Everything runs in a single [uv](https://docs.astral.sh/uv/)-managed virtual environment at `.venv`,
shared by every day's lesson.

### First-time setup

```powershell
python -m pip install uv
python -m uv venv .venv --python 3.10
python -m uv pip install --python .venv\Scripts\python.exe -r requirements.txt
.venv\Scripts\python.exe -m ipykernel install --user --name ai-upskill --display-name "Python (ai-upskill)"
```

The last line registers the venv as a Jupyter kernel called **Python (ai-upskill)**. Every notebook in
this repo is already pinned to that kernel, so it will pick the right interpreter on open.

### Every session after that

```powershell
.venv\Scripts\activate
```

Once activated, plain `python` and `jupyter` refer to the venv. To launch a lesson:

```powershell
python -m jupyterlab projects\day-01-text-to-numbers\lesson.ipynb
```

If you prefer not to activate, prefix commands with `.venv\Scripts\python.exe -m ...` instead.

### Adding a package

Add it to `requirements.txt`, then re-run the install line above. Never `pip install` into the system
Python — if `python -c "import sys; print(sys.executable)"` does not print a path inside `.venv`, the
environment is not active.

## Layout

```
.venv/               the uv environment (gitignored)
requirements.txt     shared dependencies for all days
projects/            one folder per day, plus the reusable template
```

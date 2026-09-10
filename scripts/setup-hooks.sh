#!/usr/bin/env bash
# Wire up the repo's git hooks + notebook output-stripping filter.
# Run once per clone:   ./scripts/setup-hooks.sh
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

chmod +x .githooks/pre-commit scripts/strip_notebook.py
git config core.hooksPath .githooks

# `git clean` filter used by .gitattributes for practice notebooks:
# whatever is committed has outputs removed; your working copy keeps them.
PY=$(command -v python3 || echo "$PWD/.venv/bin/python")
git config filter.nbstripout.clean "$PY $PWD/scripts/strip_notebook.py --stdin"
git config filter.nbstripout.smudge cat
git config filter.nbstripout.required true

echo "hooks + notebook filter configured:"
echo "  - pre-commit blocks secrets / .env files, strips practice-notebook outputs"
echo "  - projects/practice/**/*.ipynb are committed without outputs"
echo
echo "verify:  git config --get core.hooksPath   ->  .githooks"

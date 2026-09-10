# Week lab targets. Run `make help` for the list.
PY ?= ../../../.venv/bin/python
PRESET := $(if $(wildcard .env.preset),env $$(grep -v '^\#' .env.preset | xargs),)

.PHONY: help setup test solution live lab clean

help:
	@echo "make setup     - install this lab's deps into the shared venv"
	@echo "make test      - offline unit tests (no API, no cost)"
	@echo "make solution  - run the tests against solution/ (reference impl)"
	@echo "make live      - real Claude/GPT integration tests  (~$0.02)"
	@echo "make lab       - open the walkthrough notebook"
	@echo "make clean     - remove caches"

setup:
	$(PY) -m pip install -q -e ../common
	$(PY) -m pip install -q -r requirements.txt

test:
	$(PY) -m pytest -q -m "not live"

solution:
	LAB_SRC=solution $(PY) -m pytest -q -m "not live"

live:
	@echo "This calls real APIs and costs money (cap: $0.02). Ctrl-C to abort."; sleep 2
	$(PRESET) LLM_LIVE=1 $(PY) -m pytest -q -m live -s

lab:
	$(PY) -m jupyter lab lab.ipynb

clean:
	rm -rf .pytest_cache **/__pycache__ tests/__pycache__ src/**/__pycache__

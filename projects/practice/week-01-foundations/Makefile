# Week 1 lab (no API). Run `make help`.
PY ?= ../../../.venv/bin/python

.PHONY: help lab solution clean

help:
	@echo "make lab       - open the lab notebook (implement the TODOs)"
	@echo "make solution  - open the filled reference notebook"
	@echo "make clean     - remove caches"

lab:
	$(PY) -m jupyter lab lab.ipynb

solution:
	$(PY) -m jupyter lab solution.ipynb

clean:
	rm -rf .ipynb_checkpoints **/__pycache__

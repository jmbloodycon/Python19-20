TESTS = tests

VENV ?= .venv

venv:
	python3 -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install -r requirements.txt

test:
	$(VENV)/bin/pytest -v tests

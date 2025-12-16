PYTHON := python
PYTEST := $(PYTHON) -m pytest

.PHONY: test unit_test perf_test coverage lint doc

test: #
	$(PYTEST)

unit_test: # 
	$(PYTEST) -m "not perf"

perf_test:
	$(PYTEST) -m perf

coverage: #pour générer un rapport de couverture avec coverage.py
	coverage run -m pytest
	coverage report
	@echo "Pour un rapport HTML : coverage html"

lint: #pour analyser le code avec ruff
	ruff check .

doc: #pour générer la documentation avec pdoc3
	pdoc3 triangulator -o docs
	@echo "Documentation générée dans le dossier docs/"

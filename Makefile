.PHONY: help install validate generate clean test

PYTHON := venv/bin/python
PIP := venv/bin/pip

help:
	@echo "Ultimate Agent Directory - Build Commands"
	@echo ""
	@echo "  make install    - Install dependencies in virtual environment"
	@echo "  make validate   - Validate all YAML files"
	@echo "  make generate   - Generate README.md from YAML data"
	@echo "  make test       - Run validation and generation"
	@echo "  make clean      - Remove generated files and cache"
	@echo "  make migrate    - Run migration (dry-run)"
	@echo ""

install:
	python3 -m venv venv
	$(PIP) install -q -r requirements.txt
	@echo "✓ Dependencies installed in venv/"

validate:
	$(PYTHON) scripts/validate.py

generate:
	$(PYTHON) scripts/generate_readme.py

test: validate generate
	@echo "✓ All tests passed!"

migrate:
	$(PYTHON) scripts/migrate.py --all --dry-run

clean:
	rm -rf __pycache__ scripts/__pycache__
	find . -type f -name "*.pyc" -delete
	@echo "✓ Cleaned cache files"

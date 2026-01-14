.PHONY: help install validate validate-agents validate-boilerplates generate generate-boilerplates migrate-boilerplates clean test test-unit test-all lint typecheck site serve check-links check-links-quick

PYTHON := venv/bin/python
PIP := venv/bin/pip
PYTEST := venv/bin/pytest

help:
	@echo "Ultimate Agent Directory - Build Commands"
	@echo ""
	@echo "  make install              - Install dependencies in virtual environment"
	@echo "  make validate             - Validate all YAML files (agents + boilerplates)"
	@echo "  make validate-agents      - Validate agent YAML files only"
	@echo "  make validate-boilerplates - Validate boilerplate YAML files only"
	@echo "  make generate             - Generate README.md from agent YAML data"
	@echo "  make generate-boilerplates - Generate BOILERPLATES.md from boilerplate data"
	@echo "  make site                 - Generate static website in _site/"
	@echo "  make serve                - Build site and start local web server"
	@echo "  make test                 - Run validation, generation, and quick link check"
	@echo "  make test-unit            - Run unit tests (pytest)"
	@echo "  make test-all             - Run all tests (unit + validation + generation)"
	@echo "  make lint                 - Run linter (ruff check)"
	@echo "  make typecheck            - Run type checker (mypy)"
	@echo "  make check-links          - Check all links in repository"
	@echo "  make check-links-quick    - Quick link check (YAML only, no issues)"
	@echo "  make clean                - Remove generated files and cache"
	@echo "  make migrate              - Run agent migration (dry-run)"
	@echo "  make migrate-boilerplates - Run boilerplate migration (dry-run)"
	@echo ""

install:
	python3 -m venv venv
	$(PIP) install -q -r requirements.txt
	@echo "Dependencies installed in venv/"

validate-agents:
	@echo "Validating agent YAML files..."
	$(PYTHON) scripts/validate.py --agents --categories

validate-boilerplates:
	@echo "Validating boilerplate YAML files..."
	$(PYTHON) scripts/validate.py --boilerplates --boilerplate-categories

validate: validate-agents validate-boilerplates
	@echo "All validation passed!"

generate:
	$(PYTHON) scripts/generate_readme.py

generate-boilerplates:
	$(PYTHON) scripts/generate_boilerplates.py

test: validate generate generate-boilerplates check-links-quick
	@echo "All tests passed!"

test-unit:
	@echo "Running unit tests..."
	$(PYTEST) tests/ -v

test-all: test-unit validate generate generate-boilerplates
	@echo "All tests passed!"

lint:
	@echo "Running linter..."
	venv/bin/ruff check scripts/ tests/

typecheck:
	@echo "Running type checker..."
	venv/bin/mypy scripts/ --ignore-missing-imports

check-links:
	$(PYTHON) scripts/check_links.py --verbose

check-links-quick:
	$(PYTHON) scripts/check_links.py --yaml-only --no-issues

migrate:
	$(PYTHON) scripts/migrate.py --all --dry-run

migrate-boilerplates:
	$(PYTHON) scripts/migrate_boilerplates.py --dry-run

site:
	$(PYTHON) scripts/generate_site.py

serve: site
	@echo ""
	@echo "Starting local web server..."
	@echo "Visit: http://localhost:8001"
	@echo "Press Ctrl+C to stop"
	@echo ""
	cd _site && python3 -m http.server 8001

clean:
	rm -rf __pycache__ scripts/__pycache__ tests/__pycache__ .pytest_cache _site/ reports/*
	find . -type f -name "*.pyc" -delete
	@echo "Cleaned cache files, reports, and _site/"

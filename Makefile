.PHONY: help install validate generate clean test site serve check-links check-links-quick

PYTHON := venv/bin/python
PIP := venv/bin/pip

help:
	@echo "Ultimate Agent Directory - Build Commands"
	@echo ""
	@echo "  make install          - Install dependencies in virtual environment"
	@echo "  make validate         - Validate all YAML files"
	@echo "  make generate         - Generate README.md from YAML data"
	@echo "  make site             - Generate static website in _site/"
	@echo "  make serve            - Build site and start local web server"
	@echo "  make test             - Run validation, generation, and quick link check"
	@echo "  make check-links      - Check all links in repository"
	@echo "  make check-links-quick - Quick link check (YAML only, no issues)"
	@echo "  make clean            - Remove generated files and cache"
	@echo "  make migrate          - Run migration (dry-run)"
	@echo ""

install:
	python3 -m venv venv
	$(PIP) install -q -r requirements.txt
	@echo "✓ Dependencies installed in venv/"

validate:
	$(PYTHON) scripts/validate.py

generate:
	$(PYTHON) scripts/generate_readme.py

test: validate generate check-links-quick
	@echo "✓ All tests passed!"

check-links:
	$(PYTHON) scripts/check_links.py --verbose

check-links-quick:
	$(PYTHON) scripts/check_links.py --yaml-only --no-issues

migrate:
	$(PYTHON) scripts/migrate.py --all --dry-run

site:
	$(PYTHON) scripts/generate_site.py

serve: site
	@echo ""
	@echo "Starting local web server..."
	@echo "Visit: http://localhost:8000"
	@echo "Press Ctrl+C to stop"
	@echo ""
	cd _site && python3 -m http.server 8000

clean:
	rm -rf __pycache__ scripts/__pycache__ _site/ reports/*
	find . -type f -name "*.pyc" -delete
	@echo "✓ Cleaned cache files, reports, and _site/"

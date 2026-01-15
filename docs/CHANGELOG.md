# Changelog

All notable changes to the **Ultimate AI Agent Ecosystem Directory 2025** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

See Previous Changelogs for More Details: `docs/previous_changelogs/`

---

## [2.1.0] - 2026-01-15

### Added
- GitHub metadata refresh workflow for automated star counts and update dates
- `update_github_metadata.py` script to sync repository statistics
- Centralized `tags.yml` file for tag management across the directory
- Shared `filter-utils.js` module for frontend filtering code reuse
- New tests for generators and improved model/validation test coverage

### Changed
- Enhanced tag validation with uniqueness checks and pattern enforcement
- Refactored category and boilerplate JavaScript for better maintainability
- Improved search functionality with token-based matching
- Updated documentation (REFERENCE.md, ARCHITECTURE.md, ADVANCED.md)

### Technical
- Added scheduled GitHub Actions workflow (weekly metadata refresh)
- Centralized tag validation logic in `models.py`
- Improved test coverage for URL extraction and model validation

---

## [2.0.0] - 2025-12-21

### Added
- Full-stack boilerplate directory with 100+ starter kit entries
- 17 ecosystem categories for boilerplates (Next.js, Django, FastAPI, Rails, etc.)
- `BoilerplateEntry` and `TechStackComponent` Pydantic schemas
- `generate_boilerplates.py` for BOILERPLATES.md generation
- `migrate_boilerplates.py` for markdown-to-YAML migration
- Boilerplate-specific website pages and templates
- New Makefile targets: `validate-boilerplates`, `generate-boilerplates`, `migrate-boilerplates`

### Changed
- Updated ARCHITECTURE.md to reflect parallel structure design
- Extended `validate.py` to handle both agents and boilerplates
- Enhanced website with boilerplate navigation and search
- Updated CI/CD workflows for boilerplate validation and deployment

### Technical
- Completed Phase 00 (Feature Addition) with 6 sessions, 141 tasks

---

## [1.0.0] - 2025-11-05

### Added
- Initial YAML-based data architecture
- 277 AI agent entries across 10 categories
- Pydantic schema validation with strict enforcement
- Automated README.md generation from YAML
- Static website with search and filtering
- GitHub Actions CI/CD for validation and deployment
- GitHub Pages deployment

---

## Version History Summary

See Previous Changelogs for More Details: `docs/previous_changelogs/`

| Version | Release Date | Key Features |
|---------|--------------|--------------|
| **2.1.0** | 2026-01-15 | GitHub metadata automation, enhanced validation |
| **2.0.0** | 2025-12-21 | Full-stack boilerplate directory integration |
| **1.0.0** | 2025-11-05 | Initial YAML architecture and AI agent directory |

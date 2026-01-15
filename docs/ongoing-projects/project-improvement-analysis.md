# Project Improvement Analysis

## Scope
- Reviewed docs in `docs/`, scripts in `scripts/`, templates in `templates/`, static JS in `static/js/`, workflows in `.github/workflows/`, and tests in `tests/`.
- Focused on data integrity, automation, site UX, and maintainability.

## Summary
- The data-driven architecture is solid, but there are gaps in validation, documentation consistency, and front-end behavior.
- Most improvements are low to medium effort and reduce drift, reduce user confusion, and improve data quality.

## Progress Update (2026-01-15)
- Removed remaining non-ASCII characters from docs/REFERENCE.md, docs/ADVANCED.md, docs/ROADMAP.md, docs/PRD.md, docs/CLAUDE.md.example, and docs/previous_changelogs/2025-11-05_changelog.md.
- Converted documentation diagrams and examples to ASCII-only formatting, including emoji defaults and arrow notation.
- Updated docs/ADVANCED.md to reference `data/metadata.yml` for base URL changes and removed the maintainer URL from docs/REFERENCE.md.
- Removed the last hardcoded ecosystem count in docs/ARCHITECTURE.md.

## Progress Update (2026-01-14)
- Completed validation CLI argument parsing and Makefile filters for agent and boilerplate validation.
- Added cross-file validation for category existence and duplicate url/github_repo detection.
- Fixed search results to route boilerplate categories based on the search index flag.
- Removed non-ASCII characters and attribution in templates and data, replaced category emoji with ASCII markers, and regenerated README.md and BOILERPLATES.md.
- Removed duplicate agent entries discovered by the new duplicate checks.
- Added `data/metadata.yml` and wired site config into README, site, and boilerplate generators/templates.
- Updated documentation references for boilerplate-categories, current work link, and contribution TODOs.
- Extended link checker to scan docs recursively and support skip rules.
- Added CI quality gates for pytest, ruff, and mypy.
- Added tag registry validation with strict tag formatting and dedupe checks.
- Introduced shared filter utilities and tokenized search on category and boilerplate pages.
- Improved global search scoring with tokenization/prefix matching and escaped regex highlights.
- Removed non-functional boilerplate index search input and cleaned up scripts.
- Added generator output tests plus search index structure coverage.
- Removed hardcoded counts from docs/ARCHITECTURE.md.
- Implemented GitHub metadata refresh script and scheduled workflow.

## High-priority improvements (P0)
- DONE - Validation CLI mismatch: `scripts/validate.py` documents file path usage but does not parse args. Add argument parsing and update `make validate-agents` and `make validate-boilerplates` to filter properly.
- DONE - Cross-file validation: ensure `category` values in entries exist in `data/categories/` and `data/boilerplate-categories/`. Detect duplicate `url` and `github_repo` values across entries.
- DONE - Search result routing: `static/js/search.js` always links to agent category pages. Use `is_boilerplate` from the search index to link to `boilerplates/<id>/index.html` for boilerplates.
- DONE - Rules compliance: templates and generated docs include non-ASCII characters and direct attribution. Align templates and metadata with the ASCII-only and no-attribution rules.

## Medium-priority improvements (P1)
- DONE - Central configuration: move `base_url`, title, tagline, and external links into a config file (for example `data/metadata.yml`) and load it in `scripts/generate_readme.py` and `scripts/generate_site.py`.
- DONE - Documentation drift:
  - `docs/REFERENCE.md` and `docs/ARCHITECTURE.md` reference `boilerplate_categories` but the directory is `boilerplate-categories`.
  - `docs/ROADMAP.md` references `docs/plan.md`, which does not exist.
  - `docs/TODO.md` lists `CONTRIBUTING.md` as missing even though it exists.
- DONE - Link checker coverage: `scripts/check_links.py` only scans top-level docs. Use recursive scanning for `docs/**` and add a allowlist or skip list for unstable domains.
- DONE - CI quality gates: add `pytest`, `ruff`, and `mypy` steps to `.github/workflows/validate.yml`.

## Longer-term improvements (P2)
- DONE - Tag taxonomy and consistency: define an optional tag registry and validate tags against it to prevent drift.
- DONE - Automated metadata refresh: implement the planned GitHub metadata updater and schedule it as a workflow.
- DONE - Search quality: add simple tokenization or prefix search to improve relevance without a backend.
- DONE - Shared JS utilities: reduce duplication between `static/js/category.js` and `static/js/boilerplate.js`.

## Detailed findings

### Data integrity and validation
- DONE - `AgentEntry` and `BoilerplateEntry` normalize tags but do not enforce a strict pattern or de-duplication. Consider rejecting invalid tags instead of silently normalizing them.
- DONE - `category` values are not validated against the actual category files, which allows silent drift and empty category pages.
- DONE - The `validate.py` usage text advertises per-file validation, but there is no argument parsing to support it.

### Documentation consistency
- DONE - The boilerplate category directory name is inconsistent across docs. Standardize references to `data/boilerplate-categories/`.
- DONE - `docs/ROADMAP.md` references `docs/plan.md`, which is missing.
- DONE - `docs/ARCHITECTURE.md` hard-codes counts that will drift over time. Consider generating these numbers or removing them.

### Generation and configuration
- DONE - `scripts/generate_site.py` hard-codes `base_url`. A config file or environment variable would remove the need for code edits during deployment changes.
- DONE - `DirectoryMetadata` includes values that should live in data, not code, to avoid code edits for metadata changes.

### Site UX and search
- DONE - Global search results do not distinguish agent and boilerplate category pages when generating "View Category" links.
- DONE - `static/js/search.js` uses a regex built from the raw search term without escaping special characters.
- DONE - `templates/boilerplate_index.html.jinja2` shows a search input, but the page has no list to filter. Either wire it to a global search index or remove the input to avoid a non-functional control.
- DONE - The boilerplate and agent filter scripts are nearly identical, which increases maintenance cost.

### Testing and CI
- DONE - Tests focus on schema validation and URL extraction only. Add tests for generator outputs and search index structure.
- DONE - CI does not run unit tests or lint checks, which leaves regressions undetected.

## Suggested next steps
- Implement P0 items first (validation CLI, cross-file checks, search routing, rules compliance).
- Fix documentation drift and add a configuration file for site metadata.
- Add unit tests for generators and enable linting in CI.

# AGENTS.md

This file provides guidance to Agents when working with this repository.

# IMPORTANT RULE

  - YOU MUST ONLY USE VALID ASCII UTF-8 LF CHARACTERS!

## Repository Overview

The **Ultimate AI Agent Ecosystem Directory 2025** is a data-driven documentation project that maintains a comprehensive, curated directory of AI agent frameworks, platforms, tools, and resources.

**CRITICAL:** This is NOT a software development project - there is no application code to build, test, or run. This is a documentation curation project using a modern data architecture:

- **YAML files** in `data/` are the single source of truth
- **README.md** is GENERATED - never edit directly
- **Static website** is GENERATED in `_site/` from YAML data
- Python scripts validate YAML and generate outputs

## Essential Build Commands

All development uses the Makefile:

```bash
make install    # Install Python dependencies in venv
make validate   # Validate all YAML files against schemas (ALWAYS RUN BEFORE COMMITTING)
make generate   # Generate README.md from YAML data
make site       # Generate static website in _site/
make serve      # Build site + start local server (http://localhost:8000)
make test       # Run validation + generation (CI-friendly)
make clean      # Remove generated files and cache
```

**Standard workflow:**
1. Edit YAML files in `data/agents/` or `data/categories/`
2. Run `make validate` to check schema compliance
3. Run `make generate` to update README.md
4. Run `make site` to regenerate website (optional)
5. Commit YAML files AND generated README.md

## Data Architecture

### Source of Truth: YAML Files

All content lives in structured YAML files:

**Agent/Tool Entries:** `data/agents/{category}/{name}.yml`

```yaml
# REQUIRED FIELDS
name: str                          # 1-100 characters
url: HttpUrl                       # Valid HTTP/HTTPS URL
description: str                   # 20-1000 characters
category: str                      # Must match a category ID

# CLASSIFICATION
type: framework|platform|tool|course|community|research
tags: List[str]                    # Lowercase, hyphenated

# OPTIONAL METADATA
subcategory: Optional[str]         # For grouping within categories
github_repo: Optional[str]         # Format: "owner/repo"
documentation_url: Optional[HttpUrl]
demo_url: Optional[HttpUrl]
platform: Optional[List[str]]      # e.g., ["Python", "TypeScript"]
license: Optional[str]             # e.g., "MIT", "Apache-2.0"
pricing: Optional[free|freemium|paid|enterprise]

# EDITORIAL FLAGS
featured: bool                     # Highlight on homepage
verified: bool                     # Link checked, complete metadata

# TRACKING
added_date: Optional[date]
last_verified: Optional[date]
```

**Category Definitions:** `data/categories/{category-id}.yml`

```yaml
id: str                            # URL-safe identifier
title: str                         # Display title
description: str                   # 10-500 characters
emoji: str                         # Default: "📦"
order: int                         # Display order (lower = earlier)
show_github_stats: bool            # Default: true
table_columns: List[str]           # Columns to show in tables
```

### Generated Outputs (DO NOT EDIT DIRECTLY)

1. **README.md** - Generated from `templates/readme.jinja2`
   - Markdown tables for GitHub display
   - Organized by categories with emoji headers
   - Badge with total entry count
   - **ALWAYS commit the generated README.md** (it's the main file users see on GitHub)

2. **_site/** - Static website (gitignored, not committed)
   - Interactive HTML pages with search/filtering
   - Generated from `templates/*.html.jinja2`
   - Deployed to GitHub Pages via Actions

### Data Flow

```
YAML Data (data/)
    ↓
Validation (scripts/validate.py using Pydantic schemas)
    ↓
Loading (load_categories() + load_agents())
    ↓
Template Rendering (Jinja2)
    ↓
Outputs (README.md + _site/)
```

## Key Files and Their Roles

### Data Files (Source of Truth)
- `data/agents/**/*.yml` - agent/tool entries organized by category
- `data/categories/*.yml` - category definitions

### Python Scripts
- `scripts/models.py` - Pydantic schemas (AgentEntry, Category, DirectoryMetadata)
- `scripts/validate.py` - YAML validation against schemas (exits with error on failure)
- `scripts/generate_readme.py` - README.md generator
- `scripts/generate_site.py` - Static website generator
- `scripts/migrate.py` - Migration tool (markdown → YAML, completed)

### Templates
- `templates/readme.jinja2` - README.md template
- `templates/base.html.jinja2` - Website base layout
- `templates/index.html.jinja2` - Homepage template
- `templates/category.html.jinja2` - Category page template

### Configuration
- `Makefile` - Build commands (primary interface)
- `requirements.txt` - Python dependencies (Pydantic, PyYAML, Jinja2)
- `.github/workflows/deploy.yml` - Auto-deploy to GitHub Pages on push to main
- `.github/workflows/validate.yml` - Validate YAML on PRs

## Directory Structure

```
data/
├── agents/                        # YAML files (SOURCE OF TRUTH)
│   ├── open-source-frameworks/
│   ├── no-code-platforms/
│   ├── autonomous-agents/
│   ├── specialized-tools/
│   ├── enterprise-platforms/
│   ├── coding-assistants/
│   ├── browser-automation/
│   ├── communities/
│   ├── learning-resources/
│   └── research-frameworks/
└── categories/                    # category YAML files

scripts/                           # Python automation
templates/                         # Jinja2 templates
static/                            # Website assets (CSS, JS)
_site/                             # Generated website (gitignored)
docs/                              # Project documentation
```

## Content Guidelines

### Writing Descriptions
- **Accuracy over hype** - Focus on factual capabilities, not marketing claims
- **Concise** - 20-1000 characters (2-3 sentences ideal)
- **Factual** - What the tool does and who uses it
- **No attribution** - Never mention individual authors or contributors
- **No affiliate links** - Direct to official sources only

### Technical Requirements
- **Character encoding:** ASCII UTF-8 LF only (no special characters)
- **Line endings:** LF (Unix-style), not CRLF
- **Tags:** Lowercase, hyphenated (e.g., "machine-learning")
- **GitHub repos:** Format as "owner/repo" (validated by schema)
- **URLs:** Must be valid HTTP/HTTPS (validated by Pydantic HttpUrl)

### Schema Validation
- Pydantic enforces strict validation (`extra = "forbid"`)
- Unknown fields are rejected
- Required fields must be present
- Type checking for all fields
- Custom validators for GitHub repo format, lowercase tags, etc.

## Git Workflow

### What to Commit
- YAML files in `data/agents/` and `data/categories/`
- Python scripts in `scripts/`
- Templates in `templates/`
- Static assets in `static/`
- Documentation in `docs/`
- **Generated README.md** (users see this on GitHub)

### What NOT to Commit
- `_site/` directory (generated, gitignored)
- `venv/` directory (Python environment, gitignored)
- `__pycache__/` (Python cache, gitignored)
- `CLAUDE.md` (AI assistant file, gitignored)

### Before Every Commit
1. Run `make validate` to ensure YAML files are valid
2. Run `make generate` to update README.md
3. Commit both YAML changes AND generated README.md

## CI/CD Pipeline

### GitHub Actions Workflows

**validate.yml** (runs on PRs):
- Validates all YAML files against Pydantic schemas
- Tests README generation
- Tests website generation
- Reports errors before merge

**deploy.yml** (runs on push to main):
- Validates YAML files
- Generates README.md
- Generates static website
- Deploys to GitHub Pages

### Deployment
- **Platform:** GitHub Pages
- **URL:** https://moshehbenavraham.github.io/Ultimate-Agent-Directory/
- **Trigger:** Automatic on push to main branch
- **Base path:** `/Ultimate-Agent-Directory` (subdirectory)

## Documentation

The project has three core documentation files:

1. **docs/GETTING_STARTED.md** - Setup, adding agents, GitHub Pages deployment
2. **docs/REFERENCE.md** - Command reference, YAML schema, quick lookup
3. **docs/ADVANCED.md** - Website customization, CI/CD internals, advanced topics

Additional documentation:
- **docs/CHANGELOG.md** - Version history
- **docs/ROADMAP.md** - Future plans

## Common Development Tasks

### Adding a New Agent/Tool

1. Create YAML file: `data/agents/{category}/{name}.yml`
2. Follow the schema (see "Data Architecture" section above)
3. Validate: `make validate`
4. Generate outputs: `make generate`
5. Preview website: `make serve` (view at http://localhost:8000)
6. Commit YAML file and generated README.md

### Adding a New Category

1. Create YAML file: `data/categories/{category-id}.yml`
2. Include id, title, description, emoji, order
3. Create directory: `data/agents/{category-id}/`
4. Update category references in existing agents if needed
5. Validate and generate: `make validate && make generate`

### Updating Existing Entries

1. Edit YAML file: `data/agents/{category}/{name}.yml`
2. Validate: `make validate`
3. Regenerate: `make generate`
4. Commit both YAML and README.md

### Previewing Changes Locally

```bash
make serve              # Builds site and starts server
# Visit http://localhost:8000
# Press Ctrl+C to stop
```

## Schema Validation Details

The Pydantic schemas in `scripts/models.py` enforce strict data quality:

- **AgentEntry:** Validates all agent/tool entries
  - URL validation (must be valid HTTP/HTTPS)
  - Description length (20-1000 chars)
  - GitHub repo format ("owner/repo")
  - Tag formatting (lowercase, hyphenated)
  - Type enforcement (literal enums)

- **Category:** Validates category definitions
  - ID format (URL-safe)
  - Description length (10-500 chars)
  - Required fields

- **DirectoryMetadata:** Overall directory metadata
  - Total count tracking
  - Last updated timestamp

All validation errors include:
- File path where error occurred
- Field name with issue
- Detailed error message
- Line number (when available)

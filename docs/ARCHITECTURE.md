# Architecture

System design and data flow for the Ultimate AI Agent Directory.

## System Overview

This is a **data-driven documentation project** that maintains two curated directories:
1. **AI Agent Directory** - Frameworks, platforms, tools, and resources
2. **Full-Stack Boilerplate Directory** - Starter kits, templates, and scaffolds

All content is stored as structured YAML and automatically transformed into README.md, BOILERPLATES.md, and a static website.

## Data Flow

```
YAML Data (data/)
       |
       +---> data/agents/         (278 AI agent entries)
       +---> data/boilerplates/   (100+ boilerplate entries)
       +---> data/categories/     (10 agent categories)
       +---> data/boilerplate-categories/ (17 ecosystems)
       |
       v
Schema Validation (Pydantic)
       |
       v
Data Loading (Python)
       |
       v
Template Rendering (Jinja2)
       |
       +---> README.md (AI agents)
       +---> BOILERPLATES.md (Full-stack starters)
       +---> _site/ (Static website with both directories)
```

## Component Diagram

```
+------------------------+     +---------------------------+
|     data/agents/       |     |    data/boilerplates/     |
|  278 AI agent entries  |     |  100+ boilerplate entries |
+------------------------+     +---------------------------+
            |                              |
            v                              v
+------------------------+     +---------------------------+
|    data/categories/    |     | data/boilerplate-categories/ |
|  10 agent categories   |     |  17 ecosystem categories  |
+------------------------+     +---------------------------+
            |                              |
            +------------------------------+
                           |
                           v
            +----------------------------+
            |         scripts/           |
            | - models.py (Pydantic)     |
            | - validate.py              |
            | - generate_readme.py       |
            | - generate_boilerplates.py |
            | - generate_site.py         |
            +----------------------------+
                           |
                           v
            +----------------------------+
            |        templates/          |
            +----------------------------+
                           |
           +---------------+---------------+
           |               |               |
           v               v               v
      README.md    BOILERPLATES.md    _site/
    (AI agents)    (Full-stack)     (Website)
                                         |
                                         v
                                   GitHub Pages
```

## Components

### YAML Data Layer (`data/`)

**Purpose:** Single source of truth for all directory content

**Structure:**
- `data/agents/{category}/*.yml` - AI agent/tool entries (278 files)
- `data/categories/*.yml` - Agent category definitions (10 files)
- `data/boilerplates/{ecosystem}/*.yml` - Boilerplate entries (100+ files)
- `data/boilerplate-categories/*.yml` - Boilerplate categories (17 ecosystems)

**Validation:** Pydantic models in `scripts/models.py` enforce schema compliance

### Validation Layer (`scripts/`)

**Purpose:** Ensure data quality and schema compliance

**Key Files:**
- `models.py` - AgentEntry, BoilerplateEntry, Category schemas
- `validate.py` - YAML loading and validation functions

**Features:**
- Strict schema enforcement (`extra = "forbid"`)
- URL validation (HttpUrl type)
- Description length constraints (agents: 20-1000 chars, boilerplates: 20-2000 chars)
- GitHub repo format validation (`owner/repo`)
- Tag normalization (lowercase, hyphenated)
- Technical stack validation for boilerplates

### Generation Layer

**Purpose:** Transform YAML data into readable outputs

**Generators:**
- `generate_readme.py` - Creates README.md with AI agent tables
- `generate_boilerplates.py` - Creates BOILERPLATES.md with starter kit tables
- `generate_site.py` - Creates static website in `_site/` with both directories

**Templates:**
- `templates/readme.jinja2` - AI agents README structure
- `templates/boilerplates_readme.jinja2` - Boilerplates README structure
- `templates/base.html.jinja2` - Website layout
- `templates/index.html.jinja2` - Homepage
- `templates/category.html.jinja2` - Agent category pages
- `templates/boilerplate_category.html.jinja2` - Boilerplate category pages

### Deployment Layer

**Purpose:** Automated CI/CD pipeline

**Workflows:**
- `.github/workflows/validate.yml` - PR validation
- `.github/workflows/deploy.yml` - Build and deploy to GitHub Pages

**Pipeline:**
```
Push to main
     |
     v
Validate YAML --> Generate README --> Build Site --> Deploy
```

## Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Data Format | YAML | Human-readable, version-controllable data |
| Validation | Pydantic | Type-safe schema enforcement |
| Templating | Jinja2 | README and website generation |
| Parsing | PyYAML | YAML file loading |
| Website | Static HTML | Fast, serverless hosting |
| Styling | Tailwind CSS | Responsive design |
| Hosting | GitHub Pages | Free static site hosting |
| CI/CD | GitHub Actions | Automated validation and deployment |

## Directory Structure

```
Ultimate-Agent-Directory/
|
+-- data/
|   +-- agents/                 # 278 AI agent entries
|   |   +-- open-source-frameworks/
|   |   +-- no-code-platforms/
|   |   +-- autonomous-agents/
|   |   +-- specialized-tools/
|   |   +-- enterprise-platforms/
|   |   +-- coding-assistants/
|   |   +-- browser-automation/
|   |   +-- communities/
|   |   +-- learning-resources/
|   |   +-- research-frameworks/
|   +-- categories/             # 10 agent category definitions
|   +-- boilerplates/           # 100+ boilerplate entries
|   |   +-- nextjs/
|   |   +-- django/
|   |   +-- fastapi/
|   |   +-- rails/
|   |   +-- ... (17 ecosystems)
|   +-- boilerplate-categories/ # 17 boilerplate category definitions
|
+-- scripts/                    # Python automation
|   +-- models.py               # Pydantic schemas
|   +-- validate.py             # Validation logic
|   +-- generate_readme.py      # AI agents README generator
|   +-- generate_boilerplates.py # Boilerplates README generator
|   +-- generate_site.py        # Website generator
|   +-- migrate_boilerplates.py # Boilerplate migration utilities
|   +-- check_links.py          # Link validation
|
+-- templates/                  # Jinja2 templates
|   +-- readme.jinja2
|   +-- boilerplates_readme.jinja2
|   +-- base.html.jinja2
|   +-- index.html.jinja2
|   +-- category.html.jinja2
|   +-- boilerplate_category.html.jinja2
|
+-- static/                     # Website assets
|   +-- css/style.css
|   +-- js/
|
+-- docs/                       # Documentation
+-- _site/                      # Generated website (gitignored)
+-- README.md                   # Generated AI agents directory
+-- BOILERPLATES.md             # Generated boilerplates directory
```

## Key Design Decisions

### 1. YAML as Source of Truth

**Decision:** Store all content in structured YAML files rather than directly editing README.md

**Rationale:**
- Enables schema validation before publishing
- Supports multiple output formats (markdown, HTML)
- Version control shows meaningful diffs
- Automation-friendly for bulk updates

### 2. Generated README

**Decision:** Auto-generate README.md from YAML data

**Rationale:**
- Single source of truth prevents inconsistencies
- Guaranteed schema compliance
- Consistent formatting across all entries
- Enables future features (stats, filtering)

### 3. Static Website

**Decision:** Generate static HTML rather than dynamic server application

**Rationale:**
- Zero hosting costs (GitHub Pages)
- Fast page loads (no server processing)
- No database maintenance
- Simple deployment (file upload)
- High availability and security

### 4. Client-Side Search

**Decision:** Implement search in JavaScript rather than server-side

**Rationale:**
- Works with static hosting
- Instant results (no network latency)
- Full content indexed at build time
- No backend infrastructure required

### 5. Pydantic Validation

**Decision:** Use Pydantic for schema enforcement

**Rationale:**
- Type safety with Python type hints
- Automatic validation with clear error messages
- Strict mode prevents unknown fields
- Custom validators for complex rules

## Build Commands

```bash
make install    # Create venv and install dependencies
make validate   # Validate YAML files against schemas
make generate   # Generate README.md from YAML
make site       # Generate static website
make serve      # Build and serve locally (port 8001)
make test       # Run validation + generation
make clean      # Remove generated files
```

## Deployment

**Platform:** GitHub Pages
**URL:** https://moshehbenavraham.github.io/Ultimate-Agent-Directory/
**Trigger:** Push to main branch
**Pipeline:** Validate -> Generate -> Build -> Deploy

See `docs/ADVANCED.md` for alternative deployment options.

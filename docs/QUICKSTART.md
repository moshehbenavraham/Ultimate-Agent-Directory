# Quick Start Guide - Structured Data System

This guide helps you get started with the new YAML-based structured data system for the Ultimate Agent Directory.

## System Overview

The directory now uses a **data-driven architecture**:
- **Source of Truth**: YAML files in `data/`
- **Generated Output**: README.md (and future website)
- **Validation**: Pydantic schemas ensure data quality
- **Automation**: Scripts handle generation and validation

## Prerequisites

```bash
# Python 3.10+ required
python3 --version

# Install dependencies
make install
# OR manually:
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

## Common Commands

```bash
# Validate all YAML files
make validate

# Generate README.md from YAML data
make generate

# Run both validation and generation
make test

# Preview migration (doesn't write files)
make migrate
```

## Directory Structure

```
data/
  agents/          # Individual agent YAML files
    frameworks/    # Framework agents
    platforms/     # Platform agents
    ...
  categories/      # Category definitions

scripts/
  models.py        # Pydantic schemas
  validate.py      # Validation script
  generate_readme.py  # README generator
  migrate.py       # Migration tool

templates/
  readme.jinja2    # README template
```

## Adding a New Agent

### Option 1: Create YAML file manually

1. Create a new file in the appropriate category folder:
   ```bash
   touch data/agents/frameworks/my-agent.yml
   ```

2. Add the agent data (minimum required fields):
   ```yaml
   name: My Agent
   url: https://github.com/example/my-agent
   description: >
     A clear, factual description of what this agent does.
     Minimum 20 characters, maximum 1000.

   category: open-source-frameworks
   type: framework

   # Optional but recommended
   github_repo: example/my-agent
   tags:
     - python
     - ai-agent
   ```

3. Validate:
   ```bash
   make validate
   ```

4. Generate updated README:
   ```bash
   make generate
   ```

### Option 2: Use the migration script

If you have entries in markdown format, use the migration script:

```bash
# Test first with dry-run
venv/bin/python scripts/migrate.py --section "🛠️ Section Name" --category category-id --dry-run

# If looks good, run for real
venv/bin/python scripts/migrate.py --section "🛠️ Section Name" --category category-id
```

## Adding a New Category

1. Create a category definition file:
   ```bash
   touch data/categories/my-category.yml
   ```

2. Define the category:
   ```yaml
   id: my-category
   title: My Category Title
   emoji: 🚀
   description: A brief description of this category

   order: 10  # Display order (lower = earlier)
   show_github_stats: true

   table_columns:
     - name
     - url
     - description
   ```

3. Add agents to this category (set `category: my-category` in agent YAML files)

4. Validate and generate:
   ```bash
   make test
   ```

## Schema Reference

### AgentEntry Fields

**Required:**
- `name`: Agent/tool name (1-100 chars)
- `url`: Primary URL (must be valid HTTP/HTTPS)
- `description`: Clear description (20-1000 chars)
- `category`: Category ID (must match a category file)

**Optional (but recommended):**
- `github_repo`: GitHub repo in "owner/repo" format
- `type`: framework | platform | tool | course | community | research
- `tags`: List of lowercase, hyphenated tags
- `documentation_url`: Documentation URL
- `demo_url`: Demo/website URL
- `platform`: List of languages/platforms (e.g., ["Python", "TypeScript"])
- `license`: License type (e.g., "MIT", "Apache-2.0")
- `pricing`: free | freemium | paid | enterprise
- `featured`: true/false (highlight on homepage)
- `verified`: true/false (manually verified entry)

**Auto-populated (by GitHub Actions in future):**
- `github_stars`: Star count
- `last_updated`: Last commit date
- `is_archived`: Repo archived status

### Category Fields

**Required:**
- `id`: URL-safe identifier (lowercase-hyphenated)
- `title`: Display title
- `description`: Category description (10-500 chars)

**Optional:**
- `emoji`: Emoji for visual identification (default: 📦)
- `order`: Display order (default: 0)
- `parent`: Parent category ID for subcategories
- `show_github_stats`: Show star badges (default: true)
- `table_columns`: Columns to show in tables

## Validation Errors

Common validation errors and fixes:

```
✗ url: Input should be a valid URL
→ Fix: Ensure URL starts with http:// or https://

✗ description: String should have at least 20 characters
→ Fix: Add more detail to the description

✗ github_repo must be 'owner/repo' format
→ Fix: Change "github.com/owner/repo" to "owner/repo"

✗ Extra inputs are not permitted
→ Fix: Remove any fields not in the schema
```

## Workflow

1. **Edit YAML files** in `data/`
2. **Validate** with `make validate`
3. **Generate README** with `make generate`
4. **Review changes** (compare old vs new README.md)
5. **Commit** both YAML source files and generated README.md

## Next Steps

- See `docs/plan.md` for full implementation plan
- See `docs/TODO.md` for roadmap of future features
- See `docs/SCHEMA.md` (to be created) for complete schema documentation

## Getting Help

- File issues: https://github.com/aiwithapex/Ultimate-Agent-Directory/issues
- Start discussions: https://github.com/aiwithapex/Ultimate-Agent-Directory/discussions
- Email: contact@aiwithapex.com

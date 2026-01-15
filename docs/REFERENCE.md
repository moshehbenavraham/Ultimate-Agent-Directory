# Quick Reference

## Commands

```bash
make install     # Install Python dependencies in venv
make validate    # Validate YAML against schemas
make generate    # Generate README.md from YAML
make site        # Generate static website in _site/
make serve       # Build site + start server (http://localhost:8001)
make test        # Run validation + generation (CI-friendly)
make refresh-github-metadata # Update GitHub stars and repo metadata
make clean       # Remove generated files and cache
```

## File Structure

```
data/
|-- agents/               # Agent YAML files
|   |-- open-source-frameworks/
|   |-- no-code-platforms/
|   |-- autonomous-agents/
|   |-- specialized-tools/
|   |-- enterprise-platforms/
|   |-- coding-assistants/
|   |-- browser-automation/
|   |-- communities/
|   |-- learning-resources/
|   `-- research-frameworks/
|-- boilerplates/         # Boilerplate YAML files
|   |-- nextjs/
|   |-- django/
|   |-- fastapi/
|   |-- rails/
|   `-- ... (multiple ecosystems)
|-- categories/           # Agent category definitions
|-- boilerplate-categories/ # Boilerplate category definitions
|-- tags.yml              # Optional tag registry for validation
`-- metadata.yml          # Site metadata and external links

scripts/
|-- models.py             # Pydantic schemas
|-- validate.py           # YAML validation
|-- generate_readme.py    # README generator
|-- update_github_metadata.py # Refresh GitHub stars and metadata
`-- generate_site.py      # Website generator

templates/
|-- readme.jinja2         # README template
|-- base.html.jinja2      # Website base layout
|-- index.html.jinja2     # Homepage template
`-- category.html.jinja2  # Category page template

static/
|-- css/style.css         # Custom styling
`-- js/                   # Search and filtering

_site/                    # Generated website (gitignored)
```

## YAML Schema

### Agent Entry

**Required:**
```yaml
name: str                # 1-100 characters
url: HttpUrl             # Valid HTTP/HTTPS URL
description: str         # 20-1000 characters
category: str            # Must match category ID
```

**Optional:**
```yaml
type: framework|platform|tool|course|community|research
subcategory: str
tags: [str]              # Lowercase, hyphenated (see data/tags.yml)
github_repo: str         # Format: "owner/repo"
documentation_url: HttpUrl
demo_url: HttpUrl
platform: [str]          # e.g., ["Python", "TypeScript"]
license: str             # e.g., "MIT", "Apache-2.0"
pricing: free|freemium|paid|enterprise
github_stars: int        # Auto-updated by GitHub metadata job
last_updated: date       # Last commit date
is_archived: bool        # Repo archived flag
featured: bool
verified: bool
added_date: date
last_verified: date
```

### Boilerplate Entry

**Required:**
```yaml
name: str                # 1-100 characters
url: HttpUrl             # Valid HTTP/HTTPS URL
description: str         # 20-2000 characters
category: str            # Must match boilerplate category ID
```

**Optional:**
```yaml
type: starter|boilerplate|template|scaffold|toolkit
tags: [str]              # Lowercase, hyphenated (see data/tags.yml)
github_repo: str         # Format: "owner/repo"
github_stars: int
last_updated: date
is_archived: bool
documentation_url: HttpUrl
demo_url: HttpUrl
platform: [str]          # e.g., ["TypeScript", "React"]
license: str             # e.g., "MIT"
pricing: free|freemium|paid|enterprise|open-core
technical_stack:         # Structured tech info
  - component: str       # e.g., "Frontend"
    technology: str      # e.g., "Next.js"
    reasoning: str       # Optional: why chosen
key_features: [str]      # List of features
use_case: str            # Ideal use case description
pros: [str]              # Advantages
cons: [str]              # Limitations
community: str           # Community info (Discord, forums)
deployment: [str]        # e.g., ["Vercel", "AWS"]
featured: bool
verified: bool
added_date: date
last_verified: date
```

### Category Definition

**Required:**
```yaml
id: str                  # URL-safe identifier
title: str
description: str         # 10-500 characters
```

**Optional:**
```yaml
emoji: str               # Default: "[]"
order: int               # Display order (lower = earlier)
show_github_stats: bool  # Default: true
table_columns: [str]     # Columns to show in tables
```

## Validation Errors

```
url: Input should be a valid URL
-> Ensure URL starts with http:// or https://

description: String should have at least 20 characters
-> Add more detail

github_repo must be 'owner/repo' format
-> Use "owner/repo", not full URL

Extra inputs are not permitted
-> Remove unknown fields
```

## URLs

- **Repository:** https://github.com/moshehbenavraham/Ultimate-Agent-Directory
- **Website:** https://moshehbenavraham.github.io/Ultimate-Agent-Directory
- **Issues:** https://github.com/moshehbenavraham/Ultimate-Agent-Directory/issues

## Documentation

- **GETTING_STARTED.md** - Setup, adding agents, deployment
- **REFERENCE.md** - This file (quick lookup)
- **ADVANCED.md** - Customization, CI/CD, advanced topics
- **CHANGELOG.md** - Version history
- **ROADMAP.md** - Future plans

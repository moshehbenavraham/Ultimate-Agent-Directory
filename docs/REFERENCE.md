# Quick Reference Guide

## Build Commands

```bash
# Validate YAML files
make validate

# Generate README
make generate

# Generate website
make site

# Preview website locally (builds + starts server)
make serve

# Run all checks (validate + generate)
make test

# Clean generated files
make clean
```

## File Structure

```
data/
├── agents/              # Individual agent YAML files
│   ├── open-source-frameworks/
│   ├── no-code-platforms/
│   ├── autonomous-agents/
│   └── ...
└── categories/          # Category definition YAML files

scripts/
├── models.py           # Pydantic schemas
├── validate.py         # YAML validation
├── generate_readme.py  # README generator
└── generate_site.py    # Website generator

templates/
├── readme.jinja2       # README template
├── base.html.jinja2    # Website base layout
├── index.html.jinja2   # Homepage template
└── category.html.jinja2 # Category page template

static/
├── css/style.css       # Custom styling
└── js/                 # JavaScript for search/filtering

_site/                  # Generated website (gitignored)
```

## URLs

- **Website:** https://aiwithapex.github.io/Ultimate-Agent-Directory
- **Repository:** https://github.com/AIwithApex/Ultimate-Agent-Directory
- **Issues:** https://github.com/AIwithApex/Ultimate-Agent-Directory/issues
- **Maintainer:** https://AIwithApex.com

## Documentation Index

- `docs/plan.md` - TODO list (what needs to be done)
- `docs/CHANGELOG.md` - Complete history of changes
- `docs/ROADMAP.md` - Future enhancements and long-term plans
- `docs/QUICKSTART.md` - Getting started guide
- `docs/WEBSITE.md` - Website generation guide
- `docs/DEPLOYMENT.md` - GitHub Pages deployment guide
- `docs/GITHUB_PAGES_SETUP.md` - Quick setup instructions
- `docs/REFERENCE.md` - This file (quick reference)

## Contact

- **Email:** contact@aiwithapex.com
- **Issues:** Use GitHub issue templates
- **Discussions:** GitHub Discussions

---

**Future plans:** See `docs/ROADMAP.md`

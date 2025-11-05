# Structured Data System - Implementation Roadmap

See docs/CHANGELOG.md for work completed

## Remaining Work

### PHASE 3: Data Migration

**Goal:** Convert 280+ entries from current README.md to individual YAML files

**Status:** Migration script ready, awaiting execution decision

Chosen path - manual work:

**Steps:**
1. Create all 10 category YAML files
2. Convert entries section by section
3. YES!  Add rich metadata during conversion (tags, subcategories, pricing, etc.)
4. Validate continuously with `make validate`
5. Generate and review after each section

**Pros:** Highest quality, complete metadata, no errors
**Cons:** Time-consuming, manual work

#### Category Files Needed

Create these 10 category YAML files in `data/categories/`:

1. `open-source-frameworks.yml` (order: 1) ✓ exists
2. `no-code-platforms.yml` (order: 2) ✓ exists
3. `research-frameworks.yml` (order: 3)
4. `learning-resources.yml` (order: 4)
5. `communities.yml` (order: 5)
6. `specialized-tools.yml` (order: 6)
7. `autonomous-agents.yml` (order: 7)
8. `browser-automation.yml` (order: 8)
9. `coding-assistants.yml` (order: 9)
10. `enterprise-platforms.yml` (order: 10)

---

### PHASE 4: Website Generation (3-5 days)

**Goal:** Generate static HTML website from YAML data

**Status:** Infrastructure ready, templates needed

#### 4.1 HTML Templates

Create in `templates/`:

- `base.html.jinja2` - Base layout with navigation
- `index.html.jinja2` - Homepage with category cards
- `category.html.jinja2` - Category detail pages with filterable tables
- `agent.html.jinja2` - Individual agent detail pages (optional)

**Features:**
- Responsive design (mobile-friendly)
- Client-side search with JavaScript
- Filter by tags, platform, pricing
- Sort by stars, name, date added
- Category navigation
- Statistics dashboard

#### 4.2 Static Assets

Create in `static/`:

- `css/style.css` - Clean, minimal styling (consider Tailwind CSS)
- `js/search.js` - Client-side search and filtering
- `images/` - Logos, icons, placeholders

#### 4.3 Website Generator

**File:** `scripts/generate_site.py`

Features:
- Load all YAML data
- Render HTML templates
- Copy static assets to `_site/`
- Generate sitemap.xml
- Create search index JSON

**Usage:**
```bash
venv/bin/python scripts/generate_site.py
# Output: _site/ directory ready for deployment
```

#### 4.4 Deployment

Options:
- GitHub Pages (free, automatic with Actions)

---

### PHASE 5: Automation & CI/CD (2-3 days)

**Goal:** Automate validation, builds, and metadata updates

**Status:** Ready to implement, requires GitHub Actions

#### 5.1 GitHub Actions Workflows

Create in `.github/workflows/`:

**`validate.yml`** - Run on PRs
```yaml
- Validate all YAML files
- Check for duplicates
- Verify URLs are reachable
- Run on: Pull requests to main
```

**`build.yml`** - Build and deploy
```yaml
- Validate YAML
- Generate README.md
- Generate website (_site/)
- Deploy to GitHub Pages
- Run on: Push to main
```

**`update-metadata.yml`** - Weekly updates
```yaml
- Fetch GitHub stars for all repos
- Update last_updated dates
- Check for archived repos
- Create PR with updates
- Run on: Schedule (weekly)
```

#### 5.2 Pre-commit Hooks

Add pre-commit hooks for local validation

**File:** `.pre-commit-config.yaml`
```yaml
- YAML validation
- Python linting
- Format checking
```

#### 5.3 Link Checker

Add automated link checking:
- Check all URLs are reachable (HTTP 200)
- Flag broken links
- Create issues for manual review

---

### PHASE 6: Documentation (1-2 days)

**Goal:** Update all documentation for new workflow

**Status:** QUICKSTART.md created, others need updates

#### Files to Update

**`CONTRIBUTING.md`**
- New YAML-based contribution workflow
- How to add entries via YAML files
- How to add entries via issues (automated conversion)
- Validation requirements
- PR review process

**`docs/SCHEMA.md`** (new)
- Complete field documentation
- Required vs optional fields
- Validation rules
- Examples for each field type
- Best practices

**`README.md`** (footer)
- Add note about auto-generation
- Link to CONTRIBUTING.md
- Link to SCHEMA.md

**Issue Templates**
- Update suggestion.yml to collect YAML-compatible data
- Auto-generate YAML from issue submissions

---

## Timeline Summary

| Phase | Status | Duration | Deliverable |
|-------|--------|----------|-------------|
| **Phase 1-2: Foundation** | ✓ Complete | 1 day | Schema, validation, generation working |
| **Phase 3: Migration** | Ready | 3-4 days | All 280+ entries in YAML |
| **Phase 4: Website** | Planned | 3-5 days | Static website with search |
| **Phase 5: Automation** | Planned | 2-3 days | GitHub Actions, auto-updates |
| **Phase 6: Documentation** | Partial | 1-2 days | Complete contributor docs |

**Total Remaining:** ~2 weeks to full production system

---

## Success Criteria

- [ ] All 280+ entries migrated to YAML
- [ ] 100% validation pass rate
- [ ] Generated README matches current structure
- [ ] Website deployed and functional
- [ ] GitHub Actions running automatically
- [ ] Contributors can add entries via YAML or issues
- [ ] Link checking automated
- [ ] GitHub metrics auto-update weekly

---
---

## Potential Future Enhancements (Post-Launch)

1. **API Layer** - REST API for programmatic access
2. **JSON Export** - Export directory as JSON for other tools
3. **Community Features** - Voting, reviews, ratings
4. **Automated Discovery** - Scan GitHub for new agents
5. **Quality Badges** - Verification levels, activity status
6. **Analytics** - Track popular agents, trends
7. **Newsletter** - Weekly digest of new additions
8. **Comparison Tool** - Side-by-side framework comparisons

See `docs/TODO.md` for feature ideas.

---

## Getting Help

- **Documentation:** `docs/QUICKSTART.md` for usage
- **Issues:** Report problems or suggest features
- **Discussions:** Ask questions, share ideas
- **Email:** max@aiwithapex.com

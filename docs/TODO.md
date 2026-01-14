# Work TODO List

> **History & completed work:** See `docs/CHANGELOG.md`

---

## Automation & CI/CD

### Weekly Metadata Updates

**Create:** `.github/workflows/update-metadata.yml` and `scripts/update_metadata.py`

**Tasks:**
- [ ] Write `scripts/update_metadata.py`
- [ ] Fetch GitHub stars for all repos with github_repo field
- [ ] Update last_updated dates from GitHub API
- [ ] Check for archived repos (set is_archived: true)
- [ ] Update github_stars field in YAML files
- [ ] Create automated PR with changes
- [ ] Schedule: Weekly (Sunday midnight)

### Pre-commit Hooks

**Create:** `.pre-commit-config.yaml`

**Tasks:**
- [ ] Add YAML validation hook
- [ ] Add YAML linting hook
- [ ] Test locally

---

## Documentation

### Review CONTRIBUTING.md

**File:** `CONTRIBUTING.md` (root level)

**Tasks:**
- [ ] Verify quick start steps match Makefile
- [ ] Confirm YAML submission steps are current
- [ ] Validate issue-based submission flow matches templates
- [ ] Add SCHEMA.md link when available

### Create SCHEMA.md

**File:** `SCHEMA.md` (root level)

**Tasks:**
- [ ] Document all required fields with examples
- [ ] Document all optional fields with examples
- [ ] Explain field validators
- [ ] Document Category schema
- [ ] Add full YAML examples for each entry type
- [ ] Add troubleshooting guide for common validation errors

### Enhance Issue Templates

**File:** `.github/ISSUE_TEMPLATE/suggestion.yml`

**Tasks:**
- [ ] Add platform/language field (dropdown)
- [ ] Add pricing field (dropdown: free, freemium, paid, enterprise)
- [ ] Add tags field (comma-separated)
- [ ] Add GitHub repo field (optional)
- [ ] Add auto-labeling

### Complete README.md Footer

**File:** `templates/readme.jinja2`

**Tasks:**
- [ ] Add website link to footer
- [ ] Fix CONTRIBUTING.md link (file needs to exist first)
- [ ] Add SCHEMA.md link to footer (file needs to exist first)

---

# Work TODO List

> **History & completed work:** See `docs/CHANGELOG.md`

---

## PHASE 5: Automation & CI/CD

### 5.1 Weekly Metadata Updates - NOT STARTED

**Create:** `.github/workflows/update-metadata.yml`

**Tasks:**
- [ ] Write `scripts/update_metadata.py`
- [ ] Fetch GitHub stars for all repos with github_repo field
- [ ] Update last_updated dates from GitHub API
- [ ] Check for archived repos (set is_archived: true)
- [ ] Update github_stars field in YAML files
- [ ] Create automated PR with changes
- [ ] Schedule: Weekly (Sunday midnight)

### 5.2 Pre-commit Hooks - NOT STARTED (OPTIONAL)

**Create:** `.pre-commit-config.yaml`

**Tasks:**
- [ ] Add YAML validation hook
- [ ] Add YAML linting hook
- [ ] Test locally

### 5.3 Link Checker - NOT STARTED

**Create:** `scripts/check_links.py`

**Tasks:**
- [ ] Write script to check all URLs return HTTP 200
- [ ] Add timeout handling (5 seconds per URL)
- [ ] Add retry logic for transient failures
- [ ] Flag broken links in GitHub issues
- [ ] Add rate limiting
- [ ] Create `.github/workflows/link-check.yml` for weekly checks

---

## PHASE 6: Documentation

### 6.1 Update CONTRIBUTING.md - NOT STARTED

**Tasks:**
- [ ] Add Quick Start section (fork, clone, setup)
- [ ] Document adding agents via YAML workflow
- [ ] Document adding agents via GitHub Issues
- [ ] Document adding new categories
- [ ] List validation requirements
- [ ] Explain PR review process

### 6.2 Create SCHEMA.md - NOT STARTED

**Tasks:**
- [ ] Document all required fields with examples
- [ ] Document all optional fields with examples
- [ ] Explain field validators
- [ ] Document Category schema
- [ ] Add full YAML examples for each entry type
- [ ] Add troubleshooting guide for common validation errors

### 6.3 Update Issue Templates - NOT STARTED

**File:** `.github/ISSUE_TEMPLATE/suggestion.yml`

**Tasks:**
- [ ] Add platform/language field (dropdown)
- [ ] Add pricing field (dropdown: free, freemium, paid, enterprise)
- [ ] Add tags field (comma-separated)
- [ ] Add GitHub repo field (optional)
- [ ] Add auto-labeling

### 6.4 Update README.md Footer - NOT STARTED

**Tasks:**
- [ ] Add generation notice
- [ ] Add link to CONTRIBUTING.md
- [ ] Add link to SCHEMA.md
- [ ] Add website link
- [ ] Add "do not edit directly" warning

---

## DEPLOYMENT

### First Deployment - IN PROGRESS

**Tasks:**
- [ ] Enable GitHub Pages (Settings > Pages > Source: GitHub Actions)
- [ ] Set workflow permissions (Settings > Actions > Read and write permissions)
- [ ] Commit all changes
- [ ] Push to main branch
- [ ] Monitor Actions tab for deployment
- [ ] Verify site is live at https://aiwithapex.github.io/Ultimate-Agent-Directory

---

## Success Checklist

- [ ] Website live at https://aiwithapex.github.io/Ultimate-Agent-Directory
- [ ] First deployment verified successful
- [ ] Weekly GitHub metadata updates automated
- [ ] Link checker running automatically
- [ ] CONTRIBUTING.md updated with YAML workflow
- [ ] SCHEMA.md created with complete field docs
- [ ] Issue templates enhanced for structured data
- [ ] README footer updated with generation notice

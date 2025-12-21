# Getting Started

Quick guide to set up, contribute to, and deploy the Ultimate Agent Directory.

## Prerequisites

```bash
# Python 3.10+ required
python3 --version

# Install dependencies
make install
```

## Essential Commands

```bash
make validate    # Validate YAML files
make generate    # Generate README.md
make site        # Generate website
make serve       # Build site + start local server (http://localhost:8001)
make test        # Run validation + generation
make clean       # Remove generated files
```

## Adding a New Agent

### 1. Create YAML File

Create `data/agents/{category}/{agent-name}.yml`:

```yaml
# Required fields
name: Agent Name
url: https://example.com
description: Clear, factual description of what this agent does. Minimum 20 characters.
category: specialized-tools

# Recommended fields
type: framework  # or: platform, tool, course, community, research
tags:
  - python
  - ai-agent
github_repo: owner/repo
platform:
  - Python
license: MIT
pricing: free  # or: freemium, paid, enterprise
```

### 2. Validate and Generate

```bash
make validate    # Check schema compliance
make generate    # Update README.md
```

### 3. Commit

```bash
git add data/agents/{category}/{agent-name}.yml README.md
git commit -m "Add {Agent Name}"
git push
```

## Adding a New Boilerplate

### 1. Create YAML File

Create `data/boilerplates/{category}/{boilerplate-name}.yml`:

```yaml
# Required fields
name: Boilerplate Name
url: https://github.com/owner/repo
description: Clear description of what this boilerplate provides. Minimum 20 characters.
category: nextjs

# Recommended fields
type: boilerplate  # or: starter, template, scaffold, toolkit
tags:
  - nextjs
  - react
  - typescript
github_repo: owner/repo
github_stars: 1000
license: MIT
pricing: free  # or: freemium, paid, enterprise, open-core

# Optional fields
technical_stack:
  - component: Frontend
    technology: Next.js
    reasoning: Industry standard React framework
  - component: Database
    technology: PostgreSQL
    reasoning: Reliable relational database

key_features:
  - Feature one description
  - Feature two description

use_case: Ideal for building SaaS applications...

pros:
  - Advantage one
  - Advantage two

cons:
  - Limitation one
```

### 2. Validate and Generate

```bash
make validate    # Check schema compliance
make site        # Regenerate website with boilerplate
```

### 3. Commit

```bash
git add data/boilerplates/{category}/{name}.yml
git commit -m "Add {Boilerplate Name}"
git push
```

## Deploying to GitHub Pages

### Initial Setup (One-Time)

1. **Enable GitHub Pages**
   - Go to repository Settings > Pages
   - Set Source to: **GitHub Actions**
   - Save

2. **Set Workflow Permissions**
   - Go to Settings > Actions > General
   - Select: **Read and write permissions**
   - Check: **Allow GitHub Actions to create and approve pull requests**
   - Save

3. **Push to Trigger Deployment**

```bash
git push origin main
```

### Monitor Deployment

- Go to **Actions** tab
- Watch "Build and Deploy to GitHub Pages" workflow
- Completion time: ~2-3 minutes
- Site live at: `https://{username}.github.io/{repo-name}/`

### Automatic Updates

Every push to `main` automatically:
1. Validates YAML files
2. Generates README.md
3. Builds website
4. Deploys to GitHub Pages

## Common Issues

**Validation fails:**
- Check YAML syntax
- Ensure description is 20-1000 characters
- Verify URL format: `https://example.com`
- GitHub repo format: `owner/repo` (not full URL)

**Workflow fails:**
- Check Actions tab for error logs
- Verify workflow permissions are set correctly

**Website not updating:**
- Wait 1-2 minutes for CDN propagation
- Clear browser cache (Ctrl+F5 or Cmd+Shift+R)
- Verify workflow completed successfully in Actions tab

**404 error:**
- Confirm GitHub Pages is enabled
- Ensure Source is set to "GitHub Actions"
- Check workflow completed without errors

## Content Guidelines

**Descriptions:**
- Accuracy over hype
- 2-3 sentences ideal
- What it does and who uses it
- No individual attribution
- No affiliate links

**Technical Requirements:**
- ASCII UTF-8 LF characters only
- Line endings: LF (Unix), not CRLF
- Tags: lowercase, hyphenated (`machine-learning`)
- GitHub repos: `owner/repo` format
- URLs: valid HTTP/HTTPS

## Workflow

1. Edit YAML files in `data/`
2. Run `make validate`
3. Run `make generate`
4. Preview with `make serve` (optional)
5. Commit YAML + generated README.md
6. Push (automatic deployment)

## Next Steps

- **REFERENCE.md** - Command and schema reference
- **ADVANCED.md** - Website customization, CI/CD internals
- **GitHub Issues** - Report bugs or request features

# Contributing to Ultimate AI Agent Directory

Thank you for your interest in contributing to the Ultimate AI Agent Directory! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [About This Project](#about-this-project)
- [Ways to Contribute](#ways-to-contribute)
- [Getting Started](#getting-started)
- [Contribution Workflow](#contribution-workflow)
- [Data Quality Guidelines](#data-quality-guidelines)
- [Technical Requirements](#technical-requirements)
- [Pull Request Process](#pull-request-process)
- [Code of Conduct](#code-of-conduct)

## About This Project

The Ultimate AI Agent Directory is a **data-driven documentation project** that maintains a comprehensive, curated directory of AI agent frameworks, platforms, tools, and resources. Unlike traditional software projects, this repository:

- Uses **YAML files** as the single source of truth (in `data/`)
- **Automatically generates** README.md and the static website from YAML data
- Focuses on **data quality and accuracy** over code development

## Ways to Contribute

We welcome the following types of contributions:

### 1. Adding New Entries

Submit new AI agent frameworks, platforms, tools, or resources that aren't currently in the directory. See [Adding a New Entry](#adding-a-new-entry) below.

### 2. Updating Existing Entries

- Update outdated information
- Add missing metadata (GitHub repos, documentation links, pricing info)
- Improve descriptions for clarity and accuracy
- Mark entries as `verified: true` after checking links and metadata

### 3. Reporting Issues

- Broken links or outdated information
- Incorrect categorization
- Missing important tools or frameworks
- Documentation improvements

### 4. Improving Documentation

- Enhance setup instructions
- Add examples or clarifications
- Fix typos or formatting issues

### 5. Suggesting New Categories

Propose new categories if you notice a gap in the current structure (see `data/categories/`).

## Getting Started

### Prerequisites

- Git
- Python 3.8 or higher
- Text editor or IDE

### Initial Setup

1. **Fork the repository** on GitHub

2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/Ultimate-Agent-Directory.git
   cd Ultimate-Agent-Directory
   ```

3. **Install dependencies:**
   ```bash
   make install
   ```
   This creates a virtual environment and installs all Python dependencies.

4. **Verify the setup:**
   ```bash
   make validate
   make generate
   ```
   Both commands should complete without errors.

### Understanding the Project Structure

```
data/
├── agents/                    # YAML files for all entries (SOURCE OF TRUTH)
│   ├── open-source-frameworks/
│   ├── no-code-platforms/
│   ├── autonomous-agents/
│   └── ...
└── categories/               # Category definitions

scripts/                      # Python automation tools
templates/                    # Jinja2 templates
static/                       # Website assets
README.md                     # Generated from YAML (DO NOT EDIT DIRECTLY)
```

## Contribution Workflow

### Adding a New Entry

1. **Determine the correct category** by browsing `data/categories/` or the README.md

2. **Create a YAML file** in `data/agents/{category}/{name}.yml`:
   ```yaml
   name: Your Tool Name
   url: https://example.com
   description: A concise, factual description (20-1000 characters). Focus on what the tool does and who uses it, avoiding marketing hype.
   category: category-id
   type: framework  # or platform, tool, course, community, research
   tags:
     - machine-learning
     - automation

   # Optional but recommended:
   github_repo: owner/repo
   documentation_url: https://docs.example.com
   pricing: free  # or freemium, paid, enterprise
   platform:
     - Python
     - TypeScript
   license: MIT
   featured: false
   verified: false
   ```

3. **Validate your changes:**
   ```bash
   make validate
   ```
   Fix any schema validation errors reported.

4. **Generate the README:**
   ```bash
   make generate
   ```
   This updates README.md with your new entry.

5. **Preview the website (optional):**
   ```bash
   make serve
   ```
   Visit http://localhost:8001 to see your changes locally.

6. **Commit both YAML and generated README.md:**
   ```bash
   git add data/agents/{category}/{name}.yml
   git add README.md
   git commit -m "Add {Tool Name} to {category}"
   git push origin main
   ```

### Updating an Existing Entry

1. **Edit the YAML file** in `data/agents/{category}/{name}.yml`

2. **Validate and regenerate:**
   ```bash
   make validate
   make generate
   ```

3. **Commit both files:**
   ```bash
   git add data/agents/{category}/{name}.yml
   git add README.md
   git commit -m "Update {Tool Name}: {brief description of changes}"
   git push origin main
   ```

### Before Every Commit

**Always run these commands:**
```bash
make validate    # Ensures YAML files pass schema validation
make generate    # Updates README.md from YAML data
```

Then commit **both** the YAML file(s) you edited **and** the generated README.md.

## Data Quality Guidelines

### Writing Descriptions

- **Accuracy over hype:** Focus on factual capabilities, not marketing claims
- **Concise:** 2-3 sentences ideal (20-1000 characters enforced)
- **Factual:** What the tool does and who uses it
- **No attribution:** Never mention individual contributors or maintainers
- **No affiliate links:** Direct to official sources only

**Good Example:**
```
Open-source framework for building autonomous data labeling agents. Enables creation of AI agents that can label, process, and improve data quality autonomously with feedback loops and continuous learning capabilities.
```

**Bad Example:**
```
Amazing framework created by John Doe! The best tool ever for data labeling!!! Click here to try it now!
```

### Required Fields

Every entry **must** include:
- `name` (1-100 characters)
- `url` (valid HTTP/HTTPS URL)
- `description` (20-1000 characters)
- `category` (must match a category ID in `data/categories/`)
- `type` (one of: framework, platform, tool, course, community, research)
- `tags` (list of lowercase, hyphenated tags)

### Recommended Optional Fields

Include when available:
- `github_repo` (format: "owner/repo")
- `documentation_url`
- `pricing` (free, freemium, paid, enterprise)
- `platform` (e.g., ["Python", "TypeScript"])
- `license` (e.g., "MIT", "Apache-2.0")

### Tags Guidelines

- Use lowercase letters
- Use hyphens for multi-word tags (e.g., `machine-learning`)
- Be specific and relevant
- Common tags: `automation`, `nlp`, `machine-learning`, `workflow`, `integration`, `testing`, `deployment`

## Technical Requirements

### Character Encoding

- **ASCII UTF-8 LF only** - No special characters or emojis in YAML files
- **Line endings:** LF (Unix-style), not CRLF
- Use a text editor that supports UTF-8 LF encoding

### YAML Formatting

- Use 2-space indentation (no tabs)
- Ensure proper YAML syntax (use a YAML linter)
- Quote URLs and strings with special characters
- Follow the schema defined in `scripts/models.py`

### URL Validation

- All URLs must be valid HTTP/HTTPS
- No localhost or IP addresses
- Prefer HTTPS when available
- Links should point to official sources

### GitHub Repository Format

- Format: `"owner/repo"` (e.g., `"langchain-ai/langchain"`)
- Do not include `https://github.com/`
- Validate the repository exists and is public

## Pull Request Process

1. **Fork the repository** and create a new branch:
   ```bash
   git checkout -b add-new-tool
   ```

2. **Make your changes** following the guidelines above

3. **Validate and generate:**
   ```bash
   make validate
   make generate
   ```

4. **Test locally (optional but recommended):**
   ```bash
   make serve
   ```

5. **Commit your changes:**
   ```bash
   git add data/agents/{category}/{name}.yml
   git add README.md
   git commit -m "Add {Tool Name}: brief description"
   ```

6. **Push to your fork:**
   ```bash
   git push origin add-new-tool
   ```

7. **Create a Pull Request** on GitHub with:
   - Clear title describing the change
   - Description explaining what was added/changed and why
   - Link to the official website/documentation
   - Confirmation that you've run `make validate` and `make generate`

### Pull Request Checklist

Before submitting, ensure:

- [ ] Ran `make validate` without errors
- [ ] Ran `make generate` to update README.md
- [ ] Committed both YAML file(s) **and** README.md
- [ ] Description is factual and concise (20-1000 chars)
- [ ] All URLs are valid and point to official sources
- [ ] Tags are lowercase and hyphenated
- [ ] Category is correct
- [ ] No attribution to individuals
- [ ] ASCII UTF-8 LF encoding used

### CI/CD Checks

Your pull request will automatically trigger:

- **YAML validation** against Pydantic schemas
- **README generation test**
- **Website generation test**

All checks must pass before merging.

## Code of Conduct

### Our Standards

- **Be respectful:** Treat all contributors with respect and kindness
- **Be factual:** Focus on accuracy and objectivity
- **Be collaborative:** Provide constructive feedback
- **Be inclusive:** Welcome contributions from everyone

### Unacceptable Behavior

- Harassment, discrimination, or personal attacks
- Spam or promotional content
- Deliberately submitting false or misleading information
- Violating copyright or intellectual property rights

### Enforcement

Violations of the code of conduct may result in:
1. Warning
2. Temporary ban from contributing
3. Permanent ban from the project

Report issues to the repository maintainers via GitHub Issues.

## Getting Help

- **Documentation:** Check `docs/GETTING_STARTED.md`, `docs/REFERENCE.md`, and `docs/ADVANCED.md`
- **Issues:** Search existing issues or create a new one
- **Discussions:** Join conversations in GitHub Discussions
- **Commands Reference:**
  ```bash
  make install    # Install dependencies
  make validate   # Validate YAML files
  make generate   # Generate README.md
  make site       # Generate website
  make serve      # Build and serve locally
  make test       # Run validation + generation
  make clean      # Remove generated files
  ```

## Quick Reference

### File Naming Convention

- YAML files: lowercase with hyphens (e.g., `langchain.yml`, `autogpt.yml`)
- Match the tool name when possible
- Use descriptive names for multi-word tools (e.g., `semantic-kernel.yml`)

### Common Commands

```bash
# Validate a specific file
python scripts/validate.py data/agents/open-source-frameworks/langchain.yml

# Check what changed
git status
git diff

# Preview before committing
make serve
```

### Need Help?

If you're unsure about anything:
1. Look at existing entries in `data/agents/` for examples
2. Check the schema in `scripts/models.py`
3. Open an issue asking for guidance
4. Start with a draft pull request marked as "WIP" (Work in Progress)

---

Thank you for contributing to the Ultimate AI Agent Directory! Your contributions help make this resource valuable for the entire AI community.

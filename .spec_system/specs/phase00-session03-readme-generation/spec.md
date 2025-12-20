# Session Specification

**Session ID**: `phase00-session03-readme-generation`
**Phase**: 00 - Feature Addition
**Status**: Not Started
**Created**: 2025-12-21

---

## 1. Session Overview

This session creates a README generation system for the boilerplate directory that transforms the 134 YAML entries (migrated in Session 02) into a well-organized, navigable markdown document. The generated `BOILERPLATES.md` will serve as the primary user-facing output on GitHub, mirroring the existing pattern used for the AI agents directory (`README.md`).

The generation system follows the established architecture: Python script loads YAML data using Pydantic models, applies a Jinja2 template, and outputs formatted markdown. The key difference from the agents README is the ecosystem-based organization (JavaScript/TypeScript, Python, PHP, etc.) rather than flat category listing.

This session is critical path: Session 04 (Makefile/CI) cannot integrate until generation scripts exist, and Session 05 (Website) depends on the data loading functions created here.

---

## 2. Objectives

1. Create a Python generation script that loads boilerplate YAML data and produces well-formatted markdown output
2. Create a Jinja2 template that organizes entries by ecosystem and category with proper anchor links
3. Generate `BOILERPLATES.md` with all 134 entries displayed in navigable tables
4. Ensure the generated output matches the quality and style of the existing `README.md`

---

## 3. Prerequisites

### Required Sessions
- [x] `phase00-session01-schema-and-structure` - Provides BoilerplateEntry, BoilerplateCategory, TechStackComponent Pydantic models
- [x] `phase00-session02-migration-script` - Provides 134 YAML files in `data/boilerplates/` and 21 category files in `data/boilerplate-categories/`

### Required Tools/Knowledge
- Python 3.8+ with Pydantic, PyYAML, Jinja2
- Understanding of existing `generate_readme.py` patterns
- Markdown table formatting

### Environment Requirements
- Virtual environment with dependencies installed (`make install`)
- All boilerplate YAML files passing validation (`make validate`)

---

## 4. Scope

### In Scope (MVP)
- `scripts/generate_boilerplates.py` with data loading and rendering logic
- `templates/boilerplates_readme.jinja2` with ecosystem organization
- Entry count badge generation
- Table of contents with working anchor links
- Markdown tables with configurable columns (name, stars, license, description)
- Ecosystem grouping (JavaScript/TypeScript, Python, PHP, Ruby, Go, Rust, .NET, Elixir, Specialized)
- Star count formatting (28300 -> "28.3K")
- Generated `BOILERPLATES.md` output

### Out of Scope (Deferred)
- Makefile targets (`validate-boilerplates`, `generate-boilerplates`) - *Reason: Session 04*
- Website HTML generation - *Reason: Session 05*
- Link checking/verification - *Reason: Session 06*
- GitHub star auto-update via API - *Reason: Future enhancement*

---

## 5. Technical Approach

### Architecture

```
data/boilerplates/**/*.yml          (134 YAML files - source)
data/boilerplate-categories/*.yml   (21 category files - source)
            |
            v
scripts/generate_boilerplates.py    (Python loader + renderer)
            |
            v
templates/boilerplates_readme.jinja2 (Jinja2 template)
            |
            v
BOILERPLATES.md                     (Generated output)
```

### Design Patterns
- **Data-driven generation**: Content comes from YAML, not hardcoded
- **Template separation**: Logic in Python, presentation in Jinja2
- **Model validation**: Pydantic ensures type safety
- **Ecosystem grouping**: Categories sorted within ecosystem hierarchies

### Technology Stack
- Python 3.8+ (runtime)
- Pydantic 2.x (model validation - already installed)
- PyYAML 6.x (YAML parsing - already installed)
- Jinja2 3.x (templating - already installed)

---

## 6. Deliverables

### Files to Create

| File | Purpose | Est. Lines |
|------|---------|------------|
| `scripts/generate_boilerplates.py` | Data loading and README generation | ~120 |
| `templates/boilerplates_readme.jinja2` | README markdown template | ~100 |
| `BOILERPLATES.md` | Generated output (committed) | ~800 |

### Files to Modify

| File | Changes | Est. Lines |
|------|---------|------------|
| None | This session creates new files only | - |

---

## 7. Success Criteria

### Functional Requirements
- [ ] `python scripts/generate_boilerplates.py` runs without errors
- [ ] `BOILERPLATES.md` contains all 134 boilerplate entries
- [ ] Entries are grouped by ecosystem (JavaScript/TypeScript first, then Python, etc.)
- [ ] Each category displays entries in a markdown table
- [ ] Table of contents links navigate to correct sections
- [ ] Entry count badge shows "134" (or actual count)
- [ ] Star counts display in K notation where appropriate (e.g., "28.3K")
- [ ] Names link to repository URLs
- [ ] Output matches style of existing README.md

### Testing Requirements
- [ ] Manual verification: Run script, check output renders correctly in GitHub preview
- [ ] Manual verification: Click 5+ table of contents links, verify navigation
- [ ] Manual verification: Verify entry count badge is accurate
- [ ] Validation: Compare total entries in output vs. YAML file count

### Quality Gates
- [ ] All files use ASCII-only characters (0-127)
- [ ] Unix LF line endings (no CRLF)
- [ ] Script follows existing `generate_readme.py` patterns
- [ ] Template follows existing `readme.jinja2` patterns
- [ ] No hardcoded content that should come from YAML

---

## 8. Implementation Notes

### Key Considerations

1. **Ecosystem ordering**: Categories must be grouped by ecosystem in display order:
   - JavaScript/TypeScript (order 1-12)
   - Python (order 20-22)
   - PHP (order 30)
   - Ruby (order 40)
   - Go (order 50)
   - Rust (order 60)
   - .NET (order 70)
   - Elixir (order 80)
   - Mobile/Specialized (order 90+)

2. **Anchor link generation**: GitHub converts `## Next.js & T3 Stack` to `#nextjs--t3-stack` (lowercase, spaces to hyphens, special chars removed except hyphen)

3. **Star formatting**: Numbers should display as:
   - < 1000: Show as-is (e.g., "856")
   - >= 1000: Show with K suffix (e.g., "28.3K", "1.2K")

4. **Missing data handling**: Optional fields (stars, license) should gracefully show "N/A" or be omitted

### Potential Challenges

| Challenge | Mitigation |
|-----------|------------|
| Anchor link mismatches | Use a `slugify()` helper function matching GitHub's algorithm |
| Ecosystem grouping complexity | Pre-sort categories by ecosystem, then by order within ecosystem |
| Long descriptions truncating tables | Limit description display to 150 chars with ellipsis |
| Special characters in names | Ensure YAML values are properly escaped, use ASCII only |

### ASCII Reminder
All output files must use ASCII-only characters (0-127). The existing YAML data was sanitized during migration (Session 02). If any non-ASCII characters appear, replace with ASCII equivalents or remove.

---

## 9. Testing Strategy

### Manual Testing

1. **Script Execution Test**
   ```bash
   cd /home/aiwithapex/projects/Ultimate-Agent-Directory
   source venv/bin/activate
   python scripts/generate_boilerplates.py
   ```
   Expected: Success message, `BOILERPLATES.md` created

2. **Entry Count Verification**
   ```bash
   # Count entries in output
   grep -c "^|" BOILERPLATES.md
   # Compare to YAML count
   find data/boilerplates -name "*.yml" | wc -l
   ```
   Expected: Numbers match (accounting for table headers)

3. **GitHub Preview Test**
   - Open `BOILERPLATES.md` in VS Code preview or GitHub
   - Verify tables render correctly
   - Verify links are clickable
   - Verify badge displays

4. **Anchor Link Test**
   - Click 5+ links in table of contents
   - Verify each navigates to correct section

### Edge Cases
- Category with 0 entries (should show "No entries yet" or skip)
- Entry with no stars (should show "-" or omit column)
- Entry with no license (should show "-" or omit column)
- Very long description (should truncate gracefully)

---

## 10. Dependencies

### External Libraries
- `pydantic>=2.0.0` (already in requirements.txt)
- `PyYAML>=6.0` (already in requirements.txt)
- `Jinja2>=3.0` (already in requirements.txt)

### Other Sessions
- **Depends on**:
  - `phase00-session01-schema-and-structure` (models)
  - `phase00-session02-migration-script` (YAML data)
- **Depended by**:
  - `phase00-session04-makefile-and-ci-integration` (needs generation script for `make generate-boilerplates`)
  - `phase00-session05-website-integration` (may reuse data loading functions)

---

## 11. Script Structure

### generate_boilerplates.py Functions

```python
def load_boilerplate_categories() -> list[BoilerplateCategory]:
    """Load all category definitions from data/boilerplate-categories/*.yml"""

def load_boilerplates() -> list[BoilerplateEntry]:
    """Load all boilerplate entries from data/boilerplates/**/*.yml"""

def group_by_ecosystem(categories: list[BoilerplateCategory]) -> dict[str, list[BoilerplateCategory]]:
    """Group categories by ecosystem for hierarchical display"""

def group_by_category(boilerplates: list[BoilerplateEntry]) -> dict[str, list[BoilerplateEntry]]:
    """Group entries by category ID"""

def format_stars(count: int | None) -> str:
    """Format star count: 28300 -> '28.3K', None -> '-'"""

def slugify(text: str) -> str:
    """Convert text to GitHub-compatible anchor slug"""

def generate_boilerplates_readme():
    """Main function: load data, render template, write output"""
```

### Template Structure

```
# Full-Stack Boilerplate Directory
[badge: entries count]
[description paragraph]

## Table of Contents
### JavaScript/TypeScript
- [Next.js & T3 Stack](#nextjs--t3-stack)
- [Remix](#remix)
...

### Python
- [FastAPI](#fastapi)
- [Django](#django)
...

---

## JavaScript/TypeScript

### Next.js & T3 Stack
> Category description

| Name | Stars | License | Description |
|------|-------|---------|-------------|
| create-t3-app | 28.3K | MIT | The TypeScript standard for... |

---

[footer with stats and contribution info]
```

---

## Next Steps

Run `/tasks` to generate the implementation task checklist.

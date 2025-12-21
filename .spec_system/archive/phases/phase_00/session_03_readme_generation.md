# Session 03: README Generation

**Session ID**: `phase00-session03-readme-generation`
**Status**: Not Started
**Estimated Tasks**: ~15-20
**Estimated Duration**: 2-3 hours
**Priority**: P0

---

## Objective

Create a README generation system for boilerplates that produces a well-organized, navigable markdown document with tables grouped by ecosystem and category.

---

## Scope

### In Scope (MVP)
- Create `scripts/generate_boilerplates.py` script
- Create `templates/boilerplates_readme.jinja2` template
- Generate markdown tables grouped by ecosystem/category
- Include entry count badge
- Generate table of contents with anchor links
- Support configurable column display per category
- Output to `BOILERPLATES.md`

### Out of Scope
- Makefile integration (Session 04)
- Website HTML generation (Session 05)
- Link checking (Session 06)

---

## Prerequisites

- [ ] Session 01 completed (schema in place)
- [ ] Session 02 completed (YAML files generated)
- [ ] Boilerplate YAML files pass validation

---

## Deliverables

1. **`scripts/generate_boilerplates.py`** with:
   - `load_boilerplate_categories()` function
   - `load_boilerplates()` function
   - README generation logic
   - Table generation with configurable columns

2. **`templates/boilerplates_readme.jinja2`** with:
   - Header with badge and description
   - Table of contents by ecosystem
   - Category sections with emoji headers
   - Markdown tables for each category
   - Footer with contribution info

3. **`BOILERPLATES.md`** generated output with:
   - Entry count badge
   - Ecosystem organization
   - Category tables with name, stars, license, description
   - Working anchor links

---

## Technical Details

### Template Structure

```markdown
# Full-Stack Boilerplate Directory

![Entries](https://img.shields.io/badge/entries-XXX-blue)

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

| Name | Stars | License | Description |
|------|-------|---------|-------------|
| ... | ... | ... | ... |

...
```

### Column Configuration

Default columns: `name`, `stars`, `license`, `description`
Optional columns: `tags`, `pricing`, `last_updated`

---

## Success Criteria

- [ ] `BOILERPLATES.md` generates without errors
- [ ] All boilerplate entries appear in tables
- [ ] Table of contents links work correctly
- [ ] Entry count badge displays correct total
- [ ] Ecosystem grouping is logical and complete
- [ ] Tables are properly formatted markdown

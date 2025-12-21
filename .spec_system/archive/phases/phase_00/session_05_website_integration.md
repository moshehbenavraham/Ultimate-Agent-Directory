# Session 05: Website Integration

**Session ID**: `phase00-session05-website-integration`
**Status**: Not Started
**Estimated Tasks**: ~20-25
**Estimated Duration**: 3-4 hours
**Priority**: P1

---

## Objective

Extend the static website to include dedicated boilerplate pages with search, filtering, and rich detail views for each entry.

---

## Scope

### In Scope (MVP)
- Extend `scripts/generate_site.py` for boilerplate pages
- Create boilerplate index page template
- Create boilerplate category page template
- Add navigation links between agents and boilerplates
- Update `.github/workflows/deploy.yml` for boilerplate pages
- Responsive design for boilerplate pages

### Out of Scope
- Search functionality (Session 06)
- Filter functionality (Session 06)
- Technical stack visualization (future enhancement)

---

## Prerequisites

- [ ] Session 03 completed (generation scripts working)
- [ ] Session 04 completed (CI/CD updated)
- [ ] YAML files validated and complete

---

## Deliverables

1. **Extended `scripts/generate_site.py`** with:
   - Boilerplate index page generation
   - Boilerplate category page generation
   - Navigation context for templates

2. **`templates/boilerplate_index.html.jinja2`** with:
   - Overview of all ecosystems
   - Entry count per category
   - Links to category pages
   - Featured boilerplates section

3. **`templates/boilerplate_category.html.jinja2`** with:
   - Category header with emoji
   - Entry cards/table
   - Technical stack display
   - Pros/cons display
   - Links to repositories

4. **Updated `templates/base.html.jinja2`** with:
   - Navigation link to boilerplates section
   - Updated footer if needed

5. **Updated `.github/workflows/deploy.yml`** with:
   - Boilerplate page generation step

---

## Technical Details

### Page Structure

```
_site/
+-- index.html              (existing - add boilerplate link)
+-- boilerplates/
    +-- index.html          (boilerplate home)
    +-- nextjs/
    |   +-- index.html      (Next.js category)
    +-- django/
    |   +-- index.html      (Django category)
    +-- ...
```

### Entry Card Design

Each boilerplate entry should display:
- Name with link to repository
- GitHub stars badge
- License badge
- Short description
- Tags as pills
- Expandable: technical stack, pros/cons

### Navigation

- Main nav: Home | AI Agents | Boilerplates
- Breadcrumbs: Home > Boilerplates > Next.js
- Cross-links between related content

---

## Success Criteria

- [ ] Boilerplate index page renders correctly
- [ ] All category pages generate without errors
- [ ] Navigation between agents and boilerplates works
- [ ] Entry details display correctly
- [ ] Pages are responsive on mobile
- [ ] Deployment workflow succeeds
- [ ] No broken links within site

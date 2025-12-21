# Full-Stack Boilerplate Directory Integration - Product Requirements Document

**Version:** 1.1
**Status:** Phase 00 Complete
**Last Updated:** 2025-12-21

---

## Executive Summary

This PRD outlines the integration of a comprehensive Full-Stack Starter, Boilerplate & Template Kit collection into the Ultimate AI Agent Directory system. The integration follows a **Parallel Structure** approach, maintaining separation between AI agent entries and full-stack boilerplate entries while sharing core infrastructure, validation tooling, and generation pipelines.

### Objectives

1. Expand the directory to include ~100+ full-stack boilerplate/starter entries
2. Preserve rich metadata (technical stacks, pros/cons, community info) from source material
3. Maintain clean separation between AI agents and boilerplates
4. Enable independent evolution of each content type
5. Deliver a unified user experience across both directories

### Success Metrics

- All ~100+ boilerplate entries migrated to YAML format
- 100% schema validation passing
- README generation for boilerplates functional
- Website integration with dedicated boilerplate section
- Zero regression to existing AI agent directory functionality

---

## Background and Context

### Current State

The Ultimate AI Agent Directory currently manages:
- **277 AI agent/tool entries** across 10 categories
- **YAML-based data architecture** with Pydantic validation
- **Automated generation** of README.md and static website
- **GitHub Actions CI/CD** for validation and deployment

### Source Material

The `full-stack_starter_boilerplate_template_kit.md` contains:
- **~100+ starter/boilerplate entries**
- **12+ language ecosystems** (JS/TS, Python, PHP, Ruby, Go, Rust, .NET, Elixir)
- **Rich metadata per entry:**
  - Repository URL, stars, license, last updated
  - Technical stack tables (component/technology/reasoning)
  - Key features lists
  - Pros and cons
  - Use cases and deployment notes
  - Community information (Discord, maintainers)

### Problem Statement

The boilerplate collection exists as unstructured markdown with no:
- Schema validation
- Automated link checking
- Searchable/filterable interface
- Consistent data format
- Integration with existing directory infrastructure

---

## Proposed Solution: Parallel Structure Architecture

### Architecture Overview

```
data/
+-- agents/                      # EXISTING: AI agent entries (277 files)
|   +-- open-source-frameworks/
|   +-- autonomous-agents/
|   +-- ...
+-- categories/                  # EXISTING: AI agent categories (10 files)
|   +-- ...
+-- boilerplates/                # NEW: Boilerplate entries (~100 files)
|   +-- nextjs/
|   +-- remix/
|   +-- django/
|   +-- fastapi/
|   +-- laravel/
|   +-- rails/
|   +-- go/
|   +-- rust/
|   +-- dotnet/
|   +-- phoenix/
|   +-- mobile/
|   +-- enterprise/
+-- boilerplate-categories/      # NEW: Boilerplate category definitions
    +-- ...

scripts/
+-- models.py                    # EXTEND: Add BoilerplateEntry model
+-- validate.py                  # EXTEND: Add boilerplate validation
+-- generate_readme.py           # EXISTING: AI agents README
+-- generate_boilerplates.py     # NEW: Boilerplate README generator
+-- generate_site.py             # EXTEND: Add boilerplate pages
+-- migrate_boilerplates.py      # NEW: Markdown to YAML migration

templates/
+-- readme.jinja2                # EXISTING: AI agents README template
+-- boilerplates_readme.jinja2   # NEW: Boilerplate README template
+-- boilerplate_category.html.jinja2  # NEW: Website category page
+-- ...
```

### Data Model Design

#### BoilerplateEntry Schema

```python
class TechStackComponent(BaseModel):
    """Individual component in a technical stack"""
    component: str = Field(description="Component type (e.g., 'Frontend', 'Database')")
    technology: str = Field(description="Technology name (e.g., 'Next.js', 'PostgreSQL')")
    reasoning: Optional[str] = Field(default=None, description="Why this choice")

class BoilerplateEntry(BaseModel):
    """Schema for a full-stack boilerplate/starter entry"""

    # ===== REQUIRED FIELDS =====
    name: str = Field(
        min_length=1,
        max_length=100,
        description="Boilerplate/starter name"
    )

    url: HttpUrl = Field(
        description="Primary URL (GitHub repository)"
    )

    description: str = Field(
        min_length=20,
        max_length=2000,
        description="Clear description of the boilerplate"
    )

    category: str = Field(
        description="Primary category (must match boilerplate-category ID)"
    )

    # ===== REPOSITORY METADATA =====
    github_repo: Optional[str] = Field(
        default=None,
        description="GitHub repo in 'owner/repo' format"
    )

    stars: Optional[int] = Field(
        default=None,
        description="GitHub star count (can be auto-updated)"
    )

    license: Optional[str] = Field(
        default=None,
        description="License type (e.g., 'MIT', 'Apache-2.0')"
    )

    last_updated: Optional[str] = Field(
        default=None,
        description="Last significant update (e.g., 'December 2025')"
    )

    # ===== TECHNICAL DETAILS =====
    technical_stack: Optional[List[TechStackComponent]] = Field(
        default=None,
        description="Technical stack breakdown"
    )

    key_features: Optional[List[str]] = Field(
        default=None,
        description="Main features and capabilities"
    )

    # ===== EVALUATION =====
    pros: Optional[List[str]] = Field(
        default=None,
        description="Advantages and strengths"
    )

    cons: Optional[List[str]] = Field(
        default=None,
        description="Limitations and drawbacks"
    )

    # ===== CONTEXTUAL INFO =====
    use_case: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Ideal use cases and target audience"
    )

    deployment: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Deployment platform and notes"
    )

    community: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Community resources (Discord, forums)"
    )

    # ===== CLASSIFICATION =====
    subcategory: Optional[str] = Field(
        default=None,
        description="Subcategory (e.g., 'batteries-included', 'minimal')"
    )

    tags: List[str] = Field(
        default_factory=list,
        description="Tags for filtering (lowercase, hyphenated)"
    )

    pricing: Optional[Literal["free", "freemium", "paid", "open-core"]] = Field(
        default=None,
        description="Pricing model"
    )

    # ===== EDITORIAL FLAGS =====
    featured: bool = Field(
        default=False,
        description="Highlight in featured section"
    )

    verified: bool = Field(
        default=False,
        description="Link checked, metadata verified"
    )

    # ===== TRACKING =====
    added_date: Optional[date] = None
    last_verified: Optional[date] = None

    class Config:
        extra = "forbid"
```

#### BoilerplateCategory Schema

```python
class BoilerplateCategory(BaseModel):
    """Schema for a boilerplate category definition"""

    id: str = Field(
        description="URL-safe identifier (e.g., 'nextjs', 'django')"
    )

    title: str = Field(
        description="Display title (e.g., 'Next.js & T3 Stack')"
    )

    emoji: str = Field(
        default=":",
        description="Category emoji"
    )

    description: str = Field(
        min_length=10,
        max_length=500,
        description="Category description"
    )

    ecosystem: str = Field(
        description="Parent ecosystem (e.g., 'JavaScript', 'Python')"
    )

    order: int = Field(
        default=0,
        description="Display order within ecosystem"
    )

    # Display configuration
    show_stars: bool = Field(
        default=True,
        description="Show GitHub stars in tables"
    )

    table_columns: List[str] = Field(
        default=["name", "stars", "license", "description"],
        description="Columns to show in markdown tables"
    )

    class Config:
        extra = "forbid"
```

---

## Phases

| Phase | Name | Sessions | Status |
|-------|------|----------|--------|
| 00 | Feature Addition | 6 | Complete |

## Phase 00: Feature Addition (Complete)

### Session Breakdown

| Session | Name | Priority | Tasks | Validated |
|---------|------|----------|-------|-----------|
| 01 | Schema & Structure | P0 | 22 | 2025-12-21 |
| 02 | Migration Script | P0 | 26 | 2025-12-21 |
| 03 | README Generation | P0 | 23 | 2025-12-21 |
| 04 | Makefile & CI Integration | P0 | 22 | 2025-12-21 |
| 05 | Website Integration | P1 | 24 | 2025-12-21 |
| 06 | Polish & Verification | P2 | 24 | 2025-12-21 |

**Total**: 141 tasks completed across 6 sessions.

See `.spec_system/archive/phases/phase_00/` for detailed session specifications.

---

## Functional Requirements

### FR-1: Data Schema and Validation

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1.1 | Add `BoilerplateEntry` Pydantic model to `scripts/models.py` | P0 |
| FR-1.2 | Add `TechStackComponent` nested model for technical stack entries | P0 |
| FR-1.3 | Add `BoilerplateCategory` model for category definitions | P0 |
| FR-1.4 | Extend `scripts/validate.py` to validate boilerplate YAML files | P0 |
| FR-1.5 | Validate `github_repo` format as `owner/repo` | P1 |
| FR-1.6 | Validate tags are lowercase and hyphenated | P1 |
| FR-1.7 | Reject unknown fields (strict validation) | P0 |

### FR-2: Data Migration

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-2.1 | Create `scripts/migrate_boilerplates.py` migration script | P0 |
| FR-2.2 | Parse markdown headers to determine category hierarchy | P0 |
| FR-2.3 | Extract repository tables (name, URL, stars, license) | P0 |
| FR-2.4 | Extract technical stack tables into structured format | P1 |
| FR-2.5 | Extract key features as list items | P0 |
| FR-2.6 | Extract pros and cons as separate lists | P1 |
| FR-2.7 | Extract use case, deployment, and community text | P1 |
| FR-2.8 | Generate valid YAML files with proper escaping | P0 |
| FR-2.9 | Create category YAML files based on parsed structure | P0 |
| FR-2.10 | Handle edge cases (missing fields, malformed tables) | P1 |

### FR-3: README Generation

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-3.1 | Create `scripts/generate_boilerplates.py` or extend existing | P0 |
| FR-3.2 | Create `templates/boilerplates_readme.jinja2` template | P0 |
| FR-3.3 | Generate markdown tables grouped by ecosystem/category | P0 |
| FR-3.4 | Include entry count badge | P1 |
| FR-3.5 | Generate table of contents with anchor links | P1 |
| FR-3.6 | Support configurable column display per category | P2 |
| FR-3.7 | Output to `BOILERPLATES.md` or similar | P0 |

### FR-4: Website Integration

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-4.1 | Extend `scripts/generate_site.py` for boilerplate pages | P1 |
| FR-4.2 | Create boilerplate index page template | P1 |
| FR-4.3 | Create boilerplate category page template | P1 |
| FR-4.4 | Add navigation links between agents and boilerplates | P1 |
| FR-4.5 | Implement search/filter for boilerplates | P2 |
| FR-4.6 | Display technical stack as formatted table | P2 |
| FR-4.7 | Display pros/cons as styled lists | P2 |

### FR-5: Makefile Integration

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-5.1 | Add `make validate-boilerplates` target | P0 |
| FR-5.2 | Add `make generate-boilerplates` target | P0 |
| FR-5.3 | Add `make migrate-boilerplates` target | P1 |
| FR-5.4 | Update `make validate` to include boilerplates | P0 |
| FR-5.5 | Update `make test` to include boilerplate validation | P0 |

### FR-6: CI/CD Integration

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-6.1 | Update `.github/workflows/validate.yml` for boilerplate validation | P0 |
| FR-6.2 | Update `.github/workflows/deploy.yml` to generate boilerplate pages | P1 |
| FR-6.3 | Add boilerplate-specific validation job | P2 |

---

## Boilerplate Categories

Based on source material analysis, the following categories will be created:

### JavaScript/TypeScript Ecosystem

| Category ID | Title | Entries (Est.) |
|-------------|-------|----------------|
| `nextjs` | Next.js & T3 Stack | ~20 |
| `remix` | Remix | ~5 |
| `blitzjs` | Blitz.js | ~3 |
| `redwoodjs` | RedwoodJS | ~3 |
| `nuxt` | Vue / Nuxt.js | ~8 |
| `sveltekit` | Svelte / SvelteKit | ~8 |
| `nodejs` | Node.js / Express | ~6 |
| `astro` | Astro & HTML-First | ~4 |

### Python Ecosystem

| Category ID | Title | Entries (Est.) |
|-------------|-------|----------------|
| `fastapi` | FastAPI | ~6 |
| `django` | Django | ~10 |
| `flask` | Flask | ~4 |

### Other Ecosystems

| Category ID | Title | Entries (Est.) |
|-------------|-------|----------------|
| `laravel` | Laravel (PHP) | ~8 |
| `rails` | Rails (Ruby) | ~8 |
| `go` | Go / Golang | ~6 |
| `rust` | Rust | ~5 |
| `dotnet` | .NET / C# | ~4 |
| `phoenix` | Elixir / Phoenix | ~4 |
| `mobile` | Mobile & Cross-Platform | ~5 |

### Specialized Categories

| Category ID | Title | Entries (Est.) |
|-------------|-------|----------------|
| `enterprise` | Enterprise & B2B | ~6 |
| `realtime` | Real-Time & WebSocket | ~4 |
| `headless-cms` | Headless CMS | ~5 |

---

## Sample YAML Entry

```yaml
# data/boilerplates/nextjs/create-t3-app.yml

name: create-t3-app
url: https://github.com/t3-oss/create-t3-app
description: >
  The TypeScript standard for Next.js development, offering an interactive
  CLI with modular architecture. Full type-safety end-to-end with tRPC and
  the largest community with best documentation.
category: nextjs
subcategory: minimal-cli

github_repo: t3-oss/create-t3-app
stars: 28300
license: MIT
last_updated: December 2025

technical_stack:
  - component: Frontend
    technology: Next.js (App Router)
    reasoning: Industry standard for React full-stack
  - component: Type Safety
    technology: tRPC
    reasoning: End-to-end type safety without code generation
  - component: Database
    technology: Prisma or Drizzle
    reasoning: User choice during scaffold
  - component: Auth
    technology: NextAuth.js
    reasoning: Flexible authentication with multiple providers
  - component: Styling
    technology: Tailwind CSS
    reasoning: Utility-first CSS framework

key_features:
  - Interactive CLI for modular component selection
  - Full type-safety end-to-end with tRPC
  - Largest community with best documentation (create.t3.gg)
  - 378+ contributors

pros:
  - Maximum flexibility, only use what you need
  - Excellent documentation and huge Discord community (~30k members)
  - Type-safe end-to-end approach means fewer runtime errors
  - Maintainers keep it updated promptly with new Next.js versions

cons:
  - No payments/email built-in, requires manual SaaS feature additions
  - Focuses on dev-stack rather than features
  - Reliance on tRPC and NextAuth means a learning curve if unfamiliar
  - Not a turnkey SaaS solution, but a high-quality starting scaffold

use_case: >
  Perfect for those who want a solid foundation without extra cruft. If you
  value developer experience and type safety, T3 is ideal. Many indie SaaS
  projects start with T3 Stack. Great for small teams/startups who plan to
  build out features themselves.

deployment: Vercel (recommended), any Node.js hosting

community: >
  Active Discord (~30k members), weekly community calls, many contributors.
  Lots of content (blogs, YouTube) about building with T3.

tags:
  - nextjs
  - typescript
  - trpc
  - prisma
  - tailwind
  - full-stack
  - cli

pricing: free
featured: true
verified: false
added_date: 2025-12-20
```

---

## Sample Category Definition

```yaml
# data/boilerplate-categories/nextjs.yml

id: nextjs
title: Next.js & T3 Stack
emoji: "N"
description: >
  Next.js dominates the React full-stack landscape with its App Router,
  Server Components, and seamless Vercel deployment. The T3 Stack has
  emerged as the TypeScript community's preferred starting point.

ecosystem: JavaScript/TypeScript
order: 1

show_stars: true

table_columns:
  - name
  - stars
  - license
  - description

subcategories:
  - id: minimal-cli
    title: Minimal / CLI-Based Starters
    order: 1
  - id: batteries-included
    title: Batteries-Included / SaaS-Ready
    order: 2
  - id: enterprise
    title: Enterprise & B2B Focused
    order: 3
  - id: multi-tenant
    title: Multi-Tenant & Platform Starters
    order: 4
```

---

## Migration Script Design

### Parsing Strategy

```python
# scripts/migrate_boilerplates.py

class BoilerplateMarkdownParser:
    """
    Parses the full-stack boilerplate markdown into structured data
    """

    def parse(self, markdown_path: str) -> List[dict]:
        """
        Main parsing flow:
        1. Split into sections by headers
        2. Identify ecosystem (## header)
        3. Identify category (### header)
        4. Identify subcategory (#### header)
        5. Parse each entry (##### header)
        """
        pass

    def parse_entry(self, section: str) -> dict:
        """
        Parse a single entry section:
        1. Extract name from ##### header
        2. Parse attribute table (Repository, Stars, License, etc.)
        3. Parse technical stack table
        4. Extract key features list
        5. Extract pros/cons from **Pros:**/**Cons:** sections
        6. Extract use case, deployment, community text
        """
        pass

    def extract_table(self, text: str, table_type: str) -> dict:
        """Extract and parse markdown tables"""
        pass

    def extract_list(self, text: str, header: str) -> List[str]:
        """Extract bullet lists under a header"""
        pass

    def generate_yaml(self, entry: dict, category: str) -> str:
        """Generate YAML string from parsed entry"""
        pass
```

### Handling Edge Cases

| Edge Case | Strategy |
|-----------|----------|
| Missing repository URL | Skip entry, log warning |
| Missing description | Use first paragraph of section |
| Malformed table | Attempt regex fallback, then skip |
| Special characters in YAML | Use block scalars (`>` or `\|`) |
| Very long descriptions | Truncate to 2000 chars |
| Duplicate entries | Deduplicate by URL |
| Non-ASCII characters | Convert or remove |

---

## Implementation Phases

### Phase 1: Schema & Structure (P0)

**Deliverables:**
- [ ] `BoilerplateEntry` model in `models.py`
- [ ] `TechStackComponent` model in `models.py`
- [ ] `BoilerplateCategory` model in `models.py`
- [ ] Create `data/boilerplates/` directory structure
- [ ] Create `data/boilerplate-categories/` directory
- [ ] Update `validate.py` with boilerplate validation functions

**Validation Criteria:**
- Empty directories created
- Models importable without errors
- Validation functions callable

### Phase 2: Migration Script (P0)

**Deliverables:**
- [ ] `scripts/migrate_boilerplates.py` script
- [ ] Markdown parsing logic
- [ ] YAML generation logic
- [ ] Category extraction and creation
- [ ] ~100+ YAML files generated in `data/boilerplates/`
- [ ] ~20 category YAML files generated

**Validation Criteria:**
- All entries successfully parsed
- All YAML files pass schema validation
- No data loss from source material

### Phase 3: README Generation (P0)

**Deliverables:**
- [ ] `scripts/generate_boilerplates.py` script
- [ ] `templates/boilerplates_readme.jinja2` template
- [ ] Generated `BOILERPLATES.md` output
- [ ] Makefile targets added

**Validation Criteria:**
- README generates without errors
- All entries appear in tables
- Links are valid
- Table of contents works

### Phase 4: Makefile & CI Integration (P0)

**Deliverables:**
- [ ] `make validate-boilerplates` target
- [ ] `make generate-boilerplates` target
- [ ] `make migrate-boilerplates` target
- [ ] Updated `make validate` and `make test`
- [ ] Updated `.github/workflows/validate.yml`

**Validation Criteria:**
- All make targets functional
- CI passes on boilerplate changes
- Validation catches schema errors

### Phase 5: Website Integration (P1)

**Deliverables:**
- [ ] Boilerplate index page
- [ ] Category pages for each ecosystem
- [ ] Navigation integration
- [ ] Updated `.github/workflows/deploy.yml`

**Validation Criteria:**
- Website builds successfully
- Boilerplate pages accessible
- Navigation works between sections

### Phase 6: Polish & Verification (P2)

**Deliverables:**
- [ ] Link checking for all boilerplate URLs
- [ ] Search/filter functionality
- [ ] Featured entries display
- [ ] Documentation updates

**Validation Criteria:**
- No broken links
- Search returns relevant results
- Documentation accurate

---

## File Changes Summary

### New Files

| File | Purpose |
|------|---------|
| `data/boilerplates/**/*.yml` | ~100 boilerplate entry files |
| `data/boilerplate-categories/*.yml` | ~20 category definition files |
| `scripts/migrate_boilerplates.py` | Markdown to YAML migration |
| `scripts/generate_boilerplates.py` | README generation for boilerplates |
| `templates/boilerplates_readme.jinja2` | README template |
| `templates/boilerplate_index.html.jinja2` | Website index page |
| `templates/boilerplate_category.html.jinja2` | Website category page |
| `BOILERPLATES.md` | Generated boilerplate directory |

### Modified Files

| File | Changes |
|------|---------|
| `scripts/models.py` | Add `BoilerplateEntry`, `TechStackComponent`, `BoilerplateCategory` |
| `scripts/validate.py` | Add boilerplate validation functions |
| `scripts/generate_site.py` | Add boilerplate page generation |
| `Makefile` | Add boilerplate targets |
| `.github/workflows/validate.yml` | Add boilerplate validation step |
| `.github/workflows/deploy.yml` | Add boilerplate generation step |
| `templates/base.html.jinja2` | Add boilerplate navigation |

---

## Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Markdown parsing errors | Medium | High | Robust error handling, manual fixes for edge cases |
| Schema too restrictive | Medium | Medium | Start permissive, tighten iteratively |
| Large PR size | Low | High | Split into phases, merge incrementally |
| Stale source data | Medium | Medium | Verify top entries manually, add `last_verified` dates |
| Mixed content confusion | Low | Low | Clear navigation, separate README files |

---

## Open Questions

1. **Output file name**: Should boilerplate README be `BOILERPLATES.md` or integrated into main `README.md` with a separate section?

2. **URL structure**: Should website boilerplate pages be at `/boilerplates/nextjs/` or `/Ultimate-Agent-Directory/boilerplates/nextjs/`?

3. **Star count updates**: Should we implement GitHub API integration to auto-update star counts for boilerplates?

4. **Cross-linking**: Should boilerplate entries link to related AI agent entries (e.g., AI-integrated starters)?

5. **Deduplication**: Some entries may overlap with existing AI agent directory (e.g., AI-focused starters). How to handle?

---

## Technical Stack

- Python (validation, generation scripts)
- Pydantic (YAML schema validation)
- Jinja2 (template rendering)
- PyYAML (data parsing)
- GitHub Pages (static site hosting)
- GitHub Actions (CI/CD)

---

## Appendix A: Source Material Statistics

| Ecosystem | Sections | Estimated Entries |
|-----------|----------|-------------------|
| JavaScript/TypeScript | 15 | ~55 |
| Python | 5 | ~20 |
| PHP (Laravel) | 3 | ~8 |
| Ruby (Rails) | 3 | ~8 |
| Go | 2 | ~6 |
| Rust | 3 | ~5 |
| .NET | 2 | ~4 |
| Elixir | 2 | ~4 |
| Mobile | 3 | ~5 |
| Specialized | 6 | ~15 |
| **Total** | **44** | **~130** |

---

## Appendix B: Technical Stack Components Reference

Common component types found in source material:

| Component | Common Technologies |
|-----------|---------------------|
| Frontend | Next.js, Nuxt, SvelteKit, React, Vue |
| Backend | Node.js, Django, FastAPI, Rails, Go |
| Database | PostgreSQL, MySQL, SQLite, MongoDB |
| ORM | Prisma, Drizzle, SQLAlchemy, ActiveRecord |
| Auth | NextAuth, Clerk, Supabase Auth, Auth.js |
| Styling | Tailwind CSS, shadcn/ui, Bootstrap |
| Payments | Stripe, Lemon Squeezy, Paddle |
| Deployment | Vercel, Railway, Fly.io, Docker |
| Type Safety | TypeScript, tRPC, Zod |
| Testing | Vitest, Jest, Playwright, Cypress |

---

## Appendix C: Tag Taxonomy

Recommended tags for boilerplate entries:

**By Stack:**
`nextjs`, `react`, `vue`, `nuxt`, `svelte`, `sveltekit`, `astro`, `django`, `fastapi`, `flask`, `laravel`, `rails`, `go`, `rust`, `dotnet`, `phoenix`

**By Feature:**
`saas`, `auth`, `payments`, `stripe`, `multi-tenant`, `i18n`, `realtime`, `websocket`, `graphql`, `trpc`, `prisma`, `drizzle`, `tailwind`, `typescript`

**By Use Case:**
`enterprise`, `b2b`, `ecommerce`, `cms`, `dashboard`, `admin`, `mobile`, `pwa`, `monorepo`

**By Pricing:**
`free`, `open-source`, `freemium`, `paid`, `open-core`

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-20 | Initial draft |
| 1.1 | 2025-12-21 | Phase 00 complete - 6 sessions, 141 tasks |

# Session 06: Polish & Verification

**Session ID**: `phase00-session06-polish-and-verification`
**Status**: Not Started
**Estimated Tasks**: ~15-20
**Estimated Duration**: 2-3 hours
**Priority**: P2

---

## Objective

Ensure all boilerplate content is accurate, links are valid, and the user experience is polished with search, filtering, and featured entries.

---

## Scope

### In Scope (MVP)
- Link checking for all boilerplate URLs
- Implement search functionality for website
- Implement filter functionality for website
- Featured entries display on index page
- Documentation updates
- Final validation and cleanup

### Out of Scope
- GitHub API integration for auto-updating stars (future)
- Advanced analytics (future)
- User submissions system (future)

---

## Prerequisites

- [ ] Session 05 completed (website integration done)
- [ ] All YAML files migrated and validated
- [ ] Website builds and deploys successfully

---

## Deliverables

1. **Link Checking**:
   - Run link checker on all boilerplate URLs
   - Fix or flag broken links
   - Update `verified` field for checked entries

2. **Search Functionality**:
   - Client-side search for boilerplates
   - Search by name, description, tags
   - Highlight matching terms

3. **Filter Functionality**:
   - Filter by ecosystem
   - Filter by pricing model
   - Filter by tags
   - Combine multiple filters

4. **Featured Entries**:
   - Curate featured boilerplates
   - Display featured section on index
   - Visual distinction for featured items

5. **Documentation**:
   - Updated CLAUDE.md with boilerplate workflow
   - Updated docs/GETTING_STARTED.md
   - Updated docs/REFERENCE.md

---

## Technical Details

### Link Checking

Extend `scripts/check_links.py` to include:
- Boilerplate repository URLs
- Documentation URLs
- Community URLs (Discord, etc.)

### Search Implementation

```javascript
// Client-side search with lunr.js or similar
const searchIndex = lunr(function() {
  this.ref('name');
  this.field('name');
  this.field('description');
  this.field('tags');

  boilerplates.forEach(entry => this.add(entry));
});
```

### Filter Implementation

```javascript
// URL-based filtering for shareability
// ?ecosystem=javascript&pricing=free&tags=nextjs,typescript
```

### Featured Curation

Criteria for featured boilerplates:
- High GitHub stars (>5000)
- Active maintenance (updated within 6 months)
- Complete documentation
- Strong community

---

## Success Criteria

- [ ] All URLs checked and verified
- [ ] Broken links fixed or removed
- [ ] Search returns relevant results
- [ ] Filters work correctly and can combine
- [ ] Featured section displays curated entries
- [ ] Documentation is complete and accurate
- [ ] No console errors on website
- [ ] Lighthouse score > 90 for performance

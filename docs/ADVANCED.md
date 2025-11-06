# Advanced Topics

Deep dives into website customization, CI/CD internals, and deployment options.

## Website Generation

### Build Process

```bash
make serve    # Generate site + start server at http://localhost:8000
make site     # Generate only (no server)
```

Generated output in `_site/`:

```
_site/
├── index.html              # Homepage
├── categories/*.html       # 10 category pages
├── search-index.json       # Client-side search data
├── sitemap.xml            # SEO sitemap
├── stats.json             # Directory statistics
└── static/                # CSS, JS, images
```

### Website Features

**Homepage:**
- Hero with directory stats
- Global search (live results)
- Category cards with entry counts
- Featured agents section

**Category Pages:**
- Full agent listings
- Search within category
- Filter by: type, pricing, tags
- Sort by: name, GitHub stars, date added
- Responsive design

**Search:**
- Client-side (no backend)
- Instant results
- Searches: names, descriptions, tags, categories
- Relevance ranking

### Templates (Jinja2)

Edit in `templates/`:
- `base.html.jinja2` - Layout, header, footer, navigation
- `index.html.jinja2` - Homepage structure
- `category.html.jinja2` - Category page structure

Regenerate with `make site` after changes.

### Styling

Edit `static/css/style.css` for custom styles.

Stack:
- Tailwind CSS (CDN)
- Font Awesome (CDN)
- Custom CSS for animations

### Base URL Configuration

Update in `scripts/generate_site.py` (line 72):

```python
base_url = "https://yourdomain.com/path"
```

## CI/CD Workflows

### Deployment Workflow (`.github/workflows/deploy.yml`)

Triggers on push to `main`:

1. **Build Job**
   - Validates YAML files
   - Generates README.md
   - Generates website
   - Uploads `_site/` artifact

2. **Deploy Job**
   - Deploys artifact to GitHub Pages
   - Updates live site

### Validation Workflow (`.github/workflows/validate.yml`)

Triggers on pull requests:
- Validates YAML syntax
- Tests README generation
- Tests website generation
- Blocks merge if validation fails

### Monitoring

- **Actions tab:** Build/deploy status
- **Environments:** Deployment history
- **Pages settings:** Current deployment URL

## Alternative Deployment Options

### Netlify

1. Connect GitHub repository
2. Build command: `make site`
3. Publish directory: `_site`
4. Auto-deploy on push

### Vercel

1. Import repository
2. Build command: `make site`
3. Output directory: `_site`
4. Auto-deploy on push

### AWS S3 + CloudFront

```bash
make site
aws s3 sync _site/ s3://your-bucket/ --delete
aws cloudfront create-invalidation --distribution-id XXX --paths "/*"
```

### Traditional Hosting

Upload `_site/` contents via FTP/SFTP to any static host.

## Custom Domain Setup

### DNS Configuration

1. Add `CNAME` file to `static/`:
   ```
   agents.yourdomain.com
   ```

2. Create DNS record:
   - Type: CNAME
   - Name: agents
   - Value: `{username}.github.io`

3. Enable HTTPS in GitHub Pages settings

4. Update base URL in `scripts/generate_site.py`

### GitHub Pages Custom Domain

1. Go to Settings > Pages
2. Enter custom domain
3. Check "Enforce HTTPS"
4. Wait for DNS check to complete

## Adding New Categories

### 1. Create Category Definition

`data/categories/{category-id}.yml`:

```yaml
id: new-category
title: Category Title
emoji: 🚀
description: Brief category description
order: 10              # Display order
show_github_stats: true
table_columns:
  - name
  - url
  - description
```

### 2. Create Directory

```bash
mkdir -p data/agents/new-category
```

### 3. Add Agents

Create agent YAML files with `category: new-category`

### 4. Validate and Generate

```bash
make test
```

## Performance Optimization

Current optimizations:
- Static HTML (no SSR)
- Client-side search (no API calls)
- Minimal JavaScript (< 10KB)
- CDN-hosted dependencies
- Mobile-responsive design
- SEO-optimized with sitemap

### Caching

GitHub Pages CDN automatically caches:
- HTML: 10 minutes
- Static assets: 1 hour

Clear with deployment or manual cache invalidation.

## Advanced Troubleshooting

### Build Fails in CI

Check Actions logs for:
- YAML validation errors → Fix syntax in data files
- Missing dependencies → Verify `requirements.txt`
- Python version mismatch → Workflow uses Python 3.11

### Website Generation Fails Locally

```bash
# Clean and rebuild
make clean
make install
make site
```

Verify:
- Python 3.10+ installed
- Dependencies installed in venv
- YAML files validate (`make validate`)

### Search Not Working

Verify:
- `search-index.json` exists in `_site/`
- Browser console shows no JavaScript errors
- `static/js/search.js` loaded correctly

### Category Pages Empty

Check:
- Agent YAML files have correct `category:` field
- Category ID matches category definition file
- Files in correct subdirectory under `data/agents/`

### Styles Not Loading

- Verify static assets copied to `_site/static/`
- Check browser console for 404 errors
- Confirm CDN links accessible (Tailwind CSS, Font Awesome)

## Workflow Internals

### GitHub Actions Permissions

Required in Settings > Actions > General:
- **Read and write permissions**
- **Allow GitHub Actions to create and approve pull requests**

Without these, deployment will fail.

### Manual Workflow Trigger

1. Go to Actions tab
2. Select "Build and Deploy to GitHub Pages"
3. Click "Run workflow"
4. Select branch: `main`
5. Click "Run workflow"

### Artifact Management

Build artifacts stored for 90 days:
- Download from Actions > Workflow run > Artifacts
- Contains complete `_site/` directory
- Useful for debugging deployment issues

## Migration Tools

### Markdown to YAML Migration

Script: `scripts/migrate.py`

Converts markdown sections to structured YAML:

```bash
# Dry run (preview only)
venv/bin/python scripts/migrate.py --section "🛠️ Section" --category cat-id --dry-run

# Execute migration
venv/bin/python scripts/migrate.py --section "🛠️ Section" --category cat-id
```

Handles:
- Table parsing
- URL extraction
- GitHub repo detection
- Description cleanup

## Security Considerations

**YAML Validation:**
- Pydantic schemas prevent code injection
- `extra = "forbid"` blocks unknown fields
- URL validation prevents malicious links

**Static Site:**
- No server-side code execution
- No database or user input
- Read-only GitHub Pages deployment

**Content Guidelines:**
- No affiliate links
- Official sources only
- Factual descriptions only

## Maintenance

### Regular Tasks

**Weekly:**
- Review new issues/PRs
- Validate links (manual or automated)
- Update agent entries with major changes

**Monthly:**
- Check GitHub stars for featured agents
- Review category organization
- Update documentation

**Quarterly:**
- Audit for dead links
- Reorganize categories if needed
- Update ROADMAP.md

### Automated Maintenance (Future)

See `docs/ROADMAP.md` for planned automation:
- Link validation
- GitHub stats updates
- Stale entry detection
- Duplicate detection

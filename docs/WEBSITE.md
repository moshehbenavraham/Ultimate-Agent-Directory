# Website Generation Guide

This guide explains how to generate and deploy the static HTML website for the Ultimate Agent Directory.

## Quick Start

Generate the website and start a local preview server:

```bash
make serve
```

This will:
1. Generate the static website in `_site/`
2. Start a local web server at http://localhost:8000
3. Allow you to preview the site locally

## Build Commands

### Generate Website Only

```bash
make site
```

This generates the static website in the `_site/` directory without starting a server.

### Manual Generation

```bash
venv/bin/python scripts/generate_site.py
```

## What Gets Generated

The build process creates:

### HTML Pages
- `index.html` - Homepage with category overview and search
- `categories/*.html` - Individual category pages (10 pages)

### Data Files
- `search-index.json` - Client-side search index (277 entries)
- `stats.json` - Statistics about the directory
- `sitemap.xml` - SEO sitemap

### Static Assets
- `static/css/style.css` - Custom styling
- `static/js/main.js` - Core JavaScript
- `static/js/search.js` - Homepage search functionality
- `static/js/category.js` - Category filtering and sorting

## Website Features

### Homepage (/)
- Hero section with directory stats
- Global search with live results
- Category cards with entry counts
- Featured agents section
- Call-to-action for contributions

### Category Pages (/categories/{category}.html)
- Full listing of agents in category
- Search within category
- Filter by:
  - Type (framework, platform, tool, etc.)
  - Pricing (free, freemium, paid, enterprise)
  - Tags (multiple selection)
- Sort by:
  - Name (alphabetical)
  - GitHub stars (if available)
  - Date added
- Responsive design for mobile/tablet/desktop

### Search Functionality
- Client-side search (no backend required)
- Instant results as you type
- Searches across:
  - Agent names
  - Descriptions
  - Tags
  - Categories
- Relevance scoring and ranking

## File Structure

```
_site/
├── index.html              # Homepage
├── categories/             # Category pages
│   ├── open-source-frameworks.html
│   ├── no-code-platforms.html
│   └── ...
├── search-index.json       # Search data
├── sitemap.xml            # SEO sitemap
├── stats.json             # Statistics
└── static/                # Assets
    ├── css/
    │   └── style.css
    ├── js/
    │   ├── main.js
    │   ├── search.js
    │   └── category.js
    └── images/            # (placeholder)
```

## Templates

Templates are written in Jinja2 and located in `templates/`:

- `base.html.jinja2` - Base layout with header/footer/navigation
- `index.html.jinja2` - Homepage template
- `category.html.jinja2` - Category page template

## Customization

### Styling
Edit `static/css/style.css` for custom styles. The site uses:
- Tailwind CSS (via CDN) for utility classes
- Font Awesome (via CDN) for icons
- Custom CSS for animations and special effects

### Templates
Modify templates in `templates/` and regenerate with `make site`.

### Base URL
Update the base URL in `scripts/generate_site.py` (line 72):
```python
base_url = "https://aiwithapex.com/ultimate-agent-directory"
```

## Deployment Options

### GitHub Pages

1. Generate the site:
   ```bash
   make site
   ```

2. Push `_site/` contents to `gh-pages` branch:
   ```bash
   git subtree push --prefix _site origin gh-pages
   ```

3. Enable GitHub Pages in repository settings

### Netlify

1. Connect your GitHub repository
2. Set build command: `make site`
3. Set publish directory: `_site`
4. Deploy automatically on push

### Vercel

1. Import repository
2. Set build command: `make site`
3. Set output directory: `_site`
4. Deploy automatically on push

### Manual Deployment

The `_site/` directory contains a complete static website. Upload to any web host that serves static files:

- AWS S3 + CloudFront
- Azure Static Web Apps
- Google Cloud Storage
- Traditional web hosting (via FTP/SFTP)

## Development Workflow

1. **Make changes to data**: Edit YAML files in `data/`
2. **Validate**: Run `make validate` to check YAML syntax
3. **Generate website**: Run `make site` to build
4. **Preview locally**: Run `make serve` to test
5. **Deploy**: Push to your hosting platform

## Troubleshooting

### Website not generating
- Check that all dependencies are installed: `make install`
- Validate YAML files: `make validate`
- Check Python version: `python3 --version` (requires 3.10+)

### Styles not loading
- Ensure static assets were copied correctly
- Check browser console for 404 errors
- Verify CDN links are accessible (Tailwind CSS, Font Awesome)

### Search not working
- Verify `search-index.json` exists in `_site/`
- Check browser console for JavaScript errors
- Ensure search.js is loaded correctly

### Category pages empty
- Verify agents are assigned to correct category IDs
- Check that category YAML files exist in `data/categories/`
- Ensure entries are in correct subdirectories under `data/agents/`

## Performance

The generated website is optimized for performance:

- Static HTML (no server-side rendering)
- Client-side search (no backend API calls)
- Minimal JavaScript (< 10KB total)
- CDN-hosted dependencies (Tailwind CSS, Font Awesome)
- Mobile-responsive design
- SEO-friendly with sitemap.xml

## Next Steps

See `docs/plan.md` for upcoming features:
- Phase 5: Automation & CI/CD
- Phase 6: Documentation improvements

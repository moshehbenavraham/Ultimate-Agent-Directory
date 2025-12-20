#!/usr/bin/env python3
"""
Generate static HTML website from YAML data files

Usage:
    python scripts/generate_site.py
"""

from pathlib import Path
from collections import defaultdict
from datetime import date
import yaml
import json
import shutil
from jinja2 import Environment, FileSystemLoader
from models import AgentEntry, Category, DirectoryMetadata


def load_categories() -> list[Category]:
    """Load all category definitions"""
    categories = []
    category_dir = Path("data/categories")

    for yml_file in sorted(category_dir.glob("*.yml")):
        with open(yml_file) as f:
            data = yaml.safe_load(f)
        categories.append(Category(**data))

    return sorted(categories, key=lambda c: c.order)


def load_agents() -> list[AgentEntry]:
    """Load all agent entries"""
    agents = []
    agents_dir = Path("data/agents")

    for yml_file in agents_dir.rglob("*.yml"):
        with open(yml_file) as f:
            data = yaml.safe_load(f)
        agents.append(AgentEntry(**data))

    return agents


def group_by_category(agents: list[AgentEntry]) -> dict:
    """Group agents by category"""
    grouped = defaultdict(list)
    for agent in agents:
        grouped[agent.category].append(agent)

    # Sort entries within each category by name
    for category in grouped:
        grouped[category].sort(key=lambda a: a.name.lower())

    return dict(grouped)


def create_search_index(
    agents: list[AgentEntry], categories: list[Category]
) -> list[dict]:
    """Create JSON search index for client-side search"""
    index = []

    # Create category title lookup
    category_titles = {cat.id: cat.title for cat in categories}

    for agent in agents:
        index.append(
            {
                "name": agent.name,
                "url": str(agent.url),
                "description": agent.description,
                "category": agent.category,
                "category_title": category_titles.get(agent.category, agent.category),
                "type": agent.type,
                "tags": agent.tags,
                "github_stars": agent.github_stars,
                "pricing": agent.pricing,
            }
        )

    return index


def generate_sitemap(categories: list[Category], output_dir: Path):
    """Generate sitemap.xml for SEO"""
    base_url = "https://aiwithapex.github.io/Ultimate-Agent-Directory"
    today = date.today().isoformat()

    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    # Homepage
    sitemap.append("  <url>")
    sitemap.append(f"    <loc>{base_url}/</loc>")
    sitemap.append(f"    <lastmod>{today}</lastmod>")
    sitemap.append("    <changefreq>weekly</changefreq>")
    sitemap.append("    <priority>1.0</priority>")
    sitemap.append("  </url>")

    # Category pages
    for category in categories:
        sitemap.append("  <url>")
        sitemap.append(f"    <loc>{base_url}/categories/{category.id}.html</loc>")
        sitemap.append(f"    <lastmod>{today}</lastmod>")
        sitemap.append("    <changefreq>weekly</changefreq>")
        sitemap.append("    <priority>0.8</priority>")
        sitemap.append("  </url>")

    sitemap.append("</urlset>")

    sitemap_path = output_dir / "sitemap.xml"
    sitemap_path.write_text("\n".join(sitemap))
    print(f"✓ Generated {sitemap_path}")


def copy_static_assets(output_dir: Path):
    """Copy static assets to output directory"""
    static_src = Path("static")
    static_dst = output_dir / "static"

    if static_dst.exists():
        shutil.rmtree(static_dst)

    shutil.copytree(static_src, static_dst)
    print(f"✓ Copied static assets to {static_dst}")


def generate_site():
    """Generate complete static website"""

    print("=" * 60)
    print("Ultimate Agent Directory - Website Generator")
    print("=" * 60)

    # Create output directory
    output_dir = Path("_site")
    output_dir.mkdir(exist_ok=True)

    # Load data
    print("\nLoading data...")
    categories = load_categories()
    agents = load_agents()
    entries_by_category = group_by_category(agents)

    print(f"  Loaded {len(categories)} categories")
    print(f"  Loaded {len(agents)} agents")

    # Build metadata
    metadata = DirectoryMetadata(total_entries=len(agents), last_generated=date.today())

    # Base URL for GitHub Pages (repo name)
    base_url = "/Ultimate-Agent-Directory"

    # Setup Jinja2 environment
    env = Environment(
        loader=FileSystemLoader("templates"), trim_blocks=True, lstrip_blocks=True
    )

    # Add custom filters
    env.filters["formatdate"] = lambda d: d.strftime("%B %d, %Y") if d else "N/A"

    # Generate homepage
    print("\nGenerating pages...")
    print("  Homepage (index.html)")
    index_template = env.get_template("index.html.jinja2")
    index_html = index_template.render(
        metadata=metadata,
        categories=categories,
        entries_by_category=entries_by_category,
        base_url=base_url,
    )
    (output_dir / "index.html").write_text(index_html)

    # Generate category pages
    categories_dir = output_dir / "categories"
    categories_dir.mkdir(exist_ok=True)

    category_template = env.get_template("category.html.jinja2")

    for category in categories:
        category_agents = entries_by_category.get(category.id, [])
        print(f"  {category.title} ({len(category_agents)} entries)")

        category_html = category_template.render(
            metadata=metadata,
            category=category,
            agents=category_agents,
            base_url=base_url,
        )

        category_file = categories_dir / f"{category.id}.html"
        category_file.write_text(category_html)

    # Generate search index
    print("\nGenerating search index...")
    search_index = create_search_index(agents, categories)
    search_index_path = output_dir / "search-index.json"
    search_index_path.write_text(json.dumps(search_index, indent=2))
    print(f"✓ Generated {search_index_path} ({len(search_index)} entries)")

    # Copy static assets
    print("\nCopying static assets...")
    copy_static_assets(output_dir)

    # Generate sitemap
    print("\nGenerating sitemap...")
    generate_sitemap(categories, output_dir)

    # Generate stats file
    stats = {
        "total_entries": len(agents),
        "total_categories": len(categories),
        "entries_by_category": {
            cat.id: len(entries_by_category.get(cat.id, [])) for cat in categories
        },
        "entries_by_type": {},
        "last_generated": date.today().isoformat(),
    }

    # Count by type
    for agent in agents:
        stats["entries_by_type"][agent.type] = (
            stats["entries_by_type"].get(agent.type, 0) + 1
        )

    stats_path = output_dir / "stats.json"
    stats_path.write_text(json.dumps(stats, indent=2))
    print(f"✓ Generated {stats_path}")

    # Summary
    print("\n" + "=" * 60)
    print("✓ Website generation complete!")
    print("=" * 60)
    print(f"\nOutput directory: {output_dir.absolute()}")
    print(f"Homepage: {output_dir / 'index.html'}")
    print(f"Categories: {len(categories)} pages")
    print(f"Total entries: {len(agents)}")
    print("\nTo preview locally, run:")
    print(f"  cd {output_dir} && python -m http.server 8001")
    print("  Then visit: http://localhost:8001")
    print()


if __name__ == "__main__":
    generate_site()

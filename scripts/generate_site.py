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
from models import (
    AgentEntry,
    Category,
    DirectoryMetadata,
    BoilerplateEntry,
    BoilerplateCategory,
)
from config import load_site_config


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


def load_boilerplate_categories() -> list[BoilerplateCategory]:
    """Load all boilerplate category definitions"""
    categories = []
    category_dir = Path("data/boilerplate-categories")

    for yml_file in sorted(category_dir.glob("*.yml")):
        with open(yml_file) as f:
            data = yaml.safe_load(f)
        categories.append(BoilerplateCategory(**data))

    return sorted(categories, key=lambda c: c.order)


def load_boilerplates() -> list[BoilerplateEntry]:
    """Load all boilerplate entries"""
    boilerplates = []
    boilerplates_dir = Path("data/boilerplates")

    for yml_file in boilerplates_dir.rglob("*.yml"):
        with open(yml_file) as f:
            data = yaml.safe_load(f)
        boilerplates.append(BoilerplateEntry(**data))

    return boilerplates


def group_by_category(agents: list[AgentEntry]) -> dict:
    """Group agents by category"""
    grouped = defaultdict(list)
    for agent in agents:
        grouped[agent.category].append(agent)

    # Sort entries within each category by name
    for category in grouped:
        grouped[category].sort(key=lambda a: a.name.lower())

    return dict(grouped)


def group_boilerplates_by_category(
    boilerplates: list[BoilerplateEntry],
) -> dict[str, list[BoilerplateEntry]]:
    """Group boilerplates by category"""
    grouped = defaultdict(list)
    for bp in boilerplates:
        grouped[bp.category].append(bp)

    # Sort entries within each category by stars (descending), then name
    for category in grouped:
        grouped[category].sort(key=lambda b: (-(b.github_stars or 0), b.name.lower()))

    return dict(grouped)


def group_boilerplates_by_ecosystem(
    categories: list[BoilerplateCategory],
    boilerplates_by_category: dict[str, list[BoilerplateEntry]],
) -> dict[str, list[BoilerplateCategory]]:
    """Group boilerplate categories by ecosystem for index page display"""
    ecosystem_order = [
        "JavaScript/TypeScript",
        "Python",
        "Ruby",
        "PHP",
        "Go",
        "Rust",
        ".NET",
        "Elixir",
        "Mobile",
    ]

    grouped = defaultdict(list)
    for category in categories:
        ecosystem = category.ecosystem
        grouped[ecosystem].append(category)

    # Sort categories within each ecosystem by order
    for ecosystem in grouped:
        grouped[ecosystem].sort(key=lambda c: c.order)

    # Return ordered dict based on ecosystem_order
    ordered = {}
    for ecosystem in ecosystem_order:
        if ecosystem in grouped:
            ordered[ecosystem] = grouped[ecosystem]

    # Add any remaining ecosystems not in the order list
    for ecosystem in grouped:
        if ecosystem not in ordered:
            ordered[ecosystem] = grouped[ecosystem]

    return ordered


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


def generate_sitemap(
    categories: list[Category],
    boilerplate_categories: list[BoilerplateCategory],
    output_dir: Path,
    site_url: str,
):
    """Generate sitemap.xml for SEO"""
    base_url = str(site_url).rstrip("/")
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

    # AI Agent category pages
    for category in categories:
        sitemap.append("  <url>")
        sitemap.append(f"    <loc>{base_url}/categories/{category.id}.html</loc>")
        sitemap.append(f"    <lastmod>{today}</lastmod>")
        sitemap.append("    <changefreq>weekly</changefreq>")
        sitemap.append("    <priority>0.8</priority>")
        sitemap.append("  </url>")

    # Boilerplates index page
    sitemap.append("  <url>")
    sitemap.append(f"    <loc>{base_url}/boilerplates/index.html</loc>")
    sitemap.append(f"    <lastmod>{today}</lastmod>")
    sitemap.append("    <changefreq>weekly</changefreq>")
    sitemap.append("    <priority>0.9</priority>")
    sitemap.append("  </url>")

    # Boilerplate category pages
    for bp_category in boilerplate_categories:
        sitemap.append("  <url>")
        sitemap.append(
            f"    <loc>{base_url}/boilerplates/{bp_category.id}/index.html</loc>"
        )
        sitemap.append(f"    <lastmod>{today}</lastmod>")
        sitemap.append("    <changefreq>weekly</changefreq>")
        sitemap.append("    <priority>0.7</priority>")
        sitemap.append("  </url>")

    sitemap.append("</urlset>")

    sitemap_path = output_dir / "sitemap.xml"
    sitemap_path.write_text("\n".join(sitemap))
    print(f"[OK] Generated {sitemap_path}")


def create_boilerplate_search_index(
    boilerplates: list[BoilerplateEntry],
    boilerplate_categories: list[BoilerplateCategory],
) -> list[dict]:
    """Create JSON search index entries for boilerplates"""
    index = []

    # Create category title lookup
    category_titles = {cat.id: cat.title for cat in boilerplate_categories}

    for bp in boilerplates:
        # Build tech stack summary
        tech_summary = []
        if bp.technical_stack:
            tech_summary = [t.technology for t in bp.technical_stack[:5]]

        index.append(
            {
                "name": bp.name,
                "url": str(bp.url),
                "description": bp.description,
                "category": bp.category,
                "category_title": category_titles.get(bp.category, bp.category),
                "type": bp.type,
                "tags": bp.tags,
                "github_stars": bp.github_stars,
                "pricing": bp.pricing,
                "tech_stack": tech_summary,
                "is_boilerplate": True,
            }
        )

    return index


def copy_static_assets(output_dir: Path):
    """Copy static assets to output directory"""
    static_src = Path("static")
    static_dst = output_dir / "static"

    if static_dst.exists():
        shutil.rmtree(static_dst)

    shutil.copytree(static_src, static_dst)
    print(f"[OK] Copied static assets to {static_dst}")


def generate_site():
    """Generate complete static website"""

    print("=" * 60)
    print("Ultimate Agent Directory - Website Generator")
    print("=" * 60)

    # Create output directory
    output_dir = Path("_site")
    output_dir.mkdir(exist_ok=True)

    # Load AI agents data
    print("\nLoading data...")
    site_config = load_site_config()
    categories = load_categories()
    agents = load_agents()
    entries_by_category = group_by_category(agents)

    print(f"  Loaded {len(categories)} AI agent categories")
    print(f"  Loaded {len(agents)} AI agents")

    # Load boilerplate data
    boilerplate_categories = load_boilerplate_categories()
    boilerplates = load_boilerplates()
    boilerplates_by_category = group_boilerplates_by_category(boilerplates)
    ecosystems_by_category = group_boilerplates_by_ecosystem(
        boilerplate_categories, boilerplates_by_category
    )

    print(f"  Loaded {len(boilerplate_categories)} boilerplate categories")
    print(f"  Loaded {len(boilerplates)} boilerplates")

    # Build metadata
    metadata = DirectoryMetadata(
        title=site_config.title,
        tagline=site_config.tagline,
        total_entries=len(agents),
        last_generated=date.today(),
        links=site_config.links,
    )

    # Base URL for GitHub Pages (repo name)
    base_url = site_config.base_url

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

    # Generate boilerplate pages
    print("\nGenerating boilerplate pages...")
    boilerplates_dir = output_dir / "boilerplates"
    boilerplates_dir.mkdir(exist_ok=True)

    # Boilerplate index page
    print("  Boilerplates index")
    bp_index_template = env.get_template("boilerplate_index.html.jinja2")
    bp_index_html = bp_index_template.render(
        metadata=metadata,
        boilerplate_categories=boilerplate_categories,
        boilerplates_by_category=boilerplates_by_category,
        ecosystems_by_category=ecosystems_by_category,
        total_boilerplates=len(boilerplates),
        base_url=base_url,
    )
    (boilerplates_dir / "index.html").write_text(bp_index_html)

    # Boilerplate category pages
    bp_category_template = env.get_template("boilerplate_category.html.jinja2")

    for category in boilerplate_categories:
        category_boilerplates = boilerplates_by_category.get(category.id, [])
        if category_boilerplates:
            print(f"  {category.title} ({len(category_boilerplates)} entries)")

            # Create category directory
            category_dir = boilerplates_dir / category.id
            category_dir.mkdir(exist_ok=True)

            bp_category_html = bp_category_template.render(
                metadata=metadata,
                category=category,
                boilerplates=category_boilerplates,
                base_url=base_url,
            )

            category_file = category_dir / "index.html"
            category_file.write_text(bp_category_html)

    # Generate search index (includes both agents and boilerplates)
    print("\nGenerating search index...")
    agent_search_index = create_search_index(agents, categories)
    boilerplate_search_index = create_boilerplate_search_index(
        boilerplates, boilerplate_categories
    )
    combined_search_index = agent_search_index + boilerplate_search_index
    search_index_path = output_dir / "search-index.json"
    search_index_path.write_text(json.dumps(combined_search_index, indent=2))
    print(
        f"  Generated {search_index_path} ({len(agent_search_index)} agents + {len(boilerplate_search_index)} boilerplates)"
    )

    # Copy static assets
    print("\nCopying static assets...")
    copy_static_assets(output_dir)

    # Generate sitemap (includes both agents and boilerplates)
    print("\nGenerating sitemap...")
    generate_sitemap(categories, boilerplate_categories, output_dir, site_config.site_url)

    # Generate stats file
    stats = {
        "total_agents": len(agents),
        "total_agent_categories": len(categories),
        "total_boilerplates": len(boilerplates),
        "total_boilerplate_categories": len(boilerplate_categories),
        "agents_by_category": {
            cat.id: len(entries_by_category.get(cat.id, [])) for cat in categories
        },
        "boilerplates_by_category": {
            cat.id: len(boilerplates_by_category.get(cat.id, []))
            for cat in boilerplate_categories
        },
        "agents_by_type": {},
        "last_generated": date.today().isoformat(),
    }

    # Count agents by type
    for agent in agents:
        stats["agents_by_type"][agent.type] = (
            stats["agents_by_type"].get(agent.type, 0) + 1
        )

    stats_path = output_dir / "stats.json"
    stats_path.write_text(json.dumps(stats, indent=2))
    print(f"  Generated {stats_path}")

    # Summary
    print("\n" + "=" * 60)
    print("Website generation complete!")
    print("=" * 60)
    print(f"\nOutput directory: {output_dir.absolute()}")
    print(f"Homepage: {output_dir / 'index.html'}")
    print("\nAI Agents:")
    print(f"  Categories: {len(categories)} pages")
    print(f"  Entries: {len(agents)}")
    print("\nBoilerplates:")
    print(f"  Categories: {len(boilerplate_categories)} pages")
    print(f"  Entries: {len(boilerplates)}")
    print("\nTo preview locally, run:")
    print(f"  cd {output_dir} && python -m http.server 8001")
    print("  Then visit: http://localhost:8001")
    print()


if __name__ == "__main__":
    generate_site()

#!/usr/bin/env python3
"""
Generate README.md from YAML data files

Usage:
    python scripts/generate_readme.py
"""

from pathlib import Path
from collections import defaultdict
from datetime import date
import yaml
from jinja2 import Environment, FileSystemLoader
from models import AgentEntry, Category, DirectoryMetadata
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


def count_boilerplates() -> int:
    """Count total boilerplate entries for cross-reference"""
    boilerplates_dir = Path("data/boilerplates")
    return len(list(boilerplates_dir.rglob("*.yml")))


def group_by_category(agents: list[AgentEntry]) -> dict:
    """Group agents by category"""
    grouped = defaultdict(list)
    for agent in agents:
        grouped[agent.category].append(agent)

    # Sort entries within each category by name
    for category in grouped:
        grouped[category].sort(key=lambda a: a.name.lower())

    return dict(grouped)


def render_readme(
    metadata: DirectoryMetadata,
    categories: list[Category],
    entries_by_category: dict,
    boilerplate_count: int,
) -> str:
    """Render README content from template and data."""
    env = Environment(
        loader=FileSystemLoader("templates"), trim_blocks=True, lstrip_blocks=True
    )
    template = env.get_template("readme.jinja2")

    return template.render(
        metadata=metadata,
        categories=categories,
        entries_by_category=entries_by_category,
        boilerplate_count=boilerplate_count,
    )


def generate_readme():
    """Generate README.md from templates and data"""

    print("Loading data...")
    site_config = load_site_config()
    categories = load_categories()
    agents = load_agents()
    entries_by_category = group_by_category(agents)
    boilerplate_count = count_boilerplates()

    print(f"Loaded {len(categories)} categories and {len(agents)} agents")
    print(f"Found {boilerplate_count} boilerplates for cross-reference")

    # Build metadata
    metadata = DirectoryMetadata(
        title=site_config.title,
        tagline=site_config.tagline,
        total_entries=len(agents),
        last_generated=date.today(),
        links=site_config.links,
    )

    # Render
    print("Rendering README...")
    output = render_readme(
        metadata=metadata,
        categories=categories,
        entries_by_category=entries_by_category,
        boilerplate_count=boilerplate_count,
    )

    # Write
    readme_path = Path("README.md")
    readme_path.write_text(output)

    print(f"[OK] Generated {readme_path} with {len(agents)} entries")


if __name__ == "__main__":
    generate_readme()

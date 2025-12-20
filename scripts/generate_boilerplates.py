#!/usr/bin/env python3
"""
Generate BOILERPLATES.md from YAML data files

Usage:
    python scripts/generate_boilerplates.py
"""

from pathlib import Path
from collections import defaultdict
from datetime import date
import re
import yaml
from jinja2 import Environment, FileSystemLoader
from models import BoilerplateEntry, BoilerplateCategory


def load_boilerplate_categories() -> list[BoilerplateCategory]:
    """Load all boilerplate category definitions from data/boilerplate-categories/*.yml"""
    categories = []
    category_dir = Path("data/boilerplate-categories")

    for yml_file in sorted(category_dir.glob("*.yml")):
        with open(yml_file) as f:
            data = yaml.safe_load(f)
        categories.append(BoilerplateCategory(**data))

    return sorted(categories, key=lambda c: c.order)


def load_boilerplates() -> list[BoilerplateEntry]:
    """Load all boilerplate entries from data/boilerplates/**/*.yml"""
    boilerplates = []
    boilerplates_dir = Path("data/boilerplates")

    for yml_file in boilerplates_dir.rglob("*.yml"):
        with open(yml_file) as f:
            data = yaml.safe_load(f)
        if data:  # Skip empty files
            boilerplates.append(BoilerplateEntry(**data))

    return boilerplates


def format_stars(count: int | None) -> str:
    """Format star count: 28300 -> '28.3K', None -> '-'"""
    if count is None:
        return "-"
    if count >= 1000:
        # Format with one decimal place for K notation
        k_value = count / 1000
        if k_value >= 10:
            return f"{k_value:.1f}K".replace(".0K", "K")
        return f"{k_value:.1f}K"
    return str(count)


def slugify(text: str) -> str:
    """Convert text to GitHub-compatible anchor slug

    GitHub's anchor algorithm:
    - Lowercase
    - Spaces to hyphens
    - Remove special chars except hyphens
    - Collapse multiple hyphens
    """
    # Lowercase
    slug = text.lower()
    # Replace spaces with hyphens
    slug = slug.replace(" ", "-")
    # Remove special characters (keep alphanumeric and hyphens)
    slug = re.sub(r"[^a-z0-9\-]", "", slug)
    # Collapse multiple hyphens
    slug = re.sub(r"-+", "-", slug)
    # Remove leading/trailing hyphens
    slug = slug.strip("-")
    return slug


def group_by_ecosystem(categories: list[BoilerplateCategory]) -> dict[str, list[BoilerplateCategory]]:
    """Group categories by ecosystem for hierarchical display

    Returns dict with ecosystem name as key and list of categories as value,
    maintaining the order within each ecosystem.
    """
    grouped = defaultdict(list)
    for category in categories:
        grouped[category.ecosystem].append(category)

    # Convert to regular dict and ensure order within ecosystems
    result = {}
    for ecosystem, cats in grouped.items():
        result[ecosystem] = sorted(cats, key=lambda c: c.order)

    return result


def group_by_category(boilerplates: list[BoilerplateEntry]) -> dict[str, list[BoilerplateEntry]]:
    """Group entries by category ID"""
    grouped = defaultdict(list)
    for boilerplate in boilerplates:
        grouped[boilerplate.category].append(boilerplate)

    # Sort entries within each category by stars (descending), then by name
    for category in grouped:
        grouped[category].sort(
            key=lambda b: (-(b.github_stars or 0), b.name.lower())
        )

    return dict(grouped)


def truncate_description(text: str, max_length: int = 150) -> str:
    """Limit description to max_length chars with ellipsis"""
    if not text:
        return ""
    # Clean up multi-line descriptions
    text = " ".join(text.split())
    if len(text) <= max_length:
        return text
    return text[:max_length - 3].rsplit(" ", 1)[0] + "..."


def get_ecosystem_order() -> list[str]:
    """Return the canonical ecosystem display order"""
    return [
        "JavaScript/TypeScript",
        "Python",
        "PHP",
        "Ruby",
        "Go",
        "Rust",
        ".NET",
        "Elixir",
        "Mobile",
        "Specialized",
    ]


def generate_boilerplates_readme():
    """Main function: load data, render template, write output"""

    print("Loading boilerplate data...")
    categories = load_boilerplate_categories()
    boilerplates = load_boilerplates()
    entries_by_category = group_by_category(boilerplates)
    categories_by_ecosystem = group_by_ecosystem(categories)

    print(f"Loaded {len(categories)} categories and {len(boilerplates)} boilerplates")

    # Build ordered ecosystems list (only those with categories)
    ecosystem_order = get_ecosystem_order()
    ordered_ecosystems = []
    for eco in ecosystem_order:
        if eco in categories_by_ecosystem:
            ordered_ecosystems.append(eco)
    # Add any ecosystems not in our predefined order
    for eco in categories_by_ecosystem:
        if eco not in ordered_ecosystems:
            ordered_ecosystems.append(eco)

    # Load template
    env = Environment(
        loader=FileSystemLoader("templates"),
        trim_blocks=True,
        lstrip_blocks=True
    )

    # Register custom filters
    env.filters["format_stars"] = format_stars
    env.filters["slugify"] = slugify
    env.filters["truncate_desc"] = truncate_description

    template = env.get_template("boilerplates_readme.jinja2")

    # Render
    print("Rendering BOILERPLATES.md...")
    output = template.render(
        total_entries=len(boilerplates),
        last_generated=date.today(),
        ecosystems=ordered_ecosystems,
        categories_by_ecosystem=categories_by_ecosystem,
        entries_by_category=entries_by_category,
        categories=categories,
    )

    # Write
    output_path = Path("BOILERPLATES.md")
    output_path.write_text(output)

    print(f"Generated {output_path} with {len(boilerplates)} entries")


if __name__ == "__main__":
    generate_boilerplates_readme()

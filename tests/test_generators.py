"""
Tests for generator helpers and search index structure.
"""

import sys
from datetime import date
from pathlib import Path

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from generate_boilerplates import render_boilerplates_readme
from generate_readme import render_readme
from generate_site import create_search_index, create_boilerplate_search_index
from models import (
    AgentEntry,
    BoilerplateEntry,
    BoilerplateCategory,
    Category,
    DirectoryMetadata,
    SiteLinks,
    TechStackComponent,
)


def build_site_links() -> SiteLinks:
    return SiteLinks(
        github="https://example.com/repo",
        issues="https://example.com/issues",
        discussions="https://example.com/discussions",
        contributing="https://example.com/contributing",
        suggest="https://example.com/suggest",
    )


def test_render_readme_includes_category_and_entry() -> None:
    metadata = DirectoryMetadata(
        title="Test Directory",
        tagline="Test tagline for readme rendering.",
        total_entries=1,
        last_generated=date(2025, 1, 1),
        links=build_site_links(),
    )
    category = Category(
        id="test-category",
        title="Test Category",
        description="A test category description.",
        emoji="[]",
    )
    agent = AgentEntry(
        name="Test Agent",
        url="https://example.com/agent",
        description="A valid description for the test agent.",
        category="test-category",
        tags=["testing"],
    )

    output = render_readme(
        metadata=metadata,
        categories=[category],
        entries_by_category={"test-category": [agent]},
        boilerplate_count=0,
    )

    assert "# Test Directory" in output
    assert "Test Category" in output
    assert "Test Agent" in output


def test_render_boilerplates_includes_entry() -> None:
    category = BoilerplateCategory(
        id="nextjs",
        title="Next.js Boilerplates",
        description="A test boilerplate category description.",
        ecosystem="JavaScript/TypeScript",
        emoji="[]",
    )
    boilerplate = BoilerplateEntry(
        name="Test Boilerplate",
        url="https://example.com/boilerplate",
        description="A valid boilerplate description for testing output.",
        category="nextjs",
        tags=["testing"],
        technical_stack=[
            TechStackComponent(component="Frontend", technology="Next.js"),
        ],
    )

    output = render_boilerplates_readme(
        total_entries=1,
        last_generated=date(2025, 1, 1),
        ecosystems=["JavaScript/TypeScript"],
        categories_by_ecosystem={"JavaScript/TypeScript": [category]},
        entries_by_category={"nextjs": [boilerplate]},
        categories=[category],
        agent_count=1,
        site_links=build_site_links(),
    )

    assert "Full-Stack Boilerplate Directory" in output
    assert "Next.js Boilerplates" in output
    assert "Test Boilerplate" in output


def test_create_search_index_structure() -> None:
    category = Category(
        id="test-category",
        title="Test Category",
        description="A test category description.",
        emoji="[]",
    )
    agent = AgentEntry(
        name="Test Agent",
        url="https://example.com/agent",
        description="A valid description for the test agent.",
        category="test-category",
        tags=["testing"],
    )

    index = create_search_index([agent], [category])

    assert index[0]["category_title"] == "Test Category"
    assert "is_boilerplate" not in index[0]


def test_create_boilerplate_search_index_structure() -> None:
    category = BoilerplateCategory(
        id="nextjs",
        title="Next.js Boilerplates",
        description="A test boilerplate category description.",
        ecosystem="JavaScript/TypeScript",
        emoji="[]",
    )
    boilerplate = BoilerplateEntry(
        name="Test Boilerplate",
        url="https://example.com/boilerplate",
        description="A valid boilerplate description for testing output.",
        category="nextjs",
        tags=["testing"],
        technical_stack=[
            TechStackComponent(component="Frontend", technology="Next.js"),
            TechStackComponent(component="Database", technology="PostgreSQL"),
        ],
    )

    index = create_boilerplate_search_index([boilerplate], [category])

    assert index[0]["is_boilerplate"] is True
    assert index[0]["tech_stack"] == ["Next.js", "PostgreSQL"]

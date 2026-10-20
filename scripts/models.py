"""
Pydantic models for Ultimate Agent Directory
Provides type-safe validation for all agent entries and categories
"""

import re
from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl, field_validator

TAG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def validate_tags(tags: list[str]) -> list[str]:
    normalized_tags: list[str] = []
    seen: set[str] = set()

    for tag in tags:
        if not isinstance(tag, str):
            raise ValueError("tags must be strings")  # noqa: TRY004 - ValueError is what pydantic/callers expect
        normalized = tag.strip().lower().replace(" ", "-")
        if tag != normalized:
            raise ValueError(
                f"Tag '{tag}' must be lowercase and hyphenated (ex: '{normalized}')"
            )
        if not TAG_PATTERN.match(tag):
            raise ValueError(
                f"Tag '{tag}' must match pattern {TAG_PATTERN.pattern}"
            )
        if tag in seen:
            raise ValueError(f"Duplicate tag '{tag}' is not allowed")
        normalized_tags.append(tag)
        seen.add(tag)

    return normalized_tags


class AgentEntry(BaseModel):
    """Schema for a single agent/tool/platform entry"""

    # ===== REQUIRED FIELDS =====
    name: str = Field(min_length=1, max_length=100, description="Agent/tool name")

    url: HttpUrl = Field(description="Primary URL (GitHub, website, or documentation)")

    description: str = Field(
        min_length=20,
        max_length=1000,
        description="Clear, factual description (no marketing hype)",
    )

    category: str = Field(description="Primary category (must match category ID)")

    # ===== CLASSIFICATION METADATA =====
    subcategory: str | None = Field(
        default=None, description="Optional subcategory (e.g., 'core-frameworks')"
    )

    type: Literal[
        "framework", "platform", "tool", "course", "community", "research"
    ] = Field(default="framework", description="Entry type")

    tags: list[str] = Field(
        default_factory=list, description="Tags for filtering (lowercase, hyphenated)"
    )

    # ===== OPTIONAL URLS =====
    github_repo: str | None = Field(
        default=None, description="GitHub repo in 'owner/repo' format"
    )

    documentation_url: HttpUrl | None = None
    demo_url: HttpUrl | None = None

    # ===== TECHNICAL METADATA =====
    platform: list[str] | None = Field(
        default=None, description="Languages/platforms (e.g., ['Python', 'TypeScript'])"
    )

    license: str | None = Field(
        default=None, description="License type (e.g., 'MIT', 'Apache-2.0')"
    )

    pricing: Literal["free", "freemium", "paid", "enterprise"] | None = None

    # ===== AUTO-COLLECTED (GitHub API) =====
    github_stars: int | None = Field(
        default=None, description="Auto-updated by GitHub Action"
    )

    last_updated: date | None = Field(
        default=None, description="Last commit date (auto-updated)"
    )

    is_archived: bool = Field(default=False, description="Is GitHub repo archived?")

    # ===== EDITORIAL FLAGS =====
    featured: bool = Field(default=False, description="Highlight on homepage?")

    verified: bool = Field(
        default=False, description="Link checked, metadata complete?"
    )

    # ===== METADATA TRACKING =====
    added_date: date | None = Field(
        default=None, description="When added to directory"
    )

    last_verified: date | None = Field(
        default=None, description="Last manual verification"
    )

    @field_validator("tags")
    @classmethod
    def validate_tags_field(cls, v):
        """Ensure tags are lowercase, hyphenated, and unique"""
        return validate_tags(v)

    @field_validator("github_repo")
    @classmethod
    def validate_github_repo(cls, v):
        """Ensure GitHub repo format is correct"""
        if v and "/" not in v:
            raise ValueError("github_repo must be 'owner/repo' format")
        return v

    class Config:
        extra = "forbid"  # Reject unknown fields


class Category(BaseModel):
    """Schema for a category/section definition"""

    id: str = Field(description="URL-safe identifier (lowercase, hyphenated)")

    title: str = Field(description="Display title")

    emoji: str = Field(default="[]", description="Category marker for display")

    description: str = Field(
        min_length=10, max_length=500, description="Category description"
    )

    order: int = Field(default=0, description="Display order (lower = earlier)")

    parent: str | None = Field(
        default=None, description="Parent category ID (for subcategories)"
    )

    # Display configuration
    show_github_stats: bool = Field(
        default=True, description="Show GitHub stars in tables?"
    )

    table_columns: list[str] = Field(
        default=["name", "url", "description"],
        description="Which columns to show in markdown table",
    )

    class Config:
        extra = "forbid"


class SiteLinks(BaseModel):
    """External links used across templates"""

    github: HttpUrl
    issues: HttpUrl
    discussions: HttpUrl
    contributing: HttpUrl
    suggest: HttpUrl


class SiteConfig(BaseModel):
    """Site-level configuration loaded from data/metadata.yml"""

    title: str = "Ultimate AI Agent Directory"
    version: str = "0.1.0"
    tagline: str = (
        "The most comprehensive collection of AI agent frameworks, platforms, tools, and resources"
    )
    base_url: str = "/Ultimate-Agent-Directory"
    site_url: HttpUrl = "https://moshehbenavraham.github.io/Ultimate-Agent-Directory"  # type: ignore[assignment]
    links: SiteLinks

    class Config:
        extra = "forbid"


class DirectoryMetadata(BaseModel):
    """Overall directory metadata"""

    title: str = "Ultimate AI Agent Directory"
    version: str = "0.1.0"
    tagline: str = "The most comprehensive collection of AI agent frameworks, platforms, tools, and resources"

    last_generated: date = Field(
        default_factory=date.today, description="When README/website was last generated"
    )

    total_entries: int = 0

    badges: dict = Field(default_factory=dict, description="Badge counts by type")
    links: SiteLinks | None = None


# ===== BOILERPLATE MODELS =====


class TechStackComponent(BaseModel):
    """Schema for a single technology in a boilerplate's technical stack"""

    component: str = Field(
        min_length=1,
        max_length=50,
        description="Component type (e.g., Frontend, Database)",
    )

    technology: str = Field(
        min_length=1,
        max_length=100,
        description="Technology name (e.g., Next.js, PostgreSQL)",
    )

    reasoning: str | None = Field(
        default=None,
        max_length=500,
        description="Why this technology was chosen",
    )

    class Config:
        extra = "forbid"


class BoilerplateEntry(BaseModel):
    """Schema for a single boilerplate/starter kit entry"""

    # ===== REQUIRED FIELDS =====
    name: str = Field(min_length=1, max_length=100, description="Boilerplate name")

    url: HttpUrl = Field(description="Primary URL (GitHub or website)")

    description: str = Field(
        min_length=20,
        max_length=2000,
        description="Clear, factual description of the boilerplate",
    )

    category: str = Field(
        description="Primary category (must match boilerplate category ID)"
    )

    # ===== CLASSIFICATION METADATA =====
    type: Literal["starter", "boilerplate", "template", "scaffold", "toolkit"] = Field(
        default="boilerplate", description="Entry type"
    )

    tags: list[str] = Field(
        default_factory=list, description="Tags for filtering (lowercase, hyphenated)"
    )

    # ===== OPTIONAL URLS =====
    github_repo: str | None = Field(
        default=None, description="GitHub repo in 'owner/repo' format"
    )

    documentation_url: HttpUrl | None = None
    demo_url: HttpUrl | None = None

    # ===== TECHNICAL METADATA =====
    technical_stack: list[TechStackComponent] = Field(
        default_factory=list,
        description="Structured list of technologies with reasoning",
    )

    platform: list[str] | None = Field(
        default=None,
        description="Primary languages/platforms (e.g., ['TypeScript', 'React'])",
    )

    license: str | None = Field(
        default=None, description="License type (e.g., 'MIT', 'Apache-2.0')"
    )

    pricing: Literal["free", "freemium", "paid", "enterprise", "open-core"] | None = None

    # ===== GITHUB STATS =====
    github_stars: int | None = Field(default=None, description="GitHub star count")

    last_updated: date | None = Field(default=None, description="Last commit date")

    is_archived: bool = Field(default=False, description="Is GitHub repo archived?")

    # ===== BOILERPLATE-SPECIFIC FIELDS =====
    key_features: list[str] | None = Field(
        default=None, description="List of key features"
    )

    use_case: str | None = Field(
        default=None,
        max_length=1000,
        description="Ideal use case description",
    )

    pros: list[str] | None = Field(default=None, description="List of advantages")

    cons: list[str] | None = Field(default=None, description="List of disadvantages")

    community: str | None = Field(
        default=None,
        max_length=500,
        description="Community information (Discord, forums, etc.)",
    )

    deployment: list[str] | None = Field(
        default=None, description="Deployment platforms (e.g., ['Vercel', 'AWS'])"
    )

    # ===== EDITORIAL FLAGS =====
    featured: bool = Field(default=False, description="Highlight on homepage?")

    verified: bool = Field(
        default=False, description="Link checked, metadata complete?"
    )

    # ===== METADATA TRACKING =====
    added_date: date | None = Field(
        default=None, description="When added to directory"
    )

    last_verified: date | None = Field(
        default=None, description="Last manual verification"
    )

    @field_validator("tags")
    @classmethod
    def validate_tags_field(cls, v):
        """Ensure tags are lowercase, hyphenated, and unique"""
        return validate_tags(v)

    @field_validator("github_repo")
    @classmethod
    def validate_github_repo(cls, v):
        """Ensure GitHub repo format is correct"""
        if v and "/" not in v:
            raise ValueError("github_repo must be 'owner/repo' format")
        return v

    class Config:
        extra = "forbid"


class BoilerplateCategory(BaseModel):
    """Schema for a boilerplate category/ecosystem definition"""

    id: str = Field(description="URL-safe identifier (lowercase, hyphenated)")

    title: str = Field(description="Display title")

    emoji: str = Field(default="[]", description="Category marker for display")

    description: str = Field(
        min_length=10, max_length=500, description="Category description"
    )

    ecosystem: str = Field(
        description="Language/framework ecosystem (e.g., 'JavaScript', 'Python', 'Rust')"
    )

    order: int = Field(default=0, description="Display order (lower = earlier)")

    # Display configuration
    show_github_stats: bool = Field(
        default=True, description="Show GitHub stars in tables?"
    )

    table_columns: list[str] = Field(
        default=["name", "url", "description", "github_stars"],
        description="Which columns to show in markdown table",
    )

    class Config:
        extra = "forbid"

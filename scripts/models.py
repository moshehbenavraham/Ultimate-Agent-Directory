"""
Pydantic models for Ultimate Agent Directory
Provides type-safe validation for all agent entries and categories
"""

from pydantic import BaseModel, HttpUrl, Field, field_validator
from typing import List, Optional, Literal
from datetime import date


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
    subcategory: Optional[str] = Field(
        default=None, description="Optional subcategory (e.g., 'core-frameworks')"
    )

    type: Literal[
        "framework", "platform", "tool", "course", "community", "research"
    ] = Field(default="framework", description="Entry type")

    tags: List[str] = Field(
        default_factory=list, description="Tags for filtering (lowercase, hyphenated)"
    )

    # ===== OPTIONAL URLS =====
    github_repo: Optional[str] = Field(
        default=None, description="GitHub repo in 'owner/repo' format"
    )

    documentation_url: Optional[HttpUrl] = None
    demo_url: Optional[HttpUrl] = None

    # ===== TECHNICAL METADATA =====
    platform: Optional[List[str]] = Field(
        default=None, description="Languages/platforms (e.g., ['Python', 'TypeScript'])"
    )

    license: Optional[str] = Field(
        default=None, description="License type (e.g., 'MIT', 'Apache-2.0')"
    )

    pricing: Optional[Literal["free", "freemium", "paid", "enterprise"]] = None

    # ===== AUTO-COLLECTED (GitHub API) =====
    github_stars: Optional[int] = Field(
        default=None, description="Auto-updated by GitHub Action"
    )

    last_updated: Optional[date] = Field(
        default=None, description="Last commit date (auto-updated)"
    )

    is_archived: bool = Field(default=False, description="Is GitHub repo archived?")

    # ===== EDITORIAL FLAGS =====
    featured: bool = Field(default=False, description="Highlight on homepage?")

    verified: bool = Field(
        default=False, description="Link checked, metadata complete?"
    )

    # ===== METADATA TRACKING =====
    added_date: Optional[date] = Field(
        default=None, description="When added to directory"
    )

    last_verified: Optional[date] = Field(
        default=None, description="Last manual verification"
    )

    @field_validator("tags")
    @classmethod
    def lowercase_tags(cls, v):
        """Ensure tags are lowercase and hyphenated"""
        return [tag.lower().replace(" ", "-") for tag in v]

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

    emoji: str = Field(default="📦", description="Emoji for visual identification")

    description: str = Field(
        min_length=10, max_length=500, description="Category description"
    )

    order: int = Field(default=0, description="Display order (lower = earlier)")

    parent: Optional[str] = Field(
        default=None, description="Parent category ID (for subcategories)"
    )

    # Display configuration
    show_github_stats: bool = Field(
        default=True, description="Show GitHub stars in tables?"
    )

    table_columns: List[str] = Field(
        default=["name", "url", "description"],
        description="Which columns to show in markdown table",
    )

    class Config:
        extra = "forbid"


class DirectoryMetadata(BaseModel):
    """Overall directory metadata"""

    title: str = "Ultimate AI Agent Directory 2025"
    tagline: str = "The most comprehensive collection of AI agent frameworks, platforms, tools, and resources"
    maintainer: str = "AIwithApex.com"
    maintainer_url: str = "https://AIwithApex.com"

    last_generated: date = Field(
        default_factory=date.today, description="When README/website was last generated"
    )

    total_entries: int = 0

    badges: dict = Field(default_factory=dict, description="Badge counts by type")


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

    reasoning: Optional[str] = Field(
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

    tags: List[str] = Field(
        default_factory=list, description="Tags for filtering (lowercase, hyphenated)"
    )

    # ===== OPTIONAL URLS =====
    github_repo: Optional[str] = Field(
        default=None, description="GitHub repo in 'owner/repo' format"
    )

    documentation_url: Optional[HttpUrl] = None
    demo_url: Optional[HttpUrl] = None

    # ===== TECHNICAL METADATA =====
    technical_stack: List[TechStackComponent] = Field(
        default_factory=list,
        description="Structured list of technologies with reasoning",
    )

    platform: Optional[List[str]] = Field(
        default=None,
        description="Primary languages/platforms (e.g., ['TypeScript', 'React'])",
    )

    license: Optional[str] = Field(
        default=None, description="License type (e.g., 'MIT', 'Apache-2.0')"
    )

    pricing: Optional[
        Literal["free", "freemium", "paid", "enterprise", "open-core"]
    ] = None

    # ===== GITHUB STATS =====
    github_stars: Optional[int] = Field(default=None, description="GitHub star count")

    last_updated: Optional[date] = Field(default=None, description="Last commit date")

    is_archived: bool = Field(default=False, description="Is GitHub repo archived?")

    # ===== BOILERPLATE-SPECIFIC FIELDS =====
    key_features: Optional[List[str]] = Field(
        default=None, description="List of key features"
    )

    use_case: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Ideal use case description",
    )

    pros: Optional[List[str]] = Field(default=None, description="List of advantages")

    cons: Optional[List[str]] = Field(default=None, description="List of disadvantages")

    community: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Community information (Discord, forums, etc.)",
    )

    deployment: Optional[List[str]] = Field(
        default=None, description="Deployment platforms (e.g., ['Vercel', 'AWS'])"
    )

    # ===== EDITORIAL FLAGS =====
    featured: bool = Field(default=False, description="Highlight on homepage?")

    verified: bool = Field(
        default=False, description="Link checked, metadata complete?"
    )

    # ===== METADATA TRACKING =====
    added_date: Optional[date] = Field(
        default=None, description="When added to directory"
    )

    last_verified: Optional[date] = Field(
        default=None, description="Last manual verification"
    )

    @field_validator("tags")
    @classmethod
    def lowercase_tags(cls, v):
        """Ensure tags are lowercase and hyphenated"""
        return [tag.lower().replace(" ", "-") for tag in v]

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

    emoji: str = Field(default="📦", description="Emoji for visual identification")

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

    table_columns: List[str] = Field(
        default=["name", "url", "description", "github_stars"],
        description="Which columns to show in markdown table",
    )

    class Config:
        extra = "forbid"

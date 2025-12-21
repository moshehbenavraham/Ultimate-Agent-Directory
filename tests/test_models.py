"""
Tests for Pydantic schema validation in models.py

These tests verify:
- Valid entries pass validation
- Invalid entries fail with appropriate errors
- Custom validators work correctly (tags, github_repo)
- Edge cases for field lengths and formats
- extra="forbid" rejects unknown fields
"""

import pytest
import sys
from pathlib import Path
from datetime import date

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from pydantic import ValidationError
from models import (
    AgentEntry,
    BoilerplateEntry,
    Category,
    BoilerplateCategory,
    TechStackComponent,
    DirectoryMetadata,
)


# =============================================================================
# AgentEntry Tests
# =============================================================================


class TestAgentEntryValid:
    """Test valid AgentEntry configurations"""

    def test_minimal_valid_entry(self):
        """Minimal required fields create valid entry"""
        entry = AgentEntry(
            name="Test Agent",
            url="https://github.com/test/repo",
            description="A test agent framework for building AI applications.",
            category="open-source-frameworks",
        )
        assert entry.name == "Test Agent"
        assert str(entry.url) == "https://github.com/test/repo"
        assert entry.type == "framework"  # Default value

    def test_full_valid_entry(self):
        """All fields populated creates valid entry"""
        entry = AgentEntry(
            name="Full Agent",
            url="https://example.com/agent",
            description="A comprehensive agent with all fields populated for testing.",
            category="autonomous-agents",
            subcategory="coding-agents",
            type="platform",
            tags=["ai", "automation", "enterprise"],
            github_repo="owner/repo",
            documentation_url="https://docs.example.com",
            demo_url="https://demo.example.com",
            platform=["Python", "TypeScript"],
            license="MIT",
            pricing="freemium",
            github_stars=1000,
            last_updated=date(2024, 1, 15),
            is_archived=False,
            featured=True,
            verified=True,
            added_date=date(2023, 6, 1),
            last_verified=date(2024, 1, 10),
        )
        assert entry.name == "Full Agent"
        assert entry.type == "platform"
        assert entry.pricing == "freemium"
        assert entry.featured is True


class TestAgentEntryDescription:
    """Test description field validation"""

    def test_description_minimum_length(self):
        """Description must be at least 20 characters"""
        with pytest.raises(ValidationError) as exc_info:
            AgentEntry(
                name="Test",
                url="https://example.com",
                description="Too short",  # Only 9 chars
                category="test",
            )
        assert "description" in str(exc_info.value)

    def test_description_exactly_20_chars(self):
        """Description with exactly 20 characters passes"""
        entry = AgentEntry(
            name="Test",
            url="https://example.com",
            description="A" * 20,  # Exactly 20 chars
            category="test",
        )
        assert len(entry.description) == 20

    def test_description_maximum_length(self):
        """Description must be at most 1000 characters"""
        with pytest.raises(ValidationError) as exc_info:
            AgentEntry(
                name="Test",
                url="https://example.com",
                description="A" * 1001,  # 1001 chars - over limit
                category="test",
            )
        assert "description" in str(exc_info.value)

    def test_description_exactly_1000_chars(self):
        """Description with exactly 1000 characters passes"""
        entry = AgentEntry(
            name="Test",
            url="https://example.com",
            description="A" * 1000,  # Exactly 1000 chars
            category="test",
        )
        assert len(entry.description) == 1000


class TestAgentEntryName:
    """Test name field validation"""

    def test_name_empty_fails(self):
        """Empty name fails validation"""
        with pytest.raises(ValidationError) as exc_info:
            AgentEntry(
                name="",
                url="https://example.com",
                description="A valid description here.",
                category="test",
            )
        assert "name" in str(exc_info.value)

    def test_name_maximum_length(self):
        """Name must be at most 100 characters"""
        with pytest.raises(ValidationError) as exc_info:
            AgentEntry(
                name="A" * 101,  # 101 chars - over limit
                url="https://example.com",
                description="A valid description here.",
                category="test",
            )
        assert "name" in str(exc_info.value)


class TestAgentEntryUrl:
    """Test URL field validation"""

    def test_invalid_url_fails(self):
        """Invalid URL format fails validation"""
        with pytest.raises(ValidationError) as exc_info:
            AgentEntry(
                name="Test",
                url="not-a-valid-url",
                description="A valid description here.",
                category="test",
            )
        assert "url" in str(exc_info.value).lower()

    def test_http_url_passes(self):
        """HTTP URL passes validation"""
        entry = AgentEntry(
            name="Test",
            url="http://example.com",
            description="A valid description here.",
            category="test",
        )
        assert "http://example.com" in str(entry.url)

    def test_https_url_passes(self):
        """HTTPS URL passes validation"""
        entry = AgentEntry(
            name="Test",
            url="https://example.com/path?query=value",
            description="A valid description here.",
            category="test",
        )
        assert "https://example.com" in str(entry.url)


class TestAgentEntryGithubRepo:
    """Test github_repo custom validator"""

    def test_github_repo_without_slash_fails(self):
        """github_repo without slash fails validation"""
        with pytest.raises(ValidationError) as exc_info:
            AgentEntry(
                name="Test",
                url="https://example.com",
                description="A valid description here.",
                category="test",
                github_repo="langchain",  # Missing slash
            )
        assert "owner/repo" in str(exc_info.value)

    def test_github_repo_with_slash_passes(self):
        """github_repo with owner/repo format passes"""
        entry = AgentEntry(
            name="Test",
            url="https://example.com",
            description="A valid description here.",
            category="test",
            github_repo="langchain-ai/langchain",
        )
        assert entry.github_repo == "langchain-ai/langchain"

    def test_github_repo_none_passes(self):
        """github_repo can be None"""
        entry = AgentEntry(
            name="Test",
            url="https://example.com",
            description="A valid description here.",
            category="test",
            github_repo=None,
        )
        assert entry.github_repo is None


class TestAgentEntryTags:
    """Test tags custom validator"""

    def test_tags_normalized_to_lowercase(self):
        """Tags are converted to lowercase"""
        entry = AgentEntry(
            name="Test",
            url="https://example.com",
            description="A valid description here.",
            category="test",
            tags=["AI", "Machine Learning", "NLP"],
        )
        assert entry.tags == ["ai", "machine-learning", "nlp"]

    def test_tags_spaces_to_hyphens(self):
        """Spaces in tags are converted to hyphens"""
        entry = AgentEntry(
            name="Test",
            url="https://example.com",
            description="A valid description here.",
            category="test",
            tags=["multi agent system", "natural language processing"],
        )
        assert entry.tags == ["multi-agent-system", "natural-language-processing"]

    def test_tags_empty_list_passes(self):
        """Empty tags list passes validation"""
        entry = AgentEntry(
            name="Test",
            url="https://example.com",
            description="A valid description here.",
            category="test",
            tags=[],
        )
        assert entry.tags == []


class TestAgentEntryTypeLiteral:
    """Test type field literal validation"""

    @pytest.mark.parametrize(
        "type_value",
        ["framework", "platform", "tool", "course", "community", "research"],
    )
    def test_valid_types(self, type_value):
        """All valid type literals pass validation"""
        entry = AgentEntry(
            name="Test",
            url="https://example.com",
            description="A valid description here.",
            category="test",
            type=type_value,
        )
        assert entry.type == type_value

    def test_invalid_type_fails(self):
        """Invalid type literal fails validation"""
        with pytest.raises(ValidationError) as exc_info:
            AgentEntry(
                name="Test",
                url="https://example.com",
                description="A valid description here.",
                category="test",
                type="invalid_type",
            )
        assert "type" in str(exc_info.value)


class TestAgentEntryPricing:
    """Test pricing field literal validation"""

    @pytest.mark.parametrize(
        "pricing_value", ["free", "freemium", "paid", "enterprise", None]
    )
    def test_valid_pricing(self, pricing_value):
        """All valid pricing literals pass validation"""
        entry = AgentEntry(
            name="Test",
            url="https://example.com",
            description="A valid description here.",
            category="test",
            pricing=pricing_value,
        )
        assert entry.pricing == pricing_value

    def test_invalid_pricing_fails(self):
        """Invalid pricing literal fails validation"""
        with pytest.raises(ValidationError) as exc_info:
            AgentEntry(
                name="Test",
                url="https://example.com",
                description="A valid description here.",
                category="test",
                pricing="subscription",  # Not a valid literal
            )
        assert "pricing" in str(exc_info.value)


class TestAgentEntryExtraForbid:
    """Test extra='forbid' configuration"""

    def test_unknown_field_rejected(self):
        """Unknown fields are rejected"""
        with pytest.raises(ValidationError) as exc_info:
            AgentEntry(
                name="Test",
                url="https://example.com",
                description="A valid description here.",
                category="test",
                unknown_field="should fail",  # Unknown field
            )
        assert (
            "extra" in str(exc_info.value).lower()
            or "unknown" in str(exc_info.value).lower()
        )


# =============================================================================
# BoilerplateEntry Tests
# =============================================================================


class TestBoilerplateEntry:
    """Test BoilerplateEntry validation"""

    def test_valid_boilerplate_entry(self):
        """Valid boilerplate entry passes validation"""
        entry = BoilerplateEntry(
            name="Next.js Starter",
            url="https://github.com/test/nextjs-starter",
            description="A production-ready Next.js boilerplate with TypeScript.",
            category="nextjs",
        )
        assert entry.name == "Next.js Starter"
        assert entry.type == "boilerplate"  # Default value

    def test_description_allows_2000_chars(self):
        """Boilerplate description allows up to 2000 characters"""
        entry = BoilerplateEntry(
            name="Test",
            url="https://example.com",
            description="A" * 2000,  # 2000 chars - at limit
            category="test",
        )
        assert len(entry.description) == 2000

    def test_description_over_2000_fails(self):
        """Boilerplate description over 2000 characters fails"""
        with pytest.raises(ValidationError) as exc_info:
            BoilerplateEntry(
                name="Test",
                url="https://example.com",
                description="A" * 2001,  # 2001 chars - over limit
                category="test",
            )
        assert "description" in str(exc_info.value)

    @pytest.mark.parametrize(
        "type_value", ["starter", "boilerplate", "template", "scaffold", "toolkit"]
    )
    def test_valid_boilerplate_types(self, type_value):
        """All valid boilerplate type literals pass"""
        entry = BoilerplateEntry(
            name="Test",
            url="https://example.com",
            description="A valid description here.",
            category="test",
            type=type_value,
        )
        assert entry.type == type_value

    def test_tags_normalized(self):
        """Boilerplate tags use same normalization as AgentEntry"""
        entry = BoilerplateEntry(
            name="Test",
            url="https://example.com",
            description="A valid description here.",
            category="test",
            tags=["Full Stack", "TypeScript"],
        )
        assert entry.tags == ["full-stack", "typescript"]

    def test_github_repo_validated(self):
        """Boilerplate github_repo uses same validation as AgentEntry"""
        with pytest.raises(ValidationError):
            BoilerplateEntry(
                name="Test",
                url="https://example.com",
                description="A valid description here.",
                category="test",
                github_repo="invalid-no-slash",
            )

    def test_technical_stack_valid(self):
        """Technical stack with valid components passes"""
        entry = BoilerplateEntry(
            name="Test",
            url="https://example.com",
            description="A valid description here.",
            category="test",
            technical_stack=[
                TechStackComponent(
                    component="Frontend",
                    technology="Next.js",
                    reasoning="Industry standard for React apps",
                ),
                TechStackComponent(component="Database", technology="PostgreSQL"),
            ],
        )
        assert len(entry.technical_stack) == 2
        assert entry.technical_stack[0].component == "Frontend"


# =============================================================================
# Category Tests
# =============================================================================


class TestCategory:
    """Test Category validation"""

    def test_valid_category(self):
        """Valid category passes validation"""
        category = Category(
            id="open-source-frameworks",
            title="Open Source Frameworks",
            description="Open source frameworks for building AI agents.",
        )
        assert category.id == "open-source-frameworks"
        assert category.emoji == "📦"  # Default value
        assert category.order == 0  # Default value

    def test_description_minimum_length(self):
        """Category description must be at least 10 characters"""
        with pytest.raises(ValidationError) as exc_info:
            Category(
                id="test",
                title="Test",
                description="Short",  # Only 5 chars
            )
        assert "description" in str(exc_info.value)

    def test_description_maximum_length(self):
        """Category description must be at most 500 characters"""
        with pytest.raises(ValidationError) as exc_info:
            Category(
                id="test",
                title="Test",
                description="A" * 501,  # 501 chars - over limit
            )
        assert "description" in str(exc_info.value)

    def test_unknown_field_rejected(self):
        """Category rejects unknown fields"""
        with pytest.raises(ValidationError):
            Category(
                id="test",
                title="Test",
                description="A valid description.",
                unknown_field="should fail",
            )


# =============================================================================
# BoilerplateCategory Tests
# =============================================================================


class TestBoilerplateCategory:
    """Test BoilerplateCategory validation"""

    def test_valid_boilerplate_category(self):
        """Valid boilerplate category passes validation"""
        category = BoilerplateCategory(
            id="nextjs",
            title="Next.js Boilerplates",
            description="Production-ready Next.js starter templates.",
            ecosystem="JavaScript/TypeScript",
        )
        assert category.id == "nextjs"
        assert category.ecosystem == "JavaScript/TypeScript"

    def test_ecosystem_required(self):
        """BoilerplateCategory requires ecosystem field"""
        with pytest.raises(ValidationError) as exc_info:
            BoilerplateCategory(
                id="test",
                title="Test",
                description="A valid description.",
                # Missing ecosystem
            )
        assert "ecosystem" in str(exc_info.value)


# =============================================================================
# TechStackComponent Tests
# =============================================================================


class TestTechStackComponent:
    """Test TechStackComponent validation"""

    def test_valid_component(self):
        """Valid tech stack component passes"""
        component = TechStackComponent(
            component="Frontend",
            technology="React with Next.js",
            reasoning="Industry standard for modern web apps",
        )
        assert component.component == "Frontend"
        assert component.technology == "React with Next.js"

    def test_component_without_reasoning(self):
        """Tech stack component without reasoning passes"""
        component = TechStackComponent(component="Database", technology="PostgreSQL")
        assert component.reasoning is None

    def test_component_max_length(self):
        """Component field has max length of 50"""
        with pytest.raises(ValidationError) as exc_info:
            TechStackComponent(
                component="A" * 51,  # 51 chars - over limit
                technology="Test",
            )
        assert "component" in str(exc_info.value)

    def test_technology_max_length(self):
        """Technology field has max length of 100"""
        with pytest.raises(ValidationError) as exc_info:
            TechStackComponent(
                component="Test",
                technology="A" * 101,  # 101 chars - over limit
            )
        assert "technology" in str(exc_info.value)

    def test_reasoning_max_length(self):
        """Reasoning field has max length of 500"""
        with pytest.raises(ValidationError) as exc_info:
            TechStackComponent(
                component="Test",
                technology="Test",
                reasoning="A" * 501,  # 501 chars - over limit
            )
        assert "reasoning" in str(exc_info.value)


# =============================================================================
# DirectoryMetadata Tests
# =============================================================================


class TestDirectoryMetadata:
    """Test DirectoryMetadata validation"""

    def test_defaults(self):
        """DirectoryMetadata uses sensible defaults"""
        metadata = DirectoryMetadata()
        assert metadata.title == "Ultimate AI Agent Directory 2025"
        assert metadata.total_entries == 0
        assert metadata.last_generated == date.today()

    def test_custom_values(self):
        """DirectoryMetadata accepts custom values"""
        metadata = DirectoryMetadata(
            title="Custom Directory",
            total_entries=100,
        )
        assert metadata.title == "Custom Directory"
        assert metadata.total_entries == 100

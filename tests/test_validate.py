"""
Unit tests for scripts/validate.py

Tests for validation functions including:
- get_file_kind()
- is_yaml_file()
- build_include_map()
- collect_files()
- load_yaml_data()
- load_category_ids()
- check_category_references()
- check_duplicates()
- normalize_url()
"""

import argparse
import sys
from pathlib import Path
from typing import Any

import pytest
import yaml

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from validate import (
    ValidatedEntry,
    build_include_map,
    check_category_references,
    check_duplicates,
    collect_files,
    get_file_kind,
    is_yaml_file,
    load_category_ids,
    load_yaml_data,
    normalize_url,
    validate_yaml_file,
)

# Import models for validation tests
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from models import AgentEntry, Category


# =============================================================================
# Fixtures - T004: Temporary data directory structure
# =============================================================================


@pytest.fixture
def tmp_data_dir(tmp_path: Path) -> Path:
    """Create a temporary data directory structure mirroring production layout."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    # Create subdirectories
    (data_dir / "agents" / "open-source-frameworks").mkdir(parents=True)
    (data_dir / "agents" / "specialized-tools").mkdir(parents=True)
    (data_dir / "categories").mkdir(parents=True)
    (data_dir / "boilerplates" / "nextjs").mkdir(parents=True)
    (data_dir / "boilerplate-categories").mkdir(parents=True)

    return data_dir


# =============================================================================
# Fixtures - T005: Valid YAML agent entry
# =============================================================================


@pytest.fixture
def valid_agent_yaml() -> dict[str, Any]:
    """Return valid agent entry data matching AgentEntry schema."""
    return {
        "name": "Test Agent Framework",
        "url": "https://example.com/agent",
        "description": "A test agent framework for unit testing purposes.",
        "category": "open-source-frameworks",
        "type": "framework",
        "tags": ["testing", "automation"],
        "featured": False,
        "verified": True,
    }


# =============================================================================
# Fixtures - T006: Valid YAML category entry
# =============================================================================


@pytest.fixture
def valid_category_yaml() -> dict[str, Any]:
    """Return valid category entry data matching Category schema."""
    return {
        "id": "open-source-frameworks",
        "title": "Open Source Frameworks",
        "description": "A collection of open source agent frameworks.",
        "emoji": "tools",
        "order": 1,
        "show_github_stats": True,
        "table_columns": ["name", "description", "tags"],
    }


# =============================================================================
# Fixtures - T007: Valid YAML boilerplate entry
# =============================================================================


@pytest.fixture
def valid_boilerplate_yaml() -> dict[str, Any]:
    """Return valid boilerplate entry data matching BoilerplateEntry schema."""
    return {
        "name": "Test Boilerplate",
        "url": "https://example.com/boilerplate",
        "description": "A test boilerplate for unit testing purposes.",
        "category": "nextjs",
        "ecosystem": "nextjs",
        "tags": ["testing", "nextjs"],
        "featured": False,
        "verified": True,
    }


# =============================================================================
# Helper Functions - T008: Create temporary YAML files
# =============================================================================


def create_yaml_file(path: Path, data: dict[str, Any]) -> Path:
    """Create a YAML file with the given data at the specified path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False)
    return path


def create_empty_yaml_file(path: Path) -> Path:
    """Create an empty YAML file at the specified path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()
    return path


def create_yaml_file_with_content(path: Path, content: str) -> Path:
    """Create a YAML file with raw string content."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


# =============================================================================
# Tests - T009: get_file_kind()
# =============================================================================


class TestGetFileKind:
    """Tests for get_file_kind() function."""

    def test_agent_file(self, tmp_data_dir: Path) -> None:
        """Files in data/agents/ return 'agent'."""
        filepath = tmp_data_dir / "agents" / "open-source-frameworks" / "test.yml"
        filepath.touch()
        assert get_file_kind(filepath, tmp_data_dir) == "agent"

    def test_category_file(self, tmp_data_dir: Path) -> None:
        """Files in data/categories/ return 'category'."""
        filepath = tmp_data_dir / "categories" / "test.yml"
        filepath.touch()
        assert get_file_kind(filepath, tmp_data_dir) == "category"

    def test_boilerplate_file(self, tmp_data_dir: Path) -> None:
        """Files in data/boilerplates/ return 'boilerplate'."""
        filepath = tmp_data_dir / "boilerplates" / "nextjs" / "test.yml"
        filepath.touch()
        assert get_file_kind(filepath, tmp_data_dir) == "boilerplate"

    def test_boilerplate_category_file(self, tmp_data_dir: Path) -> None:
        """Files in data/boilerplate-categories/ return 'boilerplate-category'."""
        filepath = tmp_data_dir / "boilerplate-categories" / "test.yml"
        filepath.touch()
        assert get_file_kind(filepath, tmp_data_dir) == "boilerplate-category"

    def test_outside_data_dir(self, tmp_path: Path) -> None:
        """Files outside data/ directory return None."""
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        filepath = tmp_path / "outside" / "test.yml"
        filepath.parent.mkdir(parents=True)
        filepath.touch()
        assert get_file_kind(filepath, data_dir) is None

    def test_unknown_subdirectory(self, tmp_data_dir: Path) -> None:
        """Files in unknown subdirectory return None."""
        unknown_dir = tmp_data_dir / "unknown"
        unknown_dir.mkdir()
        filepath = unknown_dir / "test.yml"
        filepath.touch()
        assert get_file_kind(filepath, tmp_data_dir) is None


# =============================================================================
# Tests - T010: is_yaml_file()
# =============================================================================


class TestIsYamlFile:
    """Tests for is_yaml_file() function."""

    def test_yml_extension(self, tmp_path: Path) -> None:
        """Files with .yml extension return True."""
        filepath = tmp_path / "test.yml"
        filepath.touch()
        assert is_yaml_file(filepath) is True

    def test_yaml_extension(self, tmp_path: Path) -> None:
        """Files with .yaml extension return True."""
        filepath = tmp_path / "test.yaml"
        filepath.touch()
        assert is_yaml_file(filepath) is True

    def test_json_extension(self, tmp_path: Path) -> None:
        """Files with .json extension return False."""
        filepath = tmp_path / "test.json"
        assert is_yaml_file(filepath) is False

    def test_txt_extension(self, tmp_path: Path) -> None:
        """Files with .txt extension return False."""
        filepath = tmp_path / "test.txt"
        assert is_yaml_file(filepath) is False

    def test_no_extension(self, tmp_path: Path) -> None:
        """Files without extension return False."""
        filepath = tmp_path / "test"
        assert is_yaml_file(filepath) is False

    def test_yml_in_name_wrong_extension(self, tmp_path: Path) -> None:
        """Files with yml in name but wrong extension return False."""
        filepath = tmp_path / "test.yml.bak"
        assert is_yaml_file(filepath) is False


# =============================================================================
# Tests - T011: build_include_map()
# =============================================================================


class TestBuildIncludeMap:
    """Tests for build_include_map() function."""

    def test_no_flags_includes_all(self) -> None:
        """When no flags are set, all types are included."""
        args = argparse.Namespace(
            agents=False,
            categories=False,
            boilerplates=False,
            boilerplate_categories=False,
        )
        result = build_include_map(args)
        assert result == {
            "agent": True,
            "category": True,
            "boilerplate": True,
            "boilerplate-category": True,
        }

    def test_agents_only(self) -> None:
        """When --agents flag is set, only agents are included."""
        args = argparse.Namespace(
            agents=True,
            categories=False,
            boilerplates=False,
            boilerplate_categories=False,
        )
        result = build_include_map(args)
        assert result == {
            "agent": True,
            "category": False,
            "boilerplate": False,
            "boilerplate-category": False,
        }

    def test_categories_only(self) -> None:
        """When --categories flag is set, only categories are included."""
        args = argparse.Namespace(
            agents=False,
            categories=True,
            boilerplates=False,
            boilerplate_categories=False,
        )
        result = build_include_map(args)
        assert result["category"] is True
        assert result["agent"] is False

    def test_multiple_flags(self) -> None:
        """Multiple flags can be combined."""
        args = argparse.Namespace(
            agents=True,
            categories=True,
            boilerplates=False,
            boilerplate_categories=False,
        )
        result = build_include_map(args)
        assert result["agent"] is True
        assert result["category"] is True
        assert result["boilerplate"] is False

    def test_boilerplates_only(self) -> None:
        """When --boilerplates flag is set, only boilerplates are included."""
        args = argparse.Namespace(
            agents=False,
            categories=False,
            boilerplates=True,
            boilerplate_categories=False,
        )
        result = build_include_map(args)
        assert result["boilerplate"] is True
        assert result["agent"] is False


# =============================================================================
# Tests - T012: collect_files()
# =============================================================================


class TestCollectFiles:
    """Tests for collect_files() function."""

    def test_default_collects_all(
        self, tmp_data_dir: Path, valid_agent_yaml: dict, valid_category_yaml: dict
    ) -> None:
        """With no paths, collects all matching files."""
        # Create test files
        create_yaml_file(
            tmp_data_dir / "agents" / "open-source-frameworks" / "test.yml",
            valid_agent_yaml,
        )
        create_yaml_file(
            tmp_data_dir / "categories" / "test.yml",
            valid_category_yaml,
        )

        include = {
            "agent": True,
            "category": True,
            "boilerplate": True,
            "boilerplate-category": True,
        }
        files, errors = collect_files([], tmp_data_dir, include)

        assert len(files["agent"]) == 1
        assert len(files["category"]) == 1
        assert len(errors) == 0

    def test_path_filtering(
        self, tmp_data_dir: Path, valid_agent_yaml: dict
    ) -> None:
        """Path argument filters to specific directory."""
        # Create files in different directories
        create_yaml_file(
            tmp_data_dir / "agents" / "open-source-frameworks" / "test1.yml",
            valid_agent_yaml,
        )
        create_yaml_file(
            tmp_data_dir / "agents" / "specialized-tools" / "test2.yml",
            valid_agent_yaml,
        )

        include = {
            "agent": True,
            "category": True,
            "boilerplate": True,
            "boilerplate-category": True,
        }
        target_path = str(tmp_data_dir / "agents" / "open-source-frameworks")
        files, errors = collect_files([target_path], tmp_data_dir, include)

        assert len(files["agent"]) == 1
        assert files["agent"][0].name == "test1.yml"

    def test_nonexistent_path_error(self, tmp_data_dir: Path) -> None:
        """Nonexistent paths generate errors."""
        include = {"agent": True, "category": True, "boilerplate": True, "boilerplate-category": True}
        files, errors = collect_files(["/nonexistent/path"], tmp_data_dir, include)

        assert len(errors) == 1
        assert "Path not found" in errors[0]

    def test_explicit_file_outside_data_error(self, tmp_path: Path) -> None:
        """Explicit file outside data directory generates error."""
        data_dir = tmp_path / "data"
        data_dir.mkdir()

        outside_file = tmp_path / "outside.yml"
        create_yaml_file(outside_file, {"test": "data"})

        include = {"agent": True, "category": True, "boilerplate": True, "boilerplate-category": True}
        files, errors = collect_files([str(outside_file)], data_dir, include)

        assert len(errors) == 1
        assert "outside data directory" in errors[0]

    def test_respects_include_filter(
        self, tmp_data_dir: Path, valid_agent_yaml: dict, valid_category_yaml: dict
    ) -> None:
        """Respects include filter to only collect specified types."""
        create_yaml_file(
            tmp_data_dir / "agents" / "open-source-frameworks" / "test.yml",
            valid_agent_yaml,
        )
        create_yaml_file(
            tmp_data_dir / "categories" / "test.yml",
            valid_category_yaml,
        )

        include = {
            "agent": True,
            "category": False,
            "boilerplate": False,
            "boilerplate-category": False,
        }
        files, errors = collect_files([], tmp_data_dir, include)

        assert len(files["agent"]) == 1
        assert len(files["category"]) == 0

    def test_ignores_gitkeep(self, tmp_data_dir: Path) -> None:
        """Ignores .gitkeep files."""
        gitkeep = tmp_data_dir / "agents" / "open-source-frameworks" / ".gitkeep"
        gitkeep.touch()

        include = {"agent": True, "category": True, "boilerplate": True, "boilerplate-category": True}
        files, errors = collect_files([], tmp_data_dir, include)

        assert len(files["agent"]) == 0


# =============================================================================
# Tests - T013: load_yaml_data()
# =============================================================================


class TestLoadYamlData:
    """Tests for load_yaml_data() function."""

    def test_valid_yaml(self, tmp_path: Path) -> None:
        """Valid YAML files are loaded correctly."""
        data = {"name": "test", "value": 123}
        filepath = create_yaml_file(tmp_path / "test.yml", data)

        result = load_yaml_data(filepath)
        assert result == data

    def test_empty_file_raises(self, tmp_path: Path) -> None:
        """Empty YAML files raise ValueError."""
        filepath = create_empty_yaml_file(tmp_path / "empty.yml")

        with pytest.raises(ValueError, match="Empty YAML file"):
            load_yaml_data(filepath)

    def test_comments_only_raises(self, tmp_path: Path) -> None:
        """YAML files with only comments raise ValueError."""
        filepath = create_yaml_file_with_content(
            tmp_path / "comments.yml",
            "# This is a comment\n# Another comment\n"
        )

        with pytest.raises(ValueError, match="Empty YAML file"):
            load_yaml_data(filepath)

    def test_non_dict_yaml_raises(self, tmp_path: Path) -> None:
        """YAML files with non-dict content raise ValueError."""
        filepath = create_yaml_file_with_content(
            tmp_path / "list.yml",
            "- item1\n- item2\n"
        )

        with pytest.raises(ValueError, match="YAML content must be a mapping"):
            load_yaml_data(filepath)

    def test_scalar_yaml_raises(self, tmp_path: Path) -> None:
        """YAML files with scalar content raise ValueError."""
        filepath = create_yaml_file_with_content(
            tmp_path / "scalar.yml",
            "just a string"
        )

        with pytest.raises(ValueError, match="YAML content must be a mapping"):
            load_yaml_data(filepath)


# =============================================================================
# Tests - T014: load_category_ids()
# =============================================================================


class TestLoadCategoryIds:
    """Tests for load_category_ids() function."""

    def test_valid_directory(self, tmp_data_dir: Path) -> None:
        """Loads category IDs from valid directory."""
        create_yaml_file(
            tmp_data_dir / "categories" / "cat1.yml",
            {"id": "category-one", "title": "Category One", "description": "First category."}
        )
        create_yaml_file(
            tmp_data_dir / "categories" / "cat2.yml",
            {"id": "category-two", "title": "Category Two", "description": "Second category."}
        )

        ids = load_category_ids(tmp_data_dir / "categories")

        assert ids == {"category-one", "category-two"}

    def test_missing_directory_returns_empty(self, tmp_path: Path) -> None:
        """Missing directory returns empty set."""
        ids = load_category_ids(tmp_path / "nonexistent")
        assert ids == set()

    def test_ignores_missing_id_field(self, tmp_data_dir: Path) -> None:
        """Files without id field are skipped gracefully."""
        create_yaml_file(
            tmp_data_dir / "categories" / "valid.yml",
            {"id": "valid-category", "title": "Valid", "description": "Valid category."}
        )
        create_yaml_file(
            tmp_data_dir / "categories" / "invalid.yml",
            {"title": "No ID", "description": "Missing id field."}
        )

        ids = load_category_ids(tmp_data_dir / "categories")

        assert ids == {"valid-category"}

    def test_ignores_gitkeep(self, tmp_data_dir: Path) -> None:
        """Ignores .gitkeep files."""
        (tmp_data_dir / "categories" / ".gitkeep").touch()
        create_yaml_file(
            tmp_data_dir / "categories" / "valid.yml",
            {"id": "valid-category", "title": "Valid", "description": "Valid category."}
        )

        ids = load_category_ids(tmp_data_dir / "categories")

        assert ids == {"valid-category"}

    def test_handles_invalid_yaml_gracefully(self, tmp_data_dir: Path) -> None:
        """Invalid YAML files are skipped without crashing."""
        create_yaml_file(
            tmp_data_dir / "categories" / "valid.yml",
            {"id": "valid-category", "title": "Valid", "description": "Valid category."}
        )
        create_yaml_file_with_content(
            tmp_data_dir / "categories" / "invalid.yml",
            "invalid: yaml: content:"
        )

        ids = load_category_ids(tmp_data_dir / "categories")

        # Should still load the valid one
        assert "valid-category" in ids


# =============================================================================
# Tests - T015: check_category_references()
# =============================================================================


class TestCheckCategoryReferences:
    """Tests for check_category_references() function."""

    def test_valid_references(self, tmp_path: Path) -> None:
        """Valid category references produce no errors."""
        entries = [
            ValidatedEntry(
                filepath=tmp_path / "agent1.yml",
                data={"name": "Agent1", "category": "valid-category"},
                kind="agent"
            ),
            ValidatedEntry(
                filepath=tmp_path / "agent2.yml",
                data={"name": "Agent2", "category": "another-category"},
                kind="agent"
            ),
        ]
        valid_ids = {"valid-category", "another-category"}

        errors = check_category_references(entries, valid_ids, "agent")

        assert len(errors) == 0

    def test_invalid_reference(self, tmp_path: Path) -> None:
        """Invalid category references produce errors."""
        entries = [
            ValidatedEntry(
                filepath=tmp_path / "agent1.yml",
                data={"name": "Agent1", "category": "nonexistent-category"},
                kind="agent"
            ),
        ]
        valid_ids = {"valid-category"}

        errors = check_category_references(entries, valid_ids, "agent")

        assert len(errors) == 1
        assert "Unknown agent category 'nonexistent-category'" in errors[0]

    def test_missing_category_field_no_error(self, tmp_path: Path) -> None:
        """Entries without category field produce no errors."""
        entries = [
            ValidatedEntry(
                filepath=tmp_path / "agent1.yml",
                data={"name": "Agent1"},
                kind="agent"
            ),
        ]
        valid_ids = {"valid-category"}

        errors = check_category_references(entries, valid_ids, "agent")

        assert len(errors) == 0

    def test_multiple_invalid_references(self, tmp_path: Path) -> None:
        """Multiple invalid references produce multiple errors."""
        entries = [
            ValidatedEntry(
                filepath=tmp_path / "agent1.yml",
                data={"name": "Agent1", "category": "bad-category-1"},
                kind="agent"
            ),
            ValidatedEntry(
                filepath=tmp_path / "agent2.yml",
                data={"name": "Agent2", "category": "bad-category-2"},
                kind="agent"
            ),
        ]
        valid_ids = {"valid-category"}

        errors = check_category_references(entries, valid_ids, "agent")

        assert len(errors) == 2


# =============================================================================
# Tests - T016: check_duplicates()
# =============================================================================


class TestCheckDuplicates:
    """Tests for check_duplicates() function."""

    def test_no_duplicates(self, tmp_path: Path) -> None:
        """No duplicates produces no errors."""
        entries = [
            ValidatedEntry(
                filepath=tmp_path / "agent1.yml",
                data={"url": "https://example.com/1"},
                kind="agent"
            ),
            ValidatedEntry(
                filepath=tmp_path / "agent2.yml",
                data={"url": "https://example.com/2"},
                kind="agent"
            ),
        ]

        errors = check_duplicates(entries, "url")

        assert len(errors) == 0

    def test_duplicate_urls(self, tmp_path: Path) -> None:
        """Duplicate URLs are detected."""
        entries = [
            ValidatedEntry(
                filepath=tmp_path / "agent1.yml",
                data={"url": "https://example.com/same"},
                kind="agent"
            ),
            ValidatedEntry(
                filepath=tmp_path / "agent2.yml",
                data={"url": "https://example.com/same"},
                kind="agent"
            ),
        ]

        errors = check_duplicates(entries, "url")

        assert len(errors) == 1
        assert "Duplicate url" in errors[0]
        assert "agent1.yml" in errors[0]
        assert "agent2.yml" in errors[0]

    def test_duplicate_github_repos(self, tmp_path: Path) -> None:
        """Duplicate github_repo values are detected."""
        entries = [
            ValidatedEntry(
                filepath=tmp_path / "agent1.yml",
                data={"github_repo": "owner/repo"},
                kind="agent"
            ),
            ValidatedEntry(
                filepath=tmp_path / "agent2.yml",
                data={"github_repo": "owner/repo"},
                kind="agent"
            ),
        ]

        errors = check_duplicates(entries, "github_repo")

        assert len(errors) == 1
        assert "Duplicate github_repo" in errors[0]

    def test_none_values_ignored(self, tmp_path: Path) -> None:
        """None values are ignored in duplicate detection."""
        entries = [
            ValidatedEntry(
                filepath=tmp_path / "agent1.yml",
                data={"github_repo": None},
                kind="agent"
            ),
            ValidatedEntry(
                filepath=tmp_path / "agent2.yml",
                data={"github_repo": None},
                kind="agent"
            ),
        ]

        errors = check_duplicates(entries, "github_repo")

        assert len(errors) == 0

    def test_missing_field_ignored(self, tmp_path: Path) -> None:
        """Entries without the field are ignored."""
        entries = [
            ValidatedEntry(
                filepath=tmp_path / "agent1.yml",
                data={"name": "Agent1"},
                kind="agent"
            ),
            ValidatedEntry(
                filepath=tmp_path / "agent2.yml",
                data={"name": "Agent2"},
                kind="agent"
            ),
        ]

        errors = check_duplicates(entries, "github_repo")

        assert len(errors) == 0

    def test_cross_kind_duplicates(self, tmp_path: Path) -> None:
        """Duplicates across different kinds are detected."""
        entries = [
            ValidatedEntry(
                filepath=tmp_path / "agent.yml",
                data={"url": "https://example.com/same"},
                kind="agent"
            ),
            ValidatedEntry(
                filepath=tmp_path / "boilerplate.yml",
                data={"url": "https://example.com/same"},
                kind="boilerplate"
            ),
        ]

        errors = check_duplicates(entries, "url")

        assert len(errors) == 1
        assert "(agent)" in errors[0]
        assert "(boilerplate)" in errors[0]

    def test_multiple_groups_of_duplicates(self, tmp_path: Path) -> None:
        """Multiple groups of duplicates each produce an error."""
        entries = [
            ValidatedEntry(
                filepath=tmp_path / "agent1.yml",
                data={"url": "https://example.com/a"},
                kind="agent"
            ),
            ValidatedEntry(
                filepath=tmp_path / "agent2.yml",
                data={"url": "https://example.com/a"},
                kind="agent"
            ),
            ValidatedEntry(
                filepath=tmp_path / "agent3.yml",
                data={"url": "https://example.com/b"},
                kind="agent"
            ),
            ValidatedEntry(
                filepath=tmp_path / "agent4.yml",
                data={"url": "https://example.com/b"},
                kind="agent"
            ),
        ]

        errors = check_duplicates(entries, "url")

        assert len(errors) == 2


# =============================================================================
# Tests - T017: normalize_url()
# =============================================================================


class TestNormalizeUrl:
    """Tests for normalize_url() function."""

    def test_trailing_slash_removed(self) -> None:
        """Trailing slashes are removed from paths."""
        assert normalize_url("https://example.com/path/") == "https://example.com/path"

    def test_root_slash_preserved(self) -> None:
        """Root path slash is preserved."""
        assert normalize_url("https://example.com/") == "https://example.com/"

    def test_no_trailing_slash_unchanged(self) -> None:
        """URLs without trailing slash are unchanged."""
        assert normalize_url("https://example.com/path") == "https://example.com/path"

    def test_host_lowercase(self) -> None:
        """Host is normalized to lowercase."""
        assert normalize_url("https://EXAMPLE.COM/path") == "https://example.com/path"

    def test_http_to_https(self) -> None:
        """HTTP URLs are normalized to HTTPS."""
        assert normalize_url("http://example.com/path") == "https://example.com/path"

    def test_https_unchanged(self) -> None:
        """HTTPS URLs remain HTTPS."""
        assert normalize_url("https://example.com/path") == "https://example.com/path"

    def test_combined_normalization(self) -> None:
        """Multiple normalizations are applied together."""
        result = normalize_url("http://EXAMPLE.COM/path/")
        assert result == "https://example.com/path"

    def test_query_params_preserved(self) -> None:
        """Query parameters are preserved."""
        result = normalize_url("https://example.com/path?foo=bar")
        assert result == "https://example.com/path?foo=bar"

    def test_fragment_removed(self) -> None:
        """URL fragments are removed."""
        result = normalize_url("https://example.com/path#section")
        assert result == "https://example.com/path"

    def test_complex_path_preserved(self) -> None:
        """Complex paths are preserved correctly."""
        result = normalize_url("https://example.com/a/b/c/file.html")
        assert result == "https://example.com/a/b/c/file.html"

    def test_invalid_url_returned_unchanged(self) -> None:
        """Invalid URLs are returned unchanged."""
        # Empty string
        assert normalize_url("") == ""
        # Just a path
        result = normalize_url("not-a-url")
        assert result is not None  # Should not crash


class TestCheckDuplicatesWithNormalization:
    """Tests for check_duplicates() with URL normalization."""

    def test_detects_trailing_slash_duplicates(self, tmp_path: Path) -> None:
        """Detects URLs that differ only by trailing slash."""
        entries = [
            ValidatedEntry(
                filepath=tmp_path / "agent1.yml",
                data={"url": "https://example.com/path"},
                kind="agent"
            ),
            ValidatedEntry(
                filepath=tmp_path / "agent2.yml",
                data={"url": "https://example.com/path/"},
                kind="agent"
            ),
        ]

        errors = check_duplicates(entries, "url", normalize=True)

        assert len(errors) == 1
        assert "Duplicate url" in errors[0]

    def test_detects_case_duplicates(self, tmp_path: Path) -> None:
        """Detects URLs that differ only by host case."""
        entries = [
            ValidatedEntry(
                filepath=tmp_path / "agent1.yml",
                data={"url": "https://example.com/path"},
                kind="agent"
            ),
            ValidatedEntry(
                filepath=tmp_path / "agent2.yml",
                data={"url": "https://EXAMPLE.COM/path"},
                kind="agent"
            ),
        ]

        errors = check_duplicates(entries, "url", normalize=True)

        assert len(errors) == 1

    def test_detects_http_https_duplicates(self, tmp_path: Path) -> None:
        """Detects URLs that differ only by http vs https."""
        entries = [
            ValidatedEntry(
                filepath=tmp_path / "agent1.yml",
                data={"url": "https://example.com/path"},
                kind="agent"
            ),
            ValidatedEntry(
                filepath=tmp_path / "agent2.yml",
                data={"url": "http://example.com/path"},
                kind="agent"
            ),
        ]

        errors = check_duplicates(entries, "url", normalize=True)

        assert len(errors) == 1

    def test_no_normalization_for_non_url_fields(self, tmp_path: Path) -> None:
        """Normalization is not applied to non-url fields."""
        entries = [
            ValidatedEntry(
                filepath=tmp_path / "agent1.yml",
                data={"github_repo": "owner/repo"},
                kind="agent"
            ),
            ValidatedEntry(
                filepath=tmp_path / "agent2.yml",
                data={"github_repo": "OWNER/REPO"},
                kind="agent"
            ),
        ]

        # These should NOT be treated as duplicates (case matters for github_repo)
        errors = check_duplicates(entries, "github_repo", normalize=True)

        assert len(errors) == 0

    def test_normalize_false_disables_normalization(self, tmp_path: Path) -> None:
        """normalize=False disables URL normalization."""
        entries = [
            ValidatedEntry(
                filepath=tmp_path / "agent1.yml",
                data={"url": "https://example.com/path"},
                kind="agent"
            ),
            ValidatedEntry(
                filepath=tmp_path / "agent2.yml",
                data={"url": "https://example.com/path/"},
                kind="agent"
            ),
        ]

        errors = check_duplicates(entries, "url", normalize=False)

        # Without normalization, these are different URLs
        assert len(errors) == 0


# =============================================================================
# Tests: validate_yaml_file()
# =============================================================================


class TestValidateYamlFile:
    """Tests for validate_yaml_file() function."""

    def test_valid_agent_entry(self, tmp_path: Path, valid_agent_yaml: dict) -> None:
        """Valid agent YAML passes validation."""
        filepath = create_yaml_file(tmp_path / "agent.yml", valid_agent_yaml)

        success, message, data = validate_yaml_file(filepath, AgentEntry)

        assert success is True
        assert "OK" in message
        assert data == valid_agent_yaml

    def test_valid_category_entry(self, tmp_path: Path, valid_category_yaml: dict) -> None:
        """Valid category YAML passes validation."""
        filepath = create_yaml_file(tmp_path / "category.yml", valid_category_yaml)

        success, message, data = validate_yaml_file(filepath, Category)

        assert success is True
        assert "OK" in message

    def test_invalid_agent_entry(self, tmp_path: Path) -> None:
        """Invalid agent YAML fails validation."""
        invalid_data = {
            "name": "Test",
            # Missing required fields: url, description, category
        }
        filepath = create_yaml_file(tmp_path / "invalid.yml", invalid_data)

        success, message, data = validate_yaml_file(filepath, AgentEntry)

        assert success is False
        assert "ERROR" in message
        assert "Validation error" in message
        assert data is None

    def test_empty_file(self, tmp_path: Path) -> None:
        """Empty YAML file fails validation."""
        filepath = create_empty_yaml_file(tmp_path / "empty.yml")

        success, message, data = validate_yaml_file(filepath, AgentEntry)

        assert success is False
        assert "ERROR" in message
        assert data is None

    def test_yaml_syntax_error(self, tmp_path: Path) -> None:
        """YAML with syntax errors fails validation."""
        filepath = create_yaml_file_with_content(
            tmp_path / "syntax_error.yml",
            "invalid: yaml: : content"
        )

        success, message, data = validate_yaml_file(filepath, AgentEntry)

        assert success is False
        assert "ERROR" in message
        assert data is None

    def test_non_dict_yaml(self, tmp_path: Path) -> None:
        """Non-dict YAML fails validation."""
        filepath = create_yaml_file_with_content(
            tmp_path / "list.yml",
            "- item1\n- item2"
        )

        success, message, data = validate_yaml_file(filepath, AgentEntry)

        assert success is False
        assert "ERROR" in message
        assert data is None


# =============================================================================
# Additional coverage tests
# =============================================================================


class TestCollectFilesAdditional:
    """Additional tests for collect_files() edge cases."""

    def test_yaml_extension_files(
        self, tmp_data_dir: Path, valid_agent_yaml: dict
    ) -> None:
        """Files with .yaml extension are also collected."""
        create_yaml_file(
            tmp_data_dir / "agents" / "open-source-frameworks" / "test.yaml",
            valid_agent_yaml,
        )

        include = {
            "agent": True,
            "category": True,
            "boilerplate": True,
            "boilerplate-category": True,
        }
        target_path = str(tmp_data_dir / "agents")
        files, errors = collect_files([target_path], tmp_data_dir, include)

        assert len(files["agent"]) == 1
        assert files["agent"][0].suffix == ".yaml"

    def test_directory_path_with_yaml_extension(
        self, tmp_data_dir: Path, valid_agent_yaml: dict
    ) -> None:
        """Directory scanning finds both .yml and .yaml files."""
        create_yaml_file(
            tmp_data_dir / "agents" / "open-source-frameworks" / "test1.yml",
            valid_agent_yaml,
        )
        create_yaml_file(
            tmp_data_dir / "agents" / "open-source-frameworks" / "test2.yaml",
            valid_agent_yaml,
        )

        include = {
            "agent": True,
            "category": True,
            "boilerplate": True,
            "boilerplate-category": True,
        }
        target_path = str(tmp_data_dir / "agents" / "open-source-frameworks")
        files, errors = collect_files([target_path], tmp_data_dir, include)

        assert len(files["agent"]) == 2

    def test_exclude_by_include_filter(
        self, tmp_data_dir: Path, valid_agent_yaml: dict
    ) -> None:
        """Files are excluded when their type is not in include filter."""
        create_yaml_file(
            tmp_data_dir / "agents" / "open-source-frameworks" / "test.yml",
            valid_agent_yaml,
        )

        include = {
            "agent": False,
            "category": False,
            "boilerplate": True,
            "boilerplate-category": False,
        }
        target_path = str(tmp_data_dir / "agents")
        files, errors = collect_files([target_path], tmp_data_dir, include)

        assert len(files["agent"]) == 0


class TestNormalizeUrlAdditional:
    """Additional tests for normalize_url() edge cases."""

    def test_non_http_scheme_preserved(self) -> None:
        """Non-HTTP schemes are preserved."""
        result = normalize_url("ftp://example.com/file")
        assert result.startswith("ftp://")

    def test_empty_path(self) -> None:
        """URLs without path work correctly."""
        result = normalize_url("https://example.com")
        assert result == "https://example.com"

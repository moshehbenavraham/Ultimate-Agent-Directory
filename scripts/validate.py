#!/usr/bin/env python3
"""
Validation script for Ultimate Agent Directory
Validates YAML files against Pydantic schemas.

Usage:
    python scripts/validate.py
    python scripts/validate.py data/agents/open-source-frameworks/example.yml
    python scripts/validate.py data/agents --agents
    python scripts/validate.py --agents --categories
    python scripts/validate.py --boilerplates --boilerplate-categories
"""

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse, urlunparse

import yaml

from models import AgentEntry, Category, BoilerplateEntry, BoilerplateCategory


@dataclass
class ValidatedEntry:
    filepath: Path
    data: dict
    kind: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate YAML files against Pydantic schemas."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Optional files or directories to validate",
    )
    parser.add_argument("--agents", action="store_true", help="Validate agent entries")
    parser.add_argument(
        "--categories", action="store_true", help="Validate agent categories"
    )
    parser.add_argument(
        "--boilerplates", action="store_true", help="Validate boilerplate entries"
    )
    parser.add_argument(
        "--boilerplate-categories",
        action="store_true",
        help="Validate boilerplate categories",
    )
    return parser.parse_args()


def build_include_map(args: argparse.Namespace) -> dict[str, bool]:
    flags = {
        "agent": args.agents,
        "category": args.categories,
        "boilerplate": args.boilerplates,
        "boilerplate-category": args.boilerplate_categories,
    }
    if any(flags.values()):
        return flags
    return {key: True for key in flags}


def is_yaml_file(filepath: Path) -> bool:
    return filepath.suffix in {".yml", ".yaml"}


def get_file_kind(filepath: Path, data_dir: Path) -> str | None:
    try:
        relative = filepath.resolve().relative_to(data_dir.resolve())
    except ValueError:
        return None
    parts = relative.parts
    if not parts:
        return None
    root = parts[0]
    if root == "agents":
        return "agent"
    if root == "categories":
        return "category"
    if root == "boilerplates":
        return "boilerplate"
    if root == "boilerplate-categories":
        return "boilerplate-category"
    return None


def collect_files(
    paths: Iterable[str], data_dir: Path, include: dict[str, bool]
) -> tuple[dict[str, list[Path]], list[str]]:
    collected = {
        "agent": [],
        "category": [],
        "boilerplate": [],
        "boilerplate-category": [],
    }
    errors: list[str] = []

    def add_file(file_path: Path, is_explicit: bool) -> None:
        if file_path.name == ".gitkeep" or not is_yaml_file(file_path):
            return
        kind = get_file_kind(file_path, data_dir)
        if kind is None:
            if is_explicit:
                errors.append(f"ERROR Path outside data directory: {file_path}")
            return
        if not include.get(kind, False):
            return
        collected[kind].append(file_path)

    if not paths:
        if include["agent"]:
            collected["agent"] = list(data_dir.glob("agents/**/*.yml"))
        if include["category"]:
            collected["category"] = list(data_dir.glob("categories/*.yml"))
        if include["boilerplate"]:
            collected["boilerplate"] = list(data_dir.glob("boilerplates/**/*.yml"))
        if include["boilerplate-category"]:
            collected["boilerplate-category"] = list(
                data_dir.glob("boilerplate-categories/*.yml")
            )
    else:
        for raw_path in paths:
            path = Path(raw_path)
            if not path.exists():
                errors.append(f"ERROR Path not found: {path}")
                continue
            if path.is_dir():
                for file_path in path.rglob("*.yml"):
                    add_file(file_path, is_explicit=False)
                for file_path in path.rglob("*.yaml"):
                    add_file(file_path, is_explicit=False)
            else:
                add_file(path, is_explicit=True)

    for kind in collected:
        collected[kind] = sorted(set(collected[kind]))

    return collected, errors


def load_yaml_data(filepath: Path) -> dict:
    with open(filepath) as f:
        data = yaml.safe_load(f)
    if data is None:
        raise ValueError("Empty YAML file")
    if not isinstance(data, dict):
        raise ValueError("YAML content must be a mapping")
    return data


def validate_yaml_file(filepath: Path, model) -> tuple[bool, str, dict | None]:
    try:
        data = load_yaml_data(filepath)
    except yaml.YAMLError as e:
        return False, f"ERROR {filepath}: YAML syntax error: {e}", None
    except Exception as e:
        return False, f"ERROR {filepath}: {e}", None

    try:
        model(**data)
    except Exception as e:
        return False, f"ERROR {filepath}: Validation error: {e}", None

    return True, f"OK {filepath}", data


def load_category_ids(category_dir: Path) -> set[str]:
    ids: set[str] = set()
    if not category_dir.exists():
        return ids
    for filepath in category_dir.glob("*.yml"):
        if filepath.name == ".gitkeep":
            continue
        try:
            data = load_yaml_data(filepath)
            category_id = data.get("id")
            if category_id:
                ids.add(str(category_id))
        except Exception:
            continue
    return ids


def check_category_references(
    entries: list[ValidatedEntry], valid_ids: set[str], kind_label: str
) -> list[str]:
    errors: list[str] = []
    for entry in entries:
        category = entry.data.get("category")
        if category and category not in valid_ids:
            errors.append(
                f"ERROR {entry.filepath}: Unknown {kind_label} category '{category}'"
            )
    return errors


def normalize_url(url: str) -> str:
    """Normalize URL for duplicate detection.

    Normalizes:
    - Trailing slashes (removes from path)
    - Host case (lowercase)
    - Protocol (http -> https)
    """
    try:
        parsed = urlparse(url)
    except Exception:
        return url

    # Normalize scheme: http -> https
    scheme = "https" if parsed.scheme in ("http", "https") else parsed.scheme

    # Normalize host: lowercase
    netloc = parsed.netloc.lower() if parsed.netloc else ""

    # Normalize path: remove trailing slash (but keep root "/")
    path = parsed.path.rstrip("/") if parsed.path != "/" else parsed.path

    # Reconstruct URL
    normalized = urlunparse((
        scheme,
        netloc,
        path,
        parsed.params,
        parsed.query,
        "",  # Remove fragment
    ))

    return normalized


def check_duplicates(
    entries: list[ValidatedEntry], field: str, normalize: bool = True
) -> list[str]:
    """Check for duplicate values in a field across entries.

    Args:
        entries: List of validated entries to check
        field: Field name to check for duplicates
        normalize: Whether to normalize URLs (only applies to 'url' field)
    """
    errors: list[str] = []
    values: dict[str, list[ValidatedEntry]] = {}
    for entry in entries:
        value = entry.data.get(field)
        if not value:
            continue
        key = str(value)
        # Apply URL normalization for url field
        if normalize and field == "url":
            key = normalize_url(key)
        values.setdefault(key, []).append(entry)

    for value, matched in sorted(values.items()):
        if len(matched) > 1:
            lines = [f"ERROR Duplicate {field} '{value}' found in:"]
            for item in matched:
                lines.append(f"  - {item.filepath} ({item.kind})")
            errors.append("\n".join(lines))

    return errors


def main() -> None:
    data_dir = Path("data")
    if not data_dir.exists():
        print("ERROR: data/ directory not found")
        sys.exit(1)

    args = parse_args()
    include = build_include_map(args)
    files_by_type, path_errors = collect_files(args.paths, data_dir, include)

    errors: list[str] = list(path_errors)
    successes: list[str] = []
    agent_entries: list[ValidatedEntry] = []
    boilerplate_entries: list[ValidatedEntry] = []

    total_files = sum(len(files_by_type[key]) for key in files_by_type)
    if total_files == 0:
        if errors:
            print("\n".join(errors))
            sys.exit(1)
        print("WARNING: No YAML files found to validate")
        sys.exit(0)

    print(
        "Validating "
        f"{len(files_by_type['agent'])} agent files, "
        f"{len(files_by_type['category'])} category files, "
        f"{len(files_by_type['boilerplate'])} boilerplate files, "
        f"{len(files_by_type['boilerplate-category'])} boilerplate category files..."
    )

    for filepath in files_by_type["agent"]:
        success, message, data = validate_yaml_file(filepath, AgentEntry)
        if success:
            successes.append(message)
            if data:
                agent_entries.append(
                    ValidatedEntry(filepath=filepath, data=data, kind="agent")
                )
        else:
            errors.append(message)

    for filepath in files_by_type["category"]:
        success, message, _ = validate_yaml_file(filepath, Category)
        if success:
            successes.append(message)
        else:
            errors.append(message)

    for filepath in files_by_type["boilerplate"]:
        success, message, data = validate_yaml_file(filepath, BoilerplateEntry)
        if success:
            successes.append(message)
            if data:
                boilerplate_entries.append(
                    ValidatedEntry(filepath=filepath, data=data, kind="boilerplate")
                )
        else:
            errors.append(message)

    for filepath in files_by_type["boilerplate-category"]:
        success, message, _ = validate_yaml_file(filepath, BoilerplateCategory)
        if success:
            successes.append(message)
        else:
            errors.append(message)

    if include["agent"]:
        valid_agent_categories = load_category_ids(data_dir / "categories")
        errors.extend(
            check_category_references(agent_entries, valid_agent_categories, "agent")
        )

    if include["boilerplate"]:
        valid_boilerplate_categories = load_category_ids(
            data_dir / "boilerplate-categories"
        )
        errors.extend(
            check_category_references(
                boilerplate_entries, valid_boilerplate_categories, "boilerplate"
            )
        )

    combined_entries: list[ValidatedEntry] = []
    if include["agent"]:
        combined_entries.extend(agent_entries)
    if include["boilerplate"]:
        combined_entries.extend(boilerplate_entries)

    if combined_entries:
        errors.extend(check_duplicates(combined_entries, "url"))
        errors.extend(check_duplicates(combined_entries, "github_repo"))

    if successes:
        print("\n".join(successes))

    if errors:
        print("\n" + "=" * 60)
        print("VALIDATION ERRORS:")
        print("=" * 60)
        print("\n".join(errors))
        print(f"\n{len(errors)} error(s) found")
        sys.exit(1)

    print(f"\nOK: All {len(successes)} files passed validation")


if __name__ == "__main__":
    main()

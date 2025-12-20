#!/usr/bin/env python3
"""
Validation script for Ultimate Agent Directory
Validates all YAML files against Pydantic schemas

Usage:
    python scripts/validate.py                  # Validate all
    python scripts/validate.py data/agents/...  # Validate specific file
"""

import sys
from pathlib import Path
from typing import Tuple
import yaml
from models import AgentEntry, Category, BoilerplateEntry, BoilerplateCategory


def validate_agent_file(filepath: Path) -> Tuple[bool, str]:
    """Validate a single agent YAML file"""
    try:
        with open(filepath) as f:
            data = yaml.safe_load(f)

        # Validate against schema
        AgentEntry(**data)
        return True, f"✓ {filepath}"

    except yaml.YAMLError as e:
        return False, f"✗ {filepath}: YAML syntax error\n  {e}"

    except Exception as e:
        return False, f"✗ {filepath}: Validation error\n  {e}"


def validate_category_file(filepath: Path) -> Tuple[bool, str]:
    """Validate a single category YAML file"""
    try:
        with open(filepath) as f:
            data = yaml.safe_load(f)

        Category(**data)
        return True, f"✓ {filepath}"

    except Exception as e:
        return False, f"✗ {filepath}: {e}"


def validate_boilerplate_file(filepath: Path) -> Tuple[bool, str]:
    """Validate a single boilerplate YAML file"""
    try:
        with open(filepath) as f:
            data = yaml.safe_load(f)

        BoilerplateEntry(**data)
        return True, f"✓ {filepath}"

    except yaml.YAMLError as e:
        return False, f"✗ {filepath}: YAML syntax error\n  {e}"

    except Exception as e:
        return False, f"✗ {filepath}: Validation error\n  {e}"


def validate_boilerplate_category_file(filepath: Path) -> Tuple[bool, str]:
    """Validate a single boilerplate category YAML file"""
    try:
        with open(filepath) as f:
            data = yaml.safe_load(f)

        BoilerplateCategory(**data)
        return True, f"✓ {filepath}"

    except Exception as e:
        return False, f"✗ {filepath}: {e}"


def load_boilerplates(data_dir: Path) -> list:
    """Load all boilerplate entries from YAML files"""
    boilerplates = []
    boilerplate_files = list(data_dir.glob("boilerplates/**/*.yml"))

    for filepath in boilerplate_files:
        if filepath.name == ".gitkeep":
            continue
        try:
            with open(filepath) as f:
                data = yaml.safe_load(f)
            if data:
                boilerplates.append(BoilerplateEntry(**data))
        except Exception:
            pass  # Validation errors handled separately

    return boilerplates


def load_boilerplate_categories(data_dir: Path) -> list:
    """Load all boilerplate category definitions from YAML files"""
    categories = []
    category_files = list(data_dir.glob("boilerplate-categories/*.yml"))

    for filepath in category_files:
        if filepath.name == ".gitkeep":
            continue
        try:
            with open(filepath) as f:
                data = yaml.safe_load(f)
            if data:
                categories.append(BoilerplateCategory(**data))
        except Exception:
            pass  # Validation errors handled separately

    return categories


def main():
    """Run validation on all YAML files"""

    data_dir = Path("data")

    if not data_dir.exists():
        print("ERROR: data/ directory not found")
        sys.exit(1)

    # Collect all files to validate
    agent_files = list(data_dir.glob("agents/**/*.yml"))
    category_files = list(data_dir.glob("categories/*.yml"))

    # Collect boilerplate files (excluding .gitkeep)
    boilerplate_files = [
        f for f in data_dir.glob("boilerplates/**/*.yml")
        if f.name != ".gitkeep"
    ]
    boilerplate_category_files = [
        f for f in data_dir.glob("boilerplate-categories/*.yml")
        if f.name != ".gitkeep"
    ]

    total_files = (
        len(agent_files)
        + len(category_files)
        + len(boilerplate_files)
        + len(boilerplate_category_files)
    )

    if total_files == 0:
        print("WARNING: No YAML files found to validate")
        sys.exit(0)

    print(f"Validating {len(agent_files)} agent files, {len(category_files)} category files,")
    print(f"           {len(boilerplate_files)} boilerplate files, {len(boilerplate_category_files)} boilerplate category files...\n")

    errors = []
    successes = []

    # Validate agents
    for filepath in agent_files:
        success, message = validate_agent_file(filepath)
        if success:
            successes.append(message)
        else:
            errors.append(message)

    # Validate categories
    for filepath in category_files:
        success, message = validate_category_file(filepath)
        if success:
            successes.append(message)
        else:
            errors.append(message)

    # Validate boilerplates
    for filepath in boilerplate_files:
        success, message = validate_boilerplate_file(filepath)
        if success:
            successes.append(message)
        else:
            errors.append(message)

    # Validate boilerplate categories
    for filepath in boilerplate_category_files:
        success, message = validate_boilerplate_category_file(filepath)
        if success:
            successes.append(message)
        else:
            errors.append(message)

    # Print results
    if successes:
        print("\n".join(successes))

    if errors:
        print("\n" + "=" * 60)
        print("VALIDATION ERRORS:")
        print("=" * 60)
        print("\n".join(errors))
        print(f"\n{len(errors)} file(s) failed validation")
        sys.exit(1)

    print(f"\n✓ All {len(successes)} files passed validation!")


if __name__ == "__main__":
    main()

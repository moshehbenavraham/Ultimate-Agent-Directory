#!/usr/bin/env python3
"""
Migrate existing README.md markdown tables to YAML files

Usage:
    python scripts/migrate.py --section "Open-Source Agent Frameworks" --category open-source-frameworks
    python scripts/migrate.py --dry-run  # Preview without writing files
"""

import re
import argparse
from pathlib import Path
import yaml
from datetime import date
from models import AgentEntry


def parse_markdown_table(content: str) -> list[dict]:
    """
    Extract entries from a markdown table

    Expected format:
    | **Name** | [🔗 Link](url) | Description |
    """
    entries = []

    lines = content.split('\n')

    for line in lines:
        # Skip non-table lines, headers, and separators
        if not line.startswith('|'):
            continue
        if '---' in line:
            continue

        # Parse cells
        cells = [cell.strip() for cell in line.split('|')[1:-1]]

        if len(cells) < 3:
            continue

        # Skip header row
        if any(header in cells[0].lower() for header in ['framework', 'name', 'platform', 'course']):
            continue

        # Extract name (remove **bold**)
        name = re.sub(r'\*\*(.+?)\*\*', r'\1', cells[0]).strip()

        if not name:
            continue

        # Extract URL from markdown link
        url_match = re.search(r'\[.*?\]\((https?://[^\)]+)\)', cells[1])
        url = url_match.group(1) if url_match else ""

        # Get description (third column)
        description = cells[2].strip()

        # Detect GitHub repo
        github_repo = None
        if 'github.com' in url:
            repo_match = re.search(r'github\.com/([^/]+/[^/\s]+)', url)
            if repo_match:
                github_repo = repo_match.group(1).rstrip('/')

        # Build entry
        entry = {
            'name': name,
            'url': url,
            'description': description,
            'github_repo': github_repo
        }

        entries.append(entry)

    return entries


def extract_section(readme_content: str, section_title: str) -> str:
    """Extract a specific section from README"""

    # Find section start
    section_pattern = rf'^##\s+{re.escape(section_title)}.*?(?=^##\s|\Z)'

    match = re.search(section_pattern, readme_content, re.MULTILINE | re.DOTALL)

    if not match:
        print(f"ERROR: Section '{section_title}' not found")
        return ""

    return match.group(0)


def save_yaml_file(entry_data: dict, category: str, dry_run: bool = False):
    """Save entry as YAML file"""

    # Generate filename from name
    filename = re.sub(r'[^a-z0-9]+', '-', entry_data['name'].lower()).strip('-')

    # Determine subdirectory
    output_dir = Path(f"data/agents/{category}")
    output_dir.mkdir(parents=True, exist_ok=True)

    filepath = output_dir / f"{filename}.yml"

    # Add metadata
    entry_data['category'] = category
    entry_data['added_date'] = str(date.today())
    entry_data['verified'] = False

    # Determine type
    if 'framework' in category:
        entry_data['type'] = 'framework'
    elif 'platform' in category:
        entry_data['type'] = 'platform'
    elif 'course' in category or 'learning' in category:
        entry_data['type'] = 'course'
    elif 'community' in category:
        entry_data['type'] = 'community'
    else:
        entry_data['type'] = 'tool'

    if dry_run:
        print(f"  [DRY-RUN] Would create: {filepath}")
        return

    # Write YAML
    with open(filepath, 'w') as f:
        yaml.dump(
            entry_data,
            f,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True
        )

    print(f"  ✓ Created {filepath}")


def migrate_section(readme_path: str, section_title: str, category_id: str, dry_run: bool = False):
    """Migrate a specific section from README to YAML files"""

    print(f"\nMigrating section: {section_title}")
    print(f"Target category: {category_id}")
    print("-" * 60)

    # Read README
    readme_content = Path(readme_path).read_text()

    # Extract section
    section_content = extract_section(readme_content, section_title)

    if not section_content:
        return

    # Parse table entries
    entries = parse_markdown_table(section_content)

    print(f"Found {len(entries)} entries\n")

    # Save each entry
    for entry in entries:
        save_yaml_file(entry, category_id, dry_run)

    print(f"\n✓ Migrated {len(entries)} entries from '{section_title}'")


def main():
    parser = argparse.ArgumentParser(description="Migrate README.md to YAML files")
    parser.add_argument('--section', help="Section title to migrate")
    parser.add_argument('--category', help="Target category ID")
    parser.add_argument('--dry-run', action='store_true', help="Preview without writing")
    parser.add_argument('--all', action='store_true', help="Migrate all sections")

    args = parser.parse_args()

    readme_path = "README.md"

    if not Path(readme_path).exists():
        print("ERROR: README.md not found")
        return

    if args.all:
        # Define all sections to migrate
        migrations = [
            ("🛠️ Open-Source Agent Frameworks", "open-source-frameworks"),
            ("🎨 No-Code/Low-Code Agent Platforms", "no-code-platforms"),
            ("🔬 Research-Focused Frameworks", "research-frameworks"),
            ("📚 Learning Resources and Courses", "learning-resources"),
            ("💬 GitHub Repositories and Communities", "communities"),
            ("🛠 Specialized AI Agent Tools", "specialized-tools"),
            ("🤖 Autonomous Agents", "autonomous-agents"),
            ("🌐 Browser Automation Agents", "browser-automation"),
            ("💻 Coding Assistant Agents", "coding-assistants"),
            ("🏢 Enterprise Agent Platforms", "enterprise-platforms"),
        ]

        for section, category in migrations:
            migrate_section(readme_path, section, category, args.dry_run)

    elif args.section and args.category:
        migrate_section(readme_path, args.section, args.category, args.dry_run)

    else:
        parser.print_help()
        print("\nExample usage:")
        print("  python scripts/migrate.py --section '🛠️ Open-Source Agent Frameworks' --category open-source-frameworks")
        print("  python scripts/migrate.py --all --dry-run")


if __name__ == "__main__":
    main()

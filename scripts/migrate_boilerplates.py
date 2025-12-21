#!/usr/bin/env python3
"""
Migration script for transforming full-stack_starter_boilerplate_template_kit.md
into validated YAML files for the boilerplate directory.

This script parses the markdown hierarchy (H2 ecosystems, H3 categories,
H4 subcategories, H5 entries) and extracts structured data including
attribute tables, technical stack tables, feature lists, pros/cons,
and descriptive text.

Usage:
    python scripts/migrate_boilerplates.py
"""

import re
import sys
from datetime import date
from pathlib import Path
from typing import Optional

import yaml
from pydantic import ValidationError

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from models import BoilerplateEntry, BoilerplateCategory


# ============================================================================
# CONFIGURATION
# ============================================================================

SOURCE_FILE = Path("full-stack_starter_boilerplate_template_kit.md")
BOILERPLATES_DIR = Path("data/boilerplates")
CATEGORIES_DIR = Path("data/boilerplate-categories")

# Category ID mapping: H3 header text -> (category_id, ecosystem, emoji, order)
CATEGORY_MAPPING = {
    # JavaScript/TypeScript Ecosystem
    "Next.js & T3 Stack": ("nextjs", "JavaScript/TypeScript", "N", 10),
    "Remix": ("remix", "JavaScript/TypeScript", "R", 20),
    "Blitz.js": ("blitz", "JavaScript/TypeScript", "B", 30),
    "RedwoodJS": ("redwood", "JavaScript/TypeScript", "R", 40),
    "Meteor (Real-Time JavaScript)": ("meteor", "JavaScript/TypeScript", "M", 50),
    "Wasp & Open SaaS (DSL-Based)": ("wasp", "JavaScript/TypeScript", "W", 60),
    "Vue / Nuxt.js": ("nuxt", "JavaScript/TypeScript", "V", 70),
    "Svelte / SvelteKit": ("sveltekit", "JavaScript/TypeScript", "S", 80),
    "Node.js / Express (Traditional)": ("nodejs", "JavaScript/TypeScript", "N", 90),
    "Astro & HTML-First Approaches": ("astro", "JavaScript/TypeScript", "A", 100),
    "HTMX-Based Full-Stack": ("htmx", "JavaScript/TypeScript", "H", 105),
    # Python Ecosystem
    "FastAPI": ("fastapi", "Python", "F", 110),
    "Django": ("django", "Python", "D", 120),
    "Flask": ("flask", "Python", "F", 130),
    # PHP Ecosystem
    "Laravel": ("laravel", "PHP", "L", 140),
    # Ruby Ecosystem
    "Rails": ("rails", "Ruby", "R", 150),
    # Systems Languages
    "Go / Golang": ("go", "Go", "G", 160),
    "Rust": ("rust", "Rust", "R", 170),
    # .NET Ecosystem
    "Blazor": ("dotnet", ".NET", "B", 180),
    "ASP.NET + React": ("dotnet", ".NET", "A", 185),
    "ASP.NET + Vue": ("dotnet", ".NET", "A", 186),
    # Elixir Ecosystem
    "Phoenix LiveView": ("phoenix", "Elixir", "P", 190),
    "Phoenix + React / Vue": ("phoenix", "Elixir", "P", 195),
    # Mobile & Cross-Platform
    "React Native": ("react-native", "Mobile", "R", 200),
    "Expo": ("expo", "Mobile", "E", 210),
    "Cross-Platform Web + Mobile (Monorepo)": ("cross-platform", "Mobile", "C", 220),
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def slugify(text: str) -> str:
    """
    Convert text to URL-safe slug for file names.

    Examples:
        "create-t3-app" -> "create-t3-app"
        "Next.js Boilerplate (ixartz)" -> "nextjs-boilerplate-ixartz"
        "Supabase + Next.js Starter" -> "supabase-nextjs-starter"
    """
    # Convert to lowercase
    slug = text.lower()
    # Replace common separators with hyphens
    slug = re.sub(r"[+/&]", "-", slug)
    # Remove parentheses content as separate words
    slug = re.sub(r"\(([^)]+)\)", r"-\1", slug)
    # Replace non-alphanumeric characters with hyphens
    slug = re.sub(r"[^a-z0-9-]", "-", slug)
    # Collapse multiple hyphens
    slug = re.sub(r"-+", "-", slug)
    # Strip leading/trailing hyphens
    slug = slug.strip("-")
    return slug


def parse_star_count(text: str) -> Optional[int]:
    """
    Parse star count strings into integers.

    Examples:
        "~28,300" -> 28300
        "~15.1k" -> 15100
        "~5,900" -> 5900
        "~1.2k+" -> 1200
    """
    if not text:
        return None

    # Remove ~ prefix, + suffix, and commas
    cleaned = re.sub(r"[~+,]", "", text.strip())

    # Handle "k" suffix (thousands)
    if cleaned.lower().endswith("k"):
        try:
            return int(float(cleaned[:-1]) * 1000)
        except ValueError:
            return None

    # Try direct integer parsing
    try:
        return int(float(cleaned))
    except ValueError:
        return None


def sanitize_ascii(text: str) -> str:
    """
    Remove or replace non-ASCII characters to ensure clean output.

    Handles:
        - Curly quotes -> straight quotes
        - Em dashes -> regular dashes
        - Other non-ASCII -> removed
    """
    if not text:
        return ""

    # Replace common Unicode characters
    replacements = {
        "\u2018": "'",  # Left single quote
        "\u2019": "'",  # Right single quote
        "\u201c": '"',  # Left double quote
        "\u201d": '"',  # Right double quote
        "\u2013": "-",  # En dash
        "\u2014": "--",  # Em dash
        "\u2026": "...",  # Ellipsis
        "\u00a0": " ",  # Non-breaking space
        "\u2022": "-",  # Bullet
        "\u00b7": "-",  # Middle dot
    }

    for char, replacement in replacements.items():
        text = text.replace(char, replacement)

    # Remove any remaining non-ASCII characters
    return "".join(c if ord(c) < 128 else "" for c in text)


def extract_url_from_markdown(text: str) -> Optional[str]:
    """Extract URL from markdown link format [text](url)."""
    match = re.search(r"\[([^\]]+)\]\(([^)]+)\)", text)
    if match:
        return match.group(2)
    return None


def extract_github_repo(url: str) -> Optional[str]:
    """Extract owner/repo from GitHub URL."""
    if not url:
        return None
    match = re.search(r"github\.com/([^/]+/[^/]+)", url)
    if match:
        return match.group(1).rstrip("/")
    return None


# ============================================================================
# PARSER CLASS
# ============================================================================


class BoilerplateMarkdownParser:
    """
    Parser for the full-stack boilerplate markdown documentation.

    Parses H2 (ecosystems) -> H3 (categories) -> H4 (subcategories) -> H5 (entries)
    and extracts structured data from each entry.
    """

    def __init__(self, source_path: Path):
        self.source_path = source_path
        self.content = ""
        self.entries: list[dict] = []
        self.categories: dict[str, dict] = {}
        self.seen_urls: set[str] = set()
        self.stats = {
            "total_entries": 0,
            "migrated": 0,
            "skipped": 0,
            "validation_errors": 0,
            "duplicate_urls": 0,
        }

    def run(self) -> None:
        """Execute the full migration pipeline."""
        print("=" * 60)
        print("Boilerplate Migration Script")
        print("=" * 60)
        print()

        self.load_document()
        self.parse_document()
        self.write_category_files()
        self.write_entry_files()
        self.print_report()

    def load_document(self) -> None:
        """Read the source markdown file."""
        print(f"Loading: {self.source_path}")
        self.content = self.source_path.read_text(encoding="utf-8")
        lines = len(self.content.split("\n"))
        print(f"Loaded {lines} lines")
        print()

    def parse_document(self) -> None:
        """Parse the entire document by splitting on H2 headers."""
        print("Parsing document structure...")

        # Split by H2 headers
        h2_pattern = re.compile(r"^## (.+)$", re.MULTILINE)
        sections = h2_pattern.split(self.content)

        # Process pairs of (header, content)
        for i in range(1, len(sections), 2):
            if i + 1 < len(sections):
                ecosystem_name = sections[i].strip()
                ecosystem_content = sections[i + 1]
                self.parse_ecosystem(ecosystem_name, ecosystem_content)

        print(
            f"Found {len(self.entries)} entries across {len(self.categories)} categories"
        )
        print()

    def parse_ecosystem(self, ecosystem_name: str, content: str) -> None:
        """Parse an H2 ecosystem section by splitting on H3 headers."""
        # Skip non-boilerplate sections
        skip_sections = [
            "Discovery & Aggregation Resources",
            "Feature-Specific Resources",
            "Pricing & Licensing",
            "Comparison & Selection",
            "Quick Reference",
            "Appendix",
            "Specialized Categories",
        ]
        if ecosystem_name in skip_sections:
            return

        # Split by H3 headers
        h3_pattern = re.compile(r"^### (.+)$", re.MULTILINE)
        sections = h3_pattern.split(content)

        for i in range(1, len(sections), 2):
            if i + 1 < len(sections):
                category_name = sections[i].strip()
                category_content = sections[i + 1]
                self.parse_category(category_name, category_content, ecosystem_name)

    def parse_category(
        self, category_name: str, content: str, ecosystem_name: str
    ) -> None:
        """Parse an H3 category section by extracting H5 entries."""
        # Get category mapping
        category_info = CATEGORY_MAPPING.get(category_name)
        if not category_info:
            # Try partial matching
            for key, info in CATEGORY_MAPPING.items():
                if (
                    key.lower() in category_name.lower()
                    or category_name.lower() in key.lower()
                ):
                    category_info = info
                    break

        if not category_info:
            print(f"  Warning: No mapping for category '{category_name}', skipping")
            return

        category_id, ecosystem, emoji, order = category_info

        # Register category
        if category_id not in self.categories:
            self.categories[category_id] = {
                "id": category_id,
                "title": category_name,
                "emoji": emoji,
                "ecosystem": ecosystem,
                "order": order,
                "description": f"Production-ready {category_name} boilerplates and starter kits",
            }

        # Split by H5 headers to get entries
        # Also handle H4 subcategories
        h5_pattern = re.compile(r"^##### (.+)$", re.MULTILINE)
        h5_matches = list(h5_pattern.finditer(content))

        for idx, match in enumerate(h5_matches):
            entry_name = match.group(1).strip()
            start = match.end()
            end = (
                h5_matches[idx + 1].start()
                if idx + 1 < len(h5_matches)
                else len(content)
            )
            entry_content = content[start:end]

            self.parse_entry(entry_name, entry_content, category_id)

    def parse_entry(self, name: str, content: str, category_id: str) -> None:
        """Parse a single H5 entry and extract all data."""
        self.stats["total_entries"] += 1

        # Extract description (first paragraph after header)
        desc_match = re.search(r"^([A-Z][^\n|#]+)", content.strip())
        description = desc_match.group(1).strip() if desc_match else ""

        # Extract attribute table
        attrs = self.extract_attribute_table(content)

        # Get URL
        url = attrs.get("url")
        if not url:
            # Try to find URL in first markdown link
            url = extract_url_from_markdown(content[:500])

        if not url:
            print(f"  Skipping '{name}': No URL found")
            self.stats["skipped"] += 1
            return

        # Check for duplicates
        if url in self.seen_urls:
            print(f"  Skipping '{name}': Duplicate URL")
            self.stats["duplicate_urls"] += 1
            self.stats["skipped"] += 1
            return
        self.seen_urls.add(url)

        # Build entry data
        entry_data = {
            "name": sanitize_ascii(name),
            "url": url,
            "description": sanitize_ascii(description)[:2000]
            if description
            else f"A {category_id} boilerplate for building full-stack applications",
            "category": category_id,
            "type": "boilerplate",
            "tags": self.generate_tags(name, content, category_id),
            "github_repo": extract_github_repo(url),
            "github_stars": parse_star_count(attrs.get("stars", "")),
            "license": sanitize_ascii(attrs.get("license", "")).split("(")[0].strip()
            or None,
            "technical_stack": self.extract_tech_stack_table(content),
            "key_features": self.extract_features_list(content),
            "use_case": sanitize_ascii(self.extract_text_section(content, "Use Case") or ""),
            "pros": self.extract_pros_cons(content, "Pros"),
            "cons": self.extract_pros_cons(content, "Cons"),
            "community": sanitize_ascii(
                self.extract_text_section(content, "Community") or ""
            ),
            "deployment": self.extract_deployment(content),
            "added_date": str(date.today()),
        }

        # Clean up None values and empty lists
        entry_data = {
            k: v for k, v in entry_data.items() if v is not None and v != [] and v != ""
        }

        self.entries.append(entry_data)

    def extract_attribute_table(self, content: str) -> dict:
        """
        Extract data from the attribute table.

        Looks for:
        | Attribute | Details |
        |-----------|---------|
        | Repository | [owner/repo](url) |
        | Stars | ~X,XXX |
        | License | MIT |
        | Last Updated | Month Year |
        """
        attrs = {}

        # Find table rows
        table_pattern = re.compile(r"^\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|", re.MULTILINE)
        for match in table_pattern.finditer(content):
            key = match.group(1).strip().lower()
            value = match.group(2).strip()

            if "repository" in key:
                url = extract_url_from_markdown(value)
                if url:
                    attrs["url"] = url
            elif "star" in key:
                attrs["stars"] = value
            elif "license" in key:
                attrs["license"] = value
            elif "updated" in key:
                attrs["last_updated"] = value

        return attrs

    def extract_tech_stack_table(self, content: str) -> list[dict]:
        """
        Extract technical stack table data.

        Looks for:
        | Component | Technology | Reasoning |
        |-----------|------------|-----------|
        | Frontend | Next.js | Industry standard |
        """
        tech_stack: list[dict[str, str | None]] = []

        # Find Technical Stack section
        stack_match = re.search(
            r"\*\*Technical Stack[:\*]*\*?\*?\s*\n\|[^|]+\|[^|]+\|[^|]*\|?\s*\n\|[-:| ]+\|",
            content,
            re.IGNORECASE,
        )

        if not stack_match:
            return tech_stack

        # Parse table rows after the header
        start = stack_match.end()
        table_text = content[start : start + 2000]

        row_pattern = re.compile(
            r"^\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]*)\s*\|?", re.MULTILINE
        )
        for match in row_pattern.finditer(table_text):
            component = match.group(1).strip()
            technology = match.group(2).strip()
            reasoning = match.group(3).strip() if match.group(3) else ""

            # Skip header/separator rows
            if component.startswith("-") or component.lower() in [
                "component",
                "attribute",
            ]:
                continue

            if component and technology:
                tech_stack.append(
                    {
                        "component": sanitize_ascii(component)[:50],
                        "technology": sanitize_ascii(technology)[:100],
                        "reasoning": sanitize_ascii(reasoning)[:500] or None,
                    }
                )

        return tech_stack

    def extract_features_list(self, content: str) -> Optional[list[str]]:
        """
        Extract key features from bullet list.

        Looks for:
        **Key Features:**
        - Feature 1
        - Feature 2
        """
        features = []

        # Find Key Features section
        features_match = re.search(
            r"\*\*Key Features[:\*]*\*?\*?", content, re.IGNORECASE
        )
        if not features_match:
            return None

        # Extract bullet points after the header
        start = features_match.end()
        section = content[start : start + 1500]

        # Stop at next section header
        end_match = re.search(r"\n\*\*[A-Z]", section)
        if end_match:
            section = section[: end_match.start()]

        bullet_pattern = re.compile(r"^[-*]\s+(.+)$", re.MULTILINE)
        for match in bullet_pattern.finditer(section):
            feature = sanitize_ascii(match.group(1).strip())
            if feature and len(feature) > 3:
                features.append(feature[:200])

        return features if features else None

    def extract_pros_cons(self, content: str, section_type: str) -> Optional[list[str]]:
        """
        Extract pros or cons list.

        Handles both bullet lists and inline format:
        **Pros:** Item 1. Item 2. Item 3.
        **Pros:**
        - Item 1
        - Item 2
        """
        items = []

        # Find section
        pattern = re.compile(
            rf"\*\*{section_type}[:\*]*\*?\*?\s*(.+?)(?=\*\*[A-Z]|\n\n\*\*|\Z)",
            re.IGNORECASE | re.DOTALL,
        )
        match = pattern.search(content)

        if not match:
            return None

        section_content = match.group(1).strip()

        # Check for bullet points
        bullet_pattern = re.compile(r"^[-*]\s+(.+)$", re.MULTILINE)
        bullets = bullet_pattern.findall(section_content)

        if bullets:
            items = [
                sanitize_ascii(b.strip())[:200] for b in bullets if len(b.strip()) > 3
            ]
        else:
            # Split by periods or semicolons for inline format
            # But be careful not to split on abbreviations
            sentences = re.split(r"(?<=[.;])\s+(?=[A-Z])", section_content)
            items = [
                sanitize_ascii(s.strip().rstrip("."))[:200]
                for s in sentences
                if len(s.strip()) > 5
            ]

        return items if items else None

    def extract_text_section(self, content: str, section_name: str) -> Optional[str]:
        """
        Extract prose text from a named section.

        Looks for:
        **Use Case:** Description text...
        **Community:** Discord info...
        """
        pattern = re.compile(
            rf"\*\*{section_name}[:\*]*\*?\*?\s*(.+?)(?=\n\n\*\*|\n\*\*[A-Z]|\Z)",
            re.IGNORECASE | re.DOTALL,
        )
        match = pattern.search(content)

        if match:
            text = match.group(1).strip()
            # Clean up the text
            text = re.sub(r"\s+", " ", text)
            return text[:1000] if text else None

        return None

    def extract_deployment(self, content: str) -> Optional[list[str]]:
        """Extract deployment platforms from text."""
        platforms = []

        deployment_text = self.extract_text_section(content, "Deployment") or ""
        if not deployment_text:
            return None

        # Common deployment platforms to look for
        known_platforms = [
            "Vercel",
            "Netlify",
            "AWS",
            "Fly.io",
            "Heroku",
            "Docker",
            "Cloudflare",
            "Railway",
            "Render",
            "DigitalOcean",
            "GCP",
            "Azure",
            "Kubernetes",
            "EAS",
            "Supabase",
        ]

        for platform in known_platforms:
            if platform.lower() in deployment_text.lower():
                platforms.append(platform)

        return platforms if platforms else None

    def generate_tags(self, name: str, content: str, category_id: str) -> list[str]:
        """Generate relevant tags for the entry."""
        tags = [category_id]

        # Add technology-based tags
        tech_patterns = [
            (r"next\.?js", "nextjs"),
            (r"react", "react"),
            (r"typescript", "typescript"),
            (r"tailwind", "tailwindcss"),
            (r"prisma", "prisma"),
            (r"drizzle", "drizzle"),
            (r"supabase", "supabase"),
            (r"stripe", "stripe"),
            (r"trpc", "trpc"),
            (r"auth\.?js|nextauth", "authjs"),
            (r"clerk", "clerk"),
            (r"saas", "saas"),
            (r"monorepo|turborepo", "monorepo"),
            (r"expo", "expo"),
            (r"fastapi", "fastapi"),
            (r"django", "django"),
            (r"rails", "rails"),
            (r"laravel", "laravel"),
            (r"postgres", "postgresql"),
            (r"docker", "docker"),
        ]

        combined = f"{name} {content}".lower()
        for pattern, tag in tech_patterns:
            if re.search(pattern, combined):
                if tag not in tags:
                    tags.append(tag)

        return tags[:10]  # Limit to 10 tags

    def write_category_files(self) -> None:
        """Write category YAML files."""
        print("Writing category files...")

        for category_id, data in self.categories.items():
            file_path = CATEGORIES_DIR / f"{category_id}.yml"

            # Build category data
            category_data = {
                "id": data["id"],
                "title": data["title"],
                "emoji": data["emoji"],
                "description": data["description"],
                "ecosystem": data["ecosystem"],
                "order": data["order"],
                "show_github_stats": True,
                "table_columns": ["name", "url", "description", "github_stars"],
            }

            # Validate with Pydantic
            try:
                BoilerplateCategory(**category_data)
            except ValidationError as e:
                print(f"  Validation error for category {category_id}: {e}")
                continue

            # Write YAML
            with open(file_path, "w", encoding="utf-8", newline="\n") as f:
                yaml.dump(
                    category_data,
                    f,
                    default_flow_style=False,
                    allow_unicode=False,
                    sort_keys=False,
                )

            print(f"  Created: {file_path}")

        print(f"  Total: {len(self.categories)} category files")
        print()

    def write_entry_files(self) -> None:
        """Write boilerplate entry YAML files."""
        print("Writing entry files...")

        for entry_data in self.entries:
            category_id = entry_data["category"]
            slug = slugify(entry_data["name"])

            # Ensure category directory exists
            category_dir = BOILERPLATES_DIR / category_id
            if not category_dir.exists():
                category_dir.mkdir(parents=True)

            file_path = category_dir / f"{slug}.yml"

            # Convert technical_stack to proper format
            if "technical_stack" in entry_data:
                tech_stack = []
                for item in entry_data["technical_stack"]:
                    tech_item = {
                        "component": item["component"],
                        "technology": item["technology"],
                    }
                    if item.get("reasoning"):
                        tech_item["reasoning"] = item["reasoning"]
                    tech_stack.append(tech_item)
                entry_data["technical_stack"] = tech_stack

            # Validate with Pydantic
            try:
                BoilerplateEntry(**entry_data)
            except ValidationError as e:
                print(f"  Validation error for '{entry_data['name']}': {e}")
                self.stats["validation_errors"] += 1
                self.stats["skipped"] += 1
                continue

            # Write YAML with block scalars for long text
            yaml_content = self.generate_yaml_content(entry_data)

            with open(file_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(yaml_content)

            self.stats["migrated"] += 1

        print(f"  Total: {self.stats['migrated']} entry files")
        print()

    def generate_yaml_content(self, data: dict) -> str:
        """
        Generate YAML content with proper formatting.
        Uses block scalars for long text fields.
        """
        lines = []

        # Required fields first
        lines.append(f"name: {self.yaml_value(data.get('name', ''))}")
        lines.append(f"url: {data.get('url', '')}")

        # Description with block scalar if long
        desc = data.get("description", "")
        if len(desc) > 80:
            lines.append("description: |")
            for line in self.wrap_text(desc, 78):
                lines.append(f"  {line}")
        else:
            lines.append(f"description: {self.yaml_value(desc)}")

        lines.append(f"category: {data.get('category', '')}")

        # Type
        if data.get("type"):
            lines.append(f"type: {data['type']}")

        # Tags
        if data.get("tags"):
            lines.append("tags:")
            for tag in data["tags"]:
                lines.append(f"  - {tag}")

        # GitHub info
        if data.get("github_repo"):
            lines.append(f"github_repo: {data['github_repo']}")

        if data.get("github_stars"):
            lines.append(f"github_stars: {data['github_stars']}")

        if data.get("license"):
            lines.append(f"license: {self.yaml_value(data['license'])}")

        # Technical stack
        if data.get("technical_stack"):
            lines.append("technical_stack:")
            for tech in data["technical_stack"]:
                lines.append(f"  - component: {self.yaml_value(tech['component'])}")
                lines.append(f"    technology: {self.yaml_value(tech['technology'])}")
                if tech.get("reasoning"):
                    if len(tech["reasoning"]) > 60:
                        lines.append("    reasoning: |")
                        for line in self.wrap_text(tech["reasoning"], 74):
                            lines.append(f"      {line}")
                    else:
                        lines.append(
                            f"    reasoning: {self.yaml_value(tech['reasoning'])}"
                        )

        # Key features
        if data.get("key_features"):
            lines.append("key_features:")
            for feature in data["key_features"]:
                lines.append(f"  - {self.yaml_value(feature)}")

        # Use case
        if data.get("use_case"):
            use_case = data["use_case"]
            if len(use_case) > 80:
                lines.append("use_case: |")
                for line in self.wrap_text(use_case, 78):
                    lines.append(f"  {line}")
            else:
                lines.append(f"use_case: {self.yaml_value(use_case)}")

        # Pros
        if data.get("pros"):
            lines.append("pros:")
            for pro in data["pros"]:
                lines.append(f"  - {self.yaml_value(pro)}")

        # Cons
        if data.get("cons"):
            lines.append("cons:")
            for con in data["cons"]:
                lines.append(f"  - {self.yaml_value(con)}")

        # Community
        if data.get("community"):
            community = data["community"]
            if len(community) > 80:
                lines.append("community: |")
                for line in self.wrap_text(community, 78):
                    lines.append(f"  {line}")
            else:
                lines.append(f"community: {self.yaml_value(community)}")

        # Deployment
        if data.get("deployment"):
            lines.append("deployment:")
            for platform in data["deployment"]:
                lines.append(f"  - {platform}")

        # Metadata
        if data.get("added_date"):
            lines.append(f"added_date: {data['added_date']}")

        return "\n".join(lines) + "\n"

    def yaml_value(self, value: str) -> str:
        """Format a value for YAML, quoting if necessary."""
        if not value:
            return '""'

        # Quote if contains special characters
        needs_quotes = any(
            [
                value.startswith(
                    ("'", '"', "&", "*", "!", "|", ">", "{", "[", "@", "`")
                ),
                ":" in value,
                "#" in value,
                value.startswith("-"),
                value.startswith(" "),
                value.endswith(" "),
                value in ("true", "false", "null", "yes", "no", "on", "off"),
            ]
        )

        if needs_quotes:
            # Escape any existing quotes and wrap
            escaped = value.replace('"', '\\"')
            return f'"{escaped}"'

        return value

    def wrap_text(self, text: str, width: int) -> list[str]:
        """Wrap text to specified width for block scalars."""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            if current_length + len(word) + 1 <= width:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)

        if current_line:
            lines.append(" ".join(current_line))

        return lines

    def print_report(self) -> None:
        """Print migration statistics report."""
        print("=" * 60)
        print("Migration Report")
        print("=" * 60)
        print()
        print(f"Total entries found:    {self.stats['total_entries']}")
        print(f"Successfully migrated:  {self.stats['migrated']}")
        print(f"Skipped:                {self.stats['skipped']}")
        print(f"  - Duplicate URLs:     {self.stats['duplicate_urls']}")
        print(f"  - Validation errors:  {self.stats['validation_errors']}")
        print()
        print(f"Categories created:     {len(self.categories)}")
        print()
        print("Category breakdown:")

        # Count entries per category
        category_counts: dict[str, int] = {}
        for entry in self.entries:
            cat = entry.get("category", "unknown")
            category_counts[cat] = category_counts.get(cat, 0) + 1

        for cat, count in sorted(category_counts.items()):
            print(f"  {cat}: {count}")

        print()
        print("=" * 60)
        print("Migration complete!")
        print("Run 'make validate' to verify all generated files.")
        print("=" * 60)


# ============================================================================
# MAIN
# ============================================================================


def main():
    """Main entry point."""
    if not SOURCE_FILE.exists():
        print(f"Error: Source file not found: {SOURCE_FILE}")
        sys.exit(1)

    if not BOILERPLATES_DIR.exists():
        print(f"Error: Target directory not found: {BOILERPLATES_DIR}")
        sys.exit(1)

    if not CATEGORIES_DIR.exists():
        print(f"Error: Categories directory not found: {CATEGORIES_DIR}")
        sys.exit(1)

    parser = BoilerplateMarkdownParser(SOURCE_FILE)
    parser.run()


if __name__ == "__main__":
    main()

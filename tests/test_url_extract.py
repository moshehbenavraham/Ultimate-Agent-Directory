"""
Tests for URL extraction functions in check_links.py

These tests verify:
- Correct extraction of URLs from markdown (inline, reference, direct)
- Correct extraction of URLs from templates
- Edge cases with special characters and nested structures
"""

import sys
from pathlib import Path

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from check_links import (
    extract_urls_from_markdown,
    extract_urls_from_template,
    extract_urls_from_static,
)


# =============================================================================
# Markdown URL Extraction Tests
# =============================================================================


class TestMarkdownInlineLinks:
    """Test extraction of inline markdown links [text](url)"""

    def test_simple_inline_link(self, tmp_path):
        """Extract simple inline link"""
        md_file = tmp_path / "test.md"
        md_file.write_text("Check out [Example](https://example.com) for more.")

        urls = extract_urls_from_markdown(md_file)

        assert len(urls) == 1
        assert urls[0] == ("https://example.com", "inline:[Example]")

    def test_multiple_inline_links(self, tmp_path):
        """Extract multiple inline links"""
        md_file = tmp_path / "test.md"
        md_file.write_text(
            """
            Visit [Site A](https://site-a.com) and [Site B](https://site-b.com).
            Also check [Site C](http://site-c.com).
            """
        )

        urls = extract_urls_from_markdown(md_file)

        assert len(urls) == 3
        url_strings = [url for url, _ in urls]
        assert "https://site-a.com" in url_strings
        assert "https://site-b.com" in url_strings
        assert "http://site-c.com" in url_strings

    def test_inline_link_with_path(self, tmp_path):
        """Extract inline link with path and query parameters"""
        md_file = tmp_path / "test.md"
        md_file.write_text(
            "[Docs](https://example.com/docs/getting-started?version=2#installation)"
        )

        urls = extract_urls_from_markdown(md_file)

        assert len(urls) == 1
        assert (
            urls[0][0]
            == "https://example.com/docs/getting-started?version=2#installation"
        )

    def test_inline_link_ignores_relative(self, tmp_path):
        """Relative links are ignored"""
        md_file = tmp_path / "test.md"
        md_file.write_text(
            """
            [Relative](./other-page.md)
            [Anchor](#section)
            [Absolute](https://example.com)
            """
        )

        urls = extract_urls_from_markdown(md_file)

        assert len(urls) == 1
        assert urls[0][0] == "https://example.com"


class TestMarkdownReferenceLinks:
    """Test extraction of reference-style markdown links [ref]: url"""

    def test_simple_reference_link(self, tmp_path):
        """Extract reference-style link"""
        md_file = tmp_path / "test.md"
        md_file.write_text(
            """
            Check the [documentation][docs].

            [docs]: https://docs.example.com
            """
        )

        urls = extract_urls_from_markdown(md_file)

        url_strings = [url for url, _ in urls]
        assert "https://docs.example.com" in url_strings

    def test_multiple_reference_links(self, tmp_path):
        """Extract multiple reference-style links"""
        md_file = tmp_path / "test.md"
        md_file.write_text(
            """
            See [repo] and [docs].

            [repo]: https://github.com/example/repo
            [docs]: https://docs.example.com
            """
        )

        urls = extract_urls_from_markdown(md_file)

        url_strings = [url for url, _ in urls]
        assert "https://github.com/example/repo" in url_strings
        assert "https://docs.example.com" in url_strings


class TestMarkdownDirectUrls:
    """Test extraction of direct URLs in markdown text"""

    def test_direct_url_in_text(self, tmp_path):
        """Extract URL appearing directly in text"""
        md_file = tmp_path / "test.md"
        md_file.write_text("Visit https://example.com for more information.")

        urls = extract_urls_from_markdown(md_file)

        assert len(urls) == 1
        assert urls[0] == ("https://example.com", "direct")

    def test_direct_url_not_duplicated(self, tmp_path):
        """URL in markdown link is not also captured as direct URL"""
        md_file = tmp_path / "test.md"
        md_file.write_text("[Example](https://example.com)")

        urls = extract_urls_from_markdown(md_file)

        # Should only be captured once as inline link
        assert len(urls) == 1
        assert urls[0][1] == "inline:[Example]"

    def test_multiple_direct_urls(self, tmp_path):
        """Extract multiple direct URLs"""
        md_file = tmp_path / "test.md"
        md_file.write_text(
            """
            Primary: https://primary.com
            Secondary: https://secondary.com
            """
        )

        urls = extract_urls_from_markdown(md_file)

        url_strings = [url for url, _ in urls]
        assert "https://primary.com" in url_strings
        assert "https://secondary.com" in url_strings


class TestMarkdownMixedLinks:
    """Test extraction with mixed link types"""

    def test_mixed_link_types(self, tmp_path):
        """Extract all link types from a realistic markdown file"""
        md_file = tmp_path / "test.md"
        md_file.write_text(
            """
            # My Project

            Check out the [documentation](https://docs.example.com).

            For source code, see [GitHub][gh].

            Direct link: https://example.com/direct

            [gh]: https://github.com/example/project
            """
        )

        urls = extract_urls_from_markdown(md_file)

        url_strings = [url for url, _ in urls]
        assert "https://docs.example.com" in url_strings
        assert "https://github.com/example/project" in url_strings
        assert "https://example.com/direct" in url_strings


class TestMarkdownEdgeCases:
    """Test edge cases in markdown URL extraction"""

    def test_url_with_special_characters(self, tmp_path):
        """Extract URL with special characters in path"""
        md_file = tmp_path / "test.md"
        md_file.write_text(
            "[API](https://api.example.com/v1/users?filter=active&sort=name)"
        )

        urls = extract_urls_from_markdown(md_file)

        assert len(urls) == 1
        assert "filter=active&sort=name" in urls[0][0]

    def test_empty_file(self, tmp_path):
        """Empty file returns empty list"""
        md_file = tmp_path / "test.md"
        md_file.write_text("")

        urls = extract_urls_from_markdown(md_file)

        assert urls == []

    def test_no_urls(self, tmp_path):
        """File without URLs returns empty list"""
        md_file = tmp_path / "test.md"
        md_file.write_text("This is just plain text without any links.")

        urls = extract_urls_from_markdown(md_file)

        assert urls == []

    def test_malformed_markdown_link(self, tmp_path):
        """Malformed markdown link is handled gracefully"""
        md_file = tmp_path / "test.md"
        md_file.write_text(
            """
            [broken(https://example.com)
            [valid](https://valid.com)
            """
        )

        urls = extract_urls_from_markdown(md_file)

        url_strings = [url for url, _ in urls]
        assert "https://valid.com" in url_strings


# =============================================================================
# Template URL Extraction Tests
# =============================================================================


class TestTemplateExtraction:
    """Test extraction of URLs from Jinja2 templates"""

    def test_literal_url_in_template(self, tmp_path):
        """Extract literal URL from template"""
        template_file = tmp_path / "test.html.jinja2"
        template_file.write_text(
            """
            <html>
            <head>
                <link rel="stylesheet" href="https://cdn.example.com/style.css">
            </head>
            </html>
            """
        )

        urls = extract_urls_from_template(template_file)

        assert len(urls) == 1
        assert urls[0][0] == "https://cdn.example.com/style.css"

    def test_multiple_literal_urls(self, tmp_path):
        """Extract multiple literal URLs from template"""
        template_file = tmp_path / "test.html.jinja2"
        template_file.write_text(
            """
            <script src="https://cdn.example.com/script.js"></script>
            <link href="https://fonts.googleapis.com/css?family=Roboto">
            """
        )

        urls = extract_urls_from_template(template_file)

        url_strings = [url for url, _ in urls]
        assert "https://cdn.example.com/script.js" in url_strings
        assert "https://fonts.googleapis.com/css?family=Roboto" in url_strings

    def test_jinja_variable_urls_ignored(self, tmp_path):
        """URLs inside Jinja variables are ignored"""
        template_file = tmp_path / "test.html.jinja2"
        template_file.write_text(
            """
            <a href="{{ entry.url }}">Link</a>
            <a href="https://static.example.com">Static</a>
            """
        )

        urls = extract_urls_from_template(template_file)

        # Should only get the static URL, not the variable
        assert len(urls) == 1
        assert urls[0][0] == "https://static.example.com"


# =============================================================================
# Static File URL Extraction Tests
# =============================================================================


class TestStaticFileExtraction:
    """Test extraction of URLs from CSS/JS files"""

    def test_url_in_css(self, tmp_path):
        """Extract URL from CSS file"""
        css_file = tmp_path / "style.css"
        css_file.write_text(
            """
            @import url('https://fonts.googleapis.com/css?family=Open+Sans');

            .hero {
                background-image: url('https://example.com/bg.jpg');
            }
            """
        )

        urls = extract_urls_from_static(css_file)

        url_strings = [url for url, _ in urls]
        assert any("fonts.googleapis.com" in url for url in url_strings)
        assert any("example.com/bg.jpg" in url for url in url_strings)

    def test_url_in_javascript(self, tmp_path):
        """Extract URL from JavaScript file"""
        js_file = tmp_path / "app.js"
        js_file.write_text(
            """
            const API_BASE = 'https://api.example.com/v1';

            fetch('https://api.example.com/users')
                .then(response => response.json());
            """
        )

        urls = extract_urls_from_static(js_file)

        url_strings = [url for url, _ in urls]
        assert any("api.example.com" in url for url in url_strings)


# =============================================================================
# Integration-style Tests
# =============================================================================


class TestRealWorldPatterns:
    """Test patterns commonly found in real markdown files"""

    def test_github_readme_pattern(self, tmp_path):
        """Extract URLs from GitHub README pattern"""
        md_file = tmp_path / "README.md"
        md_file.write_text(
            """
            # Project Name

            [![Build Status](https://github.com/owner/repo/actions/workflows/ci.yml/badge.svg)](https://github.com/owner/repo/actions)
            [![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

            ## Installation

            ```bash
            pip install project
            ```

            ## Documentation

            See the [full documentation](https://project.readthedocs.io).

            ## Links

            - [GitHub](https://github.com/owner/repo)
            - [PyPI](https://pypi.org/project/project/)
            """
        )

        urls = extract_urls_from_markdown(md_file)

        url_strings = [url for url, _ in urls]
        # Should capture badge URLs and link URLs
        assert any("github.com/owner/repo" in url for url in url_strings)
        assert any("readthedocs.io" in url for url in url_strings)
        assert any("pypi.org" in url for url in url_strings)

    def test_table_with_links(self, tmp_path):
        """Extract URLs from markdown table"""
        md_file = tmp_path / "test.md"
        md_file.write_text(
            """
            | Name | Link | Description |
            |------|------|-------------|
            | Tool A | [Link](https://tool-a.com) | First tool |
            | Tool B | [Link](https://tool-b.com) | Second tool |
            """
        )

        urls = extract_urls_from_markdown(md_file)

        url_strings = [url for url, _ in urls]
        assert "https://tool-a.com" in url_strings
        assert "https://tool-b.com" in url_strings

#!/usr/bin/env python3
"""
Link checker for Ultimate Agent Directory.

Scans all repository files (YAML, Markdown, templates, static assets) for URLs,
validates them with async HTTP requests, and reports broken links.

Usage:
    python scripts/check_links.py                    # Full check with default settings
    python scripts/check_links.py --yaml-only        # Check only YAML files (fast)
    python scripts/check_links.py --timeout 10       # Custom timeout
    python scripts/check_links.py --no-issues        # Skip GitHub issue creation
    python scripts/check_links.py --verbose          # Detailed logging
"""

import asyncio
import argparse
import json
import os
import re
import sys
import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import urlparse

import aiohttp
import yaml
from tqdm import tqdm

# Import local models for YAML parsing
try:
    from models import AgentEntry, Category
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from models import AgentEntry, Category


# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


@dataclass
class URLCheck:
    """Result of checking a single URL."""
    url: str
    status: str  # 'success', 'error', 'warning'
    status_code: Optional[int]
    error_message: Optional[str]
    source_file: str
    source_type: str  # 'yaml', 'markdown', 'template', 'static'
    field_name: Optional[str]  # For YAML: 'url', 'documentation_url', etc.


@dataclass
class RateLimiter:
    """Rate limiter for domain-based request throttling."""
    max_per_second: int
    domain_timestamps: Dict[str, List[float]] = None

    def __post_init__(self):
        if self.domain_timestamps is None:
            self.domain_timestamps = defaultdict(list)

    async def wait_if_needed(self, url: str):
        """Wait if we've exceeded rate limit for this domain."""
        domain = urlparse(url).netloc
        now = time.time()

        # Remove timestamps older than 1 second
        self.domain_timestamps[domain] = [
            ts for ts in self.domain_timestamps[domain]
            if now - ts < 1.0
        ]

        # If we've hit the limit, wait
        if len(self.domain_timestamps[domain]) >= self.max_per_second:
            oldest = self.domain_timestamps[domain][0]
            wait_time = 1.0 - (now - oldest)
            if wait_time > 0:
                await asyncio.sleep(wait_time)

        # Record this request
        self.domain_timestamps[domain].append(time.time())


def extract_urls_from_yaml(file_path: Path) -> List[Tuple[str, str]]:
    """
    Extract URLs from YAML files.

    Returns:
        List of (url, field_name) tuples
    """
    urls = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if not data:
            return urls

        # Check if it's an agent file or category file
        if 'url' in data:  # Agent file
            try:
                entry = AgentEntry(**data)
                urls.append((str(entry.url), 'url'))

                if entry.documentation_url:
                    urls.append((str(entry.documentation_url), 'documentation_url'))

                if entry.demo_url:
                    urls.append((str(entry.demo_url), 'demo_url'))

                # Construct GitHub URL from github_repo field
                if entry.github_repo:
                    github_url = f"https://github.com/{entry.github_repo}"
                    urls.append((github_url, 'github_repo'))

            except Exception as e:
                # If Pydantic validation fails, try manual extraction
                if 'url' in data:
                    urls.append((data['url'], 'url'))
                if 'documentation_url' in data:
                    urls.append((data['documentation_url'], 'documentation_url'))
                if 'demo_url' in data:
                    urls.append((data['demo_url'], 'demo_url'))
                if 'github_repo' in data:
                    urls.append((f"https://github.com/{data['github_repo']}", 'github_repo'))

    except Exception as e:
        print(f"  {Colors.YELLOW}Warning: Could not parse {file_path}: {e}{Colors.RESET}")

    return urls


def extract_urls_from_markdown(file_path: Path) -> List[Tuple[str, str]]:
    """
    Extract URLs from Markdown files.

    Returns:
        List of (url, context) tuples
    """
    urls = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Pattern 1: Inline links [text](url)
        inline_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        for match in re.finditer(inline_pattern, content):
            url = match.group(2)
            if url.startswith('http://') or url.startswith('https://'):
                urls.append((url, f'inline:[{match.group(1)}]'))

        # Pattern 2: Reference links [ref]: url
        reference_pattern = r'^\[([^\]]+)\]:\s*(.+)$'
        for match in re.finditer(reference_pattern, content, re.MULTILINE):
            url = match.group(2).strip()
            if url.startswith('http://') or url.startswith('https://'):
                urls.append((url, f'reference:[{match.group(1)}]'))

        # Pattern 3: Direct URLs (not in markdown links)
        # Exclude URLs already captured in patterns 1 and 2
        direct_pattern = r'(?<!\()https?://[^\s<>"{}|\\^`\[\]]+'
        captured_urls = {url for url, _ in urls}
        for match in re.finditer(direct_pattern, content):
            url = match.group(0)
            if url not in captured_urls:
                urls.append((url, 'direct'))
                captured_urls.add(url)

    except Exception as e:
        print(f"  {Colors.YELLOW}Warning: Could not parse {file_path}: {e}{Colors.RESET}")

    return urls


def extract_urls_from_template(file_path: Path) -> List[Tuple[str, str]]:
    """
    Extract URLs from Jinja2 template files.

    Returns:
        List of (url, context) tuples
    """
    urls = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Pattern: Literal URLs in templates (not in variables)
        url_pattern = r'https?://[^\s"\'<>]+'
        for match in re.finditer(url_pattern, content):
            url = match.group(0)
            # Skip if it's inside a Jinja2 variable (contains {})
            if '{{' not in url and '}}' not in url:
                urls.append((url, 'literal'))

    except Exception as e:
        print(f"  {Colors.YELLOW}Warning: Could not parse {file_path}: {e}{Colors.RESET}")

    return urls


def extract_urls_from_static(file_path: Path) -> List[Tuple[str, str]]:
    """
    Extract URLs from static files (CSS, JS).

    Returns:
        List of (url, context) tuples
    """
    urls = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract all HTTP/HTTPS URLs
        url_pattern = r'https?://[^\s"\'<>)\]};]+'
        for match in re.finditer(url_pattern, content):
            urls.append((match.group(0), 'static'))

    except Exception as e:
        print(f"  {Colors.YELLOW}Warning: Could not parse {file_path}: {e}{Colors.RESET}")

    return urls


def collect_all_urls(yaml_only: bool = False, verbose: bool = False) -> Dict[str, List[Tuple[str, str]]]:
    """
    Collect all URLs from repository files.

    Returns:
        Dict mapping file paths to list of (url, field_name/context) tuples
    """
    project_root = Path(__file__).parent.parent
    url_map = defaultdict(list)

    if verbose:
        print(f"\n{Colors.BOLD}Collecting URLs...{Colors.RESET}")

    # 1. YAML files (highest priority)
    yaml_pattern = "data/**/*.yml"
    yaml_files = list(project_root.glob(yaml_pattern))
    if verbose:
        print(f"  Scanning {len(yaml_files)} YAML files...")

    for yaml_file in yaml_files:
        urls = extract_urls_from_yaml(yaml_file)
        if urls:
            url_map[str(yaml_file.relative_to(project_root))] = [
                (url, field) for url, field in urls
            ]

    if yaml_only:
        return url_map

    # 2. Markdown files (documentation)
    md_files = []
    # Root level markdown
    for md_file in project_root.glob("*.md"):
        # Skip generated README.md (redundant with YAML)
        if md_file.name != "README.md":
            md_files.append(md_file)
    # Documentation markdown
    docs_dir = project_root / "docs"
    if docs_dir.exists():
        md_files.extend(docs_dir.glob("*.md"))

    if verbose:
        print(f"  Scanning {len(md_files)} Markdown files...")

    for md_file in md_files:
        urls = extract_urls_from_markdown(md_file)
        if urls:
            url_map[str(md_file.relative_to(project_root))] = urls

    # 3. Jinja2 templates
    templates_dir = project_root / "templates"
    if templates_dir.exists():
        template_files = list(templates_dir.glob("*.jinja2")) + list(templates_dir.glob("*.html"))
        if verbose:
            print(f"  Scanning {len(template_files)} template files...")

        for template_file in template_files:
            urls = extract_urls_from_template(template_file)
            if urls:
                url_map[str(template_file.relative_to(project_root))] = urls

    # 4. Static assets (CSS, JS)
    static_dir = project_root / "static"
    if static_dir.exists():
        static_files = list(static_dir.glob("**/*.css")) + list(static_dir.glob("**/*.js"))
        if verbose:
            print(f"  Scanning {len(static_files)} static files...")

        for static_file in static_files:
            urls = extract_urls_from_static(static_file)
            if urls:
                url_map[str(static_file.relative_to(project_root))] = urls

    return url_map


async def check_url(
    session: aiohttp.ClientSession,
    url: str,
    timeout: int,
    retries: int,
    rate_limiter: RateLimiter,
    verbose: bool = False
) -> Tuple[int, Optional[str]]:
    """
    Check a single URL asynchronously.

    Default settings optimized for 100Mbps home connection:
    - timeout: 10 seconds (forgiving for slower servers)
    - retries: 3 attempts with exponential backoff
    - rate_limit: 5 requests/second per domain

    Returns:
        Tuple of (status_code, error_message)
    """
    # Wait for rate limiter
    await rate_limiter.wait_if_needed(url)

    for attempt in range(retries):
        try:
            async with session.head(
                url,
                timeout=aiohttp.ClientTimeout(total=timeout),
                allow_redirects=True,
                ssl=False  # Don't verify SSL to avoid certificate issues
            ) as response:
                return response.status, None

        except asyncio.TimeoutError:
            if attempt == retries - 1:
                return 0, "Timeout"
            await asyncio.sleep(2 ** attempt)  # Exponential backoff

        except aiohttp.ClientError as e:
            # Try GET request if HEAD fails (some servers don't support HEAD)
            if attempt == 0:
                try:
                    async with session.get(
                        url,
                        timeout=aiohttp.ClientTimeout(total=timeout),
                        allow_redirects=True,
                        ssl=False
                    ) as response:
                        return response.status, None
                except Exception:
                    pass

            if attempt == retries - 1:
                return 0, str(e)
            await asyncio.sleep(2 ** attempt)

        except Exception as e:
            if attempt == retries - 1:
                return 0, f"Unexpected error: {str(e)}"
            await asyncio.sleep(2 ** attempt)

    return 0, "Max retries exceeded"


async def check_all_urls(
    url_map: Dict[str, List[Tuple[str, str]]],
    timeout: int,
    retries: int,
    rate_limit: int,
    verbose: bool = False
) -> List[URLCheck]:
    """
    Check all URLs asynchronously with rate limiting.

    Returns:
        List of URLCheck results
    """
    results = []
    rate_limiter = RateLimiter(max_per_second=rate_limit)

    # Flatten URL map to list of (url, file, field) tuples
    url_checks = []
    for file_path, urls in url_map.items():
        for url, field in urls:
            url_checks.append((url, file_path, field))

    # Deduplicate URLs while preserving source information
    url_to_sources = defaultdict(list)
    for url, file_path, field in url_checks:
        url_to_sources[url].append((file_path, field))

    unique_urls = list(url_to_sources.keys())

    print(f"\n{Colors.BOLD}Checking {len(unique_urls)} unique URLs...{Colors.RESET}")

    # Create aiohttp session
    connector = aiohttp.TCPConnector(limit=100, limit_per_host=10)
    async with aiohttp.ClientSession(connector=connector) as session:
        # Create progress bar
        with tqdm(total=len(unique_urls), desc="Progress", unit="url") as pbar:
            # Check URLs in batches to avoid overwhelming the system
            batch_size = 50
            for i in range(0, len(unique_urls), batch_size):
                batch = unique_urls[i:i+batch_size]

                # Create tasks for this batch
                tasks = [
                    check_url(session, url, timeout, retries, rate_limiter, verbose)
                    for url in batch
                ]

                # Wait for all tasks in batch to complete
                batch_results = await asyncio.gather(*tasks)

                # Process results
                for url, (status_code, error_msg) in zip(batch, batch_results):
                    # Classify result
                    if status_code == 0:
                        status = 'error'
                    elif status_code < 400:
                        status = 'success'
                    elif status_code in [403, 401]:
                        status = 'warning'  # May be auth-required
                    elif status_code == 429:
                        status = 'warning'  # Rate limited
                    elif status_code >= 500:
                        status = 'warning'  # Server error (may be temporary)
                    else:
                        status = 'error'  # 404, 410, etc.

                    # Create URLCheck for each source
                    for file_path, field in url_to_sources[url]:
                        # Determine source type
                        if file_path.endswith('.yml') or file_path.endswith('.yaml'):
                            source_type = 'yaml'
                        elif file_path.endswith('.md'):
                            source_type = 'markdown'
                        elif '.jinja' in file_path or file_path.endswith('.html'):
                            source_type = 'template'
                        else:
                            source_type = 'static'

                        results.append(URLCheck(
                            url=url,
                            status=status,
                            status_code=status_code,
                            error_message=error_msg,
                            source_file=file_path,
                            source_type=source_type,
                            field_name=field
                        ))

                pbar.update(len(batch))

    return results


def print_results(results: List[URLCheck], verbose: bool = False):
    """Print check results to terminal with color coding."""
    # Group by status
    success = [r for r in results if r.status == 'success']
    warnings = [r for r in results if r.status == 'warning']
    errors = [r for r in results if r.status == 'error']

    # Deduplicate for display (same URL may appear in multiple files)
    unique_errors = {}
    for result in errors:
        if result.url not in unique_errors:
            unique_errors[result.url] = result

    unique_warnings = {}
    for result in warnings:
        if result.url not in unique_warnings:
            unique_warnings[result.url] = result

    print(f"\n{Colors.BOLD}=== Link Check Results ==={Colors.RESET}\n")

    print(f"{Colors.GREEN}✓ Passed:{Colors.RESET} {len(success)}")
    print(f"{Colors.YELLOW}⚠ Warnings:{Colors.RESET} {len(warnings)}")
    print(f"{Colors.RED}✗ Failed:{Colors.RESET} {len(errors)}\n")

    # Show errors
    if unique_errors:
        print(f"{Colors.RED}{Colors.BOLD}Failed Links:{Colors.RESET}")
        for url, result in unique_errors.items():
            sources = [r.source_file for r in errors if r.url == url]
            print(f"  {Colors.RED}✗{Colors.RESET} {url}")
            print(f"    Status: {result.status_code or 'N/A'}")
            if result.error_message:
                print(f"    Error: {result.error_message}")
            print(f"    Found in: {', '.join(set(sources))}")
            print()

    # Show warnings if verbose
    if verbose and unique_warnings:
        print(f"{Colors.YELLOW}{Colors.BOLD}Warnings:{Colors.RESET}")
        for url, result in unique_warnings.items():
            sources = [r.source_file for r in warnings if r.url == url]
            print(f"  {Colors.YELLOW}⚠{Colors.RESET} {url}")
            print(f"    Status: {result.status_code}")
            print(f"    Found in: {', '.join(set(sources))}")
            print()


def save_report(results: List[URLCheck], output_file: str = "reports/link-check-report.json"):
    """Save detailed results to JSON file."""
    project_root = Path(__file__).parent.parent
    output_path = project_root / output_file

    # Create reports directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "summary": {
            "total": len(results),
            "success": len([r for r in results if r.status == 'success']),
            "warnings": len([r for r in results if r.status == 'warning']),
            "errors": len([r for r in results if r.status == 'error'])
        },
        "results": [
            {
                "url": r.url,
                "status": r.status,
                "status_code": r.status_code,
                "error_message": r.error_message,
                "source_file": r.source_file,
                "source_type": r.source_type,
                "field_name": r.field_name
            }
            for r in results
        ]
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print(f"{Colors.BLUE}Report saved to: {output_file}{Colors.RESET}")


def create_github_issues(results: List[URLCheck], verbose: bool = False):
    """Create GitHub issues for broken links."""
    errors = [r for r in results if r.status == 'error']

    if not errors:
        print(f"{Colors.GREEN}No broken links to report!{Colors.RESET}")
        return

    # Check for GitHub token
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        print(f"{Colors.YELLOW}Warning: GITHUB_TOKEN not found. Skipping issue creation.{Colors.RESET}")
        print(f"To create issues, set GITHUB_TOKEN environment variable.")
        return

    # Group errors by URL to avoid duplicate issues
    unique_errors = {}
    for result in errors:
        if result.url not in unique_errors:
            unique_errors[result.url] = []
        unique_errors[result.url].append(result)

    print(f"\n{Colors.BOLD}Creating GitHub issues for {len(unique_errors)} broken links...{Colors.RESET}")

    # Import requests for GitHub API
    import requests

    # Detect repository from git config or environment
    repo = os.environ.get('GITHUB_REPOSITORY', 'moshehbenavraham/Ultimate-Agent-Directory')
    api_url = f"https://api.github.com/repos/{repo}/issues"

    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    for url, url_errors in unique_errors.items():
        # Check if issue already exists
        search_url = f"https://api.github.com/search/issues?q=repo:{repo}+is:issue+is:open+{url}+in:title"
        try:
            response = requests.get(search_url, headers=headers)
            if response.status_code == 200:
                existing = response.json()
                if existing['total_count'] > 0:
                    if verbose:
                        print(f"  Issue already exists for: {url}")
                    continue
        except Exception as e:
            if verbose:
                print(f"  Warning: Could not check for existing issue: {e}")

        # Prepare issue body
        sources = "\n".join([f"- `{e.source_file}` (field: `{e.field_name}`)" for e in url_errors])
        error_info = url_errors[0]

        title = f"Broken link: {url[:80]}"
        body = f"""## Broken Link Detected

**URL:** {url}

**Status Code:** {error_info.status_code or 'N/A'}

**Error:** {error_info.error_message or 'Link is not accessible'}

**Found in:**
{sources}

**Detected:** {time.strftime('%Y-%m-%d %H:%M:%S')}

---
This issue was automatically created by the link checker.
"""

        # Create issue
        issue_data = {
            'title': title,
            'body': body,
            'labels': ['broken-link', 'automated']
        }

        try:
            response = requests.post(api_url, headers=headers, json=issue_data)
            if response.status_code == 201:
                issue_url = response.json()['html_url']
                print(f"  {Colors.GREEN}✓{Colors.RESET} Created issue: {issue_url}")
            else:
                print(f"  {Colors.RED}✗{Colors.RESET} Failed to create issue for {url}: {response.status_code}")
                if verbose:
                    print(f"    Response: {response.text}")
        except Exception as e:
            print(f"  {Colors.RED}✗{Colors.RESET} Error creating issue for {url}: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Check all links in the Ultimate Agent Directory repository",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Full check with default settings
  %(prog)s --yaml-only              # Check only YAML files (fast)
  %(prog)s --timeout 10             # Custom timeout (10 seconds)
  %(prog)s --no-issues              # Skip GitHub issue creation
  %(prog)s --verbose                # Show detailed output
        """
    )

    parser.add_argument(
        '--timeout',
        type=int,
        default=10,
        help='Request timeout in seconds (default: 10, optimized for 100Mbps home connection)'
    )

    parser.add_argument(
        '--retries',
        type=int,
        default=3,
        help='Number of retry attempts (default: 3)'
    )

    parser.add_argument(
        '--rate-limit',
        type=int,
        default=5,
        help='Max requests per second per domain (default: 5, prevents rate limiting on home connection)'
    )

    parser.add_argument(
        '--yaml-only',
        action='store_true',
        help='Check only YAML files (faster, skips docs/templates)'
    )

    parser.add_argument(
        '--no-issues',
        action='store_true',
        help='Skip GitHub issue creation (report only)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed output including warnings'
    )

    args = parser.parse_args()

    # Print banner
    print(f"\n{Colors.BOLD}{'='*60}")
    print("  Ultimate Agent Directory - Link Checker")
    print(f"{'='*60}{Colors.RESET}\n")

    # Collect URLs
    url_map = collect_all_urls(yaml_only=args.yaml_only, verbose=args.verbose)

    if not url_map:
        print(f"{Colors.YELLOW}No URLs found to check.{Colors.RESET}")
        return

    total_urls = sum(len(urls) for urls in url_map.values())
    print(f"Found {total_urls} URLs in {len(url_map)} files")

    # Check URLs
    results = asyncio.run(check_all_urls(
        url_map,
        timeout=args.timeout,
        retries=args.retries,
        rate_limit=args.rate_limit,
        verbose=args.verbose
    ))

    # Print results
    print_results(results, verbose=args.verbose)

    # Save report
    save_report(results)

    # Create GitHub issues (unless disabled)
    if not args.no_issues:
        create_github_issues(results, verbose=args.verbose)

    # Exit with appropriate code
    errors = [r for r in results if r.status == 'error']
    if errors:
        print(f"\n{Colors.RED}{Colors.BOLD}Link check FAILED: {len(errors)} broken links found{Colors.RESET}")
        sys.exit(1)
    else:
        print(f"\n{Colors.GREEN}{Colors.BOLD}All links are valid!{Colors.RESET}")
        sys.exit(0)


if __name__ == "__main__":
    main()

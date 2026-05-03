#!/usr/bin/env python3
"""
Link checker for Ultimate Agent Directory.

Scans all repository files (YAML, Markdown, templates, static assets) for URLs,
validates them with async HTTP requests, and reports broken links.

Usage:
    python scripts/check_links.py                    # Full check, report only
    python scripts/check_links.py --yaml-only        # Check only YAML files (fast)
    python scripts/check_links.py --file data/agents/example.yml
    python scripts/check_links.py --file-list changed-files.txt
    python scripts/check_links.py --timeout 10       # Custom timeout
    python scripts/check_links.py --create-issues    # Explicitly create GitHub issues
    python scripts/check_links.py --verbose          # Detailed logging
    python scripts/check_links.py --skip-domain localhost
    python scripts/check_links.py --skip-url https://example.com
"""

import asyncio
import argparse
import json
import os
import re
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote_plus, urlparse

import aiohttp
import yaml
from tqdm import tqdm

# Import local models for YAML parsing
try:
    from models import AgentEntry, BoilerplateEntry
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from models import AgentEntry, BoilerplateEntry


# ANSI color codes for terminal output
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


DEFAULT_SKIP_DOMAINS = {
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "yourdomain.com",
}

HTTP_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; UltimateAgentDirectoryLinkChecker/1.0; "
        "+https://github.com/moshehbenavraham/Ultimate-Agent-Directory)"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

GENERATED_MARKDOWN_FILES = {"README.md", "BOILERPLATES.md"}
LOW_VALUE_DOC_PATHS = {"docs/previous_changelogs"}


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
    domain_timestamps: Dict[str, List[float]] = field(
        default_factory=lambda: defaultdict(list)
    )

    async def wait_if_needed(self, url: str):
        """Wait if we've exceeded rate limit for this domain."""
        domain = urlparse(url).netloc
        now = time.time()

        # Remove timestamps older than 1 second
        self.domain_timestamps[domain] = [
            ts for ts in self.domain_timestamps[domain] if now - ts < 1.0
        ]

        # If we've hit the limit, wait
        if len(self.domain_timestamps[domain]) >= self.max_per_second:
            oldest = self.domain_timestamps[domain][0]
            wait_time = 1.0 - (now - oldest)
            if wait_time > 0:
                await asyncio.sleep(wait_time)

        # Record this request
        self.domain_timestamps[domain].append(time.time())


def normalize_extracted_url(raw_url: str) -> Optional[str]:
    """Normalize scanner-captured URLs without changing canonical YAML values."""
    url = str(raw_url).strip().strip("<>\"'")

    # Bare URL extraction often captures sentence punctuation. Keep balanced
    # parentheses so URLs like Wikipedia titles do not get damaged.
    while url:
        last_char = url[-1]
        if last_char in ".,;:!?\"'":
            url = url[:-1]
            continue
        if last_char == ")" and url.count(")") > url.count("("):
            url = url[:-1]
            continue
        if last_char == "]" and url.count("]") > url.count("["):
            url = url[:-1]
            continue
        if last_char == "}" and url.count("}") > url.count("{"):
            url = url[:-1]
            continue
        break

    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None
    return url


def add_normalized_url(urls: List[Tuple[str, str]], raw_url: str, context: str) -> None:
    """Append a URL if it normalizes to a usable HTTP(S) URL."""
    normalized = normalize_extracted_url(raw_url)
    if normalized:
        urls.append((normalized, context))


def markdown_reference_url(raw_url: str) -> str:
    """Return the URL part of a Markdown reference target."""
    raw_url = raw_url.strip()
    if raw_url.startswith("<") and ">" in raw_url:
        return raw_url[1 : raw_url.index(">")]
    return raw_url.split(maxsplit=1)[0]


def is_low_value_doc_path(path: Path, project_root: Path) -> bool:
    """Skip generated/historical docs that are not canonical link sources."""
    relative_path = path.relative_to(project_root).as_posix()
    return any(
        relative_path == prefix or relative_path.startswith(f"{prefix}/")
        for prefix in LOW_VALUE_DOC_PATHS
    )


def extract_urls_from_yaml(file_path: Path) -> List[Tuple[str, str]]:
    """
    Extract URLs from YAML files (agents and boilerplates).

    Returns:
        List of (url, field_name) tuples
    """
    urls: List[Tuple[str, str]] = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not data:
            return urls

        # Determine if this is a boilerplate or agent file based on path
        file_path_str = str(file_path)
        is_boilerplate = "boilerplates" in file_path_str

        # Check if it's an entry file (has url field) vs category file
        if "url" in data:
            try:
                if is_boilerplate:
                    bp_entry = BoilerplateEntry(**data)
                    add_normalized_url(urls, str(bp_entry.url), "url")
                    if bp_entry.documentation_url:
                        add_normalized_url(
                            urls, str(bp_entry.documentation_url), "documentation_url"
                        )
                    if bp_entry.demo_url:
                        add_normalized_url(urls, str(bp_entry.demo_url), "demo_url")
                    if bp_entry.github_repo:
                        github_url = f"https://github.com/{bp_entry.github_repo}"
                        add_normalized_url(urls, github_url, "github_repo")
                else:
                    agent_entry = AgentEntry(**data)
                    add_normalized_url(urls, str(agent_entry.url), "url")
                    if agent_entry.documentation_url:
                        add_normalized_url(
                            urls,
                            str(agent_entry.documentation_url),
                            "documentation_url",
                        )
                    if agent_entry.demo_url:
                        add_normalized_url(urls, str(agent_entry.demo_url), "demo_url")
                    if agent_entry.github_repo:
                        github_url = f"https://github.com/{agent_entry.github_repo}"
                        add_normalized_url(urls, github_url, "github_repo")

            except Exception:
                # If Pydantic validation fails, try manual extraction
                if "url" in data:
                    add_normalized_url(urls, data["url"], "url")
                if "documentation_url" in data:
                    add_normalized_url(
                        urls, data["documentation_url"], "documentation_url"
                    )
                if "demo_url" in data:
                    add_normalized_url(urls, data["demo_url"], "demo_url")
                if "github_repo" in data:
                    add_normalized_url(
                        urls,
                        f"https://github.com/{data['github_repo']}",
                        "github_repo",
                    )

    except Exception as e:
        print(
            f"  {Colors.YELLOW}Warning: Could not parse {file_path}: {e}{Colors.RESET}"
        )

    return urls


def extract_urls_from_markdown(file_path: Path) -> List[Tuple[str, str]]:
    """
    Extract URLs from Markdown files.

    Returns:
        List of (url, context) tuples
    """
    urls: List[Tuple[str, str]] = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Pattern 1: Inline links [text](url)
        inline_pattern = r"\[([^\]]+)\]\(([^)]+)\)"
        for match in re.finditer(inline_pattern, content):
            url = match.group(2)
            add_normalized_url(urls, url, f"inline:[{match.group(1)}]")

        # Pattern 2: Reference links [ref]: url
        reference_pattern = r"^\[([^\]]+)\]:\s*(.+)$"
        for match in re.finditer(reference_pattern, content, re.MULTILINE):
            url = markdown_reference_url(match.group(2))
            add_normalized_url(urls, url, f"reference:[{match.group(1)}]")

        # Pattern 3: Direct URLs (not in markdown links)
        # Exclude URLs already captured in patterns 1 and 2
        direct_pattern = r'(?<!\()https?://[^\s<>"{}|\\^`\[\]]+'
        captured_urls = {url for url, _ in urls}
        for match in re.finditer(direct_pattern, content):
            url = normalize_extracted_url(match.group(0))
            if url and url not in captured_urls:
                urls.append((url, "direct"))
                captured_urls.add(url)

    except Exception as e:
        print(
            f"  {Colors.YELLOW}Warning: Could not parse {file_path}: {e}{Colors.RESET}"
        )

    return urls


def extract_urls_from_template(file_path: Path) -> List[Tuple[str, str]]:
    """
    Extract URLs from Jinja2 template files.

    Returns:
        List of (url, context) tuples
    """
    urls: List[Tuple[str, str]] = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Pattern: Literal URLs in templates (not in variables)
        url_pattern = r'https?://[^\s"\'<>]+'
        for match in re.finditer(url_pattern, content):
            url = match.group(0)
            # Skip if it's inside a Jinja2 variable (contains {})
            if "{{" not in url and "}}" not in url:
                add_normalized_url(urls, url, "literal")

    except Exception as e:
        print(
            f"  {Colors.YELLOW}Warning: Could not parse {file_path}: {e}{Colors.RESET}"
        )

    return urls


def extract_urls_from_static(file_path: Path) -> List[Tuple[str, str]]:
    """
    Extract URLs from static files (CSS, JS).

    Returns:
        List of (url, context) tuples
    """
    urls: List[Tuple[str, str]] = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract all HTTP/HTTPS URLs
        url_pattern = r'https?://[^\s"\'<>)\]};]+'
        for match in re.finditer(url_pattern, content):
            add_normalized_url(urls, match.group(0), "static")

    except Exception as e:
        print(
            f"  {Colors.YELLOW}Warning: Could not parse {file_path}: {e}{Colors.RESET}"
        )

    return urls


def should_skip_url(url: str, skip_domains: set[str], skip_urls: set[str]) -> bool:
    if url in skip_urls:
        return True
    domain = urlparse(url).netloc.lower()
    if not domain:
        return False
    if ":" in domain:
        domain = domain.split(":", 1)[0]
    if domain == "example.com" or domain.endswith(".example.com"):
        return True
    if re.search(r"github\.com/(your-username|owner)/", url, re.IGNORECASE):
        return True
    if "YOUR-USERNAME" in url:
        return True
    return domain in skip_domains


def resolve_selected_files(
    project_root: Path, files: Optional[List[str]], verbose: bool = False
) -> Optional[List[Path]]:
    """Resolve user-provided paths to existing files inside the repository."""
    if files is None:
        return None

    selected_files: set[Path] = set()
    for raw_file in files:
        raw_file = raw_file.strip()
        if not raw_file:
            continue

        path = Path(raw_file)
        candidate = path if path.is_absolute() else project_root / path
        candidate = candidate.resolve()

        try:
            candidate.relative_to(project_root)
        except ValueError:
            if verbose:
                print(
                    f"  {Colors.YELLOW}Skipping path outside repo: {raw_file}{Colors.RESET}"
                )
            continue

        if not candidate.exists() or not candidate.is_file():
            if verbose:
                print(
                    f"  {Colors.YELLOW}Skipping missing/non-file path: {raw_file}{Colors.RESET}"
                )
            continue

        selected_files.add(candidate)

    return sorted(selected_files)


def collect_all_urls(
    yaml_only: bool = False,
    verbose: bool = False,
    files: Optional[List[str]] = None,
) -> Dict[str, List[Tuple[str, str]]]:
    """
    Collect all URLs from repository files.

    Returns:
        Dict mapping file paths to list of (url, field_name/context) tuples
    """
    project_root = Path(__file__).parent.parent.resolve()
    selected_files = resolve_selected_files(project_root, files, verbose=verbose)
    url_map: Dict[str, List[Tuple[str, str]]] = defaultdict(list)

    if verbose:
        print(f"\n{Colors.BOLD}Collecting URLs...{Colors.RESET}")
        if selected_files is not None:
            print(f"  Scanning selected files only ({len(selected_files)} files)...")

    # 1. YAML files (highest priority)
    if selected_files is None:
        yaml_pattern = "data/**/*.yml"
        yaml_files = list(project_root.glob(yaml_pattern))
    else:
        yaml_files = [
            file_path
            for file_path in selected_files
            if file_path.suffix in {".yml", ".yaml"}
        ]
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
    if selected_files is None:
        md_files = []
        # Root level markdown
        for md_file in project_root.glob("*.md"):
            # Skip generated markdown (redundant with YAML canonical sources)
            if md_file.name not in GENERATED_MARKDOWN_FILES:
                md_files.append(md_file)
        # Documentation markdown
        docs_dir = project_root / "docs"
        if docs_dir.exists():
            md_files.extend(
                file_path
                for file_path in docs_dir.glob("**/*.md")
                if not is_low_value_doc_path(file_path, project_root)
            )
    else:
        md_files = [file_path for file_path in selected_files if file_path.suffix == ".md"]

    if verbose:
        print(f"  Scanning {len(md_files)} Markdown files...")

    for md_file in md_files:
        urls = extract_urls_from_markdown(md_file)
        if urls:
            url_map[str(md_file.relative_to(project_root))] = urls

    # 3. Jinja2 templates
    if selected_files is None:
        templates_dir = project_root / "templates"
        template_files = []
        if templates_dir.exists():
            template_files = list(templates_dir.glob("*.jinja2")) + list(
                templates_dir.glob("*.html")
            )
    else:
        template_files = [
            file_path
            for file_path in selected_files
            if file_path.suffix in {".jinja2", ".html"}
        ]

    if verbose:
        print(f"  Scanning {len(template_files)} template files...")

    for template_file in template_files:
        urls = extract_urls_from_template(template_file)
        if urls:
            url_map[str(template_file.relative_to(project_root))] = urls

    # 4. Static assets (CSS, JS)
    if selected_files is None:
        static_dir = project_root / "static"
        static_files = []
        if static_dir.exists():
            static_files = list(static_dir.glob("**/*.css")) + list(
                static_dir.glob("**/*.js")
            )
    else:
        static_files = [
            file_path
            for file_path in selected_files
            if file_path.suffix in {".css", ".js"}
        ]

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
    verbose: bool = False,
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

    async def request(method: str) -> Tuple[int, Optional[str]]:
        async with session.request(
            method,
            url,
            timeout=aiohttp.ClientTimeout(total=timeout),
            allow_redirects=True,
            ssl=False,
        ) as response:
            return response.status, None

    for attempt in range(retries):
        try:
            status_code, error = await request("HEAD")
            if status_code < 400:
                return status_code, error

            # Many sites reject or mis-handle HEAD. Verify any failed HEAD
            # result with GET before reporting it.
            return await request("GET")

        except asyncio.TimeoutError:
            if attempt == retries - 1:
                return 0, "Timeout"
            await asyncio.sleep(2**attempt)  # Exponential backoff

        except aiohttp.ClientError as e:
            # Try GET request if HEAD fails at the client/protocol layer.
            try:
                return await request("GET")
            except Exception:
                pass

            if attempt == retries - 1:
                return 0, str(e)
            await asyncio.sleep(2**attempt)

        except Exception as e:
            if attempt == retries - 1:
                return 0, f"Unexpected error: {str(e)}"
            await asyncio.sleep(2**attempt)

    return 0, "Max retries exceeded"


def classify_link_result(status_code: int, error_msg: Optional[str]) -> str:
    """Classify results conservatively to avoid false broken-link claims."""
    if status_code == 0:
        if error_msg and (
            "Name or service not known" in error_msg
            or "No address associated with hostname" in error_msg
        ):
            return "error"
        return "warning"
    if status_code < 400:
        return "success"
    if status_code in {404, 410}:
        return "error"
    return "warning"


async def check_all_urls(
    url_map: Dict[str, List[Tuple[str, str]]],
    timeout: int,
    retries: int,
    rate_limit: int,
    skip_domains: set[str],
    skip_urls: set[str],
    verbose: bool = False,
) -> List[URLCheck]:
    """
    Check all URLs asynchronously with rate limiting.

    Returns:
        List of URLCheck results
    """
    results = []
    rate_limiter = RateLimiter(max_per_second=rate_limit)
    skip_domains = {domain.lower() for domain in skip_domains}
    skip_urls = {url.strip() for url in skip_urls if url.strip()}

    # Flatten URL map to list of (url, file, field_name) tuples
    url_checks = []
    for file_path, urls in url_map.items():
        for url, field_name in urls:
            url_checks.append((url, file_path, field_name))

    # Deduplicate URLs while preserving source information
    url_to_sources = defaultdict(list)
    skipped = 0
    for url, file_path, field_name in url_checks:
        if should_skip_url(url, skip_domains, skip_urls):
            skipped += 1
            if verbose:
                print(f"  Skipping URL by rule: {url}")
            continue
        url_to_sources[url].append((file_path, field_name))

    unique_urls = list(url_to_sources.keys())

    print(f"\n{Colors.BOLD}Checking {len(unique_urls)} unique URLs...{Colors.RESET}")
    if skipped:
        print(f"Skipping {skipped} URLs due to skip rules")

    # Create aiohttp session
    connector = aiohttp.TCPConnector(limit=100, limit_per_host=10)
    async with aiohttp.ClientSession(
        connector=connector,
        headers=HTTP_HEADERS,
        max_line_size=65536,
        max_field_size=65536,
    ) as session:
        # Create progress bar
        with tqdm(total=len(unique_urls), desc="Progress", unit="url") as pbar:
            # Check URLs in batches to avoid overwhelming the system
            batch_size = 50
            for i in range(0, len(unique_urls), batch_size):
                batch = unique_urls[i : i + batch_size]

                # Create tasks for this batch
                tasks = [
                    check_url(session, url, timeout, retries, rate_limiter, verbose)
                    for url in batch
                ]

                # Wait for all tasks in batch to complete
                batch_results = await asyncio.gather(*tasks)

                # Process results
                for url, (status_code, error_msg) in zip(batch, batch_results):
                    status = classify_link_result(status_code, error_msg)

                    # Create URLCheck for each source
                    for file_path, field in url_to_sources[url]:
                        # Determine source type
                        if file_path.endswith(".yml") or file_path.endswith(".yaml"):
                            source_type = "yaml"
                        elif file_path.endswith(".md"):
                            source_type = "markdown"
                        elif ".jinja" in file_path or file_path.endswith(".html"):
                            source_type = "template"
                        else:
                            source_type = "static"

                        results.append(
                            URLCheck(
                                url=url,
                                status=status,
                                status_code=status_code,
                                error_message=error_msg,
                                source_file=file_path,
                                source_type=source_type,
                                field_name=field,
                            )
                        )

                pbar.update(len(batch))

    return results


def print_results(results: List[URLCheck], verbose: bool = False):
    """Print check results to terminal with color coding."""
    # Group by status
    success = [r for r in results if r.status == "success"]
    warnings = [r for r in results if r.status == "warning"]
    errors = [r for r in results if r.status == "error"]

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

    print(f"{Colors.GREEN}[OK] Passed:{Colors.RESET} {len(success)}")
    print(f"{Colors.YELLOW}[WARN] Warnings:{Colors.RESET} {len(warnings)}")
    print(f"{Colors.RED}[FAIL] Failed:{Colors.RESET} {len(errors)}\n")

    # Show errors
    if unique_errors:
        print(f"{Colors.RED}{Colors.BOLD}Failed Links:{Colors.RESET}")
        for url, result in unique_errors.items():
            sources = [r.source_file for r in errors if r.url == url]
            print(f"  {Colors.RED}[FAIL]{Colors.RESET} {url}")
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
            print(f"  {Colors.YELLOW}[WARN]{Colors.RESET} {url}")
            print(f"    Status: {result.status_code}")
            print(f"    Found in: {', '.join(set(sources))}")
            print()


def save_report(
    results: List[URLCheck], output_file: str = "reports/link-check-report.json"
):
    """Save detailed results to JSON file."""
    project_root = Path(__file__).parent.parent
    output_path = project_root / output_file

    # Create reports directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "summary": {
            "total": len(results),
            "success": len([r for r in results if r.status == "success"]),
            "warnings": len([r for r in results if r.status == "warning"]),
            "errors": len([r for r in results if r.status == "error"]),
        },
        "results": [
            {
                "url": r.url,
                "status": r.status,
                "status_code": r.status_code,
                "error_message": r.error_message,
                "source_file": r.source_file,
                "source_type": r.source_type,
                "field_name": r.field_name,
            }
            for r in results
        ],
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"{Colors.BLUE}Report saved to: {output_file}{Colors.RESET}")


def create_github_issues(results: List[URLCheck], verbose: bool = False):
    """Create GitHub issues for broken links."""
    errors = [r for r in results if r.status == "error"]

    if not errors:
        print(f"{Colors.GREEN}No broken links to report!{Colors.RESET}")
        return

    # Check for GitHub token
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        print(
            f"{Colors.YELLOW}Warning: GITHUB_TOKEN not found. Skipping issue creation.{Colors.RESET}"
        )
        print("To create issues, set GITHUB_TOKEN environment variable.")
        return

    # Group errors by URL to avoid duplicate issues
    unique_errors: Dict[str, List[URLCheck]] = {}
    for result in errors:
        if result.url not in unique_errors:
            unique_errors[result.url] = []
        unique_errors[result.url].append(result)

    print(
        f"\n{Colors.BOLD}Creating GitHub issues for {len(unique_errors)} broken links...{Colors.RESET}"
    )

    # Import requests for GitHub API
    import requests

    # Detect repository from git config or environment
    repo = os.environ.get(
        "GITHUB_REPOSITORY", "moshehbenavraham/Ultimate-Agent-Directory"
    )
    api_url = f"https://api.github.com/repos/{repo}/issues"

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    for url, url_errors in unique_errors.items():
        # Check if issue already exists
        query = quote_plus(f'repo:{repo} is:issue is:open in:title "{url}"')
        search_url = f"https://api.github.com/search/issues?q={query}"
        try:
            response = requests.get(search_url, headers=headers)
            if response.status_code == 200:
                existing = response.json()
                if existing["total_count"] > 0:
                    if verbose:
                        print(f"  Issue already exists for: {url}")
                    continue
        except Exception as e:
            if verbose:
                print(f"  Warning: Could not check for existing issue: {e}")

        # Prepare issue body
        sources = "\n".join(
            [f"- `{e.source_file}` (field: `{e.field_name}`)" for e in url_errors]
        )
        error_info = url_errors[0]

        title = f"Broken link: {url[:80]}"
        body = f"""## Broken Link Detected

**URL:** {url}

**Status Code:** {error_info.status_code or "N/A"}

**Error:** {error_info.error_message or "Link is not accessible"}

**Found in:**
{sources}

**Detected:** {time.strftime("%Y-%m-%d %H:%M:%S")}

---
This issue was automatically created by the link checker.
"""

        # Create issue
        issue_data = {
            "title": title,
            "body": body,
            "labels": ["broken-link", "automated"],
        }

        try:
            response = requests.post(api_url, headers=headers, json=issue_data)
            if response.status_code == 201:
                issue_url = response.json()["html_url"]
                print(f"  {Colors.GREEN}[OK]{Colors.RESET} Created issue: {issue_url}")
            else:
                print(
                    f"  {Colors.RED}[FAIL]{Colors.RESET} Failed to create issue for {url}: {response.status_code}"
                )
                if verbose:
                    print(f"    Response: {response.text}")
        except Exception as e:
            print(f"  {Colors.RED}[FAIL]{Colors.RESET} Error creating issue for {url}: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Check all links in the Ultimate Agent Directory repository",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Full check with default settings
  %(prog)s --yaml-only              # Check only YAML files (fast)
  %(prog)s --file data/agents/example.yml
  %(prog)s --file-list changed-files.txt
  %(prog)s --timeout 10             # Custom timeout (10 seconds)
  %(prog)s --create-issues          # Create GitHub issues for confirmed failures
  %(prog)s --verbose                # Show detailed output
        """,
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Request timeout in seconds (default: 10, optimized for 100Mbps home connection)",
    )

    parser.add_argument(
        "--retries", type=int, default=3, help="Number of retry attempts (default: 3)"
    )

    parser.add_argument(
        "--rate-limit",
        type=int,
        default=5,
        help="Max requests per second per domain (default: 5, prevents rate limiting on home connection)",
    )

    parser.add_argument(
        "--skip-domain",
        action="append",
        default=[],
        help="Domain to skip (repeatable)",
    )

    parser.add_argument(
        "--skip-url",
        action="append",
        default=[],
        help="Exact URL to skip (repeatable)",
    )

    parser.add_argument(
        "--yaml-only",
        action="store_true",
        help="Check only YAML files (faster, skips docs/templates)",
    )

    parser.add_argument(
        "--file",
        action="append",
        default=[],
        help="Specific repository file to scan (repeatable)",
    )

    parser.add_argument(
        "--file-list",
        action="append",
        default=[],
        help="File containing newline-separated repository paths to scan (repeatable)",
    )

    parser.add_argument(
        "--no-issues",
        action="store_true",
        help="Deprecated compatibility flag; issue creation is disabled by default",
    )

    parser.add_argument(
        "--create-issues",
        action="store_true",
        help="Create GitHub issues for confirmed broken links",
    )

    parser.add_argument(
        "--verbose", action="store_true", help="Show detailed output including warnings"
    )

    args = parser.parse_args()

    selected_mode = bool(args.file or args.file_list)
    selected_files = list(args.file)
    for file_list in args.file_list:
        try:
            with open(file_list, "r", encoding="utf-8") as f:
                selected_files.extend(line.strip() for line in f)
        except OSError as exc:
            parser.error(f"Could not read --file-list {file_list}: {exc}")

    # Print banner
    print(f"\n{Colors.BOLD}{'=' * 60}")
    print("  Ultimate Agent Directory - Link Checker")
    print(f"{'=' * 60}{Colors.RESET}\n")

    # Collect URLs
    url_map = collect_all_urls(
        yaml_only=args.yaml_only,
        verbose=args.verbose,
        files=selected_files if selected_mode else None,
    )

    if not url_map:
        print(f"{Colors.YELLOW}No URLs found to check.{Colors.RESET}")
        return

    total_urls = sum(len(urls) for urls in url_map.values())
    print(f"Found {total_urls} URLs in {len(url_map)} files")

    skip_domains = set(DEFAULT_SKIP_DOMAINS)
    skip_domains.update(args.skip_domain)
    skip_urls = set(args.skip_url)

    # Check URLs
    results = asyncio.run(
        check_all_urls(
            url_map,
            timeout=args.timeout,
            retries=args.retries,
            rate_limit=args.rate_limit,
            skip_domains=skip_domains,
            skip_urls=skip_urls,
            verbose=args.verbose,
        )
    )

    # Print results
    print_results(results, verbose=args.verbose)

    # Save report
    save_report(results)

    # Create GitHub issues only when explicitly requested.
    if args.create_issues:
        create_github_issues(results, verbose=args.verbose)
    elif args.verbose and not args.no_issues:
        print(
            f"{Colors.BLUE}GitHub issue creation disabled "
            f"(use --create-issues to opt in).{Colors.RESET}"
        )

    # Exit with appropriate code
    errors = [r for r in results if r.status == "error"]
    if errors:
        print(
            f"\n{Colors.RED}{Colors.BOLD}Link check FAILED: {len(errors)} broken links found{Colors.RESET}"
        )
        sys.exit(1)
    else:
        print(f"\n{Colors.GREEN}{Colors.BOLD}All links are valid!{Colors.RESET}")
        sys.exit(0)


if __name__ == "__main__":
    main()

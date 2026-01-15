#!/usr/bin/env python3
"""
Refresh GitHub metadata for agent and boilerplate entries.

Usage:
  python scripts/update_github_metadata.py
  python scripts/update_github_metadata.py --agents
  python scripts/update_github_metadata.py --boilerplates
  python scripts/update_github_metadata.py --dry-run --limit 25
  python scripts/update_github_metadata.py data/agents/open-source-frameworks
"""

import argparse
import os
import sys
import time
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Optional

import requests
import yaml


@dataclass
class RepoMetadata:
    stars: Optional[int]
    last_updated: Optional[date]
    is_archived: Optional[bool]


class RateLimitError(RuntimeError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Refresh GitHub metadata fields for YAML entries."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Optional files or directories to update",
    )
    parser.add_argument("--agents", action="store_true", help="Update agent entries")
    parser.add_argument(
        "--boilerplates", action="store_true", help="Update boilerplate entries"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show updates without writing files",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Limit number of entries processed (0 for no limit)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=20,
        help="HTTP request timeout in seconds (default: 20)",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.0,
        help="Seconds to sleep between requests (default: 0)",
    )
    parser.add_argument(
        "--token",
        help="GitHub token (or set GITHUB_TOKEN or GH_TOKEN)",
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    return parser.parse_args()


def build_include_map(args: argparse.Namespace) -> dict[str, bool]:
    include = {
        "agent": args.agents,
        "boilerplate": args.boilerplates,
    }
    if any(include.values()):
        return include
    return {key: True for key in include}


def is_yaml_file(filepath: Path) -> bool:
    return filepath.suffix in {".yml", ".yaml"}


def get_entry_kind(filepath: Path, data_dir: Path) -> Optional[str]:
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
    if root == "boilerplates":
        return "boilerplate"
    return None


def collect_entry_files(
    paths: list[str], data_dir: Path, include: dict[str, bool]
) -> tuple[list[Path], list[str]]:
    collected: list[Path] = []
    errors: list[str] = []

    def add_file(file_path: Path, is_explicit: bool) -> None:
        if file_path.name == ".gitkeep" or not is_yaml_file(file_path):
            return
        kind = get_entry_kind(file_path, data_dir)
        if kind is None:
            if is_explicit:
                errors.append(f"ERROR Path outside data directory: {file_path}")
            return
        if not include.get(kind, False):
            return
        collected.append(file_path)

    if not paths:
        if include["agent"]:
            collected.extend(data_dir.glob("agents/**/*.yml"))
            collected.extend(data_dir.glob("agents/**/*.yaml"))
        if include["boilerplate"]:
            collected.extend(data_dir.glob("boilerplates/**/*.yml"))
            collected.extend(data_dir.glob("boilerplates/**/*.yaml"))
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

    return sorted(set(collected)), errors


def load_yaml_data(filepath: Path) -> dict:
    with open(filepath, "r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if data is None:
        raise ValueError("Empty YAML file")
    if not isinstance(data, dict):
        raise ValueError("YAML content must be a mapping")
    return data


def normalize_repo(repo: str) -> str:
    repo = repo.strip()
    if repo.startswith("https://github.com/"):
        repo = repo.replace("https://github.com/", "", 1)
    if repo.endswith(".git"):
        repo = repo[:-4]
    return repo


def parse_github_date(value: Optional[str]) -> Optional[date]:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").date()
    except ValueError:
        return None


def fetch_repo_metadata(
    session: requests.Session,
    repo: str,
    headers: dict[str, str],
    timeout: int,
) -> RepoMetadata:
    url = f"https://api.github.com/repos/{repo}"
    response = session.get(url, headers=headers, timeout=timeout)

    if response.status_code == 403 and response.headers.get("X-RateLimit-Remaining") == "0":
        reset = response.headers.get("X-RateLimit-Reset")
        message = "GitHub API rate limit exceeded"
        if reset:
            message = f"{message}. Reset at {reset}"
        raise RateLimitError(message)

    if response.status_code == 404:
        return RepoMetadata(stars=None, last_updated=None, is_archived=None)

    if response.status_code != 200:
        return RepoMetadata(stars=None, last_updated=None, is_archived=None)

    data = response.json()
    stars = data.get("stargazers_count")
    archived = data.get("archived")
    pushed_at = data.get("pushed_at")

    stars_value = int(stars) if isinstance(stars, int) else None
    archived_value = bool(archived) if isinstance(archived, bool) else None
    last_updated = parse_github_date(pushed_at)

    return RepoMetadata(
        stars=stars_value, last_updated=last_updated, is_archived=archived_value
    )


def normalize_existing_date(value: object) -> Optional[str]:
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, str):
        return value
    return None


def normalize_existing_int(value: object) -> Optional[int]:
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return None


def format_yaml_value(key: str, value: object) -> Optional[str]:
    if value is None:
        return None
    if key == "last_updated":
        if isinstance(value, date):
            return f"{key}: '{value.isoformat()}'"
        return f"{key}: '{value}'"
    if isinstance(value, bool):
        return f"{key}: {'true' if value else 'false'}"
    return f"{key}: {value}"


def find_key_line(lines: list[str], key: str) -> Optional[int]:
    for index, line in enumerate(lines):
        if line.startswith(f"{key}:"):
            return index
    return None


def update_entry_lines(
    lines: list[str],
    updates: dict[str, object],
    anchor_keys: list[str],
) -> tuple[list[str], bool]:
    changed = False
    insert_after = None
    for key in anchor_keys:
        index = find_key_line(lines, key)
        if index is not None:
            insert_after = index

    ordered_keys = [key for key in ["github_stars", "last_updated", "is_archived"] if key in updates]

    for key in ordered_keys:
        new_line = format_yaml_value(key, updates[key])
        if new_line is None:
            continue
        index = find_key_line(lines, key)
        if index is not None:
            if lines[index] != new_line:
                lines[index] = new_line
                changed = True
            continue
        if insert_after is None:
            lines.append(new_line)
        else:
            insert_after += 1
            lines.insert(insert_after, new_line)
        changed = True

    return lines, changed


def build_updates(data: dict, metadata: RepoMetadata) -> dict[str, object]:
    updates: dict[str, object] = {}

    if metadata.stars is not None:
        existing = normalize_existing_int(data.get("github_stars"))
        if existing != metadata.stars:
            updates["github_stars"] = metadata.stars

    if metadata.last_updated is not None:
        existing_date = normalize_existing_date(data.get("last_updated"))
        if existing_date != metadata.last_updated.isoformat():
            updates["last_updated"] = metadata.last_updated

    if metadata.is_archived is not None:
        existing_archived = data.get("is_archived")
        if existing_archived is None or existing_archived != metadata.is_archived:
            updates["is_archived"] = metadata.is_archived

    return updates


def update_entry_file(path: Path, updates: dict[str, object], dry_run: bool) -> bool:
    if not updates:
        return False
    original_text = path.read_text(encoding="utf-8")
    has_trailing_newline = original_text.endswith("\n")
    lines = original_text.splitlines()

    updated_lines, changed = update_entry_lines(
        lines, updates, anchor_keys=["github_repo", "github_stars", "last_updated"]
    )
    if not changed:
        return False

    updated_text = "\n".join(updated_lines)
    if has_trailing_newline:
        updated_text += "\n"

    if dry_run:
        return True

    path.write_text(updated_text, encoding="utf-8")
    return True


def main() -> None:
    args = parse_args()
    data_dir = Path("data")
    if not data_dir.exists():
        print("ERROR: data/ directory not found")
        sys.exit(1)

    include = build_include_map(args)
    files, path_errors = collect_entry_files(args.paths, data_dir, include)

    if path_errors:
        print("\n".join(path_errors))
        sys.exit(1)

    if not files:
        print("No entry files found to update")
        sys.exit(0)

    token = args.token or os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "ultimate-agent-directory",
    }
    if token:
        headers["Authorization"] = f"token {token}"

    session = requests.Session()

    repo_cache: dict[str, RepoMetadata] = {}
    processed = 0
    updated = 0
    skipped = 0
    errors = 0

    for filepath in files:
        if args.limit and processed >= args.limit:
            break
        try:
            data = load_yaml_data(filepath)
        except Exception as exc:
            print(f"ERROR {filepath}: {exc}")
            errors += 1
            continue

        repo = data.get("github_repo")
        if not repo:
            skipped += 1
            continue

        repo = normalize_repo(str(repo))
        if "/" not in repo:
            if args.verbose:
                print(f"Skipping invalid github_repo in {filepath}: {repo}")
            skipped += 1
            continue

        processed += 1

        if repo in repo_cache:
            metadata = repo_cache[repo]
        else:
            try:
                metadata = fetch_repo_metadata(session, repo, headers, args.timeout)
            except RateLimitError as exc:
                print(f"ERROR: {exc}")
                break
            except Exception as exc:
                print(f"ERROR {filepath}: {exc}")
                errors += 1
                continue
            repo_cache[repo] = metadata

        updates = build_updates(data, metadata)
        if not updates:
            if args.verbose:
                print(f"No changes for {filepath}")
            continue

        if update_entry_file(filepath, updates, args.dry_run):
            updated += 1
            if args.verbose or args.dry_run:
                change_list = ", ".join(sorted(updates.keys()))
                print(f"Updated {filepath} ({change_list})")

        if args.sleep:
            try:
                time.sleep(args.sleep)
            except Exception:
                pass

    print(
        "Summary: "
        f"processed={processed} "
        f"updated={updated} "
        f"skipped={skipped} "
        f"errors={errors}"
    )


if __name__ == "__main__":
    main()

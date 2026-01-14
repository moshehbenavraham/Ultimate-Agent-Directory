from pathlib import Path
import yaml

from models import SiteConfig


DEFAULT_METADATA_PATH = Path("data/metadata.yml")


def load_site_config(path: Path = DEFAULT_METADATA_PATH) -> SiteConfig:
    if not path.exists():
        raise FileNotFoundError(f"Missing site metadata file: {path}")
    with open(path, "r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError("Site metadata must be a mapping")
    return SiteConfig(**data)

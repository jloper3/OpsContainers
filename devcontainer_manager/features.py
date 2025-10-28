"""Feature catalog management."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping

import yaml

Feature = Mapping[str, object]


def load_features(path: str | Path) -> list[Feature]:
    """Load feature metadata from a YAML catalog."""

    catalog_path = Path(path)
    if not catalog_path.is_file():
        raise FileNotFoundError(f"Feature catalog not found: {catalog_path}")
    data = yaml.safe_load(catalog_path.read_text())
    if not isinstance(data, list):
        raise ValueError("Feature catalog must be a list of feature mappings")
    for entry in data:
        if not isinstance(entry, Mapping):
            raise ValueError("Feature catalog entries must be mappings")
    return data


def list_feature_names(features: Iterable[Feature]) -> list[str]:
    """Return the display names for ``features`` for convenience methods."""

    return [str(feature.get("name", "Unnamed Feature")) for feature in features]

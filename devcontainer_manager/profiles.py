"""Profile persistence helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping

ProfileData = Mapping[str, object]


def save_profile(path: Path, name: str, data: ProfileData) -> Path:
    """Persist ``data`` in ``path`` using the ``name`` as file stem."""

    path.mkdir(parents=True, exist_ok=True)
    file = path / f"{name}.json"
    file.write_text(json.dumps(data, indent=2) + "\n")
    return file


def load_profiles(path: Path) -> dict[str, ProfileData]:
    """Load all saved profiles from ``path``."""

    if not path.is_dir():
        return {}
    profiles: dict[str, ProfileData] = {}
    for file in sorted(path.glob("*.json")):
        profiles[file.stem] = json.loads(file.read_text())
    return profiles


def merge_profile(devcontainer: Mapping[str, object], profile: ProfileData) -> dict:
    """Return a new devcontainer configuration with ``profile`` applied."""

    merged = dict(devcontainer)
    merged.update(profile)
    return merged

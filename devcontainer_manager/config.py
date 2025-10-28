"""Configuration helpers for the devcontainer manager."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ManagerConfig:
    """Runtime configuration for the manager application."""

    workspace: Path
    catalog_path: Path
    profiles_dir: Path

    @classmethod
    def default(cls, workspace: Path) -> "ManagerConfig":
        """Return a configuration using conventional paths."""

        catalog = workspace / "features.yml"
        profiles = workspace / ".profiles"
        return cls(workspace=workspace, catalog_path=catalog, profiles_dir=profiles)

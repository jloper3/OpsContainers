"""Core business logic for reading and updating ``devcontainer.json`` files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Mapping

Devcontainer = Mapping[str, object]
FeatureSelection = Mapping[str, object]


class DevcontainerNotFoundError(FileNotFoundError):
    """Raised when a ``devcontainer.json`` file cannot be located."""


def load_devcontainer(path: Path) -> Devcontainer:
    """Load a ``devcontainer.json`` file from ``path``.

    Parameters
    ----------
    path:
        The workspace directory containing the ``.devcontainer`` folder.

    Raises
    ------
    DevcontainerNotFoundError
        If the ``devcontainer.json`` file cannot be found.
    json.JSONDecodeError
        If the file contents are not valid JSON.
    """

    file = path / ".devcontainer" / "devcontainer.json"
    if not file.is_file():
        raise DevcontainerNotFoundError(f"No devcontainer.json found at {file}")
    return json.loads(file.read_text())


def save_devcontainer(path: Path, data: Mapping[str, object]) -> Path:
    """Persist ``data`` into the ``devcontainer.json`` file under ``path``.

    The JSON output is written using a stable two-space indentation.
    The target directory is created if it does not yet exist.
    """

    directory = path / ".devcontainer"
    directory.mkdir(parents=True, exist_ok=True)
    file = directory / "devcontainer.json"
    file.write_text(json.dumps(data, indent=2) + "\n")
    return file


def update_features(
    devcontainer: Mapping[str, object],
    selected_features: Iterable[FeatureSelection],
) -> dict:
    """Return a copy of ``devcontainer`` with ``selected_features`` applied.

    Each selected feature must provide a ``reference`` key that maps to the
    feature's image reference.  The resulting ``features`` section will be a
    dictionary keyed by reference with empty configuration objects, matching the
    expectation of the Dev Container specification.
    """

    updated = dict(devcontainer)
    features = {**updated.get("features", {})}
    for feature in selected_features:
        reference = feature.get("reference")
        if not reference:
            raise ValueError("Each feature selection must include a 'reference' key")
        features[reference] = feature.get("options", {})
    updated["features"] = features
    return updated

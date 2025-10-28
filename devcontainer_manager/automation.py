"""Automation layer that shells out to the ``devcontainer`` CLI."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Sequence


class DevcontainerCLIError(RuntimeError):
    """Raised when the ``devcontainer`` CLI exits with a failure status."""


def run_devcontainer(command: Sequence[str], workspace: Path) -> None:
    """Execute a ``devcontainer`` CLI command within ``workspace``.

    Parameters
    ----------
    command:
        Iterable of arguments, e.g. ("build",).
    workspace:
        The directory to execute the command within.
    """

    args = ["devcontainer", *command, "--workspace-folder", str(workspace)]
    process = subprocess.run(args, check=False)
    if process.returncode != 0:
        raise DevcontainerCLIError(
            f"devcontainer {' '.join(command)} failed with exit code {process.returncode}"
        )

"""Command line interface for the devcontainer manager."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from rich import print as rprint
from rich.prompt import Confirm, Prompt
from rich.table import Table

from . import automation, core, features, profiles
from .config import ManagerConfig


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path("."), help="Workspace root")
    parser.add_argument("--catalog", type=Path, help="Override feature catalog path")
    parser.add_argument("--from-profile", dest="from_profile", help="Profile name to load")
    parser.add_argument("--save-profile", dest="save_profile", help="Save configuration")
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Automatically trigger a devcontainer build after saving",
    )
    return parser


def display_catalog(catalog: Iterable[features.Feature]) -> None:
    table = Table(title="Available Features")
    table.add_column("Index", justify="right")
    table.add_column("Name")
    table.add_column("Description")

    for i, feature in enumerate(catalog):
        table.add_row(str(i), str(feature.get("name", "Unnamed")), str(feature.get("description", "")))

    rprint(table)


def prompt_for_features(catalog: list[features.Feature]) -> list[features.Feature]:
    if not catalog:
        return []

    display_catalog(catalog)
    raw = Prompt.ask("Enter comma-separated feature indices", default="")
    selections: list[features.Feature] = []
    for item in filter(None, (chunk.strip() for chunk in raw.split(","))):
        try:
            index = int(item)
        except ValueError as exc:
            raise SystemExit(f"Invalid feature index: {item}") from exc
        try:
            selections.append(catalog[index])
        except IndexError as exc:
            raise SystemExit(f"Invalid feature index: {index}") from exc
    return selections


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    workspace = args.workspace.resolve()
    config = ManagerConfig.default(workspace)
    if args.catalog:
        config.catalog_path = args.catalog

    catalog = list(features.load_features(config.catalog_path))

    try:
        devcontainer = core.load_devcontainer(workspace)
    except core.DevcontainerNotFoundError:
        devcontainer = {}

    if args.from_profile:
        all_profiles = profiles.load_profiles(config.profiles_dir)
        try:
            devcontainer = profiles.merge_profile(devcontainer, all_profiles[args.from_profile])
        except KeyError as exc:
            raise SystemExit(f"Unknown profile: {args.from_profile}") from exc

    selected = prompt_for_features(catalog)
    updated = core.update_features(devcontainer, selected)
    saved_path = core.save_devcontainer(workspace, updated)
    rprint(f"Saved updated devcontainer to [bold]{saved_path}[/bold]")

    if args.save_profile:
        file = profiles.save_profile(config.profiles_dir, args.save_profile, updated)
        rprint(f"Saved profile to [bold]{file}[/bold]")

    rebuild = args.rebuild or Confirm.ask("Rebuild the Dev Container now?", default=False)
    if rebuild:
        automation.run_devcontainer(("build",), workspace)
        rprint("devcontainer build triggered")

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

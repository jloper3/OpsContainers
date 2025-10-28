# Devcontainer Manager Prototype

This repository experiments with a thin management layer around `devcontainer.json`
files.  It exposes both a CLI and supporting modules that make it easier to enable
optional features sourced from the [devcontainers/features](https://github.com/devcontainers/features) registry.

## Quick start

```bash
pip install -e .
devcontainer-manager --workspace /path/to/project
```

The CLI will present an interactive list of available features defined in
`features.yml`, update the workspace `.devcontainer/devcontainer.json`, and offer
to trigger a `devcontainer build` automatically.

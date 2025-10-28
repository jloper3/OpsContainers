.PHONY: install lint format

install:
	pip install -e .

lint:
	uv run ruff check devcontainer_manager

format:
	uv run ruff format devcontainer_manager

.PHONY: ruff mypy prettier pytest
ruff:
	@uv run ruff check --fix .
	@uv run ruff format .

prettier:
	@npx prettier . --write

mypy:
	@uv run mypy src/

pytest:
	@uv run pytest -v tests/
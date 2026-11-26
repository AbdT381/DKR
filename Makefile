.PHONY: install test lint run clean

install:
	pip install -e ".[dev]"

test:
	pytest -v

lint:
	ruff check src tests

run:
	python -m src.cli --help

clean:
	rm -rf build dist *.egg-info .pytest_cache .ruff_cache

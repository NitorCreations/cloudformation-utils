.PHONY: help install install-dev test lint format type-check clean build upload pre-commit

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package
	pip install -e .

install-dev: ## Install development dependencies
	pip install -e .[dev]
	pre-commit install

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage report
	pytest --cov-report=html --cov-report=term

lint: ## Run linting
	ruff check .

format: ## Format code
	ruff format .

format-check: ## Check code formatting
	ruff format --check .

type-check: ## Run type checking
	mypy cloudformation_utils

quality: lint format-check type-check ## Run all quality checks

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean ## Build the package
	python -m build

check-build: build ## Build and check the package
	twine check dist/*

upload-test: build ## Upload to Test PyPI
	twine upload --repository testpypi dist/*

upload: build ## Upload to PyPI
	twine upload dist/*

pre-commit: ## Run pre-commit on all files
	pre-commit run --all-files

setup-dev: install-dev ## Setup development environment
	@echo "Development environment setup complete!"
	@echo "Run 'make help' to see available commands."
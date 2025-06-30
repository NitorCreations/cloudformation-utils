# CloudFormation Utils

[![CI](https://github.com/NitorCreations/cloudformation-utils/actions/workflows/ci.yml/badge.svg)](https://github.com/NitorCreations/cloudformation-utils/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/cloudformation-utils.svg)](https://badge.fury.io/py/cloudformation-utils)
[![Python versions](https://img.shields.io/pypi/pyversions/cloudformation-utils.svg)](https://pypi.org/project/cloudformation-utils/)
[![License](https://img.shields.io/pypi/l/cloudformation-utils.svg)](https://github.com/NitorCreations/cloudformation-utils/blob/main/LICENSE)

A Python library for reading, writing and pre-processing CloudFormation YAML stacks.

## Features

- Read and write CloudFormation templates in YAML format
- Pre-process templates with custom logic
- Validate template structure
- Support for modern Python versions (3.8+)

## Installation

Install from PyPI:

```bash
pip install cloudformation-utils
```

For development:

```bash
git clone https://github.com/NitorCreations/cloudformation-utils.git
cd cloudformation-utils
make setup-dev
```

## Usage

```python
import cloudformation_utils

# Your usage examples here
```

## Development

This project uses modern Python packaging and development tools:

### Setup Development Environment

```bash
make setup-dev
```

This will:
- Install the package in development mode
- Install all development dependencies
- Set up pre-commit hooks

### Available Commands

```bash
make help                # Show all available commands
make test               # Run tests
make test-cov           # Run tests with coverage
make lint               # Run linting
make format             # Format code
make type-check         # Run type checking
make quality            # Run all quality checks
make build              # Build the package
make clean              # Clean build artifacts
```

### Code Quality

This project uses:
- **[Ruff](https://github.com/astral-sh/ruff)** for linting and formatting
- **[MyPy](https://mypy.readthedocs.io/)** for type checking
- **[pytest](https://pytest.org/)** for testing
- **[pre-commit](https://pre-commit.com/)** for git hooks

### Testing

Run tests:
```bash
make test
```

Run tests with coverage:
```bash
make test-cov
```

### Releasing

Releases are automated via GitHub Actions when you push a tag:

```bash
git tag v0.0.4  # Next version after current 0.0.3
git push origin v0.0.4
```

## Requirements

- Python 3.8 or higher
- PyYAML 6.0 or higher

## License

This project is licensed under the Apache License, Version 2.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the test suite and quality checks
5. Submit a pull request

Please ensure your code follows the project's coding standards and includes appropriate tests.
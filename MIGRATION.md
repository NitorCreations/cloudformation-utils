# Migration Guide: Build System Modernization

This document outlines the changes made to modernize the build system and how to adapt to them.

## Summary of Changes

The build system has been completely modernized to use current Python packaging standards and tools:

### ✅ What's New

- **Modern Python packaging** using `pyproject.toml` as the single source of configuration
- **GitHub Actions CI/CD** replacing Codeship
- **Modern Python versions** (3.8-3.13) with Python 2.7/3.5/3.6/3.7 support dropped
- **Ruff** for fast linting and formatting (replacing flake8)
- **MyPy** for type checking
- **Pre-commit hooks** for code quality
- **Makefile** with common development tasks
- **Automated releases** via GitHub Actions with trusted publishing

### ❌ What's Removed

- Old Codeship configuration (`codeship-services.yml`, `codeship-steps.yml`)
- Legacy Dockerfiles for old Python versions (`p27.Dockerfile`, `p35.Dockerfile`, etc.)
- Manual shell scripts (`dist.sh`, `package.sh`)
- Old `setup.cfg` configuration (migrated to `pyproject.toml`)
- Legacy development requirements (`dev-requirements.txt`, `dev-requirements.in`)

## Migration Steps

### For Users

If you're just using this package, update your Python version:

```bash
# Old: Python 2.7, 3.5, 3.6, 3.7 supported
# New: Python 3.8+ required
pip install --upgrade cloudformation-utils
```

### For Contributors

1. **Update Python version**: Ensure you're using Python 3.8 or higher

2. **Set up development environment**:
   ```bash
   git pull origin main
   make setup-dev
   ```

3. **Use new development commands**:
   ```bash
   # Old way
   python setup.py test
   pip install -r dev-requirements.txt
   flake8 .
   
   # New way
   make test
   make install-dev
   make lint
   make format
   make type-check
   ```

4. **Pre-commit hooks**: Code quality checks now run automatically on commit
   ```bash
   # Hooks are installed automatically with make setup-dev
   # Run manually on all files:
   make pre-commit
   ```

### For Maintainers

1. **CI/CD**: GitHub Actions now handles all CI/CD
   - Tests run on Python 3.8-3.13
   - Automatic releases when tags are pushed
   - Uses trusted publishing to PyPI

2. **Releases**: 
   ```bash
   # Old way
   ./dist.sh 1.0.0 "Release message"
   
   # New way
   git tag v1.0.0
   git push origin v1.0.0
   # GitHub Actions handles the rest
   ```

3. **Package building**:
   ```bash
   # Old way
   python setup.py sdist bdist_wheel
   
   # New way
   make build
   # or
   python -m build
   ```

## Configuration Changes

### pyproject.toml

All package configuration is now in `pyproject.toml`:

- **Project metadata**: name, description, authors, etc.
- **Dependencies**: runtime and optional dependencies
- **Build system**: modern setuptools with setuptools_scm
- **Tool configuration**: pytest, coverage, ruff, mypy

### Removed Files

These files are no longer needed and can be safely removed:

- `setup.cfg` (configuration moved to `pyproject.toml`)
- `dev-requirements.txt` / `dev-requirements.in` (use `pip install -e .[dev]`)
- `dist.sh` / `package.sh` (use `make build` or GitHub Actions)
- `codeship-*.yml` (replaced by GitHub Actions)
- `p*.Dockerfile` (old Python versions no longer supported)

## Tool Changes

| Old Tool | New Tool | Purpose |
|----------|----------|---------|
| flake8 | ruff | Linting and formatting |
| setup.py test | pytest | Testing |
| pip-compile | pip install -e .[dev] | Development dependencies |
| Manual scripts | Makefile | Development tasks |
| Codeship | GitHub Actions | CI/CD |

## Benefits

- **Faster development**: Ruff is significantly faster than flake8
- **Better type safety**: MyPy integration for type checking
- **Automated quality**: Pre-commit hooks prevent bad commits
- **Modern CI/CD**: GitHub Actions with matrix testing
- **Simplified releases**: Automated publishing with trusted publishing
- **Better dependency management**: Optional dependencies in pyproject.toml
- **Consistent formatting**: Automatic code formatting

## Troubleshooting

### Common Issues

1. **Python version too old**:
   ```
   ERROR: Package requires Python >=3.8
   ```
   Solution: Upgrade to Python 3.8 or higher

2. **Missing development dependencies**:
   ```
   ModuleNotFoundError: No module named 'pytest'
   ```
   Solution: Run `make setup-dev` or `pip install -e .[dev]`

3. **Pre-commit hooks failing**:
   ```
   ruff....................................................................Failed
   ```
   Solution: Run `make format` to fix formatting issues

### Getting Help

- Check the [README.md](README.md) for updated documentation
- Run `make help` to see available development commands
- Open an issue on GitHub for build system problems
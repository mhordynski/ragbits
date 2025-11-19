# Contributing to Ragbits

Thank you for your interest in contributing to Ragbits! This document outlines the development workflow and guidelines.

## Branching Strategy

We use **trunk-based development** with the following approach:

### Main Branch (`main`)
- **Default branch** for all development work
- All feature branches should be created from and merged into `main`
- Nightly builds are published automatically from `main`
- Always in a releasable state

### Creating Pull Requests
1. Fork the repository or create a feature branch from `main`:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them with descriptive messages

3. Push your branch and create a PR targeting `main`:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Your PR will be reviewed and, once approved, merged into `main`

### Release Process

#### Stable Releases (Major/Minor)
Stable releases are created using the GitHub Actions workflow:
- Trigger the **"Stable Release"** workflow from the Actions tab
- Choose version type (major or minor)
- A PR will be created automatically with version bumps and changelog updates
- After review and merge, the release is automatically tagged and published to PyPI

#### Hotfix/Patch Releases
For urgent bug fixes:
- Trigger the **"Patch Release (Hotfix)"** workflow from the Actions tab
- Provide a brief description of the fix
- A PR will be created with patch version bumps
- After merge, the hotfix is automatically published

#### Nightly Builds
- Published automatically from `main` every day at 2 AM UTC
- Install with: `pip install ragbits --pre`
- Version format: `X.Y.Z.devYYYYMMDDHHMM`

## Installation

### Build from source

Dependencies needed to build and run Ragbits from the source code:

1. [**uv**](https://docs.astral.sh/uv/getting-started/installation/)
2. [**python**](https://docs.astral.sh/uv/guides/install-python/) 3.10


## Linting and formatting
We use `ruff` for linting and formatting our code. To format your code, run:

```bash
$ uv run ruff format
```

To lint the code, run:
```bash
$ uv run ruff check --fix
```

## Type checking
We use `mypy` for type checking. To perform type checking, simply run:

```bash
$ uv run mypy .
```

## Testing
We use `pytest` for testing. To run the tests, simply run:

```bash
$ uv run pytest
```

Running integration tests requires PostgreSQL with the pgvector extention installed.
Minimal version of pgvector is 0.7.0, which added support for sparse vectors.

On Ubuntu Linux you can get in by installing the `postgresql-17-pgvector` package.

If it is not in your system's default repositories, you can install it from the official PostgreSQL Apt Repository:

```bash
sudo apt install postgresql-common
sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh
sudo apt install postgresql-17-pgvector
```

## Install pre-commit or pre-push hooks

We also recommend to run checkers on pre-commit/push hook. To set it up, follow these steps:

```bash
$ uv run scripts/install_git_hooks.py
```

Then decide whether you want to run the checks before each commit or before each push.

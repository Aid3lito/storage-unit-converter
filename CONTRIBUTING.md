# Contributing

Thank you for your interest in contributing to Storage Unit Converter.

Contributions are welcome, whether they involve bug fixes, improvements, documentation updates, tests, or new features.

## Getting Started

Fork the repository and clone your fork:

```bash
git clone <your-fork-url>
cd storage-unit-converter
```

Install the project in editable mode:

```bash
python3 -m pip install -e .
```

Run the application:

```bash
python3 -m storage_converter.app
```

## Development Guidelines

When contributing, please:

- Keep changes focused and easy to review
- Preserve the existing project structure
- Follow the existing coding style
- Use clear and descriptive names
- Avoid unrelated refactoring
- Update documentation when behavior changes
- Add or update tests when appropriate
- Verify that the application still runs before submitting changes

## Commit Messages

This project follows a simple Conventional Commits style.

Examples:

```text
feat: add support for a new storage unit
fix: correct binary conversion result
docs: update installation instructions
refactor: simplify result formatting
test: add conversion tests
build: update packaging configuration
```

Common prefixes include:

- `feat` — new feature
- `fix` — bug fix
- `docs` — documentation
- `refactor` — internal code change without changing behavior
- `test` — tests
- `build` — build or packaging changes
- `ci` — continuous integration changes
- `chore` — maintenance tasks

## Pull Requests

Before opening a pull request:

1. Make sure the application starts correctly.
2. Test the behavior affected by your changes.
3. Keep the pull request limited to one clear purpose.
4. Provide a concise description of the change.
5. Mention any related issue when applicable.

## Bug Reports

When reporting a bug, please include:

- Operating system
- Python version
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Error messages or screenshots when relevant

## Feature Requests

Feature requests are welcome.

Please describe:

- The problem or limitation
- The proposed behavior
- Why the feature would be useful

## Security Issues

Do not publicly disclose security vulnerabilities through regular issues.

Please follow the instructions in [SECURITY.md](SECURITY.md).
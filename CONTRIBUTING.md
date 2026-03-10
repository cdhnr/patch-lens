# Contributing to patch-lens

Thanks for contributing!

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e . pytest ruff
```

## Quality checks

```bash
ruff check .
pytest
```

All pull requests run automated checks via GitHub Actions.

# patch-lens

`patchlens` is an open-source Python CLI that scans Linux update sources and reports pending updates from:

- APT packages
- Flatpak apps
- Snap packages

The project follows Python best practices (PEP 8), is built with a Strategy pattern architecture, and is ready to be distributed as an installable package.

## Installation (local)

```bash
python -m pip install .
```

Then run:

```bash
patchlens scan
```

## Commands

### Summary

```bash
patchlens scan
```

Example output:

```text
Scanning system sources...
APT packages       : 5 updates
Flatpak apps       : 2 updates
Snap packages      : 1 update
Total updates pending: 8
```

### Detailed view

```bash
patchlens scan --details
```

## Architecture (Strategy Pattern)

Each update source is implemented as a dedicated strategy:

- `AptScanner`
- `FlatpakScanner`
- `SnapScanner`

`PatchLensService` orchestrates all scanners, making it easy to add new providers later.

## Open source collaboration

- Pull requests are validated automatically through CI checks (`ruff`, `pytest`).
- A Copilot instruction file is included for contributor guidance in PR reviews.

## Packaging for APT (`sudo apt install patchlens`)

This repository includes Debian packaging metadata under `debian/`. That enables building a `.deb` package and publishing it in an APT repository/PPA so users can install with:

```bash
sudo apt install patchlens
```

(Distribution to apt depends on publishing infrastructure.)

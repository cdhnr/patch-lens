"""Concrete update scanner strategies."""

from __future__ import annotations

import re

from patchlens.models import ScanResult, UpdateItem
from patchlens.runner import CommandError, run_command
from patchlens.strategies import UpdateScannerStrategy


class AptScanner(UpdateScannerStrategy):
    """Collects update candidates from APT repositories."""

    source_label = "APT packages"

    def scan(self) -> ScanResult:
        try:
            output = run_command(["apt", "list", "--upgradable"])
        except CommandError:
            return ScanResult(source_name=self.source_label, items=[])

        items: list[UpdateItem] = []
        pattern = re.compile(r"^([^/]+)/[^ ]+ ([^ ]+) .*\[upgradable from: ([^\]]+)\]")

        for line in output.splitlines():
            line = line.strip()
            if not line or line.startswith("Listing"):
                continue
            match = pattern.match(line)
            if not match:
                continue
            name, new_version, current_version = match.groups()
            items.append(
                UpdateItem(
                    name=name,
                    current_version=current_version,
                    new_version=new_version,
                )
            )

        return ScanResult(source_name=self.source_label, items=items)


class FlatpakScanner(UpdateScannerStrategy):
    """Collects update candidates from Flatpak remotes."""

    source_label = "Flatpak apps"

    def scan(self) -> ScanResult:
        try:
            output = run_command(
                [
                    "flatpak",
                    "remote-ls",
                    "--updates",
                    "--columns=application,version",
                ]
            )
        except CommandError:
            return ScanResult(source_name=self.source_label, items=[])

        items: list[UpdateItem] = []
        for line in output.splitlines():
            cleaned = line.strip()
            if not cleaned:
                continue
            parts = cleaned.split()
            name = parts[0]
            new_version = parts[1] if len(parts) > 1 else None
            items.append(
                UpdateItem(name=name, current_version=None, new_version=new_version)
            )

        return ScanResult(source_name=self.source_label, items=items)


class SnapScanner(UpdateScannerStrategy):
    """Collects update candidates from Snap."""

    source_label = "Snap packages"

    def scan(self) -> ScanResult:
        try:
            output = run_command(["snap", "refresh", "--list"])
        except CommandError:
            return ScanResult(source_name=self.source_label, items=[])

        items: list[UpdateItem] = []
        for index, line in enumerate(output.splitlines()):
            cleaned = line.strip()
            if not cleaned:
                continue
            if index == 0 and cleaned.lower().startswith("name"):
                continue
            parts = cleaned.split()
            if not parts:
                continue
            name = parts[0]
            new_version = parts[1] if len(parts) > 1 else None
            items.append(
                UpdateItem(name=name, current_version=None, new_version=new_version)
            )

        return ScanResult(source_name=self.source_label, items=items)

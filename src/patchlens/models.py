"""Domain models used by scanners and output rendering."""

from dataclasses import dataclass


@dataclass(slots=True)
class UpdateItem:
    """Represents one pending package update."""

    name: str
    current_version: str | None
    new_version: str | None


@dataclass(slots=True)
class ScanResult:
    """Represents scan output from a single source manager."""

    source_name: str
    items: list[UpdateItem]

    @property
    def total(self) -> int:
        """Return total updates for this source."""
        return len(self.items)

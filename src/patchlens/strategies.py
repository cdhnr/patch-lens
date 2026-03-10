"""Strategy pattern contracts for update scanners."""

from abc import ABC, abstractmethod

from patchlens.models import ScanResult


class UpdateScannerStrategy(ABC):
    """Abstract scanner strategy for one package source."""

    source_label: str

    @abstractmethod
    def scan(self) -> ScanResult:
        """Collect available updates for this source."""

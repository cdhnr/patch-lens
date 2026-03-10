"""Services that coordinate scanners."""

from patchlens.models import ScanResult
from patchlens.strategies import UpdateScannerStrategy


class PatchLensService:
    """Orchestrates update scans with pluggable strategies."""

    def __init__(self, scanners: list[UpdateScannerStrategy]) -> None:
        self._scanners = scanners

    def scan_all(self) -> list[ScanResult]:
        """Run all configured scanner strategies."""
        return [scanner.scan() for scanner in self._scanners]

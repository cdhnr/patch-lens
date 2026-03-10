from patchlens.formatters import format_summary
from patchlens.models import ScanResult
from patchlens.scanners import AptScanner, FlatpakScanner, SnapScanner


def test_summary_total() -> None:
    results = [
        ScanResult(source_name="APT packages", items=[object(), object()]),
        ScanResult(source_name="Flatpak apps", items=[]),
        ScanResult(source_name="Snap packages", items=[object()]),
    ]
    text = format_summary(results)
    assert "Total updates pending: 3" in text


def test_apt_parser_extracts_versions(monkeypatch) -> None:
    sample = (
        "Listing... Done\n"
        "curl/jammy-updates 8.5.0-2ubuntu10.1 amd64 "
        "[upgradable from: 8.5.0-2ubuntu10]\n"
    )

    from patchlens import scanners

    monkeypatch.setattr(scanners, "run_command", lambda _: sample)
    result = AptScanner().scan()

    assert result.total == 1
    assert result.items[0].name == "curl"
    assert result.items[0].current_version == "8.5.0-2ubuntu10"
    assert result.items[0].new_version == "8.5.0-2ubuntu10.1"


def test_flatpak_parser(monkeypatch) -> None:
    sample = "org.mozilla.firefox 124.0.1\n"
    from patchlens import scanners

    monkeypatch.setattr(scanners, "run_command", lambda _: sample)
    result = FlatpakScanner().scan()

    assert result.total == 1
    assert result.items[0].name == "org.mozilla.firefox"


def test_snap_parser(monkeypatch) -> None:
    sample = "Name   Version   Rev   Publisher\ncore20 20240111 2015 canonical**\n"
    from patchlens import scanners

    monkeypatch.setattr(scanners, "run_command", lambda _: sample)
    result = SnapScanner().scan()

    assert result.total == 1
    assert result.items[0].name == "core20"

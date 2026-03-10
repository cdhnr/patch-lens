"""Output formatting helpers for summary and detailed reports."""

from patchlens.models import ScanResult, UpdateItem


def format_summary(results: list[ScanResult]) -> str:
    """Render human-friendly summary report."""
    total = sum(result.total for result in results)
    lines = ["Scanning system sources..."]
    for result in results:
        lines.append(f"{result.source_name:<18}: {result.total} updates")
    lines.append(f"Total updates pending: {total}")
    return "\n".join(lines)


def _format_item(index: int, item: UpdateItem) -> list[str]:
    if item.current_version and item.new_version:
        row = (
            f"{index}. {item.name:<20} "
            f"{item.current_version:<18} -> {item.new_version}"
        )
        return [row]
    if item.new_version and not item.current_version:
        return [f"{index}. {item.name}", f"   - -> {item.new_version}"]
    return [f"{index}. {item.name}"]


def format_details(results: list[ScanResult]) -> str:
    """Render details grouped by source."""
    sections: list[str] = []
    for result in results:
        title = (
            result.source_name.replace("packages", "Updates")
            .replace("apps", "Updates")
        )
        sections.append(title)
        if not result.items:
            sections.append("No pending updates.")
            sections.append("")
            continue
        for index, item in enumerate(result.items, start=1):
            sections.extend(_format_item(index, item))
        sections.append("")
    return "\n".join(sections).rstrip()

"""Command runner helpers for shell-based scanners."""

from __future__ import annotations

import subprocess


class CommandError(RuntimeError):
    """Raised when command execution fails in an expected scanner path."""


def run_command(command: list[str]) -> str:
    """Execute a command and return stdout, or raise CommandError."""
    try:
        completed = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise CommandError(str(exc)) from exc
    return completed.stdout

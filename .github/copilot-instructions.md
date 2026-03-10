# Copilot instructions for patch-lens

When reviewing contributions:

- Keep code compliant with PEP 8 and SOLID principles.
- Preserve Strategy pattern boundaries (`strategies.py`, concrete scanners in `scanners.py`).
- Prefer small functions with clear names and docstrings.
- Ensure new scanners include tests for parser behavior.
- Keep CLI output stable for `scan` and `scan --details`.

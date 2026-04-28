"""Печать целей Makefile с комментариями ## (без grep/awk — удобно для Windows / PowerShell)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

# После «:» могут быть prerequisites (например check: lint … ## …)
_RX = re.compile(r"^([a-zA-Z0-9_.%-]+):.*?##\s*(.*)$")


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    makefile = root / "Makefile"
    if not makefile.is_file():
        print("Makefile не найден рядом с репозиторием.", file=sys.stderr)
        return 1
    rows: list[tuple[str, str]] = []
    for line in makefile.read_text(encoding="utf-8").splitlines():
        m = _RX.match(line)
        if m:
            rows.append((m.group(1), m.group(2)))
    for name, desc in sorted(rows):
        print(f"  {name:26} {desc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

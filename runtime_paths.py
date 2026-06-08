"""Path helpers that work both in development and inside a PyInstaller bundle.

- resource_dir(): read-only files shipped with the app (TEMPLATE.docx, frontend build).
  In a frozen build these live next to the executable (PyInstaller's _MEIPASS).
- data_dir(): a writable location for runtime data (SQLite DB, generated output).
  In a frozen build this is %LOCALAPPDATA%\\RentalPro so we never try to write
  inside Program Files / the read-only bundle.
"""

import os
import sys


def is_frozen() -> bool:
    return getattr(sys, "frozen", False)


def resource_dir() -> str:
    if is_frozen():
        # PyInstaller extracts/locates bundled data here
        return getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def data_dir() -> str:
    if is_frozen():
        base = os.path.join(
            os.environ.get("LOCALAPPDATA", os.path.expanduser("~")),
            "RentalPro",
        )
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(base, exist_ok=True)
    return base

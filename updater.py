"""Self-update for the packaged Rental Pro desktop app (GitHub Releases).

Flow (only active in the packaged .exe with GITHUB_OWNER/REPO configured):
  1. On launch, fetch latest.json from the repo's "latest" release.
  2. If its version is newer than this build, ask the user to update.
  3. Download RentalPro.zip, extract it, then hand off to a small batch
     script that waits for the app to close, swaps the files, and relaunches.

The client's data (database + generated documents) lives in %LOCALAPPDATA%
and is never touched by an update.
"""

import os
import sys
import json
import time
import ctypes
import zipfile
import tempfile
import threading
import subprocess
import urllib.request

from version import __version__ as CURRENT_VERSION, GITHUB_OWNER, GITHUB_REPO

_BASE = (
    f"https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest/download"
    if GITHUB_OWNER and GITHUB_REPO
    else ""
)
MANIFEST_URL = f"{_BASE}/latest.json" if _BASE else ""

# Windows MessageBox flags
_MB_YESNO = 0x04
_MB_ICONQUESTION = 0x20
_MB_ICONERROR = 0x10
_MB_ICONINFO = 0x40
_IDYES = 6


def is_enabled() -> bool:
    return bool(MANIFEST_URL) and getattr(sys, "frozen", False)


def _parse_version(v) -> tuple:
    out = []
    for part in str(v).strip().lstrip("vV").split("."):
        try:
            out.append(int(part))
        except ValueError:
            out.append(0)
    return tuple(out)


def _message_box(title: str, message: str, flags: int) -> int:
    return ctypes.windll.user32.MessageBoxW(0, message, title, flags)


def check_for_update(timeout: float = 6.0):
    """Return the manifest dict if a newer version is available, else None."""
    if not is_enabled():
        return None
    try:
        req = urllib.request.Request(
            MANIFEST_URL, headers={"Cache-Control": "no-cache", "Pragma": "no-cache"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            manifest = json.loads(resp.read().decode("utf-8"))
        if _parse_version(manifest.get("version", "0")) > _parse_version(CURRENT_VERSION):
            return manifest
    except Exception:
        # Offline or unreachable -> just launch the app normally
        return None
    return None


def _install_dir() -> str:
    # onedir build: the executable sits at the top of the app folder
    return os.path.dirname(sys.executable)


def _download_and_extract(manifest: dict) -> str:
    url = manifest["url"]
    staging = tempfile.mkdtemp(prefix="rentalpro_update_")
    zip_path = os.path.join(staging, "update.zip")
    urllib.request.urlretrieve(url, zip_path)

    extract_dir = os.path.join(staging, "extracted")
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(extract_dir)

    # Expecting a top-level "RentalPro" folder inside the zip
    candidate = os.path.join(extract_dir, "RentalPro")
    new_app_dir = candidate if os.path.isdir(candidate) else extract_dir
    if not os.path.isfile(os.path.join(new_app_dir, "RentalPro.exe")):
        raise RuntimeError("Downloaded update does not contain RentalPro.exe")
    return new_app_dir


def _launch_swapper_and_exit(new_app_dir: str):
    install_dir = _install_dir()
    exe_path = sys.executable
    exe_name = os.path.basename(exe_path)
    pid = os.getpid()

    bat_path = os.path.join(tempfile.gettempdir(), "rentalpro_apply_update.bat")
    script = f"""@echo off
:waitloop
tasklist /FI "PID eq {pid}" 2>NUL | find /I "{exe_name}" >NUL
if not errorlevel 1 (
  timeout /t 1 /nobreak >NUL
  goto waitloop
)
robocopy "{new_app_dir}" "{install_dir}" /E /IS /IT /R:2 /W:1 /NFL /NDL /NJH /NJS /NC /NS >NUL
start "" "{exe_path}"
rmdir /S /Q "{os.path.dirname(os.path.dirname(new_app_dir))}" 2>NUL
del "%~f0"
"""
    with open(bat_path, "w", encoding="utf-8") as f:
        f.write(script)

    DETACHED_PROCESS = 0x00000008
    CREATE_NEW_PROCESS_GROUP = 0x00000200
    subprocess.Popen(
        ["cmd", "/c", bat_path],
        creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
        close_fds=True,
    )
    # Exit so the running files can be replaced; the batch relaunches us.
    os._exit(0)


def maybe_update():
    """Check, prompt, and apply an update. Returns normally if nothing to do."""
    manifest = check_for_update()
    if not manifest:
        return

    notes = manifest.get("notes", "").strip()
    body = f"A new version ({manifest['version']}) of Rental Pro is available."
    if notes:
        body += f"\n\nWhat's new:\n{notes}"
    body += "\n\nInstall it now? The app will restart."

    if _message_box("Rental Pro Update", body, _MB_YESNO | _MB_ICONQUESTION) != _IDYES:
        return

    try:
        new_app_dir = _download_and_extract(manifest)
    except Exception as exc:
        _message_box(
            "Rental Pro Update",
            f"The update could not be downloaded:\n\n{exc}\n\nThe app will start with the current version.",
            _MB_ICONERROR,
        )
        return

    _launch_swapper_and_exit(new_app_dir)


# --- In-app (UI driven) helpers, used by the FastAPI endpoints ---

def get_status(timeout: float = 6.0) -> dict:
    """Lightweight status for the in-app 'Check for updates' button."""
    info = {
        "enabled": is_enabled(),
        "current": CURRENT_VERSION,
        "available": False,
        "latest": CURRENT_VERSION,
        "notes": "",
    }
    manifest = check_for_update(timeout=timeout)
    if manifest:
        info["available"] = True
        info["latest"] = manifest.get("version", CURRENT_VERSION)
        info["notes"] = (manifest.get("notes") or "").strip()
    return info


def start_update_in_background():
    """Download + apply the update from within the running app.

    Returns (ok, error). On success the app downloads in the background and then
    exits/relaunches itself once the new files are swapped in.
    """
    manifest = check_for_update()
    if not manifest:
        return False, "No update is available."

    def _worker():
        try:
            new_app_dir = _download_and_extract(manifest)
        except Exception:
            return
        # Give the HTTP response time to reach the UI before we exit
        time.sleep(1.0)
        _launch_swapper_and_exit(new_app_dir)

    threading.Thread(target=_worker, daemon=True).start()
    return True, None

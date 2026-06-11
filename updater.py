"""Self-update for the packaged Rental Pro desktop app (GitHub Releases).

Flow (only active in the packaged .exe with GITHUB_OWNER/REPO configured):
  1. On launch, fetch latest.json from the repo's "latest" release.
  2. If its version is newer than this build, ask the user to update.
  3. Download RentalPro.zip, extract it, hand off to a hidden batch script that
     waits for this process to exit, copies files in place, and relaunches.

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


def _log_path() -> str:
    try:
        from runtime_paths import data_dir
        base = data_dir()
    except Exception:
        base = os.path.join(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()), "RentalPro")
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, "update.log")


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
        return None
    return None


def _install_dir() -> str:
    return os.path.dirname(os.path.abspath(sys.executable))


def _terminate_current_process():
    """Hard-exit the whole process (needed when pywebview blocks normal exit)."""
    handle = ctypes.windll.kernel32.GetCurrentProcess()
    ctypes.windll.kernel32.TerminateProcess(handle, 0)


def _run_hidden(cmd: str):
    """Run a shell command with no visible window (Win11-safe)."""
    vbs_path = os.path.join(tempfile.gettempdir(), "rentalpro_run_hidden.vbs")
    escaped = cmd.replace('"', '""')
    with open(vbs_path, "w", encoding="utf-8") as f:
        f.write(
            'Set sh = CreateObject("WScript.Shell")\n'
            f'sh.Run "{escaped}", 0, False\n'
        )
    CREATE_NO_WINDOW = 0x08000000
    subprocess.Popen(
        ["wscript.exe", "//B", "//Nologo", vbs_path],
        creationflags=CREATE_NO_WINDOW,
        close_fds=True,
    )


def _download_and_extract(manifest: dict) -> str:
    url = manifest["url"]
    staging = tempfile.mkdtemp(prefix="rentalpro_update_")
    zip_path = os.path.join(staging, "update.zip")
    urllib.request.urlretrieve(url, zip_path)

    extract_dir = os.path.join(staging, "extracted")
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(extract_dir)

    candidate = os.path.join(extract_dir, "RentalPro")
    new_app_dir = candidate if os.path.isdir(candidate) else extract_dir
    if not os.path.isfile(os.path.join(new_app_dir, "RentalPro.exe")):
        raise RuntimeError("Downloaded update does not contain RentalPro.exe")
    return new_app_dir


def _launch_swapper_and_exit(new_app_dir: str):
    """Hand off to a temp .bat script, then exit.

    Important: we must NOT spawn RentalPro.exe as the updater — that locks the
    install folder (WinError 32). A detached cmd script waits for this process
    to die, then overwrites files in place with robocopy (no folder rename).
    """
    install_dir = _install_dir()
    exe_path = os.path.abspath(sys.executable)
    pid = os.getpid()
    log_path = _log_path()
    staging_root = os.path.dirname(os.path.dirname(new_app_dir))

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Preparing update pid={pid}\n")
        f.write(f"  mode=batch-in-place (no folder rename)\n")
        f.write(f"  install={install_dir}\n")
        f.write(f"  source={new_app_dir}\n")

    bat_path = os.path.join(tempfile.gettempdir(), "rentalpro_apply_update.bat")
    bat = f"""@echo off
setlocal EnableDelayedExpansion
set "LOG={log_path}"
set "INSTALL={install_dir}"
set "SOURCE={new_app_dir}"
set "EXE={exe_path}"
set "STAGING={staging_root}"
set "PARENT={pid}"

echo [%date% %time%] Batch updater started >> "%LOG%"
echo Waiting for parent pid=%PARENT% to exit... >> "%LOG%"

set /a WAIT=0
:waitloop
tasklist /FI "PID eq %PARENT%" /NH 2>nul | find /I "RentalPro.exe" >nul
if errorlevel 1 goto parent_done
set /a WAIT+=1
if !WAIT! GEQ 90 goto force_kill
if !WAIT! EQU 5 echo Still waiting for parent pid=%PARENT%... >> "%LOG%"
timeout /t 1 /nobreak >nul
goto waitloop

:force_kill
echo Parent still running after 90s - forcing exit >> "%LOG%"
taskkill /F /PID %PARENT% /T >nul 2>&1

:parent_done
echo Parent exited after !WAIT!s >> "%LOG%"
timeout /t 2 /nobreak >nul
taskkill /F /IM msedgewebview2.exe >nul 2>&1
taskkill /F /IM RentalPro.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul

echo Copying files in place... >> "%LOG%"
robocopy "%SOURCE%" "%INSTALL%" /E /IS /IT /R:10 /W:3 /NFL /NDL /NJH /NJS /NC /NS >> "%LOG%" 2>&1
echo robocopy exit code %ERRORLEVEL% >> "%LOG%"
if errorlevel 8 (
  echo robocopy FAILED >> "%LOG%"
  msg * "Rental Pro update failed. See log: %LOG%"
  goto cleanup
)

echo Relaunching Rental Pro... >> "%LOG%"
start "" /D "%INSTALL%" "%EXE%"

:cleanup
if exist "%STAGING%" rmdir /S /Q "%STAGING%" 2>nul
del "%~f0"
endlocal
"""
    with open(bat_path, "w", encoding="utf-8") as f:
        f.write(bat)

    _run_hidden(f'cmd /c "{bat_path}"')
    _terminate_current_process()


def maybe_update():
    """Check, prompt, and apply an update. Returns normally if nothing to do."""
    manifest = check_for_update()
    if not manifest:
        return

    notes = manifest.get("notes", "").strip()
    body = f"A new version ({manifest['version']}) of Rental Pro is available."
    if notes:
        body += f"\n\nWhat's new:\n{notes}"
    body += "\n\nInstall it now? The app will close and reopen automatically."

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
    """Download + apply the update from within the running app."""
    manifest = check_for_update()
    if not manifest:
        return False, "No update is available."

    def _worker():
        try:
            new_app_dir = _download_and_extract(manifest)
        except Exception as exc:
            _message_box(
                "Rental Pro Update",
                f"Download failed:\n\n{exc}\n\nThe app will continue with the current version.",
                _MB_ICONERROR,
            )
            return
        time.sleep(2.0)
        _launch_swapper_and_exit(new_app_dir)

    threading.Thread(target=_worker, daemon=True).start()
    return True, None

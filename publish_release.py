"""Build and publish a Rental Pro release to GitHub.

One command does: bump version -> build -> zip/manifest -> GitHub Release upload.

Authentication (pick one, set up once):
  1. Create a token: https://github.com/settings/tokens  (scope: "repo")
  2. Save it in a local .env file (gitignored):
       GITHUB_TOKEN=ghp_your_token_here
  3. Or set environment variable GITHUB_TOKEN before running.
  4. Or paste when this script prompts you.

Usage:
  python publish_release.py
  python publish_release.py --version 1.0.1 --notes "Bug fixes"
  python publish_release.py --bump patch --notes "Small fixes"
"""

from __future__ import annotations

import argparse
import getpass
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

import version

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "dist")
ZIP_PATH = os.path.join(DIST, "RentalPro.zip")
MANIFEST_PATH = os.path.join(DIST, "latest.json")
SETUP_PATH = os.path.join(DIST, "RentalPro-Setup.exe")
VERSION_PY = os.path.join(HERE, "version.py")
INSTALLER_ISS = os.path.join(HERE, "installer.iss")
ENV_FILE = os.path.join(HERE, ".env")


def _load_dotenv():
    if not os.path.isfile(ENV_FILE):
        return
    with open(ENV_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key, val = key.strip(), val.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = val


def _parse_version(v: str) -> tuple[int, ...]:
    parts = []
    for p in str(v).strip().lstrip("vV").split("."):
        try:
            parts.append(int(p))
        except ValueError:
            parts.append(0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts[:3])


def _format_version(t: tuple[int, ...]) -> str:
    return ".".join(str(x) for x in t[:3])


def _bump(current: str, kind: str) -> str:
    major, minor, patch = _parse_version(current)
    if kind == "major":
        return _format_version((major + 1, 0, 0))
    if kind == "minor":
        return _format_version((major, minor + 1, 0))
    return _format_version((major, minor, patch + 1))


def _set_file_version(path: str, new_version: str, pattern: str, repl_template: str):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if not re.search(pattern, text):
        raise RuntimeError(f"Could not find version field in {path}")
    text = re.sub(pattern, repl_template.format(v=new_version), text, count=1)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def set_project_version(new_version: str):
    _set_file_version(
        VERSION_PY,
        new_version,
        r'__version__\s*=\s*["\'][^"\']+["\']',
        '__version__ = "{v}"',
    )
    _set_file_version(
        INSTALLER_ISS,
        new_version,
        r'#define MyAppVersion\s+"[^"]+"',
        '#define MyAppVersion "{v}"',
    )
    # Reload for make_release / URLs
    import importlib
    importlib.reload(version)


def run_build():
    print("\n=== Building desktop app (this may take a few minutes) ===\n")
    env = os.environ.copy()
    env["NOPAUSE"] = "1"
    cmd = ["cmd", "/c", "build_desktop.bat"] if os.name == "nt" else ["bash", "build_desktop.bat"]
    result = subprocess.run(cmd, cwd=HERE, env=env)
    if result.returncode != 0:
        sys.exit("Build failed. Fix errors and try again.")


def write_manifest(new_version: str, notes: str):
    owner, repo = version.GITHUB_OWNER, version.GITHUB_REPO
    if not owner or not repo:
        print("WARNING: GITHUB_OWNER/REPO not set in version.py")
        zip_url = "https://github.com/OWNER/REPO/releases/latest/download/RentalPro.zip"
    else:
        zip_url = f"https://github.com/{owner}/{repo}/releases/latest/download/RentalPro.zip"

    manifest = {"version": new_version, "url": zip_url, "notes": notes.strip()}
    os.makedirs(DIST, exist_ok=True)
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Wrote {MANIFEST_PATH}")


def get_token() -> str:
    _load_dotenv()
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        return token
    print("\nGitHub token required (create at https://github.com/settings/tokens, scope: repo)")
    print("Tip: save it once in .env as  GITHUB_TOKEN=ghp_...  (file is gitignored)\n")
    token = getpass.getpass("Paste GitHub token (input hidden): ").strip()
    if not token:
        sys.exit("No token provided.")
    return token


def _github_api(method: str, url: str, token: str, data: dict | None = None) -> dict:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "RentalPro-Publisher",
    }
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        sys.exit(f"GitHub API error {e.code}: {detail}")


def _upload_asset(upload_url_template: str, token: str, file_path: str):
    name = os.path.basename(file_path)
    url = upload_url_template.replace("{?name,label}", f"?name={name}")
    with open(file_path, "rb") as f:
        data = f.read()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/octet-stream",
        "Content-Length": str(len(data)),
        "User-Agent": "RentalPro-Publisher",
    }
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            resp.read()
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        sys.exit(f"Upload failed for {name} ({e.code}): {detail}")
    print(f"  Uploaded {name} ({len(data) // 1024 // 1024} MB)")


def publish_to_github(new_version: str, notes: str, token: str, include_setup: bool):
    owner, repo = version.GITHUB_OWNER, version.GITHUB_REPO
    if not owner or not repo:
        sys.exit("Set GITHUB_OWNER and GITHUB_REPO in version.py first.")

    tag = f"v{new_version}"
    api = f"https://api.github.com/repos/{owner}/{repo}/releases"

    print(f"\n=== Publishing {tag} to {owner}/{repo} ===\n")
    release = _github_api(
        "POST",
        api,
        token,
        {
            "tag_name": tag,
            "name": tag,
            "body": notes.strip() or f"Rental Pro {new_version}",
            "draft": False,
            "prerelease": False,
            "generate_release_notes": not notes.strip(),
        },
    )
    upload_url = release.get("upload_url")
    if not upload_url:
        sys.exit("GitHub did not return an upload URL.")

    for path in (ZIP_PATH, MANIFEST_PATH):
        if not os.path.isfile(path):
            sys.exit(f"Missing {path}. Run build first.")
        _upload_asset(upload_url, token, path)

    if include_setup and os.path.isfile(SETUP_PATH):
        _upload_asset(upload_url, token, SETUP_PATH)
    elif include_setup:
        print("  (Skipping Setup.exe — not found; run full build to include it)")

    html_url = release.get("html_url", f"https://github.com/{owner}/{repo}/releases")
    print(f"\nPublished: {html_url}")
    print("Clients with the desktop app will see this update on next launch.")


def main():
    parser = argparse.ArgumentParser(description="Build and publish Rental Pro to GitHub Releases")
    parser.add_argument("--version", help="New version, e.g. 1.0.1")
    parser.add_argument("--bump", choices=("patch", "minor", "major"), help="Auto-increment from current version")
    parser.add_argument("--notes", default="", help="Release notes shown to clients in the update prompt")
    parser.add_argument("--skip-build", action="store_true", help="Only publish existing dist/ artifacts")
    parser.add_argument("--no-setup", action="store_true", help="Do not upload RentalPro-Setup.exe")
    args = parser.parse_args()

    current = version.__version__
    if args.version:
        new_version = args.version.lstrip("vV")
    elif args.bump:
        new_version = _bump(current, args.bump)
    else:
        suggested = _bump(current, "patch")
        print(f"Current version: {current}")
        entered = input(f"New version [{suggested}]: ").strip()
        new_version = entered.lstrip("vV") if entered else suggested

    notes = args.notes
    if not notes and not args.skip_build:
        print("\nRelease notes (shown to clients when updating). Press Enter to skip:")
        notes = input("> ").strip()

    if new_version != current:
        print(f"Bumping version: {current} -> {new_version}")
        set_project_version(new_version)
    else:
        print(f"Keeping version: {current}")

    if not args.skip_build:
        run_build()
    else:
        if not os.path.isfile(ZIP_PATH):
            subprocess.run([sys.executable, "make_release.py"], cwd=HERE, check=True)

    write_manifest(new_version, notes)

    token = get_token()
    publish_to_github(new_version, notes, token, include_setup=not args.no_setup)

    print("\nAll done.")


if __name__ == "__main__":
    main()

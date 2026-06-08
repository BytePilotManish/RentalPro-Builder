"""Package a release for distribution / auto-update.

Run AFTER PyInstaller has produced dist\\RentalPro\\. Produces:
  - dist\\RentalPro.zip   (the full app folder, what clients download)
  - dist\\latest.json     (update manifest referencing the GitHub "latest" release)

Upload BOTH files as assets on a GitHub Release in your repo.
"""

import json
import os
import shutil
import sys

import version

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "dist")
APP_DIR = os.path.join(DIST, "RentalPro")


def main():
    if not os.path.isdir(APP_DIR):
        print("ERROR: dist\\RentalPro not found. Build with PyInstaller first.")
        sys.exit(1)

    # Create dist\RentalPro.zip with a top-level "RentalPro/" folder inside.
    zip_path = shutil.make_archive(
        os.path.join(DIST, "RentalPro"), "zip", root_dir=DIST, base_dir="RentalPro"
    )
    print(f"Created {zip_path}")

    if version.GITHUB_OWNER and version.GITHUB_REPO:
        zip_url = (
            f"https://github.com/{version.GITHUB_OWNER}/{version.GITHUB_REPO}"
            f"/releases/latest/download/RentalPro.zip"
        )
    else:
        zip_url = "https://github.com/OWNER/REPO/releases/latest/download/RentalPro.zip"
        print("NOTE: GITHUB_OWNER/REPO not set in version.py - using a placeholder URL.")

    manifest = {
        "version": version.__version__,
        "url": zip_url,
        "notes": "",
    }
    manifest_path = os.path.join(DIST, "latest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Wrote {manifest_path} (version {version.__version__})")
    print("\nUpload BOTH dist\\RentalPro.zip and dist\\latest.json to a GitHub Release.")


if __name__ == "__main__":
    main()

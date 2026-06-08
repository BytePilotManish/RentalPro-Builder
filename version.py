"""Application version and auto-update configuration.

HOW TO RELEASE AN UPDATE:
  1. Bump __version__ below (e.g. "1.0.0" -> "1.0.1").
  2. Run build_desktop.bat  (produces dist\\RentalPro.zip and dist\\latest.json).
  3. Create a GitHub Release in your repo and upload BOTH files
     (RentalPro.zip and latest.json) as release assets.
  4. Clients get the update automatically the next time they open the app.

To ENABLE auto-update, set GITHUB_OWNER and GITHUB_REPO once below.
Leave them blank to disable update checks (app still works normally).
"""

__version__ = "1.0.0"

# e.g. GITHUB_OWNER = "manoj", GITHUB_REPO = "rental-pro"
GITHUB_OWNER = "BytePilotManish"
GITHUB_REPO = "RentalPro-Builder"

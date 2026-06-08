# Releasing updates (auto-update via GitHub Releases)

The desktop app checks this repo's **latest GitHub Release** for updates. To ship
an update to clients, publish a Release with two assets: `RentalPro.zip` and
`latest.json`.

> The repository (or at least its Releases) must be **PUBLIC** — the app
> downloads the release files without any login/token. A private repo would
> require shipping a secret token to clients, which is insecure.

## First-time setup (once)

1. In `version.py`, confirm:
   - `GITHUB_OWNER = "BytePilotManish"`
   - `GITHUB_REPO  = "RentalPro-Builder"`
2. Make the GitHub repo **Public**: repo → Settings → General → Danger Zone →
   "Change visibility" → Public.

## Every time you release an update

1. Make your code changes.
2. Bump the version in `version.py`, e.g. `__version__ = "1.0.1"`.
3. Build:
   ```
   build_desktop.bat
   ```
   This produces `dist\RentalPro.zip` and `dist\latest.json`.
4. (Optional) Edit the `"notes"` field in `dist\latest.json` to describe what
   changed — this text is shown to the client in the update prompt.
5. On GitHub: **Releases → Draft a new release**.
   - Tag: `v1.0.1` (match the version), Target: `main`.
   - Title: `v1.0.1`.
   - Attach BOTH files: `dist\RentalPro.zip` and `dist\latest.json`.
   - Publish release.
6. Done. Clients auto-update on their next launch (or via Settings →
   Software Updates → Check for Updates).

## Notes

- Client data (`database.db`, generated documents) lives in
  `%LOCALAPPDATA%\RentalPro` and is **never** affected by updates.
- The first delivery to a new client is still the full `dist\RentalPro` folder
  (zip it and send). After that, updates are automatic.

# Releasing updates (auto-update via GitHub Releases)

## One-command publish (recommended)

```bat
publish_release.bat
```

This will:
1. Ask for the new version (e.g. `1.0.1`) and release notes
2. Build the app (`build_desktop.bat`)
3. Create `RentalPro.zip` + `latest.json`
4. Upload everything to **GitHub Releases**

Clients with the desktop app auto-update on next launch.

### First-time setup (once)

1. **Repo must be Public** (Settings → Change visibility → Public) so clients
   can download updates without a login.

2. Confirm `version.py`:
   ```python
   GITHUB_OWNER = "BytePilotManish"
   GITHUB_REPO  = "RentalPro-Builder"
   ```

3. **GitHub token** (stays on your PC only):
   - Open https://github.com/settings/tokens
   - Generate token (classic) with **`repo`** scope
   - Create `.env` in the project folder:
     ```
     GITHUB_TOKEN=ghp_your_token_here
     ```
   - Or run `setup_github.bat` for step-by-step help

   > Never commit `.env` or share your token. The script never stores it in code.

### Every update

```bat
publish_release.bat
```

Or with options:

```bat
python publish_release.py --bump patch --notes "Fixed clause spacing"
python publish_release.py --version 1.0.2 --notes "New feature"
```

### What gets uploaded

| File | Purpose |
|------|---------|
| `RentalPro.zip` | Auto-update download (existing clients) |
| `latest.json` | Version check + release notes |
| `RentalPro-Setup.exe` | Optional; for new installs from GitHub |

### Manual fallback

If you prefer doing it by hand: run `build_desktop.bat`, then on GitHub
**Releases → New release** upload `dist\RentalPro.zip` and `dist\latest.json`.

## New client install

Send **`dist\RentalPro-Setup.exe`** — they do not need GitHub.

## Notes

- Client data lives in `%LOCALAPPDATA%\RentalPro` and is never touched by updates.
- Bump `__version__` in `version.py` before each release (or let `publish_release.bat` do it).

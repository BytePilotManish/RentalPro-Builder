@echo off
REM ============================================================
REM  Build + publish a new version to GitHub Releases (auto-update)
REM
REM  First time only:
REM    1. Create a GitHub token: https://github.com/settings/tokens
REM       (tick "repo" scope)
REM    2. Save it in .env in this folder:
REM         GITHUB_TOKEN=ghp_your_token_here
REM    3. Make sure version.py has your GITHUB_OWNER and GITHUB_REPO
REM ============================================================

python publish_release.py %*
if errorlevel 1 (
  echo.
  echo Publish failed.
  pause
  exit /b 1
)
echo.
pause

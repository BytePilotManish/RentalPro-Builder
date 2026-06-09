@echo off
REM One-time GitHub setup for publish_release.bat

echo.
echo ============================================
echo   Rental Pro - GitHub publish setup
echo ============================================
echo.

REM --- 1. Create .env from template if missing ---
if not exist ".env" (
  if exist ".env.example" (
    copy /Y ".env.example" ".env" >nul
    echo [OK] Created .env from .env.example
  ) else (
    echo GITHUB_TOKEN=ghp_paste_your_token_here> ".env"
    echo [OK] Created empty .env file
  )
) else (
  echo [OK] .env already exists - will not overwrite
)

echo.
echo --- Step 1: Create a GitHub token ---
echo Opening https://github.com/settings/tokens in your browser...
echo.
echo   1. Click "Generate new token" -^> "Generate new token (classic)"
echo   2. Note: "Rental Pro publish"
echo   3. Expiration: your choice (90 days or No expiration)
echo   4. Scopes: tick ONLY  [x] repo   (full control of private repositories)
echo   5. Generate token -^> COPY the ghp_... string (shown once only)
echo.
start https://github.com/settings/tokens/new?scopes=repo^&description=Rental+Pro+publish

echo --- Step 2: Paste token into .env ---
echo After you copy the token, we will open .env in Notepad.
echo Replace ghp_your_personal_access_token_here with your real token.
echo Save and close Notepad.
echo.
pause

notepad ".env"

echo.
echo --- Step 3: Verify repo settings ---
findstr /C:"GITHUB_OWNER" version.py
findstr /C:"GITHUB_REPO" version.py
echo   (Should show BytePilotManish and RentalPro-Builder)
echo.

REM --- Optional: GitHub CLI ---
where gh >nul 2>&1
if %errorlevel%==0 (
  echo [OK] GitHub CLI installed.
  gh auth status 2>nul
) else (
  echo Installing GitHub CLI (optional, for git commands)...
  winget install -e --id GitHub.cli --accept-package-agreements --accept-source-agreements --disable-interactivity
  if %errorlevel%==0 (
    echo [OK] GitHub CLI installed. Run "gh auth login" later if you want.
  ) else (
    echo [SKIP] GitHub CLI install failed - not required for publish_release.bat
  )
)

echo.
echo ============================================
echo   Setup complete!
echo ============================================
echo.
echo Test publish (dry run - will ask version):
echo   publish_release.bat
echo.
echo Your token is stored only in .env (never committed to git).
echo.
pause

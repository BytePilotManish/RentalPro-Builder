@echo off
REM ============================================================
REM  Build the Rental Pro desktop app (folder distributable).
REM  Output: dist\RentalPro\  (send this whole folder to client)
REM ============================================================

echo [1/2] Building frontend (React) production bundle...
pushd frontend
call npm install
call npm run build
popd

echo [2/3] Packaging desktop app with PyInstaller...
python -m PyInstaller RentalPro.spec --noconfirm --clean

echo [3/4] Creating release zip + update manifest...
python make_release.py

echo [4/4] Building Windows installer (Setup.exe)...
set ISCC=%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe
if exist "%ISCC%" (
  "%ISCC%" installer.iss
) else (
  echo WARNING: Inno Setup not found. Install from https://jrsoftware.org/isdl.php
  echo          or skip this step and zip dist\RentalPro manually.
)

echo.
echo Done.
echo   Client install      : send dist\RentalPro-Setup.exe  (recommended)
echo   Manual folder       : send the ENTIRE dist\RentalPro folder (zip it)
echo   Auto-update release : run publish_release.bat  (builds + uploads to GitHub)
if not defined NOPAUSE pause

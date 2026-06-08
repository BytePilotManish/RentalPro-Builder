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

echo [3/3] Creating release zip + update manifest...
python make_release.py

echo.
echo Done.
echo   First-time delivery : send the ENTIRE "dist\RentalPro" folder to the client.
echo   Auto-update release : upload dist\RentalPro.zip AND dist\latest.json
echo                         as assets on a GitHub Release (see version.py).
pause

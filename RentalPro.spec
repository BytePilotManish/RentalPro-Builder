# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None

# --- Bundled (read-only) data files ---
datas = [("frontend/dist", "frontend/dist")]

# TEMPLATE.docx is required at runtime; include it if present at build time.
if os.path.exists("TEMPLATE.docx"):
    datas.append(("TEMPLATE.docx", "."))
else:
    print("\n[RentalPro build] WARNING: TEMPLATE.docx not found - the app will "
          "not be able to generate documents until it is bundled.\n")

# pywebview ships JS/backend assets that must be collected
datas += collect_data_files("webview")

# --- Hidden imports (dynamically loaded modules PyInstaller can't see) ---
hiddenimports = collect_submodules("uvicorn")
hiddenimports += [
    "win32com",
    "win32com.client",
    "pythoncom",
    "pywintypes",
    "win32timezone",
    "anyio",
    "anyio._backends._asyncio",
]

a = Analysis(
    ["desktop.py"],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="RentalPro",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="RentalPro",
)

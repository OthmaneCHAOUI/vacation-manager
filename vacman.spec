# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

PROJECT_ROOT = Path(SPECPATH).resolve()

a = Analysis(
    [str(PROJECT_ROOT / 'src' / 'main' / 'main.py')],
    pathex=[str(PROJECT_ROOT)],
    binaries=[],
    datas=[
        (str(PROJECT_ROOT / 'src' / 'style' / 'home_style.css'), 'src/style'),
        (str(PROJECT_ROOT / 'src' / 'style' / 'calendar_style.css'), 'src/style'),
        (str(PROJECT_ROOT / 'src' / 'data' / 'database.db'), 'src/data'),
        (str(PROJECT_ROOT / 'assets' / 'icons' / 'icon.png'), 'assets/icons'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='vacman',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

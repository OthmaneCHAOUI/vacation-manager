# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/main/main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('src/style/home_style.css', 'src/style'),
        ('src/style/calendar_style.css', 'src/style'),
        ('assets/icon.png', 'assets'),
    ],
    hiddenimports=[
        'src.view.home_view',
        'src.view.employee_view',
        'src.view.vacation_view',
        'src.view.calendar_view',
        'src.controller.employee_controller',
        'src.controller.vacation_controller',
        'src.model.vacation_model',
        'src.model.employee_model',
        'src.database.database',
        'src.utils.holidays',
        'src.data.database',
    ],
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
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

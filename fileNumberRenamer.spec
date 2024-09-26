# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['fileNumberRenamer.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\newto\\AppData\\Roaming\\Python\\Python312\\site-packages\\tkinterdnd2\\tkdnd\\win-x64', 'tkdnd')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='fileNumberRenamer',
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

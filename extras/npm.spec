# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['npm.py'],
    pathex=['C:/Users/manug/python stuff/npm'],
    binaries=[],
    datas=[('C:/Users/manug/python stuff/npm/ui_main.py','.'),
	('C:/Users/manug/python stuff/npm/ui_dialog.py','.')
	],
    hiddenimports=['ui_main', 'ui_dialog'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=True,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [('v', None, 'OPTION')],
    exclude_binaries=True,
    name='npm',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
	onefile=True,
	icon='C:/Users/manug/python stuff/npm/npm.ico',
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='npm',
)

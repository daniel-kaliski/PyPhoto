# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
from PyInstaller.utils.hooks import copy_metadata

datas = []
binaries = []
hiddenimports = []

datas += copy_metadata('pymatting')
datas += copy_metadata('rembg')

tmp_ctk = collect_all('customtkinter')
datas += tmp_ctk[0]; binaries += tmp_ctk[1]; hiddenimports += tmp_ctk[2]

tmp_rembg = collect_all('rembg')
datas += tmp_rembg[0]; binaries += tmp_rembg[1]; hiddenimports += tmp_rembg[2]

a = Analysis(
    ['PyGraph.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    [],
    exclude_binaries=True,
    name='PyGraph',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True, 
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
    name='PyGraph',
)

app = BUNDLE(
    coll,
    name='PyGraph.app',
    icon='icon.icns',
    bundle_identifier='com.danielkaliski.pygraph',
    info_plist={
        'NSHighResolutionCapable': 'True', 
        'LSBackgroundOnly': 'False',
        'CFBundleName': 'PyGraph',
        'CFBundleDisplayName': 'PyGraph Editor',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSRequiresAquaSystemAppearance': 'False',
        'NSHumanReadableCopyright': 'Copyright © 2026 Daniel Kaliski. All rights reserved.',
    },
)
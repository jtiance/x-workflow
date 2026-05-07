# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('workflow-config.json', '.'), ('X-Workflow.png', '.'), ('X-Workflow.icns', '.'), ('icons', 'icons')],
    hiddenimports=['polars', 'polars._polars', 'fastexcel', 'fastexcel._fastexcel'],
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
    name='X-Workflow',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['X-Workflow.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='X-Workflow',
)
app = BUNDLE(
    coll,
    name='X-Workflow.app',
    icon='X-Workflow.icns',
    bundle_identifier=None,
)

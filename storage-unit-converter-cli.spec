# -*- mode: python ; encoding: utf-8 -*-

a = Analysis(
    ["packaging/cli_launcher.py"],
    pathex=["src"],
    binaries=[],
    datas=[
        ("src/storage_converter/units_binary.json", "storage_converter"),
        ("src/storage_converter/units_decimal.json", "storage_converter"),
    ],
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
    name="suc",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)
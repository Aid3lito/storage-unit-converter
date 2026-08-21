# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ["packaging/launcher.py"],
    pathex=["src"],
    binaries=[],
    datas=[
        (
            "src/storage_converter/units_binary.json",
            "storage_converter",
        ),
        (
            "src/storage_converter/units_decimal.json",
            "storage_converter",
        ),
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
    [],
    exclude_binaries=True,
    name="Storage Unit Converter",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
)


coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="Storage Unit Converter",
)


app = BUNDLE(
    coll,
    name="Storage Unit Converter.app",
    icon="assets/icons/app-icon.icns",
    bundle_identifier="com.aid3lito.storageunitconverter",
    info_plist={
        "NSRequiresAquaSystemAppearance": True,
    },
)
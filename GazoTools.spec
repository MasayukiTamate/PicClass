# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['GazoToolsApp.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\magor\\AppData\\Local\\Python\\pythoncore-3.14-64\\Lib\\site-packages\\tkinterdnd2\\tkdnd', 'tkinterdnd2/tkdnd')],
    hiddenimports=['ctypes.wintypes', 'torch', 'torchvision', 'torchvision.models', 'torchvision.transforms', 'tkinter', 'tkinter.ttk', 'tkinter.messagebox', 'tkinter.filedialog', 'send2trash'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['GazoToolsLogic', 'lib'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GazoTools',
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
    icon=['PicClass.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GazoTools',
)

# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# Récupère tous les fichiers dans img/ de façon récursive
img_datas = []
for root, dirs, files in os.walk('img'):
    for file in files:
        full_path = os.path.join(root, file)
        img_datas.append((full_path, root))

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('font/*', 'font'),
        ('icon/*', 'icon'),
        ('images/*', 'images'),
        ('score/options.txt', 'score'),
        ('profile/compte.txt', 'profile'),
        ('docs/*', 'docs')
    ] + img_datas,
    hiddenimports=collect_submodules("pygame"),  # si tu utilises pygame ou d’autres modules
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GuessMyClass',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # garde False pour ne pas voir de terminal
    icon='gmc.ico'
)



# -*- mode: python -*-

block_cipher = None

from pathlib import Path
import sys
sys.path.append(str(Path('.').absolute()))

from pyinstaller_setup import filter_local_files
from setup import APP_NAME, STARTUP_SCRIPT, PACKAGE_DIR, EXCLUDE_PACKAGES

a = Analysis([STARTUP_SCRIPT],
             pathex=['.', PACKAGE_DIR],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=EXCLUDE_PACKAGES,
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

remains = filter_local_files(a.pure)
	
pyz = PYZ(remains, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name=APP_NAME,
          debug=False,
          strip=True,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name=APP_NAME)

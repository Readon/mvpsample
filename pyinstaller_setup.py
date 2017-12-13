#!/usr/bin/env python
import os
import sys
import subprocess
import shutil

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

def _pyinstaller_script():
    path = Path(sys.executable).parent
    if path.name != 'Scripts':
        path = path.joinpath("Scripts")
    if not path.exists():
        raise Exception("Cannot find scripts directory? %s" % path)
    return str(path / 'pyinstaller')

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def delete_path(path):
    if Path(path).exists():
        if Path(path).is_dir():
            shutil.rmtree(str(path))
        else:
            os.unlink(str(path))

def run(src_path):
    command = [
        _pyinstaller_script(),
        "setup.spec"
    ]

    from setup import APP_NAME
    dst_path = Path("dist")/APP_NAME
    delete_path(dst_path)

    subprocess.call(command)

    copytree(src_path, str(dst_path.absolute()))

def filter_local_files(toc):
    cwd = str(Path('.').absolute())
    path_id = 1
    remains = []
    for each in toc:
        if cwd not in each[path_id]:
            remains.append(each)
    return remains

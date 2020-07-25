#!/usr/bin/env python
# coding: utf-8
import os
from setup import find_python_files
import sys
import subprocess
import shutil

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path


def _pyinstaller_script():
    path = Path(sys.executable).parent
    if path.name != "Scripts":
        path = path.joinpath("Scripts")
    if path.exists():
        return str(path / "pyinstaller")
    return "pyinstaller"


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


def find_python_modules(root, packages):
    ret = []
    for package in [""] + packages:
        dir_ = os.path.join(*package.split("."))
        dir_ = os.path.join(root, dir_)
        if not os.path.exists(dir_):
            continue

        for name in os.listdir(dir_):
            if name.endswith(".py") and name != "__init__.py":
                name = os.path.basename(name)
                name = os.path.splitext(name)[0]
                if package:
                    name = ".".join([package, name])
                ret.append(name)
    return ret


def run(app, package_dir, script, imports, excludes, datas):
    command = [_pyinstaller_script()]
    command += ["--noconfirm"]

    modules = find_python_modules(package_dir, imports) + imports
    for module in modules:
        command += ["--hidden-import", module]

    for module in excludes:
        command += ["--exclude-module", module]

    for path, datafiles in datas.items():
        path = os.path.join(".", path)
        for datafile in datafiles:
            data_path = os.path.join(package_dir, datafile)
            data_str = "%s;%s" % (data_path, path)
            command += ["--add-data", data_str]

    command += [script]

    print(command)

    dst_path = Path("dist") / app
    delete_path(dst_path)

    subprocess.call(command)


def filter_local_files(toc):
    cwd = str(Path(".").absolute())
    path_id = 1
    remains = []
    for each in toc:
        if cwd not in each[path_id]:
            remains.append(each)
    return remains

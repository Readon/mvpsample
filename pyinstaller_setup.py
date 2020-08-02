#!/usr/bin/env python
# coding: utf-8
import os
import shutil

from PyInstaller.__main__ import run as pyinstaller_run

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path


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
            if (
                name.endswith(".py") or name.endswith(".pyd")
            ) and name != "__init__.py":
                name = os.path.basename(name)
                name = os.path.splitext(name)[0]
                if package:
                    name = ".".join([package, name])
                ret.append(name)
    return ret


def run(app, package_dir, script, imports, excludes, datas, paths):
    command = []
    command += ["--noconfirm"]
    command += ["--windowed"]
    command += ["--name=%s" % app]
    command += ["--paths=%s" % paths]

    modules = find_python_modules(package_dir, imports) + imports
    modules = set(modules)
    for module in modules:
        command += ["--hidden-import=%s" % module]

    for module in excludes:
        command += ["--exclude-module=%s" % module]

    for path, datafiles in datas.items():
        path = os.path.join(".", path)
        for datafile in datafiles:
            data_path = os.path.join(package_dir, datafile)
            data_str = "%s;%s" % (data_path, path)
            command += ["--add-data=%s" % data_str]

    command += [script]

    # print(command)

    dst_path = Path("dist") / app
    delete_path(dst_path)

    pyinstaller_run(command)

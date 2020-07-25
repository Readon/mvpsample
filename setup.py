#!/usr/bin/env python
# coding: utf-8
import os
from collections import defaultdict

try:
    from setuptools import setup, find_packages
    from setuptools import Extension
except ImportError:
    from distutils.core import setup, find_packages
    from distutils.extension import Extension
from Cython.Build import cythonize

APP_NAME = "MVPSample"
PACKAGE_DIR = "src"
PACKAGES = find_packages(PACKAGE_DIR)
STARTUP_SCRIPT = PACKAGE_DIR + r"\startup.pyw"
EXCLUDE_PACKAGES = ["PySide", "PyQt", "Tkinter"]

DATA_FILES = ["*.ui", "*.glade"]
PACKAGE_DATA = {"": DATA_FILES}

RUNTIME_DEPS = ["gi.repository.Gtk", "traitlets"]
BUILD_DEPS = ["pyinstaller >= 3.3", "cython", "pathlib"]


def find_python_files(root, packages):
    ret = defaultdict(list)
    for package in [""] + packages:
        dir_ = os.path.join(*package.split("."))
        dir_ = os.path.join(root, dir_)
        for name in os.listdir(dir_):
            if name.endswith(".py") and name != "__init__.py":
                ret[package].append(os.path.join(dir_, name))
    return ret


def create_extensions(root, packages):
    extensions = []
    pkg_files = find_python_files(root, packages)
    for package, files in pkg_files.items():
        for name in files:
            base = os.path.basename(name)
            base = os.path.splitext(base)[0]
            if package:
                base = ".".join([package, base])
            extensions.append(Extension(base, [name]))
    return extensions


extensions = create_extensions(PACKAGE_DIR, PACKAGES)

if __name__ == "__main__":
    ret = setup(
        name=APP_NAME,
        version="0.1",
        description="Awg waveform generation and edit application.",
        author="Yindong Xiao",
        author_email="xydarcher@uestc.edu.cn",
        install_requires=RUNTIME_DEPS,
        setup_requires=BUILD_DEPS,
        packages=PACKAGES,
        package_dir={"": PACKAGE_DIR},
        package_data=PACKAGE_DATA,
        scripts=[STARTUP_SCRIPT],
        ext_modules=cythonize(extensions),
    )

    # if "build_ext" in ret.have_run.keys():
    #     print("Clean template files.")
    #     ret.get_command_obj("build_py").cleanup_templatefiles()

    # if "bdist" in ret.commands:
    #     BUILD_PATH = ret.get_command_obj("build_py").build_lib
    #     pyinstaller_run(BUILD_PATH)

#!/usr/bin/env python
# coding: utf-8
import os
import subprocess
from pkg_resources import parse_requirements
from collections import defaultdict

try:
    from setuptools import setup, find_packages
    from setuptools import Extension
except ImportError:
    from distutils.core import setup, find_packages
    from distutils.extension import Extension
from Cython.Build import cythonize

APP_NAME = "MVPSample"
APP_DESCRIPTION = "Binding Example using MVP Pattern."
APP_VERSION = "0.2"
AUTHOR = "Yindong Xiao"
EMAIL = "xydarcher@uestc.edu.cn"

PACKAGE_DIR = "src"
PACKAGES = find_packages(PACKAGE_DIR)
STARTUP_SCRIPT = PACKAGE_DIR + r"\startup.pyw"
EXCLUDE_PACKAGES = ["PySide", "PyQt", "Tkinter"]

PACKAGE_DATA = {
    "": ["*.ui", "*.glade"],
}

REQUIRES_PATH = "requirements.txt"


def generate_requirements(dir_):
    command = ["pipreqs"]
    command += ["--use-local"]
    command += ["--savepath", REQUIRES_PATH]
    command += [dir_]

    subprocess.call(command)


if not os.path.exists(REQUIRES_PATH):
    generate_requirements(PACKAGE_DIR)


with open(REQUIRES_PATH) as f:
    requires = parse_requirements(f.read().splitlines())
    requirements = [x.name for x in requires]
RUNTIME_DEPS = ["gi.repository.Gtk", "traitlets"] + requirements
BUILD_DEPS = ["pyinstaller >= 3.3", "cython", "pathlib", "pipreqs"]


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
        version=APP_VERSION,
        description=APP_DESCRIPTION,
        author=AUTHOR,
        author_email=EMAIL,
        install_requires=RUNTIME_DEPS,
        setup_requires=BUILD_DEPS,
        packages=PACKAGES,
        package_dir={"": PACKAGE_DIR},
        package_data=PACKAGE_DATA,
        scripts=[STARTUP_SCRIPT],
        ext_modules=cythonize(extensions),
    )

#!/usr/bin/env python
# coding: utf-8
import os
import subprocess
import sys
import shutil
from pkg_resources import parse_requirements
from collections import defaultdict

from pyinstaller_setup import run as pyinstaller_run
from Cython.Build import cythonize
from setup import (
    APP_NAME,
    APP_DESCRIPTION,
    APP_VERSION,
    AUTHOR,
    EMAIL,
    PACKAGE_DIR,
    PACKAGES,
    STARTUP_SCRIPT,
    PACKAGE_DATA,
    RUNTIME_DEPS,
    BUILD_DEPS,
    REQUIRES_PATH,
    setup,
    Extension,
)


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
RUNTIME_DEPS = [
    "gi.repository.Gtk",
    "traitlets",
] + requirements
EXCLUDE_PACKAGES = ["PySide", "PyQt", "Tkinter"]


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
    return cythonize(
        extensions,
        compiler_directives={"language_level": sys.version[0]},
        build_dir=os.path.join("build", "cython"),
    )


extensions = create_extensions(PACKAGE_DIR, PACKAGES)
BUILD_DEPS = BUILD_DEPS + ["pyinstaller >= 3.3", "cython", "pipreqs"]

if __name__ == "__main__":
    old_argv = sys.argv

    sys.argv = ["setup.py", "build_ext"]
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
        ext_modules=extensions,
    )

    sys.argv = old_argv

    build_script = os.path.split(STARTUP_SCRIPT)[-1]
    build_script = os.path.join(
        ret.get_command_obj("build_ext").build_lib, build_script)
    shutil.copy2(STARTUP_SCRIPT, build_script)

    pyinstaller_run(
        APP_NAME,
        PACKAGE_DIR,
        build_script,
        PACKAGES + RUNTIME_DEPS,
        EXCLUDE_PACKAGES,
        PACKAGE_DATA,
        PACKAGE_DIR,
    )

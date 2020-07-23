#!/usr/bin/env python
try:
    from setuptools import setup, find_packages
    from setuptools import Extension
except ImportError:
    from distutils.core import setup, find_packages
    from distutils.extension import Extension

# from nuitka_setup import Nuitka
from pyinstaller_setup import run as pyinstaller_run
from cython_setup import Cython

APP_NAME = "MVPSample"
PACKAGE_DIR = "src"
PACKAGES = [""] + find_packages(PACKAGE_DIR)
STARTUP_SCRIPT = PACKAGE_DIR + r"\startup.pyw"
EXCLUDE_PACKAGES = ["PySide", "PyQt", "_tkinter"]

DATA_FILES = ["*.ui", "*.glade"]

RUNTIME_DEPS = []
BUILD_DEPS = ["pyinstaller >= 3.3", "cython", "pathlib"]

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
        package_data={"": DATA_FILES},
        scripts=[STARTUP_SCRIPT],
        cmdclass={"build_py": Cython},
    )

    if "build_ext" in ret.have_run.keys():
        print("Clean template files.")
        ret.get_command_obj("build_py").cleanup_templatefiles()

    if "bdist" in ret.commands:
        BUILD_PATH = ret.get_command_obj("build_py").build_lib
        pyinstaller_run(BUILD_PATH)

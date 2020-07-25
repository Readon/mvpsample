#!/usr/bin/env python
# coding: utf-8
import sys
from pyinstaller_setup import run as pyinstaller_run
from Cython.Build import cythonize
from setup import (
    APP_NAME,
    PACKAGE_DIR,
    PACKAGES,
    STARTUP_SCRIPT,
    EXCLUDE_PACKAGES,
    PACKAGE_DATA,
    RUNTIME_DEPS,
    BUILD_DEPS,
    setup,
    extensions,
)

if __name__ == "__main__":
    old_argv = sys.argv

    sys.argv = ["setup.py", "build_ext", "--inplace"]

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

    sys.argv = old_argv

    pyinstaller_run(
        PACKAGE_DIR,
        STARTUP_SCRIPT,
        PACKAGES + RUNTIME_DEPS,
        EXCLUDE_PACKAGES,
        PACKAGE_DATA,
    )


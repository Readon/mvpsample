#!/usr/bin/env python
# coding: utf-8
import os
from collections import defaultdict

try:
    from setuptools import Extension
except ImportError:
    from distutils.extension import Extension

from pyinstaller_setup import run as pyinstaller_run
from setup import (
    APP_NAME,
    PACKAGE_DIR,
    PACKAGES,
    STARTUP_SCRIPT,
    EXCLUDE_PACKAGES,
    PACKAGE_DATA,
    RUNTIME_DEPS,
)

if __name__ == "__main__":
    pyinstaller_run(
        APP_NAME,
        PACKAGE_DIR,
        STARTUP_SCRIPT,
        PACKAGES + RUNTIME_DEPS,
        EXCLUDE_PACKAGES,
        PACKAGE_DATA,
    )


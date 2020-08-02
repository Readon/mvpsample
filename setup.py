#!/usr/bin/env python
# coding: utf-8
from pkg_resources import parse_requirements

try:
    from setuptools import setup, find_packages
    from setuptools import Extension
except ImportError:
    from distutils.core import setup, find_packages
    from distutils.extension import Extension

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

with open(REQUIRES_PATH) as f:
    requires = parse_requirements(f.read().splitlines())
    requirements = [x.name for x in requires]
RUNTIME_DEPS = requirements
BUILD_DEPS = []

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
    )

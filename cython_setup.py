#!/usr/bin/env python
import os
import sys
import shutil
import subprocess

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

try:    
    from setuptools.command.build_py import build_py as _build_py
    from setuptools import Extension
except ImportError:
    from distutils.command.build_py import build_py as _build_py
    from distutils import Extension

from Cython.Build import cythonize

from distutils.msvccompiler import MSVCCompiler
msvc = MSVCCompiler()
msvc.initialize()
del msvc

INIT_HIDEN_NAME = u'_init'
INIT_HIDEN_FILE = INIT_HIDEN_NAME + '.py'


class Cython(_build_py):

    @staticmethod
    def _delete_path(path):
        if Path(path).exists():
            if Path(path).is_dir():
                shutil.rmtree(str(path))
            else:
                os.unlink(str(path))
    
    def cleanup_templatefiles(self):
        try:
            len(self._cython_templatefiles)
        except AttributeError:
            return
        
        for file_ in self._cython_templatefiles:
            Cython._delete_path(file_)
            Cython._delete_path(file_.with_suffix('.pyc'))
            Cython._delete_path(file_.with_suffix('.c'))

    def build_module(self, module, module_file, package):
        from nuitka.importing.Importing import setMainScriptDirectory
        dist = self.distribution
        if not dist.ext_modules or '' in dist.ext_modules:
            dist.ext_modules = []

        package_blocks = package.split('.')

        src_path = Path(module_file)
        infile = self.get_module_outfile(self.build_lib, package_blocks, module) 
        original = Path(infile)

        if module == "__init__":
            final_pyd = original.parent / INIT_HIDEN_FILE
            final_pyd = final_pyd.with_suffix('.pyd')
        else:
            final_pyd = original.with_suffix('.pyd')

        if final_pyd.exists():
            dst_mtime = final_pyd.stat().st_mtime
            src_mtime = src_path.stat().st_mtime
            if src_mtime < dst_mtime:
                return
        _build_py.build_module(self, module, module_file, package)
                
        if module == "__init__":
            new_name = original.with_name(INIT_HIDEN_FILE)
            if new_name.exists():
                self._delete_path(new_name)
            original.rename(new_name)
            with original.open('w') as stub_init:
                stub_init.write("from .%s import *" % INIT_HIDEN_NAME)
            original = new_name
            module = INIT_HIDEN_NAME

        target = original.name
        cwd = original.parent
        self._delete_path(final_pyd)

        #print("compiling %s -> %s" % (str(original), final_pyd))
        try:
            len(self._cython_templatefiles)
        except AttributeError:
            self._cython_templatefiles = []
        
        self._cython_templatefiles.append(original)
        module_name = str('.'.join([package, module]))
        extension = Extension(module_name, [str(original)])
        dist.ext_modules += cythonize([extension])


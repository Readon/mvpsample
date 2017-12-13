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
except ImportError:
    from distutils.command.build_py import build_py as _build_py

from distutils.msvccompiler import MSVCCompiler
msvc = MSVCCompiler()
msvc.initialize()
del msvc

INIT_HIDEN_NAME = u'_init'
INIT_HIDEN_FILE = INIT_HIDEN_NAME + '.py'

class Nuitka(_build_py):
    @staticmethod
    def _nuitka_script():
        """
        Only working for windows, find the nuitka run script.
        TODO: setuptools.entry_points handling could probably be used to find the correct location for any platform
        :return:
        """
        path = Path(sys.executable).parent
        if path.name != 'Scripts':
            path = path.joinpath("Scripts")
        if not path.exists():
            raise Exception("Cannot find scripts directory? %s" % path)
        return path / 'nuitka'

    @staticmethod
    def _delete_path(path):
        if Path(path).exists():
            if Path(path).is_dir():
                shutil.rmtree(str(path))
            else:
                os.unlink(str(path))

    @staticmethod
    def _cleanup_tempfiles(original):
        Nuitka._delete_path(original.with_suffix('.build'))
        Nuitka._delete_path(original.with_suffix('.lib'))
        Nuitka._delete_path(original.with_suffix('.exp'))
        Nuitka._delete_path(original.with_suffix('.pyi'))
        Nuitka._delete_path(original.with_suffix('.pyc'))

    @staticmethod
    def cleanup_module(original, cwd, target):
        """ This will delete the original python source and any temp build files
        """
        original = Path(original)
        Nuitka._delete_path(original)
        Nuitka._cleanup_tempfiles(original)

        if target == INIT_HIDEN_FILE:
            with (cwd / '__init__.py').open('w') as stub_init:
                stub_init.write("from .%s import *" % INIT_HIDEN_NAME)

    def _build_package(self, package, modules):
        cwd = Path(self.build_lib)       
        target = cwd / package
        subprocess.call([sys.executable, str(self._nuitka_script()), '--module', package,
                    '--recurse-directory', package, '--recurse-to', package], cwd=str(cwd))
        self._cleanup_tempfiles(target)
        
        for (package_, module, module_file) in modules:
            infile = self.get_module_outfile(self.build_lib, [package_], module)
            infile = Path(infile)
            self._delete_path(infile)
            self._delete_path(infile.with_suffix('.pyc'))

    def build_module(self, module, module_file, package):
        from nuitka.importing.Importing import setMainScriptDirectory

        src_path = Path(module_file)
        infile = self.get_module_outfile(self.build_lib, [package], module) 
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
            original.rename(new_name)
            original = new_name

        target = original.name
        cwd = original.parent
        self._delete_path(final_pyd)

        print("compiling %s -> %s" % ((cwd / target), final_pyd))
        command = [
            sys.executable,
            str(self._nuitka_script()),
            "--module",
            #"--plugin-enable=pylint-warnings",
            "--recurse-to=traits.api",
            "--recurse-to=traits.trait_notifiers",
            "--recurse-to=types",
            "--recurse-not-to=*.tests",
            "--show-modules",
            "--remove-output",
            target,
        ]
        subprocess.call(command, cwd=str(cwd))

        if final_pyd.exists():
            self.cleanup_module(original, cwd, target)


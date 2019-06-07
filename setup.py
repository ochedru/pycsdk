import sys
import os
import shutil

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

# clean previous build
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        if (name.startswith("pycsdk") and not(name.endswith(".pyx") or name.endswith(".pxd"))):
            os.remove(os.path.join(root, name))
    for name in dirs:
        if (name == "build"):
            shutil.rmtree(name)

# build "pycsdk.so" python extension to be added to "PYTHONPATH" afterwards...

class CsdkBuildExt(build_ext):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pyrex_gdb = True

setup(
    name='pycsdk',
    version='20.3.2',
    cmdclass = {'build_ext': CsdkBuildExt},
    ext_modules = [
        Extension("pycsdk",
                  sources=["pycsdk.pyx"],
                  libraries=["kernelapi", "recpdf", "recapiplus"],
                  extra_compile_args=["-I/usr/local/include/nuance-omnipage-csdk-20.3", "-Wno-unused", "-g", "-O0", "-ggdb", "-fno-omit-frame-pointer"],
                  extra_link_args=["-L/usr/local/lib/nuance-omnipage-csdk-lib64-20.3"]
             )
        ]
)

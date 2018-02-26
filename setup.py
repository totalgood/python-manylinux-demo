from distutils.core import setup, Extension

import os
import platform
import sys

__version__ = "0.2.11"

# distutils will try to locate and link dynamically against portaudio.
#
# If you would rather statically link in the portaudio library (e.g.,
# typically on Microsoft Windows), run:
#
# % python setup.py build --static-link
#
# Specify the environment variable PORTAUDIO_PATH with the build tree
# of PortAudio.

STATIC_LINKING = False

if "--static-link" in sys.argv:
    STATIC_LINKING = True
    sys.argv.remove("--static-link")

portaudio_path = os.environ.get("PORTAUDIO_PATH", "./portaudio-v19")
mac_sysroot_path = os.environ.get("SYSROOT_PATH", None)

pyaudio_module_sources = [os.path.join('pyaudio3', 'src', '_portaudiomodule.c')]
include_dirs = []
external_libraries = []
extra_compile_args = []
extra_link_args = []
scripts = []
defines = []

if sys.platform == 'darwin':
    defines += [('MACOSX', '1')]
    if mac_sysroot_path:
        extra_compile_args += ["-isysroot", mac_sysroot_path]
        extra_link_args += ["-isysroot", mac_sysroot_path]
elif sys.platform == 'win32':
    bits = platform.architecture()[0]
    if '64' in bits:
        defines.append(('MS_WIN64', '1'))

if not STATIC_LINKING:
    external_libraries = ['portaudio']
    extra_link_args = []
else:
    include_dirs = [os.path.join(portaudio_path, 'include/')]
    extra_link_args = [
        os.path.join(portaudio_path, 'lib', '.libs', 'libportaudio.a')
        ]

    # platform specific configuration
    if sys.platform == 'darwin':
        extra_link_args += ['-framework', 'CoreAudio',
                            '-framework', 'AudioToolbox',
                            '-framework', 'AudioUnit',
                            '-framework', 'Carbon']
    elif sys.platform == 'cygwin':
        external_libraries += ['winmm']
        extra_link_args += ['-lwinmm']
    elif sys.platform == 'win32':
        # i.e., Win32 Python with mingw32
        # run: python setup.py build -cmingw32
        external_libraries += ['winmm']
        extra_link_args += ['-lwinmm']
    elif sys.platform == 'linux2':
        extra_link_args += ['-lrt', '-lm', '-lpthread']
        # GNU/Linux has several audio systems (backends) available; be
        # sure to specify the desired ones here.  Start with ALSA and
        # JACK, since that's common today.
        extra_link_args += ['-lasound', '-ljack']

extension_module = Extension(
    '_portaudio',
    sources=pyaudio_module_sources,
    include_dirs=include_dirs,
    define_macros=defines,
    libraries=external_libraries,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args
    )

# extension_module = Extension(
#     'pymanylinuxdemo.extension',
#      sources=['pymanylinuxdemo/extension.c'],
#      library_dirs=['/usr/lib64/atlas/', '/usr/lib/atlas'],
#      include_dirs=['/usr/include'],
#      libraries=['cblas']
# )


setup(
    name='pyaudio3',
    version=__version__,
    author="Hubert Pham",
    url="http://people.csail.mit.edu/hubert/pyaudio/",
    description='PortAudio Python Bindings',
    long_description=__doc__.lstrip(),
    scripts=scripts,
    py_modules=['pyaudio'],
    package_dir={'': os.path.join('pyaudio3', 'src')},
    ext_modules=[extension_module]
    )

# setup(
#     name = 'python-manylinux-demo-pyaudio',
#     version = '1.0',
#     description = 'PyAudio package compiled for manylinux environments.',
#     ext_modules = [extension_module],
#     packages=['pymanylinuxdemo', 'pyaudio3', 'pymanylinuxdemo.tests'],
# )

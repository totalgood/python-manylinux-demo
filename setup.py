from distutils.core import setup, Extension

extension_module = Extension(
    'pymanylinuxdemo.extension',
     sources=['pymanylinuxdemo/extension.c'],
     library_dirs=['/usr/lib64/atlas/', '/usr/lib/atlas'],
     include_dirs=['/usr/include'],
     libraries=['cblas']
)

setup(
    name = 'python-manylinux-demo-pyaudio',
    version = '1.0',
    description = 'PyAudio package compiled for manylinux environments.',
    ext_modules = [extension_module],
    packages=['pymanylinuxdemo', 'pyaudio3', 'pymanylinuxdemo.tests'],
)

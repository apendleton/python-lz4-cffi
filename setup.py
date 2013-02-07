from setuptools import setup, find_packages, distutils, Extension
from setuptools.command.build_py import build_py as BaseBuild
import os, subprocess

ext = Extension('lz4/liblz4',
        sources = ['lz4/lz4.c', 'lz4/lz4hc.c', 'lz4/lz4_offset_hack.c'],
        extra_compile_args = ["-O3", "-fPIC", "-std=c99", "-Wall", "-W", "-Wundef", "-Wno-implicit-function-declaration"],
    )

f = open(os.path.join(os.path.dirname(__file__), 'README'))
readme = f.read()
f.close()

setup(
    name='lz4',
    version=0.2,
    description='A port of the python-lz4 package from the CPython API to CFFI.',
    long_description=readme,
    author='Andrew Pendleton',
    author_email='apendleton@sunlightfoundation.com',
    url='http://github.com/apendleton/python-lz4-cffi/',
    packages=find_packages(),
    license='BSD License',
    platforms=["any"],
    py_modules=["lz4"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Environment :: Web Environment',
    ],
    install_requires=["cffi"],
    ext_modules=[ext]
)

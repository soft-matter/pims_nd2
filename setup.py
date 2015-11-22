import os
from setuptools import setup


try:
    descr = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
except IOError:
    descr = ''

try:
    from pypandoc import convert
    descr = convert(descr, 'rst', format='md')
except ImportError:
    pass

setup_parameters = dict(
    name="pims_nd2",
    version="0.4",
    description="ND2SDK wrapper for PIMS",
    author="Casper van der Wel",
    install_requires=['pims>=0.3'],
    author_email="caspervdw@gmail.com",
    url="https://github.com/soft-matter/pims_nd2",
    download_url="https://github.com/soft-matter/pims_nd2/tarball/0.4",
    packages=['pims_nd2'],
    include_package_data=True,
    classifiers=["Development Status :: 4 - Beta",
                 "Intended Audience :: Science/Research",
                 "Programming Language :: C",
                 "Programming Language :: Python",
                 "Programming Language :: Python :: 2",
                 "Programming Language :: Python :: 3",
                 "Topic :: Scientific/Engineering",
                 "Operating System :: Microsoft :: Windows",
                 "Operating System :: POSIX",
                 "Operating System :: Unix",
                 "Operating System :: MacOS"],
    platforms=['MacOS X', 'Windows', 'Linux CentOs 6.5/7', 'Linux Debian 7/8'],
    long_description=descr)

setup(**setup_parameters)

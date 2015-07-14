import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup_parameters = dict(
    name="PIMS_ND2",
    version="0.1",
    description="ND2SDK wrapper for PIMS",
    author="Casper van der Wel",
    install_requires=['pims>=0.3'],
    author_email="caspervdw@gmail.com",
    url="https://github.com/soft-matter/pims_nd2",
    packages=['pims_nd2'],
    include_package_data=True,
    platforms=[
#        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows 7',
        'Operating System :: Microsoft :: Windows :: Windows Vista',
#        'Operating System :: POSIX :: Linux',
    ],
    long_description=read('README.md'))

setup(**setup_parameters)

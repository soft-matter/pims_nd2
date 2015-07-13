import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup_parameters = dict(
    name="PIMS_ND2",
    description="ND2SDK wrapper for PIMS",
    author="Casper van der Wel",
    install_requires=['pims'],
    author_email="caspervdw@gmail.com",
    url="https://github.com/caspervdw/pims_nd2",
    packages=['pims_nd2'],
    long_description=read('README.md'))

setup(**setup_parameters)

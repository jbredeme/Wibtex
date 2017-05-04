#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.command.install import install as command

class Install(command):
    """ Customized setuptools install command which uses pip. """

    def run(self, *args, **kwargs):
        import pip
        pip.main(['install', '.'])
        command.run(self, *args, **kwargs)

setup(
    name='wibtex_rms',
    version='1.0',
    cmdclass={
        'install': Install,
    },
    packages=find_packages(),
    install_requires=['bibtexparser', 'jinja2', 'lxml']
)

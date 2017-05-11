#!/usr/bin/env python
import os
import re

from setuptools import find_packages, setup

NAME = 'Wibtex'
VERSION = '1.0.2'
DESCRIPTION = 'In-text citations sourced from BibTeX to Microsoft Word Document'
KEYWORDS = 'docx office openxml word'
AUTHOR = 'Jarid Bredemeier, Charles Duso'
AUTHOR_EMAIL = 'jpb64@nau.edu'
URL = 'https://github.com/jbredeme/Wibtex'
LICENSE = 'MIT License'
PACKAGES = find_packages()
DATA_FILES = [('config', ['config/styles.json']), ('config', ['config/log.properties'])]

INSTALL_REQUIRES = ['lxml>=3.7.2', 'bs4', 'Bibtexparser>=0.6.2', 'Jinja2>=2.9']

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.6.1',
]

params = {
    'name':             NAME,
    'version':          VERSION,
    'description':      DESCRIPTION,
    'keywords':         KEYWORDS,
    'author':           AUTHOR,
    'author_email':     AUTHOR_EMAIL,
    'url':              URL,
    'license':          LICENSE,
    'packages':         PACKAGES,
    'install_requires': INSTALL_REQUIRES,
    'classifiers':      CLASSIFIERS,
    'data_files':       DATA_FILES,
}

setup(**params)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools
from pathlib import Path

VERSION_FILE = Path(__file__).parent / "version.py"
ENV = {}
with VERSION_FILE.open() as f:
    exec(f.read(), ENV)                                 # pylint: disable=w0122
__version__ = ENV['__version__']

with open("README.md") as feed:
    LONG_DESCRIPTION = feed.read()

setuptools.setup(
    name='ipythontutor',
    description='An extension for IPython to embed a pythontutor iframe'
                ' that can illustrate the code in the current cell.',
    url='https://github.com/parmentelat/ipythontutor',
    version=__version__,
    author="Thierry Parmentelat",
    author_email="thierry.parmentelat@inria.fr",
    long_description=LONG_DESCRIPTION,
    long_description_content_type = "text/markdown",
    py_modules=(
        'ipythontutor',
    ),
    install_requires=(
        'ipython',
    ),
)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='ipythontutor',
    version='0.1.0',
    description='An extension for IPython to embed a pythontutor iframe'
                ' that can illustrate the code in the current cell.',
    long_description='See https://github.com/parmentelat/ipythontutor/blob/master/README.ipynb',
    author='Thierry Parmentelat',
    author_email='thierry.parmentelat@inria.fr',
    url='https://github.com/parmentelat/ipythontutor',
    py_modules=(
        'ipythontutor',
    ),
    install_requires=(
        'ipython',
    ),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: IPython',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

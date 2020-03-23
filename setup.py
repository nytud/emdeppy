#!/usr/bin/env pyhton3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import setuptools
from emdeppy import __version__

with open('README.md') as fh:
    long_description = fh.read()

setuptools.setup(
    name='emdeppy',
    version=__version__,
    author='dlazesz',  # Will warn about missing e-mail
    description='A wrapper and REST API implemented in Python for emDep (Bohnet parser a.k.a. Mate Tools)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dlt-rilmta/emdeppy',
    # license='GNU Lesser General Public License v3 (LGPLv3)',  # Never really used in favour of classifiers
    # platforms='any',  # Never really used in favour of classifiers
    packages=setuptools.find_packages(exclude=['test']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.6',
    install_requires=['pyjnius==1.2',  # TODO: List dependencies at only one file requirements.txt vs. setup.py
                      'xtsv<1.0',
                      ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "emdeppy=emdeppy.__main__:main",
        ]
    },
)
#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

setup(
    author="timo-schuerg",
    author_email='timo82@gmx.net',
    python_requires='>=3.5',
    description="",
    keywords='dct',
    name='dct',
    packages=find_packages(include=['dct', 'dct.*']),
)

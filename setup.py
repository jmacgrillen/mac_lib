#! /usr/bin/env python -*- coding: utf-8 -*-
"""
    Name:
        setup.py
    Desscription:
        Install the maclib package.
    Version:
        1 - Inital release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requirements = [
    "PyYaml",
    "requests",
]


def setup_maclib_package() -> None:
    """
    Install and configure the mac_lib package for use
    """
    setup(
        name='maclib',
        version="0.0.1",
        description='Useful stuff for building apps',
        long_description=long_description,
        author='J.MacGrillen',
        scripts=[],
        packages=find_packages(exclude=['tests*']),
        include_package_data=True,
        install_requires=install_requirements,
        license="Apache License 2.0",
        python_requires=">= 3.9.*",
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Natural Language :: English',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
        ],
    )


if __name__ == "__main__":
    setup_maclib_package()

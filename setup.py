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
    "PyYaml=>5.3"
]

def setup_maclib_package() -> None:
    """
    Install and configure the mac_lib package for use
    """
    maclib_metdata = dict(
        name="waldo",
        version="0.0.1",
        author="John MacGrillen",
        author_email="john.macgrillen@thecodeexpress.com",
        description="Handy set of utilities for creating Python applications",
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=find_packages(exclude=["*.tests",
                                        "*.tests.*",
                                        "tests.*",
                                        "tests"]),
        package_dir={"maclib": "src"},
        py_modules=["maclib"],
        install_requires=install_requirements,
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.7',
    )

    setup(**maclib_metdata)

if __name__ == "__main__":
    setup_maclib_package()

# -*- coding: utf-8 -*-

import sys

import setuptools

if sys.version_info < (3,6):
    sys.exit("sorry, python < 3.6 is not supported")

setuptools.setup(
    name    = "fcdstools",
    version = "0.1.0",

    description      = "Famicom Disk System disk image manipulation",
    long_description = open("README.rst").read(),
    license          = "GPLv3",

    author       = "TaoTao",
    author_email = "taotao54321@gmail.com",
    url          = "https://github.com/taotao54321/fcdstools",

    classifiers = (
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: System :: Emulators",
    ),
    keywords = "nes famicom disk system fds",

    install_requires = (
        "setuptools",
        "kaitaistruct",
        "tabulate",
    ),

    packages = setuptools.find_packages(exclude=()),

    scripts = (
        "fdsbuild",
        "fdscheck",
        "fdssjson",
        "fdssplit",
    ),

    package_data = {
        "fcdstools" : (
            "data/README.txt",
            "data/fdsdb.json",
            "data/fdsdb-ja.json",
        ),
    }
)

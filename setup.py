import os
import sys
import shutil
from glob import glob
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop


install_requires = (
    "requests",
    "lxml",
    "logging"
    )

if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    sys.exit("The program is intended to run under Python 3.5+, sorry")

setup(
    name = "scraper",
    version = "0.1",
    author = "kskon",
    author_email = "kskonovalov100@gmail.com",
    description = "Simple web scraper",
    keywords = "scraper, fly-niki, web",
    packages=find_packages(),
    long_description="",
    install_requires=install_requires,
    test_suite="tests",
    cmdclass = {
        "build_py": build_py,
        "develop": develop
    },
    entry_points = {
        "console_scripts": [
            "scraper = scraper.__main__:main",
        ]
    },
)

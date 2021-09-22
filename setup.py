import sys

from setuptools import setup

if sys.version_info < (3, 7, 0):
    sys.exit("Python 3.7.0+ Required")

setup()

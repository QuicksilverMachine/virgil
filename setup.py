import sys

from setuptools import setup

if sys.version_info < (3, 9, 0):
    sys.exit("Python 3.9.0+ Required")

setup()

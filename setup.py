import sys

from setuptools import setup
from codecs import open
from os import path

if sys.version_info < (2, 7):
    raise NotImplementedError(
        'Unsupported Python version, you need Python 2.7, Python 3.3+ or '
        'PyPy 2.7 to use dbj.'
    )

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


version = '0.1.2'


setup(
    name='dbj',
    version=version,
    description='Simple embedded in memory json database',
    long_description=long_description,
    author='Pedro Buteri Gonring',
    author_email='pedro@bigode.net',
    url='https://github.com/pdrb/dbj',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='simple json database',
    py_modules=['dbj'],
    test_suite='test_dbj'
)

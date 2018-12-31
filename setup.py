from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


version = '0.1.0'


setup(
    name='dbj',
    version=version,
    description='Simple embedded in memory json database',
    long_description=long_description,
    author='Pedro Buteri Gonring',
    author_email='pedro@bigode.net',
    url='https://github.com/pdrb/dbj',
    license='MIT',
    classifiers=[],
    keywords='simple json database',
    py_modules=['dbj'],
    test_suite='test_dbj'
)

"""Installation script."""
from setuptools import setup


PACKAGE_NAME = 'astutils'
DESCRIPTION = 'Utilities for abstract syntax trees and parsing with PLY.'
PACKAGE_URL = 'https://github.com/johnyf/{name}'.format(name=PACKAGE_NAME)
README = 'README.md'
VERSION_FILE = '{name}/_version.py'.format(name=PACKAGE_NAME)
MAJOR = 0
MINOR = 0
MICRO = 5
VERSION = '{major}.{minor}.{micro}'.format(
    major=MAJOR, minor=MINOR, micro=MICRO)
VERSION_FILE_TEXT = (
    '# This file was generated from setup.py\n'
    "version = '{version}'\n").format(version=VERSION)
TESTS_REQUIRE = ['pytest >= 4.6.11']
KEYWORDS = [
    'lexing', 'parsing', 'syntax tree', 'abstract syntax tree',
    'AST', 'PLY', 'lex', 'yacc']
CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Topic :: Software Development']


if __name__ == '__main__':
    with open(VERSION_FILE, 'w') as f:
        f.write(VERSION_FILE_TEXT)
    with open(README) as f:
        long_description = f.read()
    setup(
        name=PACKAGE_NAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description=long_description,
        author='Ioannis Filippidis',
        author_email='jfilippidis@gmail.com',
        url=PACKAGE_URL,
        license='BSD',
        install_requires=['ply >= 3.4, <= 3.10'],
        tests_require=TESTS_REQUIRE,
        packages=[PACKAGE_NAME],
        package_dir={PACKAGE_NAME: PACKAGE_NAME},
        classifiers=CLASSIFIERS,
        keywords=KEYWORDS)

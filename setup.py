"""Installation script."""
import setuptools


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
PYTHON_REQUIRES = (
    '>=2.7, '
    '!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*')
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
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Topic :: Software Development']


def run_setup():
    """Install."""
    with open(VERSION_FILE, 'w') as f:
        f.write(VERSION_FILE_TEXT)
    with open(README) as f:
        long_description = f.read()
    setuptools.setup(
        name=PACKAGE_NAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description=long_description,
        long_description_content_type='text/markdown',
        author='Ioannis Filippidis',
        author_email='jfilippidis@gmail.com',
        url=PACKAGE_URL,
        license='BSD',
        python_requires=PYTHON_REQUIRES,
        install_requires=['ply >= 3.4, <= 3.10'],
        tests_require=TESTS_REQUIRE,
        packages=[PACKAGE_NAME],
        package_dir={PACKAGE_NAME: PACKAGE_NAME},
        classifiers=CLASSIFIERS,
        keywords=KEYWORDS)


if __name__ == '__main__':
    run_setup()

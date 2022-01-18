"""Installation script."""
import setuptools


PACKAGE_NAME = 'astutils'
DESCRIPTION = 'Utilities for abstract syntax trees and parsing with PLY.'
PACKAGE_URL = f'https://github.com/johnyf/{PACKAGE_NAME}'
README = 'README.md'
VERSION_FILE = f'{PACKAGE_NAME}/_version.py'
VERSION = '0.0.6'
VERSION_FILE_TEXT = (
    '# This file was generated from setup.py\n'
    f"version = '{VERSION}'\n")
PYTHON_REQUIRES = '>=3.10'
TESTS_REQUIRE = ['pytest >= 4.6.11']
KEYWORDS = [
    'lexing', 'parsing', 'syntax tree', 'abstract syntax tree',
    'AST', 'PLY', 'lex', 'yacc']
CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3 :: Only',
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

from setuptools import setup


name = 'astutils'
description = 'Utilities for abstract syntax trees and parsing with PLY.'
url = 'https://github.com/johnyf/{name}'.format(name=name)
README = 'README.md'
VERSION_FILE = '{name}/_version.py'.format(name=name)
MAJOR = 0
MINOR = 0
MICRO = 1
version = '{major}.{minor}.{micro}'.format(
    major=MAJOR, minor=MINOR, micro=MICRO)
s = (
    '# This file was generated from setup.py\n'
    "version = '{version}'\n").format(version=version)
keywords = [
    'lexing', 'parsing', 'syntax tree', 'abstract syntax tree',
    'AST', 'PLY', 'lex', 'yacc']

if __name__ == '__main__':
    with open(VERSION_FILE, 'w') as f:
        f.write(s)
    setup(
        name=name,
        version=version,
        description=description,
        long_description=open(README).read(),
        author='Ioannis Filippidis',
        author_email='jfilippidis@gmail.com',
        url=url,
        license='BSD',
        install_requires=['ply >= 3.4'],
        packages=[name],
        package_dir={name: name},
        keywords=keywords)

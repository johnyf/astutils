"""Example of a `setup.py` that builds PLY tables.

It uses `pip` to install `ply`,
then it calls `_rewrite_tables` to (re)write the table files,
and finally uses `setuptools` to install the package.

If the package contains multiple parsers,
then each parsing module can provide a `_rewrite_tables`
function that hides the details (table file name, etc).

If some parsing module has extra dependenies,
then these can be installed using `pip.main`.

Although `pip` installs dependencies in `install_requires` first,
the below works also if one runs `python setup.py install`,
assuming that `pip` is available.
"""
import pip
from setuptools import setup


name = 'foo'
description = 'foo is very useful.'
url = 'https://home.org/{name}'.format(name=name)
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
ply_required = 'ply >= 3.4'
install_requires = [ply_required]
tests_require = [
    'nose >= 1.3.4']


if __name__ == '__main__':
    with open(VERSION_FILE, 'w') as f:
        f.write(s)
    # first install PLY, then build the tables
    pip.main(['install', ply_required])
    from foo import lexyacc
    lexyacc._rewrite_tables(outputdir=name)
    # so that they will be copied to `site-packages`
    setup(
        name=name,
        version=version,
        description=description,
        long_description=open(README).read(),
        author='John Doe',
        author_email='john@doe.com',
        url=url,
        license='BSD',
        install_requires=install_requires,
        tests_require=tests_require,
        packages=[name],
        package_dir={name: name},
        keywords=['parsing', 'setup'])

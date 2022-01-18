"""Example of a `setup.py` that builds PLY tables.

It uses `pip` to install `ply`,
then it calls `_rewrite_tables` to (re)write the table files,
and finally uses `setuptools` to install the package.

If the package contains multiple parsers,
then each parsing module can provide a `_rewrite_tables`
function that hides the details (table file name, etc).

If some parsing module has extra dependenies,
then these can be installed using `pip`.

Although `pip` installs dependencies in `install_requires` first,
the below works also if one runs `python setup.py install`,
assuming that `pip` is available.
"""
import subprocess
import sys

import setuptools


PACKAGE_NAME = 'foo'
DESCRIPTION = 'foo is very useful.'
PACKAGE_URL = f'https://example.org/{PACKAGE_NAME}'
README = 'README.md'
VERSION_FILE = f'{PACKAGE_NAME}/_version.py'
VERSION = '0.0.1'
VERSION_FILE_TEXT = (
    '# This file was generated from setup.py\n'
    f"version = '{VERSION}'\n")
PYTHON_REQUIRES = '>=3.10'
PLY_REQUIRED = 'ply >= 3.4, <= 3.10'
INSTALL_REQUIRES = [PLY_REQUIRED]
TESTS_REQUIRE = [
    'pytest >= 4.6.11']


def run_setup():
    """Install."""
    with open(VERSION_FILE, 'w') as f:
        f.write(VERSION_FILE_TEXT)
    # first install PLY, then build the tables
    _install_ply()
    _build_parser()
    # so that they will be copied to `site-packages`
    with open(README) as f:
        long_description = f.read()
    setuptools.setup(
        name=PACKAGE_NAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description=long_description,
        author='Name',
        author_email='name@example.org',
        url=PACKAGE_URL,
        license='BSD',
        python_requires=PYTHON_REQUIRES,
        install_requires=INSTALL_REQUIRES,
        tests_require=TESTS_REQUIRE,
        packages=[PACKAGE_NAME],
        package_dir={PACKAGE_NAME: PACKAGE_NAME},
        keywords=['parsing', 'setup'])


def _install_ply():
    cmd = [
        sys.executable,
        '-m', 'pip', 'install',
        PLY_REQUIRED]
    subprocess.check_call(cmd)


def _build_parser():
    from foo import lexyacc
    lexyacc._rewrite_tables(
        outputdir=PACKAGE_NAME)


if __name__ == '__main__':
    run_setup()

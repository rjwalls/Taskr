#!/usr/bin/env python
__author__ = 'rjwalls'
__author_email__ = 'rjwalls@cse.psu.edu'


from setuptools import setup, find_packages
import sys

requires = []

if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    requires += ['argparse']

setup(
    name='taskr',
    version='0.1',
    packages=find_packages(),
    author=__author__,
    author_email = __author_email__,
    description='time management tool (that I develop when procrastinating)',
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'taskr = taskr.taskr:main'
        ],
    }
)

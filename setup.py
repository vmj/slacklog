#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
import slacklog

import unittest
def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('test', pattern='*.py')
    return test_suite

setup(
    name='slacklog',
    version=slacklog.__version__,
    author='Mikko Värri',
    author_email='vmj@linuxbox.fi',
    maintainer='Mikko Värri',
    maintainer_email='vmj@linuxbox.fi',
    packages=['slacklog', ],
    entry_points={
        'console_scripts': [
            'slacklog2atom      = slacklog.scripts:slacklog2atom',
            'slacklog2pyblosxom = slacklog.scripts:slacklog2pyblosxom',
            'slacklog2rss       = slacklog.scripts:slacklog2rss'
        ]
    },
    url='http://pypi.python.org/pypi/slacklog/',
    license='GNU GPLv3',
    description=slacklog.__doc__,
    long_description=''.join([
            open('README.rst').read(),
            '\n\n',
            open('CHANGES.rst').read()
            ]),
    install_requires=['python-dateutil', ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
        'Topic :: Utilities',
        ],
    keywords='slackware changelog rss atom',
    test_suite='setup.my_test_suite'
    )

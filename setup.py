#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
import slacklog
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
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        ],
    )

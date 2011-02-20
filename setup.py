#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
import slacklog
setup(
    name='slacklog',
    version=slacklog.__version__,
    author='Mikko Värri',
    author_email='vmj@linuxbox.fi',
    maintainer='Mikko Värri',
    maintainer_email='vmj@linuxbox.fi',
    packages=['slacklog',],
    scripts=['bin/slacklog2rss',
             'bin/slacklog2pyblosxom'],
    url='http://pypi.python.org/pypi/slacklog/',
    license='GNU GPLv3',
    description=slacklog.__doc__,
    long_description=''.join([
            open('README.rst').read(),
            '\n\n',
            open('CHANGES.rst').read()
            ]),
    install_requires=['python-dateutil',],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        ],
    )

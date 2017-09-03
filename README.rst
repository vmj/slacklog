.. image:: https://img.shields.io/pypi/v/slacklog.svg?style=plastic
   :target: http://pypi.python.org/pypi/slacklog
   :alt: Download
.. image:: https://travis-ci.org/vmj/slacklog.svg?branch=master
   :target: https://travis-ci.org/vmj/slacklog
   :alt: Build Status
.. image:: http://readthedocs.org/projects/slacklog/badge/?version=latest
   :target: http://slacklog.readthedocs.io/en/latest/?badge=latest
   :alt: Docs

slacklog -- Convert Slackware Changelog to various formats
**********************************************************

slacklog provides programs and a library to convert a Slackware
ChangeLogs into other formats.  Currently, RSS, Atom, and PyBlosxom
formats are supported.

| Download: http://pypi.python.org/pypi/slacklog
| Source code: http://github.com/vmj/slacklog
| Builds status: https://travis-ci.org/vmj/slacklog
| Docs: http://slacklog.readthedocs.org

.. contents::


Basic usage
===========

Typical usage of the program looks like this::

    $ slacklog2rss --changelog slackware-current/ChangeLog.txt \
                   --encoding iso8859-1 \
                   --out ~/public_html/slackware-current.rss \
                   --slackware "Slackware current" \
                   --rssLink "http://linuxbox.fi/~vmj/slackware-current.rss" \
                   --description "Slackware current activity" \
                   --managingEditor "vmj@linuxbox.fi (Mikko Värri)" \
                   --webMaster "vmj@linuxbox.fi (Mikko Värri)"

The included Python library provides the ability to make custom
formats easily::

    #!/usr/bin/env python
    from __future__ import print_function
    import codecs
    import locale
    from slacklog.parsers import SlackLogParser

    def read(file):
        '''Return file contents as Unicode.'''
        return codecs.open(file, 'r', 'iso8859-1').read()

    def write(str):
        '''Print out in preferred encoding.'''
        print(str.encode(locale.getpreferredencoding()))

    # Parse the ChangeLog
    log = SlackLogParser().parse(read('ChangeLog.txt'))

    # Just an example of walking the log tree and print it out
    for entry in log.entries:
        write(u'[%s] %s\n' % (entry.timestamp.isoformat(), entry.description))
        for pkg in entry.pkgs:
            write(u'%s:%s' % (pkg.pkg, pkg.description))

Note that slacklog package deals solely in Unicode; parser expect to
be given Unicode input and formatters generate Unicode data.


Requirements
============

In addition to Python, `python-dateutil
<http://pypi.python.org/pypi/python-dateutil>`_ is required.

Python versions 2.7 and 3.3 - 3.6 are tested, together with python-dateutil versions 2.1 - 2.6.


Installation
============

Use either ``pip install slacklog`` or download the source archive and
use ``python setup.py install``.

The source code is available at `Python Package Index (PyPI)
<http://pypi.python.org/pypi/slacklog>`_ or, if you want the
unreleased version, from `Github <https://github.com/vmj/slacklog>`_
git repository.


Trying it in Docker
===================

Here's one way to hack on this inside a container::

    $ docker run --rm -it -v $(pwd):/slacklog alpine:3.5 /bin/sh
    # apk add --no-cache python py-setuptools py-dateutil curl
    # cd /slacklog
    # python setup.py install
    # sh examples/fetch-changelogs.sh
    # sh examples/update-slacklog-rss.sh

Obviously, you need Docker installed and working,
and I'm assuming you run those commands in the git clone.


Authors
=======

Original author and current maintainer is Mikko Värri
(vmj@linuxbox.fi).


License
=======

slacklog is Free Software, licensed under GNU General Public License
(GPL), version 3 or later.  See LICENSE.txt file for details.

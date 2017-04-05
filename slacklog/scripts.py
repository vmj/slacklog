# -*- coding: utf-8 -*-
"""
SlackLog scripts
================

SlackLog scripts provides CLI (command line interface) for the SlackLog parsers and formatters.
"""
from __future__ import print_function

import codecs
import locale
from optparse import OptionParser
import slacklog
from slacklog import parsers
from slacklog import formatters

try:
    str = unicode
except NameError:
    pass  # Forward compatibility with Py3k (unicode is not defined)


def u(s):
    """A utility method for ensuring that a command line option argument is unicode.
    
    :param s: Option argument.
    :return: Unicode string or None.
    """
    if isinstance(s, str):
        return s
    if s:
        return codecs.decode(s, locale.getpreferredencoding())
    return None


def i(s):
    """A utility method for ensuring that a command line option argument is int.
    
    :param s: Option argument.
    :return: Integer or None.
    """
    if s:
        return int(s)
    return None


def read(changelog, encoding):
    """Reads the ChangeLog.txt.

    Exits on errors.
    
    :param changelog: File name.
    :param encoding: File encoding.
    :return: Unicode text from the file.
    """
    try:
        f = codecs.open(changelog, 'r', encoding)
    except IOError as e:
        print("%s: %s" % (e.filename, e.strerror))
        exit(e.errno)
    try:
        txt = f.read()
    except UnicodeDecodeError as e:
        print("%s: %s-%s: %s: %s" % (changelog, e.start, e.end, e.encoding, e.reason))
        exit(-1)
    f.close()
    return txt


def write(out, data):
    """Writes the unicode data to a file using UTF-8 encoding.
    
    :param out: File name.
    :param data: Unicode data.    
    """
    f = codecs.open(out, 'w', 'utf-8')
    f.write(data)
    f.close()


def main(**kwargs):
    kwargs['usage'] = ''
    kwargs['version'] = '%%prog %s' % slacklog.__version__
    kwargs['epilog'] = 'Bug reports, suggestions, and patches should be sent to vmj@linuxbox.fi. '\
                       + 'This software is Free Software, released under GPLv3.'

    options = kwargs['options']
    del kwargs['options']

    mandatory = []

    for option in options:
        if 'mandatory' in options[option]:
            if options[option]['mandatory']:
                kwargs['usage'] = '%s --%s %s' % (kwargs['usage'], option, options[option]['metavar'])
                mandatory.append(option)
            del options[option]['mandatory']
    kwargs['usage'] = 'USAGE: %%prog [options]%s' % kwargs['usage']

    optionParser = OptionParser(**kwargs)

    for option in options:
        optionSpec = options[option]
        optionParser.add_option('--%s' % option, **optionSpec)

    (opts, args) = optionParser.parse_args()

    missing = []
    for option in mandatory:
        if getattr(opts, option, None) is None:
            missing.append(option)
    if missing:
        optionParser.error('Missing required option(s): %s' % ', '.join(missing))

    return opts, args

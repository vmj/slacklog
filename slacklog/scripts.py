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


def slacklog2atom():
    #
    #   Define and handle command line options
    #
    (opts, args) = main(
        description='Convert Slackware ChangeLog to Atom',
        options={
            'changelog': {'help': 'Read input from FILE',
                          'metavar': 'FILE', 'mandatory': True},
            'encoding': {'help': 'ChangeLog encoding [default: %default]',
                         'default': 'iso8859-1'},
            'min-date': {'help': 'Last date to include [default: include all]',
                         'metavar': 'DATE'},
            'out': {'help': 'Write output to FILE',
                    'metavar': 'FILE', 'mandatory': True},
            'quiet': {'help': 'Do not print warnings',
                      'action': 'store_true'},
            'max-entries': {'help': 'Max number of Atom entries [default: infinity]',
                            'metavar': 'NUM'},
            'slackware': {'help': 'Slackware version [default: %default].',
                          'default': 'Slackware 13.1'},
            'link': {'help': 'Full URL of the Atom feed',
                     'metavar': 'URL', 'mandatory': True},
            'webLink': {'help': 'Full URL of the HTML version',
                        'metavar': 'URL'},
            'name': {'help': 'NAME of the feed author',
                     'metavar': 'NAME'},
            'email': {'help': 'EMAIL of the feed author',
                      'metavar': 'EMAIL'}
        })

    #
    #   Apply options to parser and formatter
    #
    parsers.SlackLogParser.quiet = opts.quiet
    parsers.SlackLogParser.min_date = parsers.SlackLogParser.parse_date(u(opts.min_date))

    formatters.SlackLogAtomFormatter.max_entries = i(opts.max_entries)
    formatters.SlackLogAtomFormatter.slackware = u(opts.slackware)
    formatters.SlackLogAtomFormatter.link = u(opts.link)
    formatters.SlackLogAtomFormatter.webLink = u(opts.webLink)
    formatters.SlackLogAtomFormatter.name = u(opts.name)
    formatters.SlackLogAtomFormatter.email = u(opts.email)

    #
    #   Read input
    #
    txt = read(opts.changelog, opts.encoding)

    #
    #   Format output
    #
    atom = formatters.SlackLogAtomFormatter.format(parsers.SlackLogParser.parse(txt))

    #
    #   Write output
    #
    write(opts.out, atom)


def slacklog2pyblosxom():
    #
    #   Define and handle command line options
    #
    (opts, args) = main(
        description='Convert Slackware ChangeLog to PyBlosxom blog entries',
        options={
            'changelog': {'help': 'Read input from FILE',
                          'metavar': 'FILE', 'mandatory': True},
            'encoding': {'help': 'ChangeLog encoding [default: %default]',
                         'default': 'iso8859-1'},
            'min-date': {'help': 'Last date to include [default: include all]',
                         'metavar': 'DATE'},
            'datadir': {'help': 'PyBlosxom blog datadir',
                        'metavar': 'DATADIR', 'mandatory': True},
            'quiet': {'help': 'Do not print warnings',
                      'action': 'store_true'},
            'max-entries': {'help': 'Max number of blog entries [default: infinity]',
                            'metavar': 'NUM'},
            'slackware': {'help': 'Slackware version [default: %default].',
                          'default': 'Slackware 13.1'},
            'entry-extension': {'help': 'PyBlosxom entry extention [default: %default]',
                                'default': 'txt'},
            'entry-encoding': {'help': 'PyBlosxom entry encoding [default: %default]',
                               'default': 'utf-8'},
            'tags-separator': {'help': 'PyBlosxom tags separator [default: %default]',
                               'default': ','},
            'pkg-separator': {'help': 'Pkg description separator [default: %default]',
                              'default': ':'},
            'pyfilemtime': {'help': 'Enable pyfilemtime compliance',
                            'action': 'store_true'},
            'overwrite': {'help': 'Overwrite entries that exist',
                          'action': 'store_true'},
            'no-backup': {'help': 'Make a backup before overwriting',
                          'action': 'store_true'},
        })

    #
    #   Apply options to parser and formatter
    #
    parsers.SlackLogParser.quiet = opts.quiet
    parsers.SlackLogParser.min_date = parsers.SlackLogParser.parse_date(u(opts.min_date))

    formatters.SlackLogPyblosxomFormatter.max_entries = i(opts.max_entries)
    formatters.SlackLogPyblosxomFormatter.quiet = opts.quiet
    formatters.SlackLogPyblosxomFormatter.slackware = u(opts.slackware)
    formatters.SlackLogPyblosxomFormatter.datadir = u(opts.datadir)
    formatters.SlackLogPyblosxomFormatter.extension = u(opts.entry_extension)
    formatters.SlackLogPyblosxomFormatter.encoding = u(opts.entry_encoding)
    formatters.SlackLogPyblosxomFormatter.tags_separator = u(opts.tags_separator)
    formatters.SlackLogPyblosxomFormatter.pkg_separator = u(opts.pkg_separator)
    formatters.SlackLogPyblosxomFormatter.overwrite = opts.overwrite
    formatters.SlackLogPyblosxomFormatter.backup = not opts.no_backup
    formatters.SlackLogPyblosxomFormatter.pyfilemtime = opts.pyfilemtime

    #
    #   Read input
    #
    txt = read(opts.changelog, opts.encoding)

    #
    #   Format output (output goes to files, no need to capture the result)
    #
    formatters.SlackLogPyblosxomFormatter.format(parsers.SlackLogParser.parse(txt))


def slacklog2rss():
    #
    #   Define and handle command line options
    #
    (opts, args) = main(
        description='Convert Slackware ChangeLog to RSS',
        options={
            'changelog': {'help': 'Read input from FILE',
                          'metavar': 'FILE', 'mandatory': True},
            'encoding': {'help': 'ChangeLog encoding [default: %default]',
                         'default': 'iso8859-1'},
            'min-date': {'help': 'Last date to include [default: include all]',
                         'metavar': 'DATE'},
            'out': {'help': 'Write output to FILE',
                    'metavar': 'FILE', 'mandatory': True},
            'quiet': {'help': 'Do not print warnings',
                      'action': 'store_true'},
            'max-entries': {'help': 'Max number of RSS entries [default: infinity]',
                            'metavar': 'NUM'},
            'slackware': {'help': 'Slackware version [default: %default].',
                          'default': 'Slackware 13.1'},
            'rssLink': {'help': 'Full URL of the RSS feed',
                        'metavar': 'URL', 'mandatory': True},
            'webLink': {'help': 'Full URL of the HTML version',
                        'metavar': 'URL'},
            'description': {'help': 'Description of the RSS feed',
                            'metavar': 'DESC'},
            'language': {'help': 'Language of the RSS feed [default: %default]',
                         'default': 'en'},
            'managingEditor': {'help': 'EMAIL, and possibly NAME, of the editor',
                               'metavar': 'EMAIL (NAME)'},
            'webMaster': {'help': 'EMAIL, and possibly NAME, of the web master',
                          'metavar': 'EMAIL (NAME)'}
        })

    #
    #   Apply options to parser and formatter
    #
    parsers.SlackLogParser.quiet = opts.quiet
    parsers.SlackLogParser.min_date = parsers.SlackLogParser.parse_date(u(opts.min_date))

    formatters.SlackLogRssFormatter.max_entries = i(opts.max_entries)
    formatters.SlackLogRssFormatter.slackware = u(opts.slackware)
    formatters.SlackLogRssFormatter.rssLink = u(opts.rssLink)
    formatters.SlackLogRssFormatter.webLink = u(opts.webLink)
    formatters.SlackLogRssFormatter.description = u(opts.description)
    formatters.SlackLogRssFormatter.language = u(opts.language)
    formatters.SlackLogRssFormatter.managingEditor = u(opts.managingEditor)
    formatters.SlackLogRssFormatter.webMaster = u(opts.webMaster)

    #
    #   Read input
    #
    txt = read(opts.changelog, opts.encoding)

    #
    #   Format output
    #
    rss = formatters.SlackLogRssFormatter.format(parsers.SlackLogParser.parse(txt))

    #
    #   Write output
    #
    write(opts.out, rss)

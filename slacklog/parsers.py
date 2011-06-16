"""
SlackLog parsers
================

SlackLog parser reads a Slackware ChangeLog.txt and builds an in-memory representation of it using SlackLog models.
"""
from sys import stderr
import re
from datetime import datetime
from dateutil import parser
from dateutil import tz
from slacklog import models


pkg_name_re = re.compile(r'\A[a-z/]+[-a-zA-Z0-9_.]+:  ')

tzinfos = {
    'CDT': -5 * 60 * 60,
    'CST': -6 * 60 * 60,
    }

class SlackLogParser (object):
    """
    Parser for recent (13.x) Slackware ChangeLogs.
    """

    quiet = False
    """If :py:const:`True`, warnings about date parsing are not printed."""
    min_date = None
    """If set to a :py:class:`datetime.datetime` object, any log entries whose timestamp is older are ignored (not parsed)."""

    ENTRY = 0
    """Counter of entries (for debugging)."""
    PKG = 0
    """Counter of packages (for debugging)."""

    def parse(cls, data):
        """
        Return the in-memory representation of the data.

        :param unicode data: the ChangeLog.txt content.
        :returns: in-memory representation of data
        :rtype: :py:class:`slacklog.models.SlackLog`
        """
        assert(isinstance(data, unicode))
        log = models.SlackLog()
        for entry_data in cls.split_log_to_entries(data):
            entry = cls.parse_entry(entry_data, log)
            if entry:
                log.entries.append(entry)
            else:
                break
        return log
    parse = classmethod(parse)

    def split_log_to_entries(cls, data):
        """
        Split the ChangeLog.txt into a list of unparsed entries.

        :param unicode data: the ChangeLog.txt content.
        :returns: list of unparsed entries, separators removed.
        :rtype: [:py:class:`unicode`]
        """
        assert(isinstance(data, unicode))
        return re.split('\n*\+-+\+\n*', data)
    split_log_to_entries = classmethod(split_log_to_entries)

    def parse_entry(cls, data, log):
        """
        Parse a single ChangeLog entry.

        :param unicode data: ChangeLog entry content.
        :param log: in-memory representation that is being parsed.
        :type: :py:class:`slacklog.models.SlackLog`
        :return: in-memory representation of the ChangeLog entry.
        :rtype: :py:class:`slacklog.models.SlackLogEntry`
        """
        assert(isinstance(data, unicode))
        assert(isinstance(log, models.SlackLog))
        cls.ENTRY += 1
        cls.PKG = 0
        #print "%s:%s" % (cls.ENTRY, cls.PKG)
        timestamp, data = cls.parse_entry_timestamp(data)
        if cls.min_date and cls.min_date > timestamp:
            return None
        description, data = cls.parse_entry_description(data)
        entry = models.SlackLogEntry(timestamp, description, log)
        for pkg_data in cls.split_entry_to_pkgs(data):
            pkg = cls.parse_pkg(pkg_data, entry)
            entry.pkgs.append(pkg)
        return entry
    parse_entry = classmethod(parse_entry)

    def parse_entry_timestamp(cls, data):
        """
        Parse ChangeLog entry timestamp from data.

        :param unicode data: ChangeLog entry content.
        :returns: a two element list: timestamp and the rest of the entry.
        :rtype: [:py:class:`datetime.datetime`, :py:class:`unicode`]
        """
        assert(isinstance(data, unicode))
        timestamp_str, data = cls.get_line(data)
        timestamp = cls.parse_date(timestamp_str)
        return [timestamp, data]
    parse_entry_timestamp = classmethod(parse_entry_timestamp)

    def parse_entry_description(cls, data):
        """
        Parse ChangeLog entry desctiption from data.

        :param unicode data: ChangeLog entry content (without timestamp).
        :returns: a two element list: description and the rest of the entry.
        :rtype: [:py:class:`unicode`, :py:class:`unicode`]
        """
        assert(isinstance(data, unicode))
        description = u''
        while data and not pkg_name_re.match(data):
            line, data = cls.get_line(data)
            description += line
        return [description, data]
    parse_entry_description = classmethod(parse_entry_description)

    def split_entry_to_pkgs(cls, data):
        """
        Split ChangeLog entry content into a list of unparsed packages.

        :param unicode data: ChangeLog entry content (without timestamp or description).
        :return: a list of unparsed packages.
        :rtype: [:py:class:`unicode`]
        """
        assert(isinstance(data, unicode))
        pkgs = []
        pkg = u''
        if data == u'' or data == u'\n':
            return []
        for line in data.split('\n'):
            if not pkg_name_re.match(line):
                line += u'\n'
                pkg += line
            else:
                if pkg:
                    pkgs.append(pkg)
                    pkg = u''
                if line:
                    line += u'\n'
                    pkg += line
        if pkg:
            pkgs.append(pkg)
        return pkgs
    split_entry_to_pkgs = classmethod(split_entry_to_pkgs)

    def parse_pkg(cls, data, entry):
        """
        Parse a single package.

        :param unicode data:  Package name and description of the update.
        :param entry: in-memory representation of the ChangeLog entry being parsed.
        :type: :py:class:`slacklog.models.SlackLogEntry`
        :return: in-memory representation of the package.
        :rtype: :py:class:`slacklog.models.SlackLogPkg`
        """
        assert(isinstance(data, unicode))
        assert(isinstance(entry, models.SlackLogEntry))
        cls.PKG += 1
        #print "%s:%s" % (cls.ENTRY, cls.PKG)
        try:
            pkg, data = cls.parse_pkg_name(data)
        except ValueError:
            print "data: '%s...'" % data[0:50]
            raise
        description = cls.parse_pkg_description(data)
        return models.SlackLogPkg(pkg, description, entry)
    parse_pkg = classmethod(parse_pkg)

    def parse_pkg_name(cls, data):
        """
        Parse package name from a package.

        :param unicode data: Package name and description.
        :return: a two element list: package name and package description.
        :rtype: [:py:class:`unicode`, :py:class:`unicode`]
        """
        assert(isinstance(data, unicode))
        return data.split(u':', 1)
    parse_pkg_name = classmethod(parse_pkg_name)

    def parse_pkg_description(cls, data):
        """
        Parse package description from a package.

        :param unicode data: Package description.
        :return: Package description.
        :rtype: :py:class:`unicode`
        """
        assert(isinstance(data, unicode))
        return data
    parse_pkg_description = classmethod(parse_pkg_description)

    def get_line(cls, data):
        """
        Consume one line from data.

        :param unicode data: Data.
        :return: a two element list: first line, rest of the data.
        :rtype: [:py:class:`unicode`, :py:class:`unicode`]
        """
        assert(isinstance(data, unicode))
        try:
            line, data = data.split(u'\n', 1)
            #print line
            line += u'\n'
        except ValueError: # No newlines
            line = data
            data = u''
        return [line, data]
    get_line = classmethod(get_line)

    def parse_date(cls, data):
        """
        Parse a time string into a timestamp.

        :param unicode data: Time string.
        :return: Timestamp in UTC timezone.
        :rtype: :py:class:`datetime.datetime`
        """
        if data is None:
            return None
        assert(isinstance(data, unicode))
        timestamp = parser.parse(data, tzinfos=tzinfos)
        if timestamp.tzinfo is None:
            # Timestamp was ambiguous, assume UTC
            if not cls.quiet:
                print >>stderr, "Warning: Assuming UTC, input was '%s'" % data
            timestamp = timestamp.replace(tzinfo=tz.tzutc())
        elif not isinstance(timestamp.tzinfo, tz.tzutc):
            # Timestamp was in some local timezone,
            # convert to UTC
            tzname = timestamp.tzinfo.tzname(timestamp)
            if not cls.quiet and tzname not in tzinfos:
                print >>stderr, "Warning: Converting '%s' to UTC" % tzname
            timestamp = timestamp.astimezone(tz.tzutc())
        return timestamp
    parse_date = classmethod(parse_date)

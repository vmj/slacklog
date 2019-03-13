"""
SlackLog parsers
================

SlackLog parser takes a unicode representation of a Slackware ChangeLog.txt and produces an in-memory representation
of it.

The in-memory representation is an instance of :any:`SlackLog`.
"""
from __future__ import print_function

import re
import hashlib
from dateutil import parser
from dateutil import tz
from slacklog.models import SlackLog, SlackLogEntry, SlackLogPkg
from codecs import encode

try:
    str = unicode
except NameError:
    pass  # Forward compatibility with Py3k (unicode is not defined)

# pkg name starts from the beginning of line, and there's a colon followed by
# a double space.  But description can also contain "something:  ",
# so "something" should contain either a slash or a dot for it to look like
# a file name.
pkg_name_re = re.compile(r'\A[-a-zA-Z0-9_]+[/.][-a-zA-Z0-9_+/.]*[*]?:  ')

# A regex for checking if the timestamp had 12-hour or 24-hour format
am_pm_re = re.compile(r' [AaPp][Mm]? ')

tzinfos = {
    'CDT': -5 * 60 * 60,
    'CST': -6 * 60 * 60,
    'UTC': 0,
    }


class SlackLogParser (object):
    """
    Parser for Slackware ChangeLog.txt files.  This implementation works for 12.x and newer Slackware versions.
    """

    def __init__(self):
        self.quiet = False
        """If :py:const:`True`, warnings about date parsing are not printed."""
        self.min_date = None
        """If set to a :py:class:`datetime.datetime` object, older log entries are ignored (not parsed)."""
        self.ENTRY = 0
        """Counter of entries (for debugging)."""
        self.PKG = 0
        """Counter of packages (for debugging)."""

    def parse(self, data):
        """
        Return the in-memory representation of the data.

        :param data: :py:class:`unicode` -- the ChangeLog.txt content.
        :returns: :any:`SlackLog` -- in-memory representation of data
        """
        assert(isinstance(data, str))
        log = SlackLog()
        log.startsWithSeparator = re.match('\A(\+-+\+[\n]?)', data)
        log.endsWithSeparator = re.search('[\n](\+-+\+[\n]?)\Z', data)
        if log.startsWithSeparator:
            data = data[log.startsWithSeparator.start():]
            log.startsWithSeparator = True
        else:
            log.startsWithSeparator = False
        if log.endsWithSeparator:
            data = data[:log.endsWithSeparator.start(1)]
            log.endsWithSeparator = True
        else:
            log.endsWithSeparator = False

        for entry_data in self.split_log_to_entries(data):
            entry = self.parse_entry(entry_data, log)
            if entry:
                log.entries.insert(0, entry)
        return log

    def split_log_to_entries(self, data):
        """
        Split the ChangeLog.txt into a list of unparsed entries.

        :param data: :py:class:`unicode` --the ChangeLog.txt content.
        :returns: [:py:class:`unicode`] -- list of unparsed entries, separators removed.
        """
        assert(isinstance(data, str))
        raw_entries = re.split('\+-+\+', data)
        entries = []
        for entry in raw_entries:
            entry = entry.lstrip()
            if entry and entry != "":
                entries.append(entry)
        entries.reverse()
        return entries

    def parse_entry(self, data, log):
        """
        Parse a single ChangeLog entry.

        :param data: :py:class:`unicode` -- ChangeLog entry content.
        :param log: :any:`SlackLog` -- in-memory representation that is being parsed.
        :return: :any:`SlackLogEntry` -- in-memory representation of the ChangeLog entry.
        """
        assert(isinstance(data, str))
        assert(isinstance(log, SlackLog))
        self.ENTRY += 1
        self.PKG = 0
        checksum = self.gen_entry_checksum(data)
        parent = None
        if log.entries:
            parent = log.entries[0].identifier
            identifier = self.gen_entry_identifier(data, checksum, parent)
        else:
            identifier = self.gen_entry_identifier(data, checksum, None)
        timestamp, timezone, twelve_hour, data = self.parse_entry_timestamp(data)
        if self.min_date and self.min_date > timestamp:
            return None
        description, data = self.parse_entry_description(data)
        entry = SlackLogEntry(timestamp, description, log, checksum=checksum, identifier=identifier, parent=parent,
                                     timezone=timezone, twelveHourFormat=twelve_hour)
        for pkg_data in self.split_entry_to_pkgs(data):
            pkg = self.parse_pkg(pkg_data, entry)
            entry.pkgs.append(pkg)
        return entry

    def gen_entry_checksum(self, data):
        """
        Generate ChangeLog entry checksum from data.

        :param data: :py:class:`unicode` -- ChangeLog entry content.
        :return: :py:class:`unicode` -- Entry checksum.
        """
        assert(isinstance(data, str))
        return u'%s' % hashlib.sha512(encode(data, 'utf-8')).hexdigest()

    def gen_entry_identifier(self, data, checksum, parent):
        """
        Generate ChangeLog entry identifier from data, checksum, and/or parent identifier.

        :param data: :py:class:`unicode` -- ChangeLog entry content.
        :param checksum: :py:class:`unicode` -- ChangeLog entry checksum.
        :param parent: :py:class:`unicode` -- Parent entry identifier or :py:const:`None`
        :return: :py:class:`unicode` -- Entry identifier.
        """
        if parent is not None:
            return u'%s' % hashlib.sha512(encode(parent + checksum, 'utf-8')).hexdigest()
        return u'%s' % hashlib.sha512(encode(checksum, 'utf-8')).hexdigest()

    def parse_entry_timestamp(self, data):
        """
        Parse ChangeLog entry timestamp from data.

        :param data: :py:class:`unicode` -- ChangeLog entry content.
        :returns: [:py:class:`datetime.datetime`, :py:class:`tzinfo`, :py:class:`bool`, :py:class:`unicode`] --
            a four element list: timestamp in UTC, original timezone, :py:const:`True` if the timestamp had a 12-hour
            clock, and the rest of the entry.
        """
        assert(isinstance(data, str))
        timestamp_str, data = self.get_line(data)
        timestamp, timezone = self.parse_date_with_timezone(timestamp_str)
        if am_pm_re.search(timestamp_str):
            return [timestamp, timezone, True, data]
        return [timestamp, timezone, False, data]

    def parse_entry_description(self, data):
        """
        Parse ChangeLog entry description from data.

        :param data: :py:class:`unicode` -- ChangeLog entry content (without timestamp).
        :returns: [:py:class:`unicode`, :py:class:`unicode`] -- a two element list: description and the rest of the entry.
        """
        assert(isinstance(data, str))
        description = u''
        while data and not pkg_name_re.match(data):
            line, data = self.get_line(data)
            description += line
        return [description, data]

    def split_entry_to_pkgs(self, data):
        """
        Split ChangeLog entry content into a list of unparsed packages.

        :param data: :py:class:`unicode` -- ChangeLog entry content (without timestamp or description).
        :return: [:py:class:`unicode`] -- a list of unparsed packages.
        """
        assert(isinstance(data, str))
        pkgs = []
        pkg_lines = []
        if data == u'' or data == u'\n':
            return []
        for line in data.split('\n'):
            if not pkg_name_re.match(line):
                pkg_lines.append(line)
            else:
                if pkg_lines:
                    # pkg_lines is not the last package in
                    # the entry: add an extra newline
                    pkgs.append('\n'.join(pkg_lines) + '\n')
                    pkg_lines = []
                if line:
                    pkg_lines.append(line)
        if pkg_lines:
            # last package in the entry: no extra newline
            pkgs.append('\n'.join(pkg_lines))
        return pkgs

    def parse_pkg(self, data, entry):
        """
        Parse a single package.

        :param data: :py:class:`unicode` -- Package name and description of the update.
        :param entry: :any:`SlackLogEntry` -- in-memory representation of the ChangeLog entry being parsed.
        :return: :any:`SlackLogPkg` -- in-memory representation of the package.
        """
        assert(isinstance(data, str))
        assert(isinstance(entry, SlackLogEntry))
        self.PKG += 1
        try:
            pkg, data = self.parse_pkg_name(data)
        except ValueError:
            print("data: '%s...'" % data[0:50])
            raise
        description = self.parse_pkg_description(data)
        return SlackLogPkg(pkg, description, entry)

    def parse_pkg_name(self, data):
        """
        Parse package name from a package.

        :param data: :py:class:`unicode` -- Package name and description.
        :return: [:py:class:`unicode`, :py:class:`unicode`] -- a two element list: package name and package description.
        """
        assert(isinstance(data, str))
        return data.split(u':', 1)

    def parse_pkg_description(self, data):
        """
        Parse package description from a package.

        :param data: :py:class:`unicode` -- Package description.
        :return: :py:class:`unicode` -- Package description.
        """
        assert(isinstance(data, str))
        return data

    def get_line(self, data):
        """
        Consume one line from data.

        :param data: :py:class:`unicode` -- Data.
        :return: [:py:class:`unicode`, :py:class:`unicode`] -- a two element list: first line, rest of the data.
        """
        assert(isinstance(data, str))
        try:
            line, data = data.split(u'\n', 1)
            line += u'\n'
        except ValueError:  # No newlines
            line = data
            data = u''
        return [line, data]

    def parse_date(self, data):
        """
        Parse a time string into a timestamp.

        :param data: :py:class:`unicode` -- Time string.
        :return: :py:class:`datetime.datetime` -- Timestamp in UTC timezone.
        """
        if data is None:
            return None
        timestamp, timezone = self.parse_date_with_timezone(data)
        return timestamp

    def parse_date_with_timezone(self, data):
        """
        Parse a time string into a timestamp.

        :param data: :py:class:`unicode` -- Time string.
        :return: [:py:class:`datetime.datetime`, :py:class:`tzinfo`] -- a two element list: Timestamp in UTC timezone, and the original timezone.
        """
        if data is None:
            return None
        assert(isinstance(data, str))
        timestamp = parser.parse(data, tzinfos=tzinfos)
        timezone = timestamp.tzinfo
        if timezone is None:
            # Timestamp was ambiguous, assume UTC
            if not self.quiet:
                from sys import stderr
                stderr.write("Warning: Assuming UTC, input was '%s'" % data)
            timestamp = timestamp.replace(tzinfo=tz.tzutc())
        elif timestamp.tzinfo.utcoffset(timestamp).total_seconds() != 0:
            # Timestamp was in some local timezone,
            # convert to UTC
            tzname = timezone.tzname(timestamp)
            if not self.quiet and tzname not in tzinfos:
                from sys import stderr
                stderr.write("Warning: Converting '%s' to UTC" % tzname)
            timestamp = timestamp.astimezone(tz.tzutc())
        return [timestamp, timezone]

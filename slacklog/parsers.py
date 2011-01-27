from sys import stderr
import re
from datetime import datetime
from dateutil import parser
from dateutil import tz
from slacklog import models


pkg_name_re = re.compile(r'\A[a-z/]+[-a-zA-Z0-9_.]+:  ')

class SlackLogParser (object):

    quiet = False

    ENTRY = 0
    PKG = 0

    def parse(cls, data):
        assert(isinstance(data, unicode))
        log = models.SlackLog()
        for entry_data in cls.split_log_to_entries(data):
            entry = cls.parse_entry(entry_data, log)
            log.entries.append(entry)
        return log
    parse = classmethod(parse)

    def split_log_to_entries(cls, data):
        assert(isinstance(data, unicode))
        return re.split('\n*\+-+\+\n*', data)
    split_log_to_entries = classmethod(split_log_to_entries)

    def parse_entry(cls, data, log):
        assert(isinstance(data, unicode))
        assert(isinstance(log, models.SlackLog))
        cls.ENTRY += 1
        cls.PKG = 0
        #print "%s:%s" % (cls.ENTRY, cls.PKG)
        timestamp, data = cls.parse_entry_timestamp(data)
        description, data = cls.parse_entry_description(data)
        entry = models.SlackLogEntry(timestamp, description, log)
        for pkg_data in cls.split_entry_to_pkgs(data):
            pkg = cls.parse_pkg(pkg_data, entry)
            entry.pkgs.append(pkg)
        return entry
    parse_entry = classmethod(parse_entry)

    def parse_entry_timestamp(cls, data):
        assert(isinstance(data, unicode))
        timestamp_str, data = cls.get_line(data)
        timestamp = parser.parse(timestamp_str)
        if timestamp.tzinfo is None:
            # Timestamp was ambiguous, assume UTC
            if not cls.quiet:
                print >>stderr, "Warning: Assuming UTC, input was '%s'" % timestamp_str
            timestamp = timestamp.replace(tzinfo=tz.tzutc())
        elif not isinstance(timestamp.tzinfo, tz.tzutc):
            # Timestamp was in some local timezone,
            # convert to UTC
            if not cls.quiet:
                print >>stderr, "Warning: Converting to UTC"
            timestamp = timestamp.astimezone(tz.tzutc())
        return [timestamp, data]
    parse_entry_timestamp = classmethod(parse_entry_timestamp)

    def parse_entry_description(cls, data):
        assert(isinstance(data, unicode))
        description = u''
        while data and not pkg_name_re.match(data):
            line, data = cls.get_line(data)
            description += line
        return [description, data]
    parse_entry_description = classmethod(parse_entry_description)

    def split_entry_to_pkgs(cls, data):
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
        assert(isinstance(data, unicode))
        return data.split(u':', 1)
    parse_pkg_name = classmethod(parse_pkg_name)

    def parse_pkg_description(cls, data):
        assert(isinstance(data, unicode))
        return data
    parse_pkg_description = classmethod(parse_pkg_description)

    def get_line(cls, data):
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

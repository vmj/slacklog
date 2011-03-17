"""
SlackLog models
===============

SlackLog models represent the ChangeLog.txt after parsing.
"""
from datetime import datetime
from dateutil import tz

class SlackLog (object):
    """
    Little more than a list of SlackLogEntry objects.
    """

    def __init__(self):
        self.entries = []


class SlackLogEntry (object):
    """
    An entry in a SlackLog.

    Consist of a timestamp in UTC, and a unicode description which may be empty.

    Also contains a list of SlackLogPkg objects.
    """

    def __init__(self, timestamp, description, log):
        assert(isinstance(timestamp, datetime))
        assert(isinstance(description, unicode))
        assert(isinstance(timestamp.tzinfo, tz.tzutc))
        assert(isinstance(log, SlackLog))
        self.timestamp = timestamp
        self.description = description
        self.log = log
        self.pkgs = []


class SlackLogPkg (object):
    """
    An entry in a SlackLogEntry.

    Consists of a unicode package identifier and a unicode description.
    """

    def __init__(self, pkg, description, entry):
        assert(isinstance(pkg, unicode))
        assert(isinstance(description, unicode))
        assert(isinstance(entry, SlackLogEntry))
        self.pkg = pkg
        self.description = description
        self.entry = entry


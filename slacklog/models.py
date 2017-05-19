"""
SlackLog models
===============

SlackLog models represent the ChangeLog.txt after parsing.
"""
from datetime import datetime
from dateutil import tz

try:
    str = unicode
except NameError:
    pass  # Forward compatibility with Py3k (unicode is not defined)


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
    
    Since 0.9.1 a checksum was added, which is either None or a unicode string.
    If using the default parser, the value is a SHA-512 as a HEX string (and never None),
    and identifies the entry by content.  Note that two entries in different changelogs
    may have the same checksum, but different parents.
    
    Since 0.9.1 an identifier was added, which is either None or a unicode string.
    If using the default parser, the value is a SHA-512 as a HEX string (and never None),
    and identifies the entry by content and parent.
    
    Since 0.9.1 a parent was added, which is either None or a unicode string.
    If using the default parser, the value is the identifier of the next (older) log entry.
    """

    def __init__(self, timestamp, description, log, checksum=None, identifier=None, parent=None):
        assert(isinstance(timestamp, datetime))
        assert(isinstance(description, str))
        assert(isinstance(timestamp.tzinfo, tz.tzutc))
        assert(isinstance(log, SlackLog))
        if checksum is not None:
            assert(isinstance(checksum, str))
        if identifier is not None:
            assert(isinstance(identifier, str))
        if parent is not None:
            assert(isinstance(parent, str))
        self.timestamp = timestamp
        self.description = description
        self.log = log
        self.checksum = checksum
        self.identifier = identifier
        self.parent = parent
        self.pkgs = []


class SlackLogPkg (object):
    """
    An entry in a SlackLogEntry.

    Consists of a unicode package identifier and a unicode description.
    """

    def __init__(self, pkg, description, entry):
        assert(isinstance(pkg, str))
        assert(isinstance(description, str))
        assert(isinstance(entry, SlackLogEntry))
        self.pkg = pkg
        self.description = description
        self.entry = entry

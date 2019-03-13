"""
SlackLog models
===============

SlackLog models represent the ChangeLog.txt after parsing.
"""
from datetime import datetime, tzinfo

try:
    str = unicode
except NameError:
    pass  # Forward compatibility with Py3k (unicode is not defined)


class SlackLog (object):
    """
    Little more than a list of :any:`SlackLogEntry` objects.
    """

    def __init__(self):
        self.entries = []
        """The list of :any:`SlackLogEntry` objects. Empty by default."""
        self.startsWithSeparator = False
        """Whether the log started with entry separator.
        
        If this is :py:const:`True`, it implies that the empty element preceding that separator
        was dropped.
        
        This defaults to :py:const:`False`.
        """
        self.endsWithSeparator = False
        """Whether the log ended with entry separator.
        
        If this is :py:const:`True`, it implies that the empty element following that separator
        was dropped.
        
        This defaults to :py:const:`False`.
        """


class SlackLogEntry (object):
    """
    An entry in a :any:`SlackLog`.
    """

    def __init__(self, timestamp, description, log, checksum=None, identifier=None, parent=None,
                 timezone=None, twelveHourFormat=None):
        assert(isinstance(timestamp, datetime))
        assert(isinstance(description, str))
        assert(timestamp.tzinfo.utcoffset(timestamp).total_seconds() == 0)
        assert(isinstance(log, SlackLog))
        if checksum is not None:
            assert(isinstance(checksum, str))
        if identifier is not None:
            assert(isinstance(identifier, str))
        if parent is not None:
            assert(isinstance(parent, str))
        if timezone is not None:
            assert(isinstance(timezone, tzinfo))
        self.timestamp = timestamp
        """A :py:class:`datetime.datetime` timestamp in UTC."""
        self.description = description
        """A unicode description which may be empty."""
        self.log = log
        """Reference to the :any:`SlackLog` that contains this entry."""
        self.checksum = checksum
        """A unicode checksum or :py:const:`None`.
        
        This should identify the entry by content.  Two different logs may have the same entry,
        but those entries have different parent.
        """
        self.identifier = identifier
        """A unicode identifier or :py:const:`None`.
        
        This should identify the entry by content and parent.
        """
        self.parent = parent
        """A unicode parent identifier or :py:const:`None`."""
        self.timezone = timezone
        """The original timezone of the entry as :py:class:`datetime.tzinfo` or :py:const:`None`."""
        self.twelveHourFormat = twelveHourFormat
        """If this is :py:const:`True`, the original timestamp was in twelve hour format."""
        self.pkgs = []
        """The list of :any:`SlackLogPkg` objects. Empty by default."""


class SlackLogPkg (object):
    """
    An entry in a :any:`SlackLogEntry`.
    """

    def __init__(self, pkg, description, entry):
        assert(isinstance(pkg, str))
        assert(isinstance(description, str))
        assert(isinstance(entry, SlackLogEntry))
        self.pkg = pkg
        """A unicode package identifier."""
        self.description = description
        """A unicode description."""
        self.entry = entry
        """Reference to the :any:`SlackLogEntry` that contains this package."""

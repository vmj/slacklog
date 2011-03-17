# -*- coding: utf-8 -*-
"""
SlackLog formatters
===================

SlackLog formatter takes an in-memory representation of a Slackware ChangeLog.txt and produces a different representation of it.
"""
import codecs
import datetime
import os
import re
import time
from slacklog import models

class SlackLogFormatter (object):
    """
    Base class for SlackLog formatters.

    This class is ment for subclassing.
    """


    max_entries = None
    """If not :py:const:`None`, must be an :py:class:`int`
    representing how many entries are formatted from the beginning of
    the log.  Rest of the entries are ignored."""
    max_pkgs = None
    """If not :py:const:`None`, must be an :py:class:`int`
    representing how many packages are formatted from the beginning of
    each entry.  Rest of the packages are ignored."""


    def format(cls, log):
        """
        Return unicode representation of the in-memory representation of the log.

        Default implementation calls :py:meth:`format_log_preamble`,
        followed by a call to :py:meth:`format_entry` for each log
        entry, and finally calls :py:meth:`format_log_postamble`.

        The return value is the concatenation of the return values of
        the mentioned functions.

        :param log: in-memory representation of the log.
        :type: :py:class:`slacklog.models.SlackLog`
        :return: Unicode representation of the log.
        :type: :py:class:`unicode`
        """
        assert(isinstance(log, models.SlackLog))
        data = u''
        data += cls.format_log_preamble(log)
        data += cls.format_list(log.entries, cls.format_entry, cls.max_entries)
        data += cls.format_log_postamble(log)
        return data
    format = classmethod(format)

    def format_log_preamble(cls, log):
        """
        Return unicode representation of the log preamble, the part
        before entries.

        Default implementation returns empty string.

        :param log: in-memory representation of the log.
        :type: :py:class:`slacklog.models.SlackLog`
        :return: Unicode representation of log preamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(log, models.SlackLog))
        return u''
    format_log_preamble = classmethod(format_log_preamble)

    def format_log_postamble(cls, log):
        """
        Return unicode representation of the log postamble, the part
        after all entries.

        Default implementation returns empty string.

        :param log: in-memory representation of the log.
        :type: :py:class:`slacklog.models.SlackLog`
        :return: Unicode representation of log postamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(log, models.SlackLog))
        return u''
    format_log_postamble = classmethod(format_log_postamble)


    def format_entry(cls, entry, is_first, is_last):
        """
        Return unicode representation of a single log entry.

        Default implementation calls :py:meth:`format_entry_separator`
        with arguments `is_first` and `is_last`, followed by a call to
        :py:meth:`format_entry_preamble`, followed by a call to
        :py:meth:`format_pkg` for each package in this log entry,
        finally followed by a call to
        :py:meth:`format_entry_postamble`.

        The return value is the concatenation of the return values of
        the mentioned functions.

        :param entry: in-memory representation of the log entry.
        :type: :py:class:`slacklog.models.SlackLogEntry`
        :param bool is_first: :py:const:`True` if this is first entry, :py:const:`False` otherwise.
        :param bool is_last: :py:const:`True` if this is last entry, :py:const:`False` otherwise.
        :return: Unicode representation of log entry.
        :type: :py:class:`unicode`
        """
        assert(isinstance(entry, models.SlackLogEntry))
        data = u''
        data += cls.format_entry_separator(is_first, is_last)
        data += cls.format_entry_preamble(entry)
        data += cls.format_list(entry.pkgs, cls.format_pkg, cls.max_pkgs)
        data += cls.format_entry_postamble(entry)
        return data
    format_entry = classmethod(format_entry)

    def format_entry_separator(cls, is_first, is_last):
        """
        Return unicode representation of the log entry separator.

        Default implementation returns an empty string.

        :param bool is_first: :py:const:`True` if this is first entry, :py:const:`False` otherwise.
        :param bool is_last: :py:const:`True` if this is last entry, :py:const:`False` otherwise.
        :return: Unicode representation of log entry separator.
        :type: :py:class:`unicode`
        """
        return u''
    format_entry_separator = classmethod(format_entry_separator)

    def format_entry_preamble(cls, entry):
        """
        Return unicode representation of the log entry preamble, the
        part before packages.

        Default implementation returns an empty string.

        :param entry: in-memory representation of the log entry.
        :type: :py:class:`slacklog.models.SlackLogEntry`
        :return: Unicode representation of log entry preamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(entry, models.SlackLogEntry))
        return u''
    format_entry_preamble = classmethod(format_entry_preamble)

    def format_entry_postamble(cls, entry):
        """
        Return unicode representation of the log entry postamble, the
        part after packages.

        Default implementation returns an empty string.

        :param entry: in-memory representation of the log entry.
        :type: :py:class:`slacklog.models.SlackLogEntry`
        :return: Unicode representation of log entry postamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(entry, models.SlackLogEntry))
        return u''
    format_entry_postamble = classmethod(format_entry_postamble)


    def format_pkg(cls, pkg, is_first, is_last):
        """
        Return unicode representation of a single log entry package.

        Default implementation calls :py:meth:`format_pkg_separator`,
        followed by a call to :py:meth:`format_pkg_preamble`, and
        finally calls :py:meth:`format_pkg_postamble`.

        The return value is the concatenation of the return values of
        the mentioned functions.

        :param pkg: in-memory representation of the log entry package
        :type: :py:class:`slacklog.models.SlackLogPkg`
        :param bool is_first: :py:const:`True` if this is first package, :py:const:`False` otherwise.
        :param bool is_last: :py:const:`True` if this is last package, :py:const:`False` otherwise.
        :return: Unicode representation of log entry package.
        :type: :py:class:`unicode`
        """
        assert(isinstance(pkg, models.SlackLogPkg))
        data = u''
        data += cls.format_pkg_separator(is_first, is_last)
        data += cls.format_pkg_preamble(pkg)
        data += cls.format_pkg_postamble(pkg)
        return data
    format_pkg = classmethod(format_pkg)

    def format_pkg_separator(cls, is_first, is_last):
        """
        Return unicode representation of the log entry package
        separator.

        Default implementation returns an empty string.

        :param bool is_first: :py:const:`True` if this is first package, :py:const:`False` otherwise.
        :param bool is_last: :py:const:`True` if this is last package, :py:const:`False` otherwise.
        :return: Unicode representation of log entry package separator.
        :type: :py:class:`unicode`
        """
        return u''
    format_pkg_separator = classmethod(format_pkg_separator)

    def format_pkg_preamble(cls, pkg):
        """
        Return unicode representation of the log entry package
        preamble.

        Default implementation returns an empty string.

        :param pkg: in-memory representation of the log entry package
        :type: :py:class:`slacklog.models.SlackLogPkg`
        :return: Unicode representation of log entry package preamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(pkg, models.SlackLogPkg))
        return u''
    format_pkg_preamble = classmethod(format_pkg_preamble)

    def format_pkg_postamble(cls, pkg):
        """
        Return unicode representation of the log entry package
        postamble.

        Default implementation returns an empty string.

        :param pkg: in-memory representation of the log entry package
        :type: :py:class:`slacklog.models.SlackLogPkg`
        :return: Unicode representation of log entry package postamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(pkg, models.SlackLogPkg))
        return u''
    format_pkg_postamble = classmethod(format_pkg_postamble)

    def format_list(cls, list_of_items, item_formatter, max_items=None):
        """
        Return unicode representation of a list of objects.

        This method is not ment for subclassing.

        :param list_of_items: List of items to format.
        :type: list
        :param item_formatter: Function that formats one item.
        :type: A callable that takes one item as the first positional
               argument, two booleans `is_first` and `is_last` as
               second and third positional arguments, and returns a
               :py:class:`unicode` string.
        :return: Formatted data.
        :rtype: :py:class:`unicode`
        """
        data = u''
        num_items = len(list_of_items)
        if max_items:
            assert(isinstance(max_items, int))
            if num_items > max_items:
                num_items = max_items
        for index in xrange(num_items):
            is_first = False
            is_last = False
            if index == 0:
                is_first = True
            if index == num_items - 1:
                is_last = True
            data += item_formatter(list_of_items[index], is_first, is_last)
        return data
    format_list = classmethod(format_list)


class SlackLogTxtFormatter (SlackLogFormatter):
    """
    Concrete SlackLog formatter that tries to regenerate the original
    ChangeLog.txt.
    """

    def format_entry_separator(cls, is_first, is_last):
        """
        Overrides :py:meth:`SlackLogFormatter.format_entry_separator`.

        :param bool is_first: :py:const:`True` if this is first entry, :py:const:`False` otherwise.
        :param bool is_last: :py:const:`True` if this is last entry, :py:const:`False` otherwise.
        :return: Unicode representation of log entry separator.
        :type: :py:class:`unicode`
        """
        if not is_first:
            return u'+--------------------------+\n'
        return u''
    format_entry_separator = classmethod(format_entry_separator)

    def format_entry_preamble(cls, entry):
        """
        Overrides :py:meth:`SlackLogFormatter.format_entry_preamble`.

        :param entry: in-memory representation of the log entry.
        :type: :py:class:`slacklog.models.SlackLogEntry`
        :return: Unicode representation of log entry preamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(entry, models.SlackLogEntry))
        data = u''
        data += entry.timestamp.strftime("%a %b %d %H:%M:%S %Z %Y")
        # Remove leading zero from the day-of-month only
        data = re.sub(r' 0(\d) ', r'  \1 ', data)
        data += u'\n'
        if entry.description:
            data += entry.description
        return data
    format_entry_preamble = classmethod(format_entry_preamble)

    def format_pkg_preamble(cls, pkg):
        """
        Overrides :py:meth:`SlackLogFormatter.format_pkg_preamble`.

        :param pkg: in-memory representation of the log entry package
        :type: :py:class:`slacklog.models.SlackLogPkg`
        :return: Unicode representation of log entry package preamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(pkg, models.SlackLogPkg))
        return u'%s:%s' % (pkg.pkg, pkg.description)
    format_pkg_preamble = classmethod(format_pkg_preamble)

class SlackLogRssFormatter (SlackLogFormatter):
    """
    Concrete SlackLog formatter that generates an RSS feed.
    """

    slackware = None
    """:py:class:`unicode` description of the distro version.
    E.g. 'Slackware 13.37' or 'Slackware64 current'."""
    rssLink = None
    """:py:class:`unicode`.  Full URL of the RSS feed."""
    webLink = None
    """:py:class:`unicode`.  Full URL of the WWW version of the
    feed."""
    description = None
    """:py:class:`unicode` description of the feed."""
    language = None
    """:py:class:`unicode` language identifier.  E.g. 'en'."""
    managingEditor = None
    """:py:class:`unicode`.  Email, and possibly name, of the feed
    manager.  E.g. 'jane@doe.net (Jane Doe)'."""
    webMaster = None
    """:py:class:`unicode`.  Email, and possibly name, of the
    webmaster.  E.g. 'john@doe.net (John Doe)'. """

    def format_log_preamble(cls, log):
        """
        Overrides :py:meth:`SlackLogFormatter.format_log_preamble`.

        :param log: in-memory representation of the log.
        :type: :py:class:`slacklog.models.SlackLog`
        :return: Unicode representation of log preamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(log, models.SlackLog))
        data  = u'<?xml version="1.0"?>\n'
        data += u'<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        data += u'  <channel>\n'
        data += u'    <atom:link href="%s" rel="self" type="application/rss+xml" />\n' % cls.rssLink
        data += u'    <title>%s ChangeLog</title>\n' % cls.slackware
        if cls.webLink:
            data += u'    <link>%s</link>\n' % cls.webLink
        else:
            data += u'    <link>%s</link>\n' % cls.rssLink
        if cls.description:
            data += u'    <description>%s</description>\n' % cls.description
        data += u'    <docs>http://www.rssboard.org/rss-specification</docs>\n'
        data += u'    <language>%s</language>\n' % cls.language
        if cls.managingEditor:
            data += u'    <managingEditor>%s</managingEditor>\n' % cls.managingEditor
        if cls.webMaster:
            data += u'    <webMaster>%s</webMaster>\n' % cls.webMaster
        data += u'    <pubDate>%s</pubDate>\n' % log.entries[0].timestamp.strftime("%a, %d %b %Y %H:%M:%S GMT")
        data += u'    <lastBuildDate>%s</lastBuildDate>\n' % datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        data += u'    <generator>SlackLog</generator>\n'
        return data
    format_log_preamble = classmethod(format_log_preamble)

    def format_log_postamble(cls, log):
        """
        Overrides :py:meth:`SlackLogFormatter.format_log_postamble`.

        :param log: in-memory representation of the log.
        :type: :py:class:`slacklog.models.SlackLog`
        :return: Unicode representation of log postamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(log, models.SlackLog))
        return u'  </channel>\n</rss>\n'
    format_log_postamble = classmethod(format_log_postamble)


    def format_entry_preamble(cls, entry):
        """
        Overrides :py:meth:`SlackLogFormatter.format_entry_preamble`.

        :param entry: in-memory representation of the log entry.
        :type: :py:class:`slacklog.models.SlackLogEntry`
        :return: Unicode representation of log entry preamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(entry, models.SlackLogEntry))
        data  = u'    <item>\n'
        if cls.webLink:
            data += u'      <guid isPermaLink="true">%s#%s</guid>\n' % (cls.webLink, entry.timestamp.strftime("%Y%m%dT%H%M%SZ"))
        else:
            data += u'      <guid isPermaLink="false">%s-%s</guid>\n' % (cls.slackware.replace(' ', '-'), entry.timestamp.strftime("%Y%m%dT%H%M%SZ"))
        data += u'      <title>%s changes for %s</title>\n' % (cls.slackware, entry.timestamp.strftime("%a, %d %b %Y %H:%M:%S GMT"))
        data += u'      <pubDate>%s</pubDate>\n' % entry.timestamp.strftime("%a, %d %b %Y %H:%M:%S GMT")
        data += u'      <description><![CDATA[<pre>'
        if entry.description:
            data += entry.description.replace('<','&lt;')
        return data
    format_entry_preamble = classmethod(format_entry_preamble)

    def format_entry_postamble(cls, entry):
        """
        Overrides :py:meth:`SlackLogFormatter.format_entry_postamble`.

        :param entry: in-memory representation of the log entry.
        :type: :py:class:`slacklog.models.SlackLogEntry`
        :return: Unicode representation of log entry postamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(entry, models.SlackLogEntry))
        return u'</pre>]]></description>\n    </item>\n'
    format_entry_postamble = classmethod(format_entry_postamble)


    def format_pkg_preamble(cls, pkg):
        """
        Overrides :py:meth:`SlackLogFormatter.format_pkg_preamble`.

        :param pkg: in-memory representation of the log entry package
        :type: :py:class:`slacklog.models.SlackLogPkg`
        :return: Unicode representation of log entry package preamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(pkg, models.SlackLogPkg))
        return u'%s:%s' % (pkg.pkg, pkg.description.replace('<','&lt;'))
    format_pkg_preamble = classmethod(format_pkg_preamble)


class SlackLogPyblosxomFormatter (SlackLogFormatter):
    """
    Concrete SlackLog formatter that generates Pyblosxom blog entries.
    """

    quiet = False
    """If :py:const:`True`, """
    slackware = None
    """:py:class:`unicode` description of the distro version.
    E.g. 'Slackware 13.37' or 'Slackware64 current'."""
    datadir = None
    """Blog entry directory."""
    extension = 'txt'
    """Blog entry filename extension."""
    encoding = 'utf-8'
    """Blog entry file encoding."""
    tags_separator = ','
    """Separator for tags."""
    pkg_separator = ':'
    """Separator for packages."""
    pyfilemtime = False
    """If :py:const:`True`, a pyfilemtime compatible filenames are generated."""
    overwrite = False
    """If :py:const:`True`, already existing blog entries are overwritten."""
    backup = True
    """If :py:const:`True`, already existing blog entries are copied to backups before overwriting."""

    # Subclass can change these
    entry_preamble       = u'<div class="slackLogEntry">\n'
    """:py:class:`unicode`.  HTML to insert before the entry."""
    entry_postamble      = u'</div>\n'
    """:py:class:`unicode`.  HTML to insert after the entry."""
    entry_desc_preamble  = u'<div class="slackLogEntryDesc">'
    """:py:class:`unicode`.  HTML to insert before the entry description."""
    entry_desc_postamble = u'</div>\n'
    """:py:class:`unicode`.  HTML to insert after the entry description."""
    entry_pkgs_preamble  = u'<div class="slackLogEntryPkgs">\n'
    """:py:class:`unicode`.  HTML to insert before the list of packages."""
    entry_pkgs_postamble = U'</div>\n'
    """:py:class:`unicode`.  HTML to insert after the list of packages."""
    pkg_preamble         = u'<div class="slackLogPkg">'
    """:py:class:`unicode`.  HTML to insert before a package."""
    pkg_postamble        = u'</div>\n'
    """:py:class:`unicode`.  HTML to insert after a package."""
    pkg_name_preamble    = u'<span class="slackLogPkgName">'
    """:py:class:`unicode`.  HTML to insert before package name."""
    pkg_name_postamble   = u'</span>'
    """:py:class:`unicode`.  HTML to insert after package name."""
    pkg_desc_preamble    = u'<span class="slackLogPkgDesc">'
    """:py:class:`unicode`.  HTML to insert before package description."""
    pkg_desc_postamble   = u'</span>'
    """:py:class:`unicode`.  HTML to insert after package description."""


    def format_entry(cls, entry, is_first, is_last):
        """
        Overrides :py:meth:`SlackLogFormatter.format_entry`.

        :param entry: in-memory representation of the log entry.
        :type: :py:class:`slacklog.models.SlackLogEntry`
        :param bool is_first: :py:const:`True` if this is first entry, :py:const:`False` otherwise.
        :param bool is_last: :py:const:`True` if this is last entry, :py:const:`False` otherwise.
        :return: Unicode representation of log entry.
        :type: :py:class:`unicode`
        """
        assert(isinstance(entry, models.SlackLogEntry))
        data = super(SlackLogPyblosxomFormatter, cls).format_entry(entry, is_first, is_last)

        # generate filename for this entry
        filename = '%s%s%s' % (cls.datadir,
                               os.path.sep,
                               cls.format_entry_basename(entry))
        if cls.pyfilemtime:
            filename += entry.timestamp.strftime("-%Y-%m-%d-%H-%M")
        filename += '.%s' % cls.extension
        filename = os.path.expanduser(filename)

        # Ensure that the directory exists
        try:
            os.makedirs(os.path.dirname(filename))
        except:
            # Directory already exists
            pass

        # Handle the entries that already exist
        if os.path.exists(filename):
            if cls.overwrite:
                if cls.backup:
                    # Make a backup
                    i = 1
                    backup = "%s~%d~" % (filename, i)
                    while os.path.exists(backup):
                        backup = "%s~%d~" % (filename, i)
                        i += 1
                    if not cls.quiet:
                        print "Backing up entry: %s" % backup
                    os.rename(filename, backup)
                else:
                    print "Overwriting entry: %s" % filename
            else:
                if not cls.quiet:
                    print "Entry already exists: %s" % filename
                return data

        # Write the entry
        file = codecs.open(filename, 'w', cls.encoding)
        file.write(data)
        file.close()

        # Set the mtime (for those who do not want to use the
        # pyfilemtime plugin)
        timestamp = time.mktime(entry.timestamp.timetuple())
        os.utime(filename, (timestamp, timestamp))

        return data
    format_entry = classmethod(format_entry)


    def format_entry_preamble(cls, entry):
        """
        Overrides :py:meth:`SlackLogFormatter.format_entry_preamble`.

        :param entry: in-memory representation of the log entry.
        :type: :py:class:`slacklog.models.SlackLogEntry`
        :return: Unicode representation of log entry preamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(entry, models.SlackLogEntry))
        data = cls.format_entry_title(entry)
        if cls.tags_separator:
            data += u'#tags %s\n' % cls.format_entry_tags(entry)
        data += cls.entry_preamble
        if entry.description:
            data += u'%s%s%s' % (cls.entry_desc_preamble,
                                 entry.description,
                                 cls.entry_desc_postamble)
        if entry.pkgs:
            data += cls.entry_pkgs_preamble
        return data
    format_entry_preamble = classmethod(format_entry_preamble)

    def format_entry_postamble(cls, entry):
        """
        Overrides :py:meth:`SlackLogFormatter.format_entry_postamble`.

        :param entry: in-memory representation of the log entry.
        :type: :py:class:`slacklog.models.SlackLogEntry`
        :return: Unicode representation of log entry postamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(entry, models.SlackLogEntry))
        data = u''
        if entry.pkgs:
            data += cls.entry_pkgs_postamble
        data += cls.entry_postamble
        return data
    format_entry_postamble = classmethod(format_entry_postamble)


    def format_pkg_preamble(cls, pkg):
        """
        Overrides :py:meth:`SlackLogFormatter.format_pkg_preamble`.

        :param pkg: in-memory representation of the log entry package
        :type: :py:class:`slacklog.models.SlackLogPkg`
        :return: Unicode representation of log entry package preamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(pkg, models.SlackLogPkg))
        data = u'%s%s%s%s%s%s%s%s%s' % (cls.pkg_preamble,
                                        cls.pkg_name_preamble,
                                        pkg.pkg,
                                        cls.pkg_name_postamble,
                                        cls.pkg_separator,
                                        cls.pkg_desc_preamble,
                                        pkg.description,
                                        cls.pkg_desc_postamble,
                                        cls.pkg_postamble)
        return data
    format_pkg_preamble = classmethod(format_pkg_preamble)


    def format_entry_basename(cls, entry):
        """
        Return basename for the log entry.

        :param entry: in-memory representation of the log entry.
        :type: :py:class:`slacklog.models.SlackLogEntry`
        :return: Unicode representation of log entry name
        :type: :py:class:`unicode`
        """
        return cls.slackware.replace(' ','-').replace('.','_').lower()
    format_entry_basename = classmethod(format_entry_basename)

    def format_entry_title(cls, entry):
        """
        Return log entry title.

        :param entry: in-memory representation of the log entry.
        :type: :py:class:`slacklog.models.SlackLogEntry`
        :return: Unicode representation of log entry title
        :type: :py:class:`unicode`
        """
        return u'%s changes for %s\n' % (cls.slackware, entry.timestamp.strftime("%a, %d %b %Y %H:%M:%S GMT"))
    format_entry_title = classmethod(format_entry_title)

    def format_entry_tags(cls, entry):
        """
        Return log entry tags.

        :param entry: in-memory representation of the log entry.
        :type: :py:class:`slacklog.models.SlackLogEntry`
        :return: Unicode representation of log entry tags
        :type: :py:class:`unicode`
        """
        return u'%s' % cls.slackware.replace(' ',cls.tags_separator)
    format_entry_tags = classmethod(format_entry_tags)


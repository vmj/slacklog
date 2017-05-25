# -*- coding: utf-8 -*-
"""
SlackLog formatters
===================

SlackLog formatter takes an in-memory representation of a Slackware ChangeLog.txt and produces a different
representation of it.
"""
from __future__ import print_function

import codecs
import datetime
import os
import re
import time
from slacklog import models


def readable(d):
    return d.strftime("%a, %d %b %Y %H:%M:%S GMT")


def anchor(d):
    return d.strftime("%Y%m%dT%H%M%SZ")


class SlackLogFormatter (object):
    """
    Base class for SlackLog formatters.

    This class is ment for subclassing.
    """

    def __init__(self):
        self.max_entries = None
        """If not :py:const:`None`, must be an :py:class:`int`
        representing how many entries are formatted from the beginning of
        the log.  Rest of the entries are ignored."""
        self.max_pkgs = None
        """If not :py:const:`None`, must be an :py:class:`int`
        representing how many packages are formatted from the beginning of
        each entry.  Rest of the packages are ignored."""

    def format(self, log):
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
        data += self.format_log_preamble(log)
        data += self.format_list(log.entries, self.format_entry, self.max_entries)
        data += self.format_log_postamble(log)
        return data

    def format_log_preamble(self, log):
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

    def format_log_postamble(self, log):
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

    def format_entry(self, entry, is_first, is_last):
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
        data += self.format_entry_separator(is_first, is_last)
        data += self.format_entry_preamble(entry)
        data += self.format_list(entry.pkgs, self.format_pkg, self.max_pkgs)
        data += self.format_entry_postamble(entry)
        return data

    def format_entry_separator(self, is_first, is_last):
        """
        Return unicode representation of the log entry separator.

        Default implementation returns an empty string.

        :param bool is_first: :py:const:`True` if this is first entry, :py:const:`False` otherwise.
        :param bool is_last: :py:const:`True` if this is last entry, :py:const:`False` otherwise.
        :return: Unicode representation of log entry separator.
        :type: :py:class:`unicode`
        """
        return u''

    def format_entry_preamble(self, entry):
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

    def format_entry_postamble(self, entry):
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

    def format_pkg(self, pkg, is_first, is_last):
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
        data += self.format_pkg_separator(is_first, is_last)
        data += self.format_pkg_preamble(pkg)
        data += self.format_pkg_postamble(pkg)
        return data

    def format_pkg_separator(self, is_first, is_last):
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

    def format_pkg_preamble(self, pkg):
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

    def format_pkg_postamble(self, pkg):
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

    def format_list(self, list_of_items, item_formatter, max_items=None):
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
        :param max_items: Maximum number of items to format.  If falsy, all items are formatted.
        :type: :py:class:`int` or falsy.
        :return: Formatted data.
        :rtype: :py:class:`unicode`
        """
        data = u''
        num_items = len(list_of_items)
        if max_items:
            assert(isinstance(max_items, int))
            if num_items > max_items:
                num_items = max_items
        for index in range(num_items):
            is_first = False
            is_last = False
            if index == 0:
                is_first = True
            if index == num_items - 1:
                is_last = True
            data += item_formatter(list_of_items[index], is_first, is_last)
        return data


class SlackLogTxtFormatter (SlackLogFormatter):
    """
    Concrete SlackLog formatter that tries to regenerate the original
    ChangeLog.txt.
    """

    def format_entry_separator(self, is_first, is_last):
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

    def format_entry_preamble(self, entry):
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

    def format_pkg_preamble(self, pkg):
        """
        Overrides :py:meth:`SlackLogFormatter.format_pkg_preamble`.

        :param pkg: in-memory representation of the log entry package
        :type: :py:class:`slacklog.models.SlackLogPkg`
        :return: Unicode representation of log entry package preamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(pkg, models.SlackLogPkg))
        return u'%s:%s' % (pkg.pkg, pkg.description)


class SlackLogRssFormatter (SlackLogFormatter):
    """
    Concrete SlackLog formatter that generates an RSS feed.
    """

    def __init__(self):
        super(SlackLogRssFormatter, self).__init__()
        self.slackware = None
        """:py:class:`unicode` description of the distro version.
        E.g. 'Slackware 13.37' or 'Slackware64 current'."""
        self.rssLink = None
        """:py:class:`unicode`.  Full URL of the RSS feed."""
        self.webLink = None
        """:py:class:`unicode`.  Full URL of the WWW version of the
        feed."""
        self.description = None
        """:py:class:`unicode` description of the feed."""
        self.language = None
        """:py:class:`unicode` language identifier.  E.g. 'en'."""
        self.managingEditor = None
        """:py:class:`unicode`.  Email, and possibly name, of the feed
        manager.  E.g. 'jane@doe.net (Jane Doe)'."""
        self.webMaster = None
        """:py:class:`unicode`.  Email, and possibly name, of the
        webmaster.  E.g. 'john@doe.net (John Doe)'. """

    def format_log_preamble(self, log):
        """
        Overrides :py:meth:`SlackLogFormatter.format_log_preamble`.

        :param log: in-memory representation of the log.
        :type: :py:class:`slacklog.models.SlackLog`
        :return: Unicode representation of log preamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(log, models.SlackLog))
        data = u'<?xml version="1.0"?>\n'
        data += u'<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        data += u'  <channel>\n'
        data += u'    <atom:link href="%s" rel="self" type="application/rss+xml" />\n' % self.rssLink
        data += u'    <title>%s ChangeLog</title>\n' % self.slackware
        if self.webLink:
            data += u'    <link>%s</link>\n' % self.webLink
        else:
            data += u'    <link>%s</link>\n' % self.rssLink
        if self.description:
            data += u'    <description>%s</description>\n' % self.description
        data += u'    <docs>http://www.rssboard.org/rss-specification</docs>\n'
        data += u'    <language>%s</language>\n' % self.language
        if self.managingEditor:
            data += u'    <managingEditor>%s</managingEditor>\n' % self.managingEditor
        if self.webMaster:
            data += u'    <webMaster>%s</webMaster>\n' % self.webMaster
        data += u'    <pubDate>%s</pubDate>\n' % readable(log.entries[0].timestamp)
        data += u'    <lastBuildDate>%s</lastBuildDate>\n' % readable(datetime.datetime.utcnow())
        data += u'    <generator>SlackLog</generator>\n'
        return data

    def format_log_postamble(self, log):
        """
        Overrides :py:meth:`SlackLogFormatter.format_log_postamble`.

        :param log: in-memory representation of the log.
        :type: :py:class:`slacklog.models.SlackLog`
        :return: Unicode representation of log postamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(log, models.SlackLog))
        return u'  </channel>\n</rss>\n'

    def format_entry_preamble(self, entry):
        """
        Overrides :py:meth:`SlackLogFormatter.format_entry_preamble`.

        :param entry: in-memory representation of the log entry.
        :type: :py:class:`slacklog.models.SlackLogEntry`
        :return: Unicode representation of log entry preamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(entry, models.SlackLogEntry))
        data = u'    <item>\n'
        if self.webLink:
            perma = u'true'
            link = u'%s#%s' % (self.webLink, anchor(entry.timestamp))
        else:
            perma = u'false'
            link = u'%s-%s' % (self.slackware.replace(' ', '-'), anchor(entry.timestamp))
        data += u'      <guid isPermaLink="%s">%s</guid>\n' % (perma, link)
        data += u'      <title>%s changes for %s</title>\n' % (self.slackware, readable(entry.timestamp))
        data += u'      <pubDate>%s</pubDate>\n' % readable(entry.timestamp)
        data += u'      <description><![CDATA[<pre>'
        if entry.description:
            data += entry.description.replace('<', '&lt;')
        return data

    def format_entry_postamble(self, entry):
        """
        Overrides :py:meth:`SlackLogFormatter.format_entry_postamble`.

        :param entry: in-memory representation of the log entry.
        :type: :py:class:`slacklog.models.SlackLogEntry`
        :return: Unicode representation of log entry postamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(entry, models.SlackLogEntry))
        return u'</pre>]]></description>\n    </item>\n'

    def format_pkg_preamble(self, pkg):
        """
        Overrides :py:meth:`SlackLogFormatter.format_pkg_preamble`.

        :param pkg: in-memory representation of the log entry package
        :type: :py:class:`slacklog.models.SlackLogPkg`
        :return: Unicode representation of log entry package preamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(pkg, models.SlackLogPkg))
        return u'%s:%s' % (pkg.pkg, pkg.description.replace('<', '&lt;'))


class SlackLogAtomFormatter (SlackLogFormatter):
    """
    Concrete SlackLog formatter that generates an Atom feed.
    """

    def __init__(self):
        super(SlackLogAtomFormatter, self).__init__()
        self.slackware = None
        """:py:class:`unicode` description of the distro version.
        E.g. 'Slackware 13.37' or 'Slackware64 current'."""
        self.link = None
        """:py:class:`unicode`.  Full URL of the Atom feed."""
        self.webLink = None
        """:py:class:`unicode`.  Full URL of the HTML version."""
        self.name = None
        """:py:class:`unicode`.  Name of the feed author."""
        self.email = None
        """:py:class:`unicode`.  Email of the feed author."""

    def format_log_preamble(self, log):
        """
        Overrides :py:meth:`SlackLogFormatter.format_log_preamble`.

        :param log: in-memory representation of the log.
        :type: :py:class:`slacklog.models.SlackLog`
        :return: Unicode representation of log preamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(log, models.SlackLog))
        data = u'<?xml version="1.0"?>\n'
        data += u'<feed xmlns="http://www.w3.org/2005/Atom">\n'
        data += u'    <link href="%s" rel="self" type="application/rss+xml" />\n' % self.link
        data += u'    <title>%s ChangeLog</title>\n' % self.slackware
        if self.webLink:
            data += u'    <link href="%s" />\n' % self.webLink
        else:
            data += u'    <link href="%s" />\n' % self.link
        data += u'    <updated>%s</updated>\n' % datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        data += u'    <author>\n'
        data += u'        <name>%s</name>\n' % self.name
        data += u'        <email>%s</email>\n' % self.email
        data += u'    </author>\n'
        data += u'    <id>%s</id>\n' % self.link
        return data

    def format_log_postamble(self, log):
        """
        Overrides :py:meth:`SlackLogFormatter.format_log_postamble`.

        :param log: in-memory representation of the log.
        :type: :py:class:`slacklog.models.SlackLog`
        :return: Unicode representation of log postamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(log, models.SlackLog))
        return u'</feed>\n'

    def format_entry_preamble(self, entry):
        """
        Overrides :py:meth:`SlackLogFormatter.format_entry_preamble`.

        :param entry: in-memory representation of the log entry.
        :type: :py:class:`slacklog.models.SlackLogEntry`
        :return: Unicode representation of log entry preamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(entry, models.SlackLogEntry))
        data = u'    <entry>\n'
        data += u'        <title>%s changes for %s</title>\n' % (self.slackware, readable(entry.timestamp))
        if self.webLink:
            data += u'        <link href="%s#%s" />\n' % (self.webLink, anchor(entry.timestamp))
        else:
            data += u'        <link href="%s#%s" />\n' % (self.link, anchor(entry.timestamp))
        data += u'        <updated>%s</updated>\n' % entry.timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
        data += u'        <id>%s#%s</id>\n' % (self.link, anchor(entry.timestamp))
        data += u'        <content type="html"><![CDATA[<pre>'
        return data

    def format_entry_postamble(self, entry):
        """
        Overrides :py:meth:`SlackLogFormatter.format_entry_postamble`.

        :param entry: in-memory representation of the log entry.
        :type: :py:class:`slacklog.models.SlackLogEntry`
        :return: Unicode representation of log entry postamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(entry, models.SlackLogEntry))
        return u'</pre>]]></content>\n    </entry>\n'

    def format_pkg_preamble(self, pkg):
        """
        Overrides :py:meth:`SlackLogFormatter.format_pkg_preamble`.

        :param pkg: in-memory representation of the log entry package
        :type: :py:class:`slacklog.models.SlackLogPkg`
        :return: Unicode representation of log entry package preamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(pkg, models.SlackLogPkg))
        return u'%s:%s' % (pkg.pkg, pkg.description.replace('<', '&lt;'))


class SlackLogPyblosxomFormatter (SlackLogFormatter):
    """
    Concrete SlackLog formatter that generates Pyblosxom blog entries.
    """

    def __init__(self):
        super(SlackLogPyblosxomFormatter, self).__init__()
        self.quiet = False
        """If :py:const:`True`, """
        self.slackware = None
        """:py:class:`unicode` description of the distro version.
        E.g. 'Slackware 13.37' or 'Slackware64 current'."""
        self.datadir = None
        """Blog entry directory."""
        self.extension = 'txt'
        """Blog entry filename extension."""
        self.encoding = 'utf-8'
        """Blog entry file encoding."""
        self.tags_separator = ','
        """Separator for tags."""
        self.pkg_separator = ':'
        """Separator for packages."""
        self.pyfilemtime = False
        """If :py:const:`True`, a pyfilemtime compatible filenames are generated."""
        self.overwrite = False
        """If :py:const:`True`, already existing blog entries are overwritten."""
        self.backup = True
        """If :py:const:`True`, already existing blog entries are copied to backups before overwriting."""

        # Subclass can change these
        self.entry_preamble = u'<div class="slackLogEntry">\n'
        """:py:class:`unicode`.  HTML to insert before the entry."""
        self.entry_postamble = u'</div>\n'
        """:py:class:`unicode`.  HTML to insert after the entry."""
        self.entry_desc_preamble = u'<div class="slackLogEntryDesc">'
        """:py:class:`unicode`.  HTML to insert before the entry description."""
        self.entry_desc_postamble = u'</div>\n'
        """:py:class:`unicode`.  HTML to insert after the entry description."""
        self.entry_pkgs_preamble = u'<div class="slackLogEntryPkgs">\n'
        """:py:class:`unicode`.  HTML to insert before the list of packages."""
        self.entry_pkgs_postamble = U'</div>\n'
        """:py:class:`unicode`.  HTML to insert after the list of packages."""
        self.pkg_preamble = u'<div class="slackLogPkg">'
        """:py:class:`unicode`.  HTML to insert before a package."""
        self.pkg_postamble = u'</div>\n'
        """:py:class:`unicode`.  HTML to insert after a package."""
        self.pkg_name_preamble = u'<span class="slackLogPkgName">'
        """:py:class:`unicode`.  HTML to insert before package name."""
        self.pkg_name_postamble = u'</span>'
        """:py:class:`unicode`.  HTML to insert after package name."""
        self.pkg_desc_preamble = u'<span class="slackLogPkgDesc">'
        """:py:class:`unicode`.  HTML to insert before package description."""
        self.pkg_desc_postamble = u'</span>'
        """:py:class:`unicode`.  HTML to insert after package description."""

    def format_entry(self, entry, is_first, is_last):
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
        data = super(SlackLogPyblosxomFormatter, self).format_entry(entry, is_first, is_last)

        # generate filename for this entry
        filename = '%s%s%s' % (self.datadir,
                               os.path.sep,
                               self.format_entry_basename(entry))
        if self.pyfilemtime:
            filename += entry.timestamp.strftime("-%Y-%m-%d-%H-%M")
        filename += '.%s' % self.extension
        filename = os.path.expanduser(filename)

        # Ensure that the directory exists
        try:
            os.makedirs(os.path.dirname(filename))
        except:
            # Directory already exists
            pass

        # Handle the entries that already exist
        if os.path.exists(filename):
            if self.overwrite:
                if self.backup:
                    # Make a backup
                    i = 1
                    backup = "%s~%d~" % (filename, i)
                    while os.path.exists(backup):
                        backup = "%s~%d~" % (filename, i)
                        i += 1
                    if not self.quiet:
                        print("Backing up entry: %s" % backup)
                    os.rename(filename, backup)
                else:
                    print("Overwriting entry: %s" % filename)
            else:
                if not self.quiet:
                    print("Entry already exists: %s" % filename)
                return data

        # Write the entry
        file = codecs.open(filename, 'w', self.encoding)
        file.write(data)
        file.close()

        # Set the mtime (for those who do not want to use the
        # pyfilemtime plugin)
        timestamp = time.mktime(entry.timestamp.timetuple())
        os.utime(filename, (timestamp, timestamp))

        return data

    def format_entry_preamble(self, entry):
        """
        Overrides :py:meth:`SlackLogFormatter.format_entry_preamble`.

        :param entry: in-memory representation of the log entry.
        :type: :py:class:`slacklog.models.SlackLogEntry`
        :return: Unicode representation of log entry preamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(entry, models.SlackLogEntry))
        data = self.format_entry_title(entry)
        if self.tags_separator:
            data += u'#tags %s\n' % self.format_entry_tags(entry)
        data += self.entry_preamble
        if entry.description:
            data += u'%s%s%s' % (self.entry_desc_preamble,
                                 entry.description,
                                 self.entry_desc_postamble)
        if entry.pkgs:
            data += self.entry_pkgs_preamble
        return data

    def format_entry_postamble(self, entry):
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
            data += self.entry_pkgs_postamble
        data += self.entry_postamble
        return data

    def format_pkg_preamble(self, pkg):
        """
        Overrides :py:meth:`SlackLogFormatter.format_pkg_preamble`.

        :param pkg: in-memory representation of the log entry package
        :type: :py:class:`slacklog.models.SlackLogPkg`
        :return: Unicode representation of log entry package preamble.
        :type: :py:class:`unicode`
        """
        assert(isinstance(pkg, models.SlackLogPkg))
        data = u'%s%s%s%s%s%s%s%s%s' % (self.pkg_preamble,
                                        self.pkg_name_preamble,
                                        pkg.pkg,
                                        self.pkg_name_postamble,
                                        self.pkg_separator,
                                        self.pkg_desc_preamble,
                                        pkg.description,
                                        self.pkg_desc_postamble,
                                        self.pkg_postamble)
        return data

    def format_entry_basename(self, entry):
        """
        Return basename for the log entry.

        :param entry: in-memory representation of the log entry.
        :type: :py:class:`slacklog.models.SlackLogEntry`
        :return: Unicode representation of log entry name
        :type: :py:class:`unicode`
        """
        return self.slackware.replace(' ', '-').replace('.', '_').lower()

    def format_entry_title(self, entry):
        """
        Return log entry title.

        :param entry: in-memory representation of the log entry.
        :type: :py:class:`slacklog.models.SlackLogEntry`
        :return: Unicode representation of log entry title
        :type: :py:class:`unicode`
        """
        return u'%s changes for %s\n' % (self.slackware, readable(entry.timestamp))

    def format_entry_tags(self, entry):
        """
        Return log entry tags.

        :param entry: in-memory representation of the log entry.
        :type: :py:class:`slacklog.models.SlackLogEntry`
        :return: Unicode representation of log entry tags
        :type: :py:class:`unicode`
        """
        return u'%s' % self.slackware.replace(' ', self.tags_separator)

# -*- coding: utf-8 -*-
import codecs
import datetime
import os
import re
import time
from slacklog import models

class SlackLogFormatter (object):

    def format(cls, log):
        assert(isinstance(log, models.SlackLog))
        data = u''
        data += cls.format_log_preamble(log)
        data += cls.format_list(log.entries, cls.format_entry)
        data += cls.format_log_postamble(log)
        return data
    format = classmethod(format)

    def format_log_preamble(cls, log):
        assert(isinstance(log, models.SlackLog))
        return u''
    format_log_preamble = classmethod(format_log_preamble)

    def format_log_postamble(cls, log):
        assert(isinstance(log, models.SlackLog))
        return u''
    format_log_postamble = classmethod(format_log_postamble)


    def format_entry(cls, entry, is_first, is_last):
        assert(isinstance(entry, models.SlackLogEntry))
        data = u''
        data += cls.format_entry_separator(is_first, is_last)
        data += cls.format_entry_preamble(entry)
        data += cls.format_list(entry.pkgs, cls.format_pkg)
        data += cls.format_entry_postamble(entry)
        return data
    format_entry = classmethod(format_entry)

    def format_entry_separator(cls, is_first, is_last):
        return u''
    format_entry_separator = classmethod(format_entry_separator)

    def format_entry_preamble(cls, entry):
        assert(isinstance(entry, models.SlackLogEntry))
        return u''
    format_entry_preamble = classmethod(format_entry_preamble)

    def format_entry_postamble(cls, entry):
        assert(isinstance(entry, models.SlackLogEntry))
        return u''
    format_entry_postamble = classmethod(format_entry_postamble)


    def format_pkg(cls, pkg, is_first, is_last):
        assert(isinstance(pkg, models.SlackLogPkg))
        data = u''
        data += cls.format_pkg_separator(is_first, is_last)
        data += cls.format_pkg_preamble(pkg)
        data += cls.format_pkg_postamble(pkg)
        return data
    format_pkg = classmethod(format_pkg)

    def format_pkg_separator(cls, is_first, is_last):
        return u''
    format_pkg_separator = classmethod(format_pkg_separator)

    def format_pkg_preamble(cls, pkg):
        assert(isinstance(pkg, models.SlackLogPkg))
        return u''
    format_pkg_preamble = classmethod(format_pkg_preamble)

    def format_pkg_postamble(cls, pkg):
        assert(isinstance(pkg, models.SlackLogPkg))
        return u''
    format_pkg_postamble = classmethod(format_pkg_postamble)

    def format_list(cls, list_of_items, item_formatter):
        data = u''
        num_items = len(list_of_items)
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

    def format_entry_separator(cls, is_first, is_last):
        if not is_first:
            return u'+--------------------------+\n'
        return u''
    format_entry_separator = classmethod(format_entry_separator)

    def format_entry_preamble(cls, entry):
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
        assert(isinstance(pkg, models.SlackLogPkg))
        return u'%s:%s' % (pkg.pkg, pkg.description)
    format_pkg_preamble = classmethod(format_pkg_preamble)

class SlackLogRssFormatter (SlackLogFormatter):

    slackware = None
    rssLink = None
    webLink = None
    description = None
    language = None
    managingEditor = None
    webMaster = None

    def format_log_preamble(cls, log):
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
        assert(isinstance(log, models.SlackLog))
        return u'  </channel>\n</rss>\n'
    format_log_postamble = classmethod(format_log_postamble)


    def format_entry_preamble(cls, entry):
        assert(isinstance(entry, models.SlackLogEntry))
        data  = u'    <item>\n'
        if cls.webLink:
            data += u'      <guid isPermaLink="true">%s#%s</guid>\n' % (cls.webLink, entry.timestamp.strftime("%Y%m%dT%H%M%SZ"))
        else:
            data += u'      <guid isPermaLink="false">%s-%s</guid>\n' % (cls.slackware.replace(' ', '-'), entry.timestamp.strftime("%Y%m%dT%H%M%SZ"))
        data += u'      <title>%s changes for %s</title>\n' % (cls.slackware, entry.timestamp.strftime("%a, %d %b %Y %H:%M:%S GMT"))
        data += u'      <pubDate>%s</pubDate>\n' % entry.timestamp.strftime("%a, %d %b %Y %H:%M:%S GMT")
        if entry.description:
            data += u'      <description>%s<br /><br />' % entry.description
        else:
            data += u'      <description>'
        return data
    format_entry_preamble = classmethod(format_entry_preamble)

    def format_entry_postamble(cls, entry):
        assert(isinstance(entry, models.SlackLogEntry))
        return u'</description>\n    </item>\n'
    format_entry_postamble = classmethod(format_entry_postamble)


    def format_pkg_preamble(cls, pkg):
        assert(isinstance(pkg, models.SlackLogPkg))
        return u'%s: %s<br />' % (pkg.pkg, pkg.description.replace('\n','<br />'))
    format_pkg_preamble = classmethod(format_pkg_preamble)


class SlackLogPyblosxomFormatter (SlackLogFormatter):
    """Print each log entry to a separate file."""

    quiet = False
    slackware = None
    datadir = None
    extension = 'txt'
    encoding = 'utf-8'
    tags_separator = ','
    pkg_separator = ':'
    pyfilemtime = False
    overwrite = False
    backup = True

    # Subclass can change these
    entry_preamble       = u'<div class="slackLogEntry">\n'
    entry_postamble      = u'</div>\n'
    entry_desc_preamble  = u'<div class="slackLogEntryDesc">'
    entry_desc_postamble = u'</div>\n'
    entry_pkgs_preamble  = u'<div class="slackLogEntryPkgs">\n'
    entry_pkgs_postamble = U'</div>\n'
    pkg_preamble         = u'<div class="slackLogPkg">'
    pkg_postamble        = u'</div>\n'
    pkg_name_preamble    = u'<span class="slackLogPkgName">'
    pkg_name_postamble   = u'</span>'
    pkg_desc_preamble    = u'<span class="slackLogPkgDesc">'
    pkg_desc_postamble   = u'</span>'


    def format_entry(cls, entry, is_first, is_last):
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
        assert(isinstance(entry, models.SlackLogEntry))
        data = u''
        if entry.pkgs:
            data += cls.entry_pkgs_postamble
        data += cls.entry_postamble
        return data
    format_entry_postamble = classmethod(format_entry_postamble)


    def format_pkg_preamble(cls, pkg):
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
        return cls.slackware.replace(' ','-').replace('.','_').lower()
    format_entry_basename = classmethod(format_entry_basename)

    def format_entry_title(cls, entry):
        return u'%s changes for %s\n' % (cls.slackware, entry.timestamp.strftime("%a, %d %b %Y %H:%M:%S GMT"))
    format_entry_title = classmethod(format_entry_title)

    def format_entry_tags(cls, entry):
        return u'%s' % cls.slackware.replace(' ',cls.tags_separator)
    format_entry_tags = classmethod(format_entry_tags)


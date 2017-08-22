# coding=utf-8
# encoding: utf-8
import unittest
import os
import filecmp
import shutil
from slacklog.scripts import read, write
from slacklog.parsers import SlackLogParser
from slacklog.formatters import SlackLogRssFormatter


class RssFormatterTest (unittest.TestCase):

    def setUp(self):
        self.input = './test/changelogs/'
        self.output = './test/rss-tmp/'
        self.baseline = './test/rss/'
        self.encoding = 'iso-8859-1'
        self.parser = SlackLogParser()
        self.formatter = SlackLogRssFormatter()
        self.lastBuildDate = self.parser.parse_date(read('./test/rss-timestamp', 'ascii'))
        # Try to ensure clean output dir
        shutil.rmtree(self.output, True)
        os.mkdir(self.output)

    def tearDown(self):
        shutil.rmtree(self.output, True)

    def test(self):

        self.update_rss("slackware",   "12.0",    u'Wed Oct 25 15:45:46 CDT 2006')
        self.update_rss("slackware",   "12.1",    u'Thu Jul 19 12:50:36 CDT 2007')
        self.update_rss("slackware",   "13.0",    u'Wed May  7 16:13:31 CDT 2008')
        self.update_rss("slackware64", "13.0",    u'Tue May 19 15:36:49 CDT 2009')
        self.update_rss("slackware",   "13.1",    u'Mon Sep  7 20:58:42 CDT 2009')
        self.update_rss("slackware64", "13.1",    u'Mon Sep  7 20:58:42 CDT 2009')
        self.update_rss("slackware",   "13.37",   u'Fri Jun 18 18:12:04 UTC 2010')
        self.update_rss("slackware64", "13.37",   u'Fri Jun 18 18:12:04 UTC 2010')
        self.update_rss("slackware",   "14.0",    u'Wed Oct 10 03:06:03 UTC 2012')
        self.update_rss("slackware64", "14.0",    u'Wed Oct 10 03:06:03 UTC 2012')
        self.update_rss("slackware",   "14.1",    u'Mon Nov 18 20:52:16 UTC 2013')
        self.update_rss("slackware64", "14.1",    u'Mon Nov 18 20:52:16 UTC 2013')
        self.update_rss("slackware",   "14.2",    u'Tue Jul  5 04:52:45 UTC 2016')
        self.update_rss("slackware64", "14.2",    u'Tue Jul  5 04:52:45 UTC 2016')
        self.update_rss("slackware",   "current", u'Thu Jan  1 00:00:00 UTC 1970')
        self.update_rss("slackware64", "current", u'Thu Jan  1 00:00:00 UTC 1970')

        base_rss = os.listdir(self.baseline)
        match, mismatch, error = filecmp.cmpfiles(self.baseline, self.output, base_rss, False)

        self.assertEqual(len(base_rss), len(match))
        self.assertEqual(0, len(mismatch))
        self.assertEqual(0, len(error))

    def update_rss(self, slackware, version, min_date):
        self.parser.min_date = self.parser.parse_date(min_date)

        self.formatter.slackware = "%s %s" % (slackware, version)
        self.formatter.rssLink = "http://linuxbox.fi/~vmj/slacklog/%s-%s.rss" % (slackware, version)
        self.formatter.description = "Recent changes in %s %s" % (slackware, version)
        self.formatter.managingEditor = u"vmj@linuxbox.fi (Mikko Värri)"
        self.formatter.webMaster = u"vmj@linuxbox.fi (Mikko Värri)"
        self.formatter.language = "en"
        self.formatter.lastBuildDate = self.lastBuildDate

        slacklog = self.parser.parse(read("%s%s-%s.txt" % (self.input, slackware, version), self.encoding))
        unicode_text = self.formatter.format(slacklog)
        write("%s%s-%s.rss" % (self.output, slackware, version), unicode_text)

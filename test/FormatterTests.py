# coding=utf-8
# encoding: utf-8
import unittest
from datetime import datetime
from dateutil import tz
from slacklog.models import SlackLog
from slacklog.formatters import SlackLogRssFormatter

class FormatterTests (unittest.TestCase):

    def test_empty_rss(self):
        log = SlackLog()

        fmt = SlackLogRssFormatter()
        fmt.lastBuildDate = datetime(2000, 1, 1, 0, 0, 0, 0, tz.tzutc())

        data = fmt.format(log)

        # Since there are no entries, both pubDate and lastBuildDate
        # get the same (injected) timestamp
        self.assertEqual(u"""<?xml version="1.0"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <atom:link href="None" rel="self" type="application/rss+xml" />
    <title>None ChangeLog</title>
    <link>None</link>
    <docs>http://www.rssboard.org/rss-specification</docs>
    <language>None</language>
    <pubDate>Sat, 01 Jan 2000 00:00:00 GMT</pubDate>
    <lastBuildDate>Sat, 01 Jan 2000 00:00:00 GMT</lastBuildDate>
    <generator>SlackLog</generator>
  </channel>
</rss>
""", data)

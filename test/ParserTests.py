# coding=utf-8
# encoding: utf-8
import unittest
from slacklog.scripts import read
from slacklog.parsers import SlackLogParser
from datetime import datetime
from dateutil import tz


class ParserTests (unittest.TestCase):

    def test_slackware_leet_release_entry(self):
        log = SlackLogParser.parse(read('./test/slackware-leet-release-entry.txt', 'iso8859-1'))
        self.assertTrue(log is not None)
        # The content starts and ends with entry separators.
        # The "empty" entries are ignored.
        self.assertEquals(len(log.entries), 1)
        e = log.entries[0]
        self.assertEqual(e.timestamp, datetime(2011, 4, 25, 13, 37, 00, tzinfo=tz.tzutc()))
        self.assertTrue(e.description.startswith(u'Slackware 13.37 x86 stable is released!\n\n'))
        self.assertTrue(e.description.endswith(u'\nHave fun!'))
        self.assertEqual(e.checksum, u'420a2b6d560f5a26c5369565b4ab18281b93f83f05d8defb7efeecaa43e990225819891638147ce2ee9edde5e56a7364583b4334e25b0283f6a4eb98ce7ccda0')
        self.assertEqual(e.identifier, u'4b3a291e203f9a92507d7982e2badc27653f265839306d906cf285be136bae114015508c099ce4d90d0e1e13553e42749957e4557da31ee684ed99a987d6658d')
        self.assertTrue(e.parent is None)
        self.assertTrue(e.pkgs == [])

    def test_slackware_leet_rc3_entry(self):
        log = SlackLogParser.parse(read('./test/slackware-leet-rc3-entry.txt', 'iso8859-1'))
        self.assertTrue(log is not None)
        self.assertEquals(len(log.entries), 1)
        e = log.entries[0]
        self.assertEqual(e.timestamp, datetime(2011, 3, 27, 8, 28, 47, tzinfo=tz.tzutc()))
        # Of special interest here is the line that starts with "candidate:  " which might be
        # confused with a package name.
        self.assertEquals(e.description, u"""There have been quite a few changes so we will have one more release
candidate:  Slackware 13.37 RC 3.14159265358979323846264338327950288419716.
Very close now!  But we'll likely hold out for 2.6.37.6.
""")
        self.assertEquals(len(e.pkgs), 62)
        self.assertEquals(e.pkgs[0].pkg, u'a/aaa_base-13.37-i486-3.txz')
        # There are a few non-typical entries at the end
        self.assertEquals(e.pkgs[57].pkg, u'extra/linux-2.6.37.5-nosmp-sdk/*')
        self.assertEquals(e.pkgs[58].pkg, u'isolinux/initrd.img')
        self.assertEquals(e.pkgs[59].pkg, u'kernels/*')
        self.assertEquals(e.pkgs[60].pkg, u'usb-and-pxe-installers/usbboot.img')
        self.assertEquals(e.pkgs[61].pkg, u'testing/source/linux-2.6.38.1-configs/')

    def test_good_11(self):
        # these logs have a the same change in both of them
        log1 = SlackLogParser.parse(read('./test/good-11-slackware-13.0.txt', 'iso8859-1'))
        log2 = SlackLogParser.parse(read('./test/good-11-slackware-13.1.txt', 'iso8859-1'))
        # even though the entry 1 checksums are the same (exact same change in both logs)...
        self.assertEqual(log1.entries[1].checksum,   log2.entries[1].checksum)
        # ... the next (newer) entries in the logs have different identifiers and parents
        self.assertNotEqual(log1.entries[1].parent,     log2.entries[1].parent)
        self.assertNotEqual(log1.entries[1].identifier, log2.entries[1].identifier)

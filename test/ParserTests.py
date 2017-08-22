# coding=utf-8
# encoding: utf-8
import unittest
from slacklog.scripts import read
from slacklog.parsers import SlackLogParser
from datetime import datetime
from dateutil import tz


class ParserTests (unittest.TestCase):

    def test_slackware_leet_release_entry(self):
        log = SlackLogParser().parse(read('./test/slackware-leet-release-entry.txt', 'iso8859-1'))
        self.assertTrue(log is not None)
        # The content starts and ends with entry separators.
        # The "empty" entries are ignored.
        self.assertEquals(len(log.entries), 1)
        e = log.entries[0]
        self.assertEqual(e.timestamp, datetime(2011, 4, 25, 13, 37, 00, tzinfo=tz.tzutc()))
        self.assertTrue(e.description.startswith(u'Slackware 13.37 x86 stable is released!\n\n'))
        self.assertTrue(e.description.endswith(u'\nHave fun!\n'))
        self.assertEqual(e.checksum, u'b69d2c808b87e4aeeecfc4a3023ed8024473e9a3337e33246ae0d357aa88abd33c78e7a0f7ffc2ba27f0205c35bbe8bffc7269b41cdc1443b5a15ab7969b2245')
        self.assertEqual(e.identifier, u'e22d108e36d622759515b5e495e0b58927bf514a8315dce9d269743826a6c0908cce7b515b3ecd76d6fadf62bb1e56aa11bd8dea1a37cb68044b27ff86c4b0c0')
        self.assertTrue(e.parent is None)
        self.assertTrue(e.pkgs == [])

    def test_slackware_leet_rc3_entry(self):
        log = SlackLogParser().parse(read('./test/slackware-leet-rc3-entry.txt', 'iso8859-1'))
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
        log1 = SlackLogParser().parse(read('./test/good-11-slackware-13.0.txt', 'iso8859-1'))
        log2 = SlackLogParser().parse(read('./test/good-11-slackware-13.1.txt', 'iso8859-1'))
        # even though the entry 1 checksums are the same (exact same change in both logs)...
        self.assertEqual(log1.entries[1].checksum,   log2.entries[1].checksum)
        # ... the next (newer) entries in the logs have different identifiers and parents
        self.assertNotEqual(log1.entries[1].parent,     log2.entries[1].parent)
        self.assertNotEqual(log1.entries[1].identifier, log2.entries[1].identifier)

    def test_single_line_change(self):
        log = SlackLogParser().parse(u"""Thu May 11 18:09:15 UTC 2017
l/gtk+3-3.22.14-i586-1.txz:  Upgraded.
""")
        self.assertEqual(1, len(log.entries))
        self.assertEqual(u'', log.entries[0].description)
        self.assertEqual(1, len(log.entries[0].pkgs))
        self.assertEqual(u'  Upgraded.\n', log.entries[0].pkgs[0].description)

    def test_parse_separators(self):
        p = SlackLogParser()

        def check(str, a, b):
            log = p.parse(str)
            self.assertEqual(a, log.startsWithSeparator)
            self.assertEqual(b, log.endsWithSeparator)

        check(u'', False, False)
        check(u'+-+', True, False)
        check(u'\n+-+', False, True)
        check(u'\n+-+\n', False, True)
        check(u'+-+\n+-+', True, True)
        check(u'Thu May 11 18:09:15 UTC 2017\n+-+\nThu May 11 18:09:15 UTC 2017', False, False)
        check(u'+-+\nThu May 11 18:09:15 UTC 2017\n+-+\nThu May 11 18:09:15 UTC 2017\n+-+', True, True)





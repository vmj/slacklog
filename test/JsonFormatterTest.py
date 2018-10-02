# coding=utf-8
# encoding: utf-8
import unittest
import os
import filecmp
import shutil
from slacklog.scripts import read, write
from slacklog.parsers import SlackLogParser
from slacklog.formatters import SlackLogJsonFormatter


class JsonFormatterTest (unittest.TestCase):

    def setUp(self):
        self.input = './test/changelogs/'
        self.output = './test/json-tmp/'
        self.baseline = './test/json/'
        self.encoding = 'iso-8859-1'
        self.out_encoding = 'utf-8'
        self.parser = SlackLogParser()
        self.formatter = SlackLogJsonFormatter()
        # Try to ensure clean output dir
        shutil.rmtree(self.output, True)
        os.mkdir(self.output)

    def tearDown(self):
        shutil.rmtree(self.output, True)

    def test(self):

        self.update_json("slackware",   "12.0")
        self.update_json("slackware",   "12.1")
        self.update_json("slackware",   "13.0")
        self.update_json("slackware64", "13.0")
        self.update_json("slackware",   "13.1")
        self.update_json("slackware64", "13.1")
        self.update_json("slackware",   "13.37")
        self.update_json("slackware64", "13.37")
        self.update_json("slackware",   "14.0")
        self.update_json("slackware64", "14.0")
        self.update_json("slackware",   "14.1")
        self.update_json("slackware64", "14.1")
        self.update_json("slackware",   "14.2")
        self.update_json("slackware64", "14.2")
        self.update_json("slackware",   "current")
        self.update_json("slackware64", "current")

        base_rss = os.listdir(self.baseline)
        match, mismatch, error = filecmp.cmpfiles(self.baseline, self.output, base_rss, False)

        self.assertEqual(len(base_rss), len(match))
        self.assertEqual(0, len(mismatch))
        self.assertEqual(0, len(error))

    def update_json(self, slackware, version):
        self.formatter.indent = 4

        slacklog = self.parser.parse(read("%s%s-%s.txt" % (self.input, slackware, version), self.encoding))
        unicode_text = self.formatter.format(slacklog)
        write("%s%s-%s.json" % (self.output, slackware, version), unicode_text)

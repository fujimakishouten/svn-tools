#!/usr/bin/env python
# -*- coding: utf-8 -*-

# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4 fileencoding=utf-8:


import argparse
import sys
from xml.etree import ElementTree

# Parse command line options.
parser = argparse.ArgumentParser(description="「svn log --xml」で出力したログを「bzr log --line」が出力する形式に変換します。")
parser.add_argument("-t", "--time", action="store_true", help="日付だけでなく時間も出力します。")
args = parser.parse_args()


# Read data from stdin.
data = sys.stdin.read()
if not data:
    sys.exit(0)

# Parse XML and display log entry.
try:
    xml = ElementTree.fromstring(data)
except:
    sys.exit(0)

for logentry in xml.iter("logentry"):
    revision = logentry.get("revision")
    author   = logentry.find("author").text.encode("utf_8")
    date     = logentry.find("date").text.encode("utf_8")
    message  = logentry.find("msg").text
    msg = ""
    if message:
        msg = message.encode("utf_8").replace("\r\n", " ").replace("\r", " ").replace("\n", " ")

    if args.time:
        date = date.replace("T", " ")[0:date.find(".")]
    else:
        date = date[0:date.find("T")]

    print("{0}: {1} {2} {3}".format(revision, author, date, msg))


# Local variables:
# tab-width: 4
# c-basic-offset: 4
# c-hanging-comment-ender-p: nil
# End:



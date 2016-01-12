#!/usr/bin/env python
# -*- coding: utf-8 -*-

# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4 fileencoding=utf-8:


import argparse
import sys
import subprocess
from   xml.etree import ElementTree


# Parse command line options.
parser = argparse.ArgumentParser(description="「svn log --xml」で出力したログを「bzr log --line」が出力する形式に変換します。")
parser.add_argument("-m", "--merged",   action="store_true", help="マージ済みのリビジョンの一覧を表示する場合に指定します。（デフォルトでは未マージのリビジョンの一覧が表示されます。)")
parser.add_argument("-r", "--revision", action="store", help="リビジョンを指定します。")
parser.add_argument("-s", "--source",   action="store", required=True, help="マージ元のパスを指定します。")
parser.add_argument("-t", "--target",   action="store", default=".", help="マージ先のパスを指定します。")
args = parser.parse_args()

type = "merged" if args.merged else "eligible"


# Get eligible revisions
print("\033[34mGet eligible revisions...\033[0m")
try:
    command   = ["/usr/bin/env", "svn", "mergeinfo"]
    if args.revision:
        command.extend(["--revision", args.revision])
    command.extend(["--show_revs", type, args.source, args.target])

    eligibles = [revs for revs in subprocess.check_output(["/usr/bin/env", "svn", "mergeinfo", "--show-revs", type, args.source, args.target]).split("\n")]
except subprocess.CalledProcessError as e:
    print("\033[31mError:\033[0m")
    print(e.output)
except:
    sys.exit(0)
print("")


# Get revision info
print("\033[34mGet revision logs...\033[0m")
try:
    data = subprocess.check_output(["/usr/bin/env", "svn", "log", "--xml", args.source])
except subprocess.CalledProcessError as e:
    print("\033[31mError:\033[0m")
    print(e.output)
except:
    sys.exit(0)
print("")


# Parse XML
try:
    xml = ElementTree.fromstring(data)
except:
    sys.exit(0)


# Display info
count = 0;
for logentry in xml.iter("logentry"):
    revision = logentry.get("revision")
    author   = logentry.find("author").text.encode("utf_8")
    date     = logentry.find("date").text.encode("utf_8")
    message  = logentry.find("msg").text
    if 'r' + revision in eligibles:
        msg = ""
        if message:
            msg = message.encode("utf_8").replace("\r\n", " ").replace("\r", " ").replace("\n", " ")

        date = date[0:date.find("T")]

        print("{0}: {1} {2} {3}".format(revision, author, date, msg))



# Local variables:
# tab-width: 4
# c-basic-offset: 4
# c-hanging-comment-ender-p: nil
# End:



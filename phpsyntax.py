#!/usr/bin/env python
# -*- coding: utf-8 -*-

# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4 fileencoding=utf-8:


import argparse
import sys
import subprocess
from xml.etree import ElementTree

# Parse command line options.
parser = argparse.ArgumentParser(description="「svn status --xml」で出力したファイルのうち、拡張子が「.php」のもののシンタックスをチェックします。")
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

for entry in xml.iter("entry"):
    path = entry.get("path")
    if '.php' == path[-4:]:
        try:
            subprocess.check_output(["/usr/bin/env", "php", "-l", path])
        except subprocess.CalledProcessError as e:
            print("\033[31mError : {0}\033[0m".format(path))
            print("\033[34mOutput: \033[0m")
            for line in e.output.split("\n"):
                if line: print("    " + line.strip())
            print("")


# Local variables:
# tab-width: 4
# c-basic-offset: 4
# c-hanging-comment-ender-p: nil
# End:



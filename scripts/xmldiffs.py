#!/usr/bin/env python
"""
Usage: {prog} [OPTION] FILE1 FILE2

Compare two XML files, ignoring element and attribute order.

Any extra options are passed to the `diff' command.

Copyright (c) 2017, Johannes H. Jensen.
License: BSD, see LICENSE for more details.
"""
from __future__ import print_function, unicode_literals
import sys
import os
import io
import xml.etree.ElementTree as ET
from tempfile import NamedTemporaryFile
import subprocess

def attr_str(k, v):
    return "{}=\"{}\"".format(k,v)

def node_str(n):
    attrs = sorted(n.attrib.items())
    astr = " ".join(attr_str(k,v) for k,v in attrs)
    s = n.tag
    if astr:
        s += " " + astr
    return s

def node_key(n):
    return node_str(n)

def indent(s, level):
    return "  " * level + s

def write_sorted(stream, node, level=0):
    children = node.getchildren()
    text = (node.text or "").strip()
    tail = (node.tail or "").strip()

    if children or text:
        children.sort(key=node_key)

        stream.write(indent("<" + node_str(node) + ">\n", level))

        if text:
            stream.write(indent(text + "\n", level))

        for child in children:
            write_sorted(stream, child, level + 1)

        stream.write(indent("</" + node.tag + ">\n", level))
    else:
        stream.write(indent("<" + node_str(node) + "/>\n", level))

    if tail:
        stream.write(indent(tail + "\n", level))

if sys.version_info < (3, 0):
    # Python 2
    import codecs
    def unicode_writer(fp):
        return codecs.getwriter('utf-8')(fp)
else:
    # Python 3
    def unicode_writer(fp):
        return fp

def xmldiffs(file1, file2, diffargs=["-u"]):
    tree = ET.parse(file1)
    tmp1 = unicode_writer(NamedTemporaryFile('w'))
    write_sorted(tmp1, tree.getroot())
    tmp1.flush()

    tree = ET.parse(file2)
    tmp2 = unicode_writer(NamedTemporaryFile('w'))
    write_sorted(tmp2, tree.getroot())
    tmp2.flush()

    args = [ "diff" ]
    args += diffargs
    args += [ "--label", file1, "--label", file2 ]
    args += [ tmp1.name, tmp2.name ]

    subprocess.call(args)

def print_usage(prog):
    print(__doc__.format(prog=prog).strip())

if __name__ == '__main__':
    args = sys.argv
    prog = os.path.basename(args.pop(0))

    if '-h' in args or '--help' in args:
        print_usage(prog)
        exit(0)

    if len(args) < 2:
        print_usage(prog)
        exit(1)

    file2 = args.pop(-1)
    file1 = args.pop(-1)
    diffargs = args if args else ["-u"]

    xmldiffs(file1, file2, diffargs)

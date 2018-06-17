#!/usr/bin/python
import sys, subprocess, os

from sys import platform as _platform
from os.path import join, dirname, normpath, exists, split, expanduser


if len(sys.argv) != 3:
    print 'This script takes two arguments to provide pawn data: a save filename, and a pawn\'s nickname.'
    exit(-1)

save = sys.argv[1]
pawn = sys.argv[2]

if not exists(save):
    print 'The specified save file doesn\'t appear to exist.'
    exit(-1)

try:
    from lxml import etree
except:
    print 'Couldn\'t load lxml. Make sure you have this library installed.\nTry running this:\n\tpip install lxml'
    exit(-1)

try:
    tree = etree.parse( save )
except etree.XMLSyntaxError, e:
    print '\tThis save is misformed; skipping it...'
    print '\tError:         %s' % e.message

# Find the pawn and show their data
for pawn in tree.xpath('/savegame/game/maps/li/things/thing[@Class="Pawn"]/name[@Class="NameTriple"]/nick[text()="%s"]' % pawn):
    pawn = pawn.getparent().getparent()
    print etree.tostring( pawn, pretty_print=True )

exit(0)

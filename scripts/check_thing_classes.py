#!/usr/bin/python
import sys, subprocess, os

from sys import platform as _platform
from os.path import join, dirname, normpath, exists, split, expanduser
from glob import glob

def stringify_children(node):
    from lxml.etree import tostring
    from itertools import chain
    parts = ([node.text] +
            list(chain(*([c.text, tostring(c), c.tail] for c in node.getchildren()))) +
            [node.tail])
    # filter removes possible Nones in texts and tails
    return ''.join(filter(None, parts))

save = sys.argv[1]

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

# Find ALL THE THINGS...
things = tree.xpath( '//li[@Class]/innerContainer | //thing[@Class]/innerContainer | //thing[@Class]/contents/innerContainer')

'''for thing in things:

    if 'Class' not in thing.items():
        print thing.getroottree().getpath(thing)
        print thing.tag, thing.items() #, thing.sourcefile

        if thing.getparent().tag == 'contents':
            print 'Parent', thing.getparent().getparent().tag, thing.getparent().getparent().items()
        else:
            print 'Parent', thing.getparent().tag, thing.getparent().items()

        #print stringify_children( thing )

        #print thing.attrib('Class') #, thing.attribs
    continue
'''

verbs = []
# Let's find all verbs
for verbId in tree.xpath('//verbTracker/verbs/li/loadID'):
    verbs.append( verbId.text )

print 'There are', len(verbs), 'verbs'

types = []
for verb in tree.xpath('//meleeVerbs'):
    for x in verb.iterchildren():
        print x.tag


found_ref_verbs = []
not_found_ref_verbs = []
for verb in tree.xpath('//meleeVerbs/curMeleeVerb'):
    if verb.text == 'null':
        continue
    verb_id = verb.text.split('_')[1]

    if verb_id in verbs:
        found_ref_verbs.append( verb_id )
    else:
        not_found_ref_verbs.append( verb_id )

    #pawn = pawn.getparent().getparent()

    #print pawn.getroottree().getpath( pawn )
    #print etree.tostring( pawn, pretty_print=True )

print len(found_ref_verbs), 'were found', len(not_found_ref_verbs), 'were not found'

import base64
#coded_string = '''Q5YACgA...'''

for prison_records in tree.xpath('//li/def[text()="Prisoners"]'):
    prison_records = prison_records.getnext()
    print base64.b64decode( prison_records.text )

exit(0)

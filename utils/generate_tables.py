#!/usr/bin/python
import sys, subprocess, os

from sys import platform as _platform
from os.path import join, dirname, normpath, exists, split, expanduser
from pprint import pprint

try:
    from lxml import etree
except:
    print 'Couldn\'t load lxml. Make sure you have this library installed.\nTry running this:\n\tpip install lxml'
    exit(-1)

pawnKind_races = {}
thing_bodies = {}
abstract_bodies = {}

print 'type_bodies = {'

for race_def in os.listdir( expanduser( '~/Library/Application Support/Steam/steamapps/common/RimWorld/RimWorldMac.app/Mods/Core/Defs/ThingDefs_Races' ) ):

    # Skip temp files
    if not race_def.endswith('.xml'):
        continue

    # Let's look at the race def
    try:
        tree = etree.parse( join( expanduser( '~/Library/Application Support/Steam/steamapps/common/RimWorld/RimWorldMac.app/Mods/Core/Defs/ThingDefs_Races' ), race_def ) )
    except etree.XMLSyntaxError, e:
        print '\tThis save is misformed; skipping it...'
        print '\tError:         %s' % e.message

    for pawnKindDef in tree.xpath('/Defs/PawnKindDef'):
        if pawnKindDef.xpath('defName'):
            pawn = pawnKindDef.xpath('defName')[0].text
            race = pawnKindDef.xpath('race')[0].text
            if pawn != race:
                pawnKind_races[ pawn ] = race
            #print '-->', pawnKindDef.xpath('defName')[0].text, 'is a kind of', pawnKindDef.xpath('race')[0].text

    for thing in tree.xpath('/Defs/ThingDef | /ThingDefs/ThingDef'):
        # Populate abstract bodies
        if not thing.xpath('defName') and thing.xpath('race/body'):
            abstract_bodies[ thing.attrib['Name'] ] = thing.xpath('race/body')[0].text
            #print 'abstract', thing.attrib['Name'], thing.xpath('race/body')[0].text

    for thing in tree.xpath('/Defs/ThingDef | /ThingDefs/ThingDef'):
        if thing.xpath('defName'):
            if thing.xpath('race/body'):
                thing_bodies[ thing.xpath('defName')[0].text ] = thing.xpath('race/body')[0].text
                print "    '%s': '%s'," % ( thing.xpath('defName')[0].text, thing.xpath('race/body')[0].text )
            else:
                thing_bodies[ thing.xpath('defName')[0].text ] = abstract_bodies[ thing.attrib['ParentName'] ]
                print "    '%s': '%s'," % ( thing.xpath('defName')[0].text, abstract_bodies[ thing.attrib['ParentName'] ] )

print '}'

print 'body_parts = {'

for body in os.listdir( expanduser( '~/Library/Application Support/Steam/steamapps/common/RimWorld/RimWorldMac.app/Mods/Core/Defs/Bodies' ) ):

    # Skip temp files
    if not body.endswith('.xml'):
        continue

    try:
        tree = etree.parse( join( expanduser( '~/Library/Application Support/Steam/steamapps/common/RimWorld/RimWorldMac.app/Mods/Core/Defs/Bodies' ), body ) )
    except etree.XMLSyntaxError, e:
        print '\t%s is misformed; skipping it...' % body
        print '\tError:         %s' % e.message

    for bodyDef in tree.xpath('/BodyDefs/BodyDef | /Defs/BodyDef'):
        print "    '%s': [" % bodyDef.xpath('defName')[0].text

        for partDef in bodyDef.xpath('.//corePart | .//parts/li'):
            print "        '%s'," % ( partDef.xpath('def')[0].text )

        print '    ],'
print '}'

#!/usr/bin/python
import sys, subprocess, os

from sys import platform as _platform
from os.path import join, dirname, normpath, exists, split, expanduser

home = expanduser("~")

save_path = '~/.config/unity3d/Ludeon Studios/RimWorld by Ludeon Studios/Saves'

if _platform == "darwin":
   save_path = '~/Library/Application Support/RimWorld/Saves'
elif _platform == "win32":
   save_path = '~\AppData\LocalLow\Ludeon Studios\RimWorld by Ludeon Studios\Saves'

# Expand the homedir
save_path = expanduser( save_path )

print 'Your saves should be at %s...'  % save_path

if not exists(save_path):
    print 'However, that path doesn\'t exist. Do you have any saves?'
    exit(-1)

try:
    from lxml import etree
    from lxml import objectify
except:
    print 'Couldn\'t load lxml. Make sure you have this library installed.\nTry running this:\n\teasy_install lxml'
    exit(-1)

for save in os.listdir( save_path ):
    # Let's find all .rws files
    if save.endswith('.rws'):
        tree = etree.parse( join( save_path, save ) )

        # Pull out the key bits
        version = tree.xpath('/savegame/meta/gameVersion' )[0].text
        seed = tree.xpath('/savegame/game/world/info/seedString' )[0].text
        size = tree.xpath('/savegame/game/world/info/size' )[0].text
        playtime = tree.xpath('/savegame/game/info/realPlayTimeInteracting' )[0].text

        # Build a string representing mods. We'll only show the modId if it
        # doesn't match the name.
        modIds = tree.xpath('/savegame/meta/modIds/li' )
        modNames = tree.xpath('/savegame/meta/modNames/li' )
        i = 0
        mods = []
        for name in modNames:
            if name.text == modIds[i].text:
                mods.append( name.text )
            else:
                mods.append( '% (%s)' % ( name.text, modIds[i].text ) )
            i += 1
        mods = ', '.join( mods )

        m, s = divmod( float(playtime), 60)
        h, m = divmod(m, 60)

        # Print that info.
        print '%s' % save[:-4]
        print '\tVersion:       %s' % version
        print '\tSeed:          %s %s' % (seed, size)
        print '\tReal playtime: %d:%02d:%02d' % (h, m, s)
        print '\tMods:          %s' % mods

exit(0)

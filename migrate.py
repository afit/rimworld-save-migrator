#!/usr/bin/python
import sys, subprocess, os

from os.path import join, dirname, normpath, split

from utils.filesystem import get_save_path

save_path, exists = get_save_path()

print 'Looking for saves in %s...'  % save_path

if not exists:
    print 'However, that path doesn\'t exist. Do you have any saves?'
    exit(-1)

try:
    from lxml import etree
except:
    print 'Couldn\'t load lxml; you can install it by running: `pip install lxml`'
    exit(-1)

for save in os.listdir( save_path ):
    # Let's find all .rws files
    if save.endswith('.rws'):
        try:
            tree = etree.parse( join( save_path, save ) )
        except etree.XMLSyntaxError, e:
            print '\tSave "%s" misformed; skipping it...' % save[:-4]
            print '\tError:         %s' % e.message
            continue

        # Pull out the key bits
        version = tree.xpath('/savegame/meta/gameVersion' )[0].text
        seed = tree.xpath('/savegame/game/world/info/seedString' )[0].text

        majorVersion = int( version.split('.')[0] )
        minorVersion = int( version.split('.')[1] )

        if majorVersion == 1:
            size = tree.xpath('/savegame/game/world/info/initialMapSize' )[0].text
        elif minorVersion >= 16:
            size = tree.xpath('/savegame/game/maps/li/mapInfo/size' )[0].text
        else:
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
                mods.append( u'"%s"' % name.text ) # , modIds[i].text ) )
            i += 1
        mods = ', '.join( mods )

        m, s = divmod( float(playtime), 60)
        h, m = divmod(m, 60)

        # Print that info.
        print ' * "%s" (version: %s, seed: %s %s, playtime: %d:%02d:%02d, mods: %s)' % ( save[:-4], version, seed, size, h, m, s, mods )

exit(0)

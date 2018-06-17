#!/usr/bin/python
import sys

from os.path import exists, join

from util.exceptions import MisformedSaveError
from util.filesystem import get_saves
from util.saves import Save

if len(sys.argv) > 1:
    save_name = sys.argv[1]
else:
    save_name = None

if not save_name:
    saves, save_path = get_saves()
    print 'No argument provided; listing saves in %s...\n'  % save_path

    if not saves:
        print 'However, there aren\'t any saves there.'
        exit(-1)

    try:
        from lxml import etree
    except:
        print 'Couldn\'t load lxml; you can install it by running: `pip install lxml`'
        exit(-1)

    for path in saves:
        try:
            save = Save( path )
        except MisformedSaveError, e:
            print '\tSave "%s" misformed; skipping it...' % path[:-4]
            print '\tError:         %s' % e.message
            continue

        # Print that info.
        print ' * "%s" (version: %s, seed: %s %s, playtime: %s, mods: %s)' % (
            save.name, save.version,
            save.seed, save.size,
            save.playtime, ', '.join( save.mods.keys() ),
        )

    print '\nRun this script again with a save name to migrate it.'
    exit(0)

# Let's figure out what to do with the save we've been told about.
if exists( save_name ): # Hey, it's a path
    save = Save( save_name )
else: # It must be a name
    save = Save( '%s.rws' % join( get_saves()[1], save_name ) )

print save.name

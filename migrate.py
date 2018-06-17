#!/usr/bin/python
import sys

from os.path import exists, join

from util.exceptions import MisformedSaveError
from util.filesystem import get_saves
from util.saves import Save

def migrate():
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

        print '\nRun this script again with a path or save name to migrate it.'
        exit(0)

    # Let's figure out what to do with the save we've been told about.
    if exists( save_name ): # Hey, it's a path
        save = Save( save_name )
    else: # It must be a name
        try:
            save = Save( '%s.rws' % join( get_saves()[1], save_name ) )
        except IOError:
            print 'Couldn\'t find path or save called "%s".' % save_name
            exit(-1)

    print 'Examining save; it is version %s.' % save.version

    # Lets look at the save we've been told about.
    version = [int(i) for i in save.version.split( ' ' )[0].split( '.' )]

    if version[0] == 1: # Version 1. That's the latest, for now.
        print 'Further migrations not supported; check for an updated script.'
        exit(-1)
    elif version[1] < 15:
        print 'Follow the guide at https://github.com/afit/rimworld-save-migrator to migrate saves from below A15.'
        exit(-1)
    elif version[1] == 17:
        print 'This save can be migrated to B18 by loading and saving it in RimWorld B18.'
        exit(-1)

    # This leaves us with A15, A16 and B18.
    print version

if __name__ == '__main__':
    migrate()

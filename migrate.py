#!/usr/bin/python
import sys

from os.path import exists, join, dirname
from importlib import import_module

from util.exceptions import MisformedSaveError
from util.filesystem import get_saves, get_save_path, get_path_from_name
from util.saves import Save


def migrate():
    if len(sys.argv) > 1:
        save_name = sys.argv[1]
    else: save_name = None

    debug = len(sys.argv) > 2 and sys.argv[2] == 'debug'

    if not save_name:
        print 'No argument provided; listing saves in %s...\n'  % get_save_path()
        saves = get_saves()

        if not saves:
            print 'However, there aren\'t any saves there.'
            exit(0)

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
            save = Save( get_path_from_name( save_name ) )
        except IOError:
            print 'Couldn\'t find path or save called "%s".' % save_name
            exit(-1)

    print 'Examining save; it is version %s.' % save.version

    if save.mods:
        print 'This save includes mods, which complicate migration. If migration does not complete, try re-saving your original game without mods.'

    # Lets look at the save we've been told about.
    if save.versions[0] == 1: # Version 1. That's the latest, for now.
        print 'Further migrations not supported; check for an updated script.'
        exit(-1)
    elif save.versions[1] < 15:
        print 'Follow the guide at https://github.com/afit/rimworld-save-migrator to migrate saves from below A15.'
        exit(-1)
    elif save.versions[1] == 17:
        print 'This save can be migrated to B18 by loading and saving it in RimWorld B18.'
        exit(-1)

    # This leaves us with A15, A16 and B18. We need a seed to be able to migrate these.
    # Let's use a matrix.
    matrix = {
        '0.18': {
            'seed_needed': None,
            'seed_readable': '1.0',
            'migration': 'versions.u1migration',
        },
        '0.16': {
            'seed_needed': [0, 17],
            'seed_readable': 'A17',
            'migration': 'versions.a17migration',
        },
        '0.15': {
            'seed_needed': [0, 16],
            'seed_readable': 'A16',
            'migration': 'versions.a16migration',
        },
    }

    mi = matrix[ '.'.join( str(x) for x in save.versions[0:2] ) ]

    # If one wasn't passed, let's use one of the sample saves.
    if mi['seed_needed']:
        print 'In order to migrate this save, data is needed from a new %s save; I\'ll use your most recently modified save of this version.' % mi['seed_readable']

        found = False
        for s in get_saves():
            seed = Save( s )
            if seed.versions[0:2] == mi['seed_needed']:
                found = True
                break

        if not found:
            print 'Couldn\'t find a save of this version to use as a seed: please create one.'
            exit(-1)

        print 'Using "%s" as seed...' % seed.name

    migration_name = '%s.%smigration.rws' % ( save.name, mi['seed_readable'] )
    migration_path = join( dirname( save.path ), migration_name )

    print 'Migrating to new save "%s"...' % migration_name

    if not debug and exists( migration_path ):
        print 'Can\'t migrate as "%s" already exists: move it away first?' % migration_name
        exit(-1)

    migration = import_module( mi['migration'] )
    if mi['seed_needed']:
        migration.migrate( save.path, seed.path, migration_path )
    else:
        migration.migrate( save.path, migration_path )

    print 'Migrated successfully to "%s", you should load and save this before migrating further. Good luck!' % migration_name
    print 'Report issues etc. to https://github.com/afit/rimworld-save-migrator.'
    exit(0)


if __name__ == '__main__':
    migrate()

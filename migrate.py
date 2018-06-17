#!/usr/bin/python
import sys, subprocess, os

from os.path import join, dirname, normpath, split

from util.exceptions import MisformedSaveError
from util.filesystem import get_save_path
from util.saves import Save

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

for path in os.listdir( save_path ):
    # Let's find all .rws files
    if path.endswith('.rws'):
        try:
            save = Save( join( save_path, path ) )
        except MisformedSaveError, e:
            print '\tSave "%s" misformed; skipping it...' % path[:-4]
            print '\tError:         %s' % e.message
            continue

        mods = ', '.join( save.mods.keys() )

        # Print that info.
        print ' * "%s" (version: %s, seed: %s %s, playtime: %s, mods: %s)' % (
            path[:-4], save.version, save.seed, save.size, save.playtime, mods
        )

exit(0)

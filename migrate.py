#!/usr/bin/python
import sys, subprocess, os

#from os.path import join, dirname, normpath, split

from util.exceptions import MisformedSaveError
from util.filesystem import get_saves
from util.saves import Save

saves, save_path = get_saves()

print 'Looking for saves in %s...'  % save_path

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

exit(0)

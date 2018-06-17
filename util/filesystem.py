from sys import platform as _platform
from os.path import exists, expanduser, join, getmtime
from os import listdir


def get_save_path():
    ''' Return available saves and the default save location. '''

    if _platform == "darwin": # macOS
        return expanduser(
            '~/Library/Application Support/RimWorld/Saves'
        )

        # FIXME very old versions used this:
        #save_path = expanduser(
        #    '~/Library/Application Support/Ludeon Studios/RimWorld/Saves'
        #)
    elif _platform == "win32": # Windows
        return expanduser(
            '~\AppData\LocalLow\Ludeon Studios\RimWorld by Ludeon Studios\Saves'
        )
    # Linux
    return expanduser(
        '~/.config/unity3d/Ludeon Studios/RimWorld by Ludeon Studios/Saves'
    )

def listsortdir( path ):
    ''' Returns files in reverse date order. '''
    def _getmtime( name ):
        return getmtime( join( path, name ) )

    return sorted( listdir( path ), key=_getmtime, reverse=True )

def get_path_from_name( name ):
    ''' Given the name of a save, puts the right path in front of it. '''
    return '%s.rws' % join( get_save_path(), name )

def get_saves():
    save_path = get_save_path()

    saves = []
    if exists( save_path ):
        for path in listsortdir( save_path ):
            # Let's find all .rws files
            if path.endswith('.rws'):
                saves.append( join( save_path, path ) )

    return saves

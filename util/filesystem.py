from sys import platform as _platform
from os.path import exists, expanduser, join
from os import listdir


def get_saves():
    ''' Return available saves and the default save location. '''

    if _platform == "darwin": # macOS
        save_path = expanduser(
            '~/Library/Application Support/RimWorld/Saves'
        )

        # FIXME very old versions used this:
        #save_path = expanduser(
        #    '~/Library/Application Support/Ludeon Studios/RimWorld/Saves'
        #)
    elif _platform == "win32": # Windows
        save_path = expanduser(
            '~\AppData\LocalLow\Ludeon Studios\RimWorld by Ludeon Studios\Saves'
        )
    else: # Linux
        save_path = expanduser(
            '~/.config/unity3d/Ludeon Studios/RimWorld by Ludeon Studios/Saves'
        )

    saves = []
    if exists( save_path ):
        for path in listdir( save_path ):
            # Let's find all .rws files
            if path.endswith('.rws'):
                saves.append( join( save_path, path ) )

    return saves, save_path

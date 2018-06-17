from sys import platform as _platform
from os.path import exists, expanduser


def get_save_path():
    ''' Return the default save path and whether it exists. '''

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

    return save_path, exists( save_path )

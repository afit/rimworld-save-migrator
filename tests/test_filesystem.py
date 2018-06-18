from util.filesystem import get_save_path, listsortdir, get_path_from_name, get_saves

import pytest, subprocess


class TestFilesystem(object):
    ''' Tests for the filesystem utils. '''

    def test_get_save_path(self):
        assert isinstance( get_save_path(), str )

    def test_listsortdir(self):
        assert isinstance( listsortdir( '.' ), list )

    def test_get_save_path(self):
        assert isinstance( get_path_from_name( 'savegame' ), str )

    def test_get_saves(self):
        for s in get_saves():
            assert isinstance( s, str )

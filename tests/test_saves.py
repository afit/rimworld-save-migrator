from util.filesystem import get_save_path, listsortdir, get_path_from_name, get_saves
from util.exceptions import MisformedSaveError
from util.saves import Save

import pytest, subprocess


class TestSaves(object):
    ''' Tests for the Save object. '''

    MATRIX = {
        'a14_bogdan': {
            'version': '0.14.1249 rev944',
            'versions': [0, 14, 1249],
            'seed': 'bogdan',
            'playtime': '0:00:24',
            'size': '(200, 150)',
            'mods': {'Core': None,},
        },
        'a15_bogdan': {
            'version': '0.15.1284 rev141',
            'versions': [0, 15, 1284],
            'seed': 'bogdan',
            'playtime': '0:00:23',
            'size': '(200, 150)',
            'mods': {'Core': None,},
        },
        'a16_bogdan': {
            'version': '0.16.1393 rev538',
            'versions': [0, 16, 1393],
            'seed': 'bogdan',
            'playtime': '0:00:26',
            'size': '(250, 1, 250)',
            'mods': {'Core': None,},
        },
        'a17_bogdan': {
            'version': '0.17.1557 rev1154',
            'versions': [0, 17, 1557],
            'seed': 'bodgan', # FIXME FFS
            'playtime': '0:00:12',
            'size': '(250, 1, 250)',
            'mods': {'Core': None,},
        },
        'b18_bogdan': {
            'version': '0.18.1722 rev1206',
            'versions': [0, 18, 1722],
            'seed': 'bogdan',
            'playtime': '0:00:06',
            'size': '(250, 1, 250)',
            'mods': {'Core': None,},
        },
        'u1_bogdan': {
            'version': '1.0.1936 rev835',
            'versions': [1, 0, 1936],
            'seed': 'bogdan',
            'playtime': '0:01:26',
            'size': '(250, 1, 250)',
            'mods': {'Core': None,},
        },

    }

    def test_missing_save(self):
        with pytest.raises(IOError) as e_info:
            s = Save( 'missing-save' )

    @pytest.mark.slow
    def test_save(self):
        for save in self.MATRIX.keys():
            s = Save( './resources/%s.rws' % save )

            assert s.version == self.MATRIX[save]['version']
            assert s.versions == self.MATRIX[save]['versions']
            assert s.seed == self.MATRIX[save]['seed']
            assert s.playtime == self.MATRIX[save]['playtime']
            assert s.size == self.MATRIX[save]['size']
            assert s.mods == self.MATRIX[save]['mods']

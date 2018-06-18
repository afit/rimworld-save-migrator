from util.saves import Save

import pytest, os


class TestMigrations(object):
    ''' Tests for the Save object. '''

    @pytest.mark.slow
    def test_a15_to_a16(self):
        from migrations.a16migration import migrate

        try:
            migrate( './resources/a15_bogdan.rws', './resources/a16_bogdan.rws', './temp-test.rws' )
        finally:
            os.remove( './temp-test.rws' )

    @pytest.mark.slow
    def test_a16_to_a17(self):
        from migrations.a17migration import migrate

        try:
            migrate( './resources/a16_bogdan.rws', './resources/a17_bogdan.rws', './temp-test.rws' )
        finally:
            os.remove( './temp-test.rws' )

    @pytest.mark.slow
    def test_b18_to_u1(self):
        from migrations.u1migration import migrate

        try:
            migrate( './resources/b18_bogdan.rws', './temp-test.rws' )
        finally:
            os.remove( './temp-test.rws' )

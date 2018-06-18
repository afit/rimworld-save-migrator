from migrate import migrate

import pytest, subprocess


class TestMigrate(object):
    ''' Tests for the migrate.py command-line script. '''

    @pytest.mark.slow
    def test_noargs(self):
        p = subprocess.Popen('python migrate.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = p.stdout.readlines()

        assert output[0].startswith( 'No argument provided' )

        # Does it exit OK?
        assert p.wait() == 0

    def test_nosave(self):
        p = subprocess.Popen('python migrate.py missing-save', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = p.stdout.readlines()

        assert output[0].startswith( 'Couldn\'t find' )

        # Should fail
        assert p.wait() == 255

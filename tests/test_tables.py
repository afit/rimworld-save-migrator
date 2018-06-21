import pytest


class TestTables(object):
    ''' Tests for the save tables. '''

    def test_imports(self):
        # Have they been generated correctly?
        from versions import a16tables
        from versions import a17tables
        from versions import b18tables
        from versions import u1tables

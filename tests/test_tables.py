import pytest


class TestTables(object):
    ''' Tests for the save tables. '''

    def test_imports(self):
        # Have they been generated correctly?
        from migrations import a16tables
        from migrations import a17tables
        from migrations import b18tables
        from migrations import u1tables

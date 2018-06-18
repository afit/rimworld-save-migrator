from util.exceptions import MisformedSaveError

import pytest


class TestExceptions(object):
    ''' Tests for the custom exceptions. '''

    def test_misformed_save_error(self):
        e = MisformedSaveError( 'Message' )

        assert e.message == 'Message'

        with pytest.raises(MisformedSaveError) as e_info:
            raise e

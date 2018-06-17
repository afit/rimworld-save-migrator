
class MisformedSaveError(Exception):
    def __init__(self, message):
        super(MisformedSaveError, self).__init__(message)
        self.message = message

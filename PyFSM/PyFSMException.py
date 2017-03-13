#####################################################################################
# Class Definitions
#####################################################################################
class InitializationError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class UndefinedStateError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class DisabledLibError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

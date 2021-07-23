class StateError(ValueError):
    """
    Same as ValueError just renamed
    """
    def __init__(self, message):
        self.message = message

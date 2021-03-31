class AgeError(Exception):
    def __init__(self, message='AgeError!!!'):
        super().__init__(message)
        self.message = message
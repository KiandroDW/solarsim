class SolarSimException(Exception):
    """
    Basic exception class for SolarSim exceptions.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class HTTPSolarSimException(SolarSimException):
    """
    Exception class for HTTP faults.
    """
    def __init__(self, message="Unable to connect to NASA JPL servers."):
        self.message = message
        super().__init__(self.message)


class FileSolarSimException(SolarSimException):
    """
    Exception class for file structure exceptions.
    """
    def __init__(self, message="Unable to change file structure."):
        self.message = message
        super().__init__(self.message)


class BackgroundSolarSimException(SolarSimException):
    """
    Exception class for background problems.
    """
    def __init__(self, message="Unable to change background."):
        self.message = message
        super().__init__(self.message)

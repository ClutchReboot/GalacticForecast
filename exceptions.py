from dataclasses import dataclass


@dataclass
class InvalidLocationError(Exception):
    """Exception for invalid account numbers.

    Attributes:
        message: The message to display.

    Args:
        message: The message to display.

    """

    def __init__(self, message) -> None:
        self.message: str = message
        super().__init__(self.message)


@dataclass
class RequestError(Exception):
    """Exception for invalid account numbers.

    Attributes:
        message: The message to display.

    Args:
        message: The message to display.

    """

    def __init__(self, message) -> None:
        self.message: str = message
        super().__init__(self.message)

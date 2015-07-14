"""Contains the definitions for the responders."""


class BaseResponseManager(object):
    """Contains responder logic to respond to messages."""

    def __init__(self):
        self.mentioned_map = {
            '(hi|hello)': self.hello,
            'ping': self.ping,
            'wolf': self.wolf,
        }

        self.not_mentioned_map = {

        }

    @staticmethod
    def hello(_):
        """Says hello!"""
        return 'Greetings. I am C-3PO, human cyborg relations.'

    @staticmethod
    def ping(_):
        """Pongs back."""
        return 'pong'

    @staticmethod
    def wolf(_):
        """Wolf... pack!"""
        return 'PACK!'

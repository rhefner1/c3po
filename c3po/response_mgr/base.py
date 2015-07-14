"""Contains the definitions for the responders."""


class BaseResponseManager(object):
    """Contains responder logic to respond to messages."""

    def __init__(self):
        self.mentioned_map = {
            'created you': self.creator,
            '(hi|hello)': self.hello,
            'ping': self.ping,
            'wolf': self.wolf,
        }

        self.not_mentioned_map = {

        }

    @staticmethod
    def creator(_):
        """Tells who the real creator is."""
        return 'My friend @Hef (and some of his friends) brought me to life!'

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

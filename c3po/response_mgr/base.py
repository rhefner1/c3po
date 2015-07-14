"""Contains the definitions for the responders."""
import random

from c3po.response_mgr import text_chunks


class BaseResponseManager(object):
    """Contains responder logic to respond to messages."""

    def __init__(self):
        self.mentioned_map = {
            'created you': self.creator,
            '(hi|hello)': self.hello,
            'motivate (.+)': self.motivate,
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
    def motivate(chunks):
        """Motivates a person!"""
        name = chunks[2]
        random_motivation = random.choice(text_chunks.motiviations)
        return random_motivation % name

    @staticmethod
    def ping(_):
        """Pongs back."""
        return 'pong'

    @staticmethod
    def wolf(_):
        """Wolf... pack!"""
        return 'PACK!'

"""Contains the definitions for the responders."""
import random

from c3po.response_mgr import text_chunks


class BaseResponseManager(object):
    """Contains responder logic to respond to messages."""

    def __init__(self):
        self.mentioned_map = {
            r'created you': self.creator,
            r'(hi|hello)': self.hello,
            r'motivate (.+)': self.motivate,
            r'ping': self.ping,
            r'tell (.+?) to (.+)': self.tell_to,
            r'tell (.+?)(\s+|\s+that )(he|she) should (.+)': self.tell_should,
            r'thank( you|s)': self.thanks,
            r'wolf': self.wolf,
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
        random_motivation = random.choice(text_chunks.MOTIVATIONS)
        return random_motivation % name

    @staticmethod
    def ping(_):
        """Pongs back."""
        return 'pong'

    @staticmethod
    def tell_to(chunks):
        """Tells someone to do something."""
        name = chunks[2]
        action = chunks[3]
        return "%s, %s!" % (name, action)

    @staticmethod
    def tell_should(chunks):
        """Tells someone to do something."""
        name = chunks[2]
        action = chunks[5]
        return "%s, you should %s!" % (name, action)

    @staticmethod
    def thanks(_):
        """You're welcome!"""
        return "%s!" % random.choice(text_chunks.THANKS_RESPONSES)

    @staticmethod
    def wolf(_):
        """Wolf... pack!"""
        return 'PACK!'

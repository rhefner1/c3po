"""Contains the definitions for the responders for TrumpBot."""

import random

from c3po import text_chunks
from c3po.persona import util


class TrumpPersona(object):
    """Contains responder logic to respond to messages."""

    def __init__(self):
        self.mentioned_map = {
        }

        self.not_mentioned_map = {
            r'america': self.america,
            r'china': self.china,
            r'clark(|.+)\?': self.clark,
            r'wom(a|e)n': self.women,
        }

    @staticmethod
    @util.should_mention(False)
    def america(_msg):
        """'Murica."""
        return 'MAKE AMERICA GREAT AGAIN!'

    @staticmethod
    @util.should_mention(False)
    def china(_msg):
        """Trump on China."""
        return random.choice(text_chunks.TRUMP_CHINA)

    @staticmethod
    @util.should_mention(False)
    def clark(msg):
        """What Trump says about Clark."""

        if util.rate_limit(msg.settings, 'trump-clark', minutes=4320):
            return

        return random.choice(text_chunks.TRUMP_CLARK)

    @staticmethod
    @util.should_mention(False)
    def women(_msg):
        """What Trump says about women."""
        return "I cherish women. I want to help women. I'm going to be " \
               "able to do things for women that no other candidate would " \
               "be able to do..."



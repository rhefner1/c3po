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
            r'clark(|.+)\?': self.clark
        }

    @staticmethod
    @util.should_mention(False)
    def america(_msg):
        """'Murica."""
        return 'MAKE AMERICA GREAT AGAIN!'

    @staticmethod
    @util.should_mention(False)
    def clark(msg):
        """What Trump says about Clark."""

        if util.rate_limit(msg.settings, 'trump-clark', minutes=4320):
            return

        return random.choice(text_chunks.TRUMP_CLARK)

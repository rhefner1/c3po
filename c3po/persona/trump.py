"""Contains the definitions for the responders for TrumpBot."""

from c3po.persona import util


class TrumpPersona(object):
    """Contains responder logic to respond to messages."""

    def __init__(self):
        self.mentioned_map = {
        }

        self.not_mentioned_map = {
            r'america': self.america,
        }

    @staticmethod
    @util.should_mention(False)
    def america(_msg):
        """'Murica."""
        return 'MAKE AMERICA GREAT AGAIN!'

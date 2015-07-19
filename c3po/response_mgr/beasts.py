"""Responder specifically for for Beasts of the East."""

from c3po.response_mgr import base


class BeastsResponseManager(base.BaseResponseManager):
    """Adds specific Beasts of the East functionality to BaseResponder."""

    def __init__(self):
        super(BeastsResponseManager, self).__init__()

        self.mentioned_map.update({
        })

        self.not_mentioned_map.update({
            r'babe wait': self.babe_wait,
            r'i like to party': self.like_to_party,
        })

    @staticmethod
    def babe_wait(_msg):
        """Babe wait!."""
        return 'Babe! Wait! Babe! No!! BABE! NO! BAAAAAAAAABE!!!'

    @staticmethod
    def like_to_party(msg):
        """Babe wait!."""
        return "%s, I know for a fact you don't party. You do *not* party." \
               % msg.name

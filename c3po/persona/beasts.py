"""Responder specifically for for Beasts of the East."""

from c3po.persona import base
from c3po.persona import small_group


class BeastsPersona(small_group.SmallGroupPersona):
    """Adds specific Beasts of the East functionality to BaseResponder."""

    def __init__(self):
        super(BeastsPersona, self).__init__()

        self.mentioned_map.update({
        })

        self.not_mentioned_map.update({
            r'babe wait': self.babe_wait,
            r'cool beans': self.cool_beans,
            r'gods of war': self.gods_of_war,
            r'legit': self.legit,
            r'i like to party': self.like_to_party,
            r'safe word': self.safe_word,
        })

    @staticmethod
    def babe_wait(msg):
        """Babe wait!."""
        if base.rate_limit(msg.settings, 'babe_wait'):
            return
        return 'Babe! Wait! Babe! No!! BABE! NO! BAAAAAAAAABE!!!'

    @staticmethod
    def cool_beans(msg):
        """Cool beans."""
        if base.rate_limit(msg.settings, 'cool_beans'):
            return
        return 'Cool cool beans beans. Cool be-be-be-beans. Cool beans?'

    @staticmethod
    def gods_of_war(msg):
        """GODS OF WAR."""
        if base.rate_limit(msg.settings, 'gods_of_war'):
            return
        return 'May your hammer be mighty.'

    @staticmethod
    def legit(msg):
        """This is legit."""
        if base.rate_limit(msg.settings, 'legit'):
            return
        return "I used to be legit. I was too legit. Too legit to quit. But " \
               "now, I'm not legit."

    @staticmethod
    def like_to_party(msg):
        """No, I like to party!"""
        if base.rate_limit(msg.settings, 'like_to_party'):
            return
        return "%s, I know for a fact you don't party. You do *not* party." \
               % msg.name

    @staticmethod
    def safe_word(msg):
        """The safe word is whiskey."""
        if base.rate_limit(msg.settings, 'safe_word'):
            return
        return 'The safe word is: Whhhiskey.'

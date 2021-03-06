"""Responder specifically for for Beasts of the East."""

import random

from c3po.persona import small_group
from c3po.util import message
from c3po.util import text_chunks


class BeastsPersona(small_group.SmallGroupPersona):
    """Adds specific Beasts of the East functionality."""

    def __init__(self):
        super(BeastsPersona, self).__init__()

        self.mentioned_map.update({
        })

        self.not_mentioned_map.update({
            r'babe wait': self.babe_wait,
            r'cool beans': self.cool_beans,
            r'gods of war': self.gods_of_war,
            r'knock knock': self.knock_knock,
            r'legit': self.legit,
            r'i like to party': self.like_to_party,
            r'safe word': self.safe_word,
        })

    @staticmethod
    @message.should_mention(False)
    def babe_wait(msg):
        """Babe wait!."""
        if message.rate_limit(msg.settings, 'babe_wait'):
            return
        return 'Babe! Wait! Babe! No!! BABE! NO! BAAAAAAAAABE!!!'

    @staticmethod
    @message.should_mention(False)
    def cool_beans(msg):
        """Cool beans."""
        if message.rate_limit(msg.settings, 'cool_beans'):
            return
        return 'Cool cool beans beans. Cool be-be-be-beans. Cool beans?'

    @staticmethod
    @message.should_mention(False)
    def gods_of_war(msg):
        """GODS OF WAR."""
        if message.rate_limit(msg.settings, 'gods_of_war'):
            return
        return 'May your hammer be mighty.'

    @staticmethod
    @message.should_mention(False)
    def knock_knock(msg):
        """Knock knock jokes?"""
        if message.rate_limit(msg.settings, 'knock_knock', minutes=10):
            return
        return random.choice(text_chunks.KNOCK_KNOCK)

    @staticmethod
    @message.should_mention(False)
    def legit(msg):
        """This is legit."""
        if message.rate_limit(msg.settings, 'legit'):
            return
        return "I used to be legit. I was too legit. Too legit to quit. But " \
               "now, I'm not legit."

    @staticmethod
    @message.should_mention(False)
    def like_to_party(msg):
        """No, I like to party!"""
        if message.rate_limit(msg.settings, 'like_to_party'):
            return
        return "%s, I know for a fact you don't party. You do *not* party." \
               % msg.name

    @staticmethod
    @message.should_mention(False)
    def safe_word(msg):
        """The safe word is whiskey."""
        if message.rate_limit(msg.settings, 'safe_word'):
            return
        return 'The safe word is: Whhhiskey.'

"""Responder specifically for for Beasts of the East."""

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
    def babe_wait(_msg):
        """Babe wait!."""
        return 'Babe! Wait! Babe! No!! BABE! NO! BAAAAAAAAABE!!!'

    @staticmethod
    def cool_beans(_msg):
        """Cool beans."""
        return 'Cool cool beans beans. Cool be-be-be-beans. Cool beans?'

    @staticmethod
    def gods_of_war(_msg):
        """GODS OF WAR."""
        return 'May your hammer be mighty.'

    @staticmethod
    def legit(_msg):
        """This is legit."""
        return "I used to be legit. I was too legit. Too legit to quit. But " \
               "now, I'm not legit."

    @staticmethod
    def like_to_party(msg):
        """No, I like to party!"""
        return "%s, I know for a fact you don't party. You do *not* party." \
               % msg.name

    @staticmethod
    def safe_word(_msg):
        """The safe word is whiskey."""
        return 'The safe word is: Whhhiskey.'
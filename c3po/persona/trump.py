"""Contains the definitions for the responders for TrumpBot."""

import random

from c3po.persona import util

TRUMP_TWITTER_USERNAME = "realDonaldTrump"


class TrumpPersona(object):
    """Contains responder logic to respond to messages."""

    def __init__(self):
        self.mentioned_map = {
        }

        self.not_mentioned_map = {
            r'america': self.america,
            r'trump': self.trump,
        }

    @staticmethod
    @util.should_mention(False)
    def america(_msg):
        """'Murica."""
        return 'MAKE AMERICA GREAT AGAIN!'

    @staticmethod
    @util.should_mention(False)
    def trump(msg):
        """When you mention Trump, you get a Trump tweet."""
        api = util.get_twitter_client(msg)
        recent_tweets = api.GetUserTimeline(screen_name=TRUMP_TWITTER_USERNAME, include_rts=False)
        tweet = random.choice(recent_tweets)
        return '%s, I tweeted: "%s"' % (util.pretty_twitter_date(tweet), tweet.text)

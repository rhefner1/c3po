"""Contains the definitions for the responders common to all personas."""

import random

from c3po.util import api
from c3po.util import message
from c3po.util import text_chunks
from c3po.util import throwback as util_throwback


class BasePersona(object):
    """Contains responder logic to respond to messages."""

    def __init__(self):
        self.mentioned_map = {
            r'choose (?:between )?(.+)*': self.choose,
            r'created you': self.creator,
            r'(hi|hello)': self.hello,
            r'motivate (.+)': self.motivate,
            r'ping': self.ping,
            r'tell (.+?) to (.+)': self.tell_to,
            r'tell (.+?)(\s+|\s+that )(he|she|they) should (.+)': self.tell_should,
            r'thank( you|s)': self.thanks,
            r'throwback': self.throwback,
            r'weather': self.weather,
            r'what can you do': self.what_can_you_do,
            r'wolf': self.wolf,
        }

        self.not_mentioned_map = {
        }

    @staticmethod
    @message.should_mention(True)
    def choose(msg):
        """Given a comma-delimited list of items, choose one."""
        items = [c.strip()
                 for a in msg.text_chunks[1].split(' or ')
                 for b in a.split(' and ')
                 for c in b.split(',')
                 if c is not '']

        # Check for only one item
        if len(items) <= 1:
            return "Whoops, you only gave me one item to choose from (%s)." \
                   % items[0]

        return random.choice(text_chunks.CHOOSE) % random.choice(items)

    @staticmethod
    @message.should_mention(True)
    def creator(_msg):
        """Tells who the real creator is."""
        return 'My friend Hef (and some of his friends) brought me to life!'

    @staticmethod
    @message.should_mention(True)
    def hello(_msg):
        """Says hello!"""
        return 'Greetings. I am C-3PO, human-cyborg relations.'

    @staticmethod
    @message.should_mention(False)
    def motivate(msg):
        """Motivates a person!"""
        name = msg.text_chunks[1]
        random_motivation = random.choice(text_chunks.MOTIVATIONS)
        return random_motivation % name

    @staticmethod
    @message.should_mention(True)
    def ping(_msg):
        """Pongs back."""
        return 'pong'

    @staticmethod
    @message.should_mention(False)
    def tell_to(msg):
        """Tells someone to do something."""
        name = msg.text_chunks[1]
        action = msg.text_chunks[2]
        return "%s, %s!" % (name, action)

    @staticmethod
    @message.should_mention(False)
    def tell_should(msg):
        """Tells someone to do something."""
        name = msg.text_chunks[1]
        action = msg.text_chunks[4]
        return "%s, you should %s!" % (name, action)

    @staticmethod
    @message.should_mention(True)
    def thanks(_msg):
        """You're welcome!"""
        return "%s!" % random.choice(text_chunks.THANKS_RESPONSES)

    @staticmethod
    @message.should_mention(False)
    def throwback(msg):
        """Retrieves a random item from the transcript history and returns."""
        random_msg = util_throwback.random_message(msg)
        time_sent = random_msg.time_sent.strftime('%m/%d/%Y')

        if random_msg.picture_url:
            msg.picture_url_to_send = random_msg.picture_url
            if random_msg.text:
                return 'Throwback! On %s, %s posted this photo saying, "%s".' % (
                    time_sent, random_msg.name, random_msg.text)
            return 'Throwback! On %s, %s posted this photo.' % (
                time_sent, random_msg.name)

        return 'Throwback! On %s, %s said, "%s".' % (
            time_sent, random_msg.name, random_msg.text)

    @staticmethod
    @message.should_mention(False)
    def weather(msg):
        """Tells the current weather."""
        api_key = msg.settings.weather_conf.api_key
        latitude = msg.settings.weather_conf.latitude
        longitude = msg.settings.weather_conf.longitude

        if not api_key or not latitude or not longitude:
            raise RuntimeError('Cannot retrieve weather because'
                               'weather_conf is not set in Settings.')

        current, temp, apparent_temp, hourly = api.get_weather(api_key, latitude, longitude)

        return "It's currently %s with a temperature of %s degrees (feels " \
               "like %s). I'm predicting %s" \
               % (current, temp, apparent_temp, hourly)

    @staticmethod
    @message.should_mention(True)
    def what_can_you_do(_msg):
        """Directs users to README where they can see C-3PO capabilities."""
        return "Check out this site: " \
               "https://github.com/rhefner1/c3po/blob/master/README.md"

    @staticmethod
    @message.should_mention(False)
    def wolf(_msg):
        """Represents the best university in the world."""
        return 'PACK!'

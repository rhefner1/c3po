"""Contains the definitions for the responders."""

from datetime import datetime
from datetime import timedelta
import json
import logging
import random

from google.appengine.api import memcache
from google.appengine.api import urlfetch

from c3po import text_chunks
from c3po.db import stored_message
from c3po.persona import util

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
FORECAST_API_ENDPOINT = "https://api.forecast.io/forecast/%s/%s,%s?units=auto"


def rate_limit(settings, key, minutes=5):
    """Rate limits a function by a number of minutes."""
    memcache_key = "%s-%s" % (key, settings.key.urlsafe())

    last_use = memcache.get(memcache_key)
    if last_use:
        delta = datetime.now() - datetime.strptime(last_use, DATE_FORMAT)
        min_delta = timedelta(minutes=minutes)
        if delta < min_delta:
            logging.info("Rate Limit: not sending a response.")
            return True

    memcache.set(memcache_key, datetime.now().strftime(DATE_FORMAT))
    return False


class BasePersona(object):
    """Contains responder logic to respond to messages."""

    def __init__(self):
        self.mentioned_map = {
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
    @util.should_mention(True)
    def creator(_msg):
        """Tells who the real creator is."""
        return 'My friend Hef (and some of his friends) brought me to life!'

    @staticmethod
    @util.should_mention(True)
    def hello(_msg):
        """Says hello!"""
        return 'Greetings. I am C-3PO, human cyborg relations.'

    @staticmethod
    @util.should_mention(False)
    def motivate(msg):
        """Motivates a person!"""
        name = msg.text_chunks[1]
        random_motivation = random.choice(text_chunks.MOTIVATIONS)
        return random_motivation % name

    @staticmethod
    @util.should_mention(True)
    def ping(_msg):
        """Pongs back."""
        return 'pong'

    @staticmethod
    @util.should_mention(False)
    def tell_to(msg):
        """Tells someone to do something."""
        name = msg.text_chunks[1]
        action = msg.text_chunks[2]
        return "%s, %s!" % (name, action)

    @staticmethod
    @util.should_mention(False)
    def tell_should(msg):
        """Tells someone to do something."""
        name = msg.text_chunks[1]
        action = msg.text_chunks[4]
        return "%s, you should %s!" % (name, action)

    @staticmethod
    @util.should_mention(True)
    def thanks(_msg):
        """You're welcome!"""
        return "%s!" % random.choice(text_chunks.THANKS_RESPONSES)

    @staticmethod
    @util.should_mention(False)
    def throwback(msg):
        """Retrieves a random item from the transcript history and returns."""
        msg_query = stored_message.StoredMessage.query(
            stored_message.StoredMessage.settings == msg.settings.key)
        msg_count = msg_query.count()
        random_msg = msg_query.fetch(offset=random.randrange(0, msg_count),
                                     limit=1)[0]
        time_sent = random_msg.time_sent.strftime('%m/%d/%Y')

        return 'Throwback! On %s, %s said, "%s".' % (
            time_sent, random_msg.name, random_msg.text)

    @staticmethod
    @util.should_mention(False)
    def weather(msg):
        """Tells the current weather."""
        api_key = msg.settings.weather_conf.api_key
        latitude = msg.settings.weather_conf.latitude
        longitude = msg.settings.weather_conf.longitude

        if not api_key or not latitude or not longitude:
            raise RuntimeError('Cannot retrieve weather because'
                               'weather_conf is not set in Settings.')

        url = FORECAST_API_ENDPOINT % (api_key, latitude, longitude)
        forecast = urlfetch.fetch(url)
        forecast_json = json.loads(forecast.content)

        current = forecast_json['currently']['summary'].lower()
        temp = forecast_json['currently']['temperature']
        apparent_temp = forecast_json['currently']['apparentTemperature']
        hourly = forecast_json['hourly']['summary']
        hourly = hourly[0].lower() + hourly[1:]

        return "It's currently %s with a temperature of %s degrees (feels " \
               "like %s). I'm predicting %s" \
               % (current, temp, apparent_temp, hourly)

    @staticmethod
    @util.should_mention(True)
    def what_can_you_do(_msg):
        """Directs users to README where they can see C-3PO capabilities."""
        return "Check out this site: " \
               "https://github.com/rhefner1/c3po/blob/master/README.md"

    @staticmethod
    @util.should_mention(False)
    def wolf(_msg):
        """Represents the best university in the world."""
        return 'PACK!'

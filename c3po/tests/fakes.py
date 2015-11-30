from datetime import datetime
import mock

from google.appengine.ext import ndb

from c3po import message
from c3po.db import settings
from c3po.persona import base
from c3po.persona import beasts
from c3po.persona import eastside
from c3po.persona import small_group
from c3po.persona import sara_lane

BOT_ID = '123'
NAME = 'Billy'
PICTURE_URL = 'https://example.com/image.jpg'
TEXT = 'hi'
TIME_SENT = 1442722989
DINING_CLOSED = """
{
    "Remote":{
        "getHours":{
            "closed": "1"
        }
    }
}
"""
DINING_MENU = """
{
    "key_1":{
        "description": "Chicken",
        "type": "Entree"
    },
    "key_2":{
        "description": "Potato",
        "type": "Side"
    }
}
"""
DINING_OPEN = """
{
    "Remote":{
        "getHours":{
            "closed": "0"
        }
    }
}
"""
TRELLO_JSON = """
[
   {
      "name":"\\"Sin hub.\\""
   }
]
"""
WEATHER_JSON = """
{
   "currently":{
      "summary":"Mostly Cloudy",
      "temperature":84.25,
      "apparentTemperature":92.7
   },
   "hourly":{
      "summary":"Rain tonight and tomorrow afternoon."
   }
}
"""


class FakeMessage(message.Message):
    def __init__(self, name, picture_url, text, time_sent):
        super(FakeMessage, self).__init__(name, picture_url, text, time_sent)

        self.settings = self._get_settings(BOT_ID)
        self.persona = self.settings.get_persona()

    def _add_mention(self, response):
        # This is mocked out in tests
        return response

    def _get_settings(self, bot_id):
        # This is mocked out in tests
        return FakeBaseSettings()

    def send_message(self, response):
        # This is mocked out in tests
        pass

    def store_message(self, response_triggered):
        # Do nothing here
        pass


class FakeStoredMessage(mock.Mock):
    def __init__(self):
        super(FakeStoredMessage, self).__init__()

        self.name = NAME
        self.picture_url = PICTURE_URL
        self.response_triggered = False
        self.text = TEXT
        self.time_sent = datetime.fromtimestamp(TIME_SENT)
        self.settings = FakeBaseSettings()


class FakeNDBQuery(mock.Mock):
    def __init__(self):
        super(FakeNDBQuery, self).__init__()

    @staticmethod
    def count():
        return 5

    @staticmethod
    def fetch(**_):
        return [FakeStoredMessage()]


class FakeBaseSettings(mock.Mock):
    def __init__(self):
        super(FakeBaseSettings, self).__init__()

        self.groupme_conf = mock.Mock()
        self.groupme_conf.bot_id = BOT_ID

        self.bot_name = 'C-3PO'
        self.bot_mentioned_regex = '(c-3po|c3po)'

        self.weather_conf = mock.Mock()
        self.weather_conf.api_key = '1234'
        self.weather_conf.latitude = '35.7806'
        self.weather_conf.longitude = '-78.6389'

        self.key = ndb.Key(settings.Settings, "ABC123")

    @staticmethod
    def get_persona():
        return base.BasePersona()


class FakeSmallGroupSettings(FakeBaseSettings):
    def __init__(self):
        super(FakeSmallGroupSettings, self).__init__()

        fake_key = mock.Mock()
        fake_key.urlsafe.return_value = "1234"
        self.key = fake_key

    @staticmethod
    def get_persona():
        return small_group.SmallGroupPersona()

    @staticmethod
    def put():
        pass


class FakeBeastsSettings(FakeSmallGroupSettings):
    def __init__(self):
        super(FakeBeastsSettings, self).__init__()

    @staticmethod
    def get_persona():
        return beasts.BeastsPersona()


class FakeEastsideSettings(FakeSmallGroupSettings):
    def __init__(self):
        super(FakeEastsideSettings, self).__init__()

        self.trello_conf = mock.Mock()
        self.trello_conf.app_key = "ABC"
        self.trello_conf.token = "DEF"
        self.trello_conf.nathan_quote_board = "GHI"

    @staticmethod
    def get_persona():
        return eastside.EastsidePersona()


class FakeSaraLaneSettings(mock.Mock):
    def __init__(self):
        super(FakeSaraLaneSettings, self).__init__()
        self.groupme_conf = mock.Mock()
        self.groupme_conf.bot_id = BOT_ID

        self.bot_name = 'SaraBot'
        self.bot_mentioned_regex = 'sarabot'

    @staticmethod
    def get_persona():
        return sara_lane.SaraLanePersona()

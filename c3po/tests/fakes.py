import mock

from c3po import message
from c3po.persona import base
from c3po.persona import beasts
from c3po.persona import eastside
from c3po.persona import small_group

BOT_ID = '123'
NAME = 'Billy'
TEXT = ''
CLARK_CLOSED = """
{
    "Remote":{
        "getHours":{
            "closed": "1"
        }
    }
}
"""
CLARK_MENU = """
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
CLARK_OPEN = """
{
    "Remote":{
        "getHours":{
            "closed": "0"
        }
    }
}
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
    def __init__(self, name, text):
        super(FakeMessage, self).__init__(name, text)
        self.settings = self._get_settings(BOT_ID)
        self.persona = self.settings.get_persona()

    def _get_settings(self, bot_id):
        # This is mocked out in tests
        return FakeBaseSettings()

    def send_message(self, response):
        # This is mocked out in tests
        pass


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

    @staticmethod
    def get_persona():
        return base.BasePersona()


class FakeSmallGroupSettings(FakeBaseSettings):
    def __init__(self):
        super(FakeSmallGroupSettings, self).__init__()
        self.prayer_requests = []

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

    @staticmethod
    def get_persona():
        return eastside.EastsidePersona()

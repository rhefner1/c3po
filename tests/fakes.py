import mock

from c3po.persona import base
from c3po.persona import beasts
from c3po.persona import eastside
from c3po.persona import small_group

BOT_ID = '123'
GROUP_ID = 'abc'
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


class FakeBaseResponseMgr(mock.Mock):
    def __init__(self):
        super(FakeBaseResponseMgr, self).__init__()
        self.groupme_conf = mock.Mock()
        self.groupme_conf.bot_id = BOT_ID

        self.weather_conf = mock.Mock()
        self.weather_conf.api_key = '1234'
        self.weather_conf.latitude = '35.7806'
        self.weather_conf.longitude = '-78.6389'

    @staticmethod
    def get_persona():
        return base.BasePersona()


class FakeSmallGroupResponseMgr(FakeBaseResponseMgr):
    def __init__(self):
        super(FakeSmallGroupResponseMgr, self).__init__()
        self.prayer_requests = []

    @staticmethod
    def get_persona():
        return small_group.SmallGroupPersona()

    @staticmethod
    def put():
        pass


class FakeBeastsResponseMgr(FakeSmallGroupResponseMgr):
    def __init__(self):
        super(FakeBeastsResponseMgr, self).__init__()

    @staticmethod
    def get_persona():
        return beasts.BeastsPersona()


class FakeEastsideResponseMgr(FakeSmallGroupResponseMgr):
    def __init__(self):
        super(FakeEastsideResponseMgr, self).__init__()

    @staticmethod
    def get_persona():
        return eastside.EastsidePersona()

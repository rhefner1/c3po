"""Defines the Settings model"""

from google.appengine.ext import ndb

from c3po.db import groupme_conf  # pylint: disable=unused-import
from c3po.db import prayer_request  # pylint: disable=unused-import
from c3po.db import weather_conf  # pylint: disable=unused-import
from c3po.persona import base
from c3po.persona import beasts
from c3po.persona import eastside
from c3po.persona import small_group

PERSONA_MAP = {
    'base': base.BasePersona,
    'beasts': beasts.BeastsPersona,
    'eastside': eastside.EastsidePersona,
    'small_group': small_group.SmallGroupPersona,
}


class Settings(ndb.Model):
    """Models the mapping between group ID and bot ID."""
    provider_name = ndb.StringProperty(required=True)
    persona_name = ndb.StringProperty(required=True)

    groupme_conf = ndb.StructuredProperty(groupme_conf.GroupmeConf)
    prayer_requests = ndb.StructuredProperty(prayer_request.PrayerRequest,
                                             repeated=True)
    weather_conf = ndb.StructuredProperty(weather_conf.WeatherConf)

    def get_persona(self):
        """Maps and initializes the response manager."""
        persona_name = str(self.persona_name)
        if persona_name not in PERSONA_MAP:
            raise ValueError("'%s' is not a valid response manager."
                             % persona_name)

        persona = PERSONA_MAP[persona_name]
        return persona()

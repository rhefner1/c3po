"""Defines the Settings model"""

from google.appengine.ext import ndb

from c3po.db import groupme_conf  # pylint: disable=unused-import
from c3po.db import trello_conf  # pylint: disable=unused-import
from c3po.db import weather_conf  # pylint: disable=unused-import
from c3po.persona import base
from c3po.persona import beasts
from c3po.persona import eastside
from c3po.persona import sara_lane
from c3po.persona import small_group
from c3po.persona import trump

PERSONA_MAP = {
    'base': base.BasePersona,
    'beasts': beasts.BeastsPersona,
    'eastside': eastside.EastsidePersona,
    'saralane': sara_lane.SaraLanePersona,
    'small_group': small_group.SmallGroupPersona,
    'trump': trump.TrumpPersona
}


class Settings(ndb.Model):
    """Models the mapping between group ID and bot ID."""
    provider_name = ndb.StringProperty(required=True)
    persona_name = ndb.StringProperty(required=True)

    # Arbitrary identifier to be included in every callback URL to identify
    # which bot the callback is for. NOT associated with any particular
    # provider.
    bot_id = ndb.StringProperty(required=True)

    bot_name = ndb.StringProperty(required=True, default='C-3PO')
    bot_mentioned_regex = ndb.StringProperty(required=True,
                                             default='(c-3po|c3po)')

    # Throwback chooses a random date between this date and current date
    throwback_first_date = ndb.DateTimeProperty(auto_now_add=True)

    # Service Configuration
    groupme_conf = ndb.StructuredProperty(groupme_conf.GroupmeConf)
    trello_conf = ndb.StructuredProperty(trello_conf.TrelloConf)
    weather_conf = ndb.StructuredProperty(weather_conf.WeatherConf)

    def get_persona(self):
        """Maps and initializes the response manager."""
        persona_name = str(self.persona_name)
        if persona_name not in PERSONA_MAP:
            raise ValueError("'%s' is not a valid persona."
                             % persona_name)

        persona = PERSONA_MAP[persona_name]
        return persona()

"""Defines the Settings model"""

from google.appengine.ext import ndb

from c3po.db import groupme_conf  # pylint: disable=unused-import
from c3po.db import weather_conf  # pylint: disable=unused-import
from c3po.response_mgr import beasts

RESPONSE_MGR_MAP = {
    'beasts': beasts.BeastsResponseManager
}


class Settings(ndb.Model):
    """Models the mapping between group ID and bot ID."""
    provider_name = ndb.StringProperty(required=True)
    response_mgr_name = ndb.StringProperty(required=True)

    groupme_conf = ndb.StructuredProperty(groupme_conf.GroupmeConf)
    weather_conf = ndb.StructuredProperty(weather_conf.WeatherConf)

    def get_response_mgr(self):
        """Maps and initializes the response manager."""
        response_mgr_name = str(self.response_mgr_name)
        if response_mgr_name not in RESPONSE_MGR_MAP:
            raise ValueError("'%s' is not a valid response manager."
                             % response_mgr_name)

        response_mgr = RESPONSE_MGR_MAP[response_mgr_name]
        return response_mgr()

"""Defines the Settings model"""

from google.appengine.ext import ndb

from c3po.db import groupme_conf  # pylint: disable=unused-import
from c3po.db import prayer_request  # pylint: disable=unused-import
from c3po.db import weather_conf  # pylint: disable=unused-import
from c3po.response_mgr import base
from c3po.response_mgr import beasts
from c3po.response_mgr import eastside
from c3po.response_mgr import small_group

RESPONSE_MGR_MAP = {
    'base': base.BaseResponseManager,
    'beasts': beasts.BeastsResponseManager,
    'eastside': eastside.EastsideResponseManager,
    'small_group': small_group.SmallGroupResponseManager,
}


class Settings(ndb.Model):
    """Models the mapping between group ID and bot ID."""
    provider_name = ndb.StringProperty(required=True)
    response_mgr_name = ndb.StringProperty(required=True)

    groupme_conf = ndb.StructuredProperty(groupme_conf.GroupmeConf)
    prayer_requests = ndb.StructuredProperty(prayer_request.PrayerRequest,
                                             repeated=True)
    weather_conf = ndb.StructuredProperty(weather_conf.WeatherConf)

    def get_response_mgr(self):
        """Maps and initializes the response manager."""
        response_mgr_name = str(self.response_mgr_name)
        if response_mgr_name not in RESPONSE_MGR_MAP:
            raise ValueError("'%s' is not a valid response manager."
                             % response_mgr_name)

        response_mgr = RESPONSE_MGR_MAP[response_mgr_name]
        return response_mgr()

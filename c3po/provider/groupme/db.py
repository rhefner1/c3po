"""Defines a model to store GroupMe data."""

from google.appengine.ext import ndb


class GroupmeConf(ndb.Model):
    """Stores GroupMe configuration data."""
    group_id = ndb.StringProperty()
    bot_id = ndb.StringProperty()

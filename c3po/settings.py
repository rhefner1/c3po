"""Defines the Settings model"""

from google.appengine.ext import ndb


class Settings(ndb.Model):
    """Models the mapping between group ID and bot ID."""
    group_id = ndb.StringProperty()
    bot_id = ndb.StringProperty()

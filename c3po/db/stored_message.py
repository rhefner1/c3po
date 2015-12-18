"""Defines a model to store previously sent messages."""

from google.appengine.ext import ndb


class StoredMessage(ndb.Model):
    """Stores previously sent messages."""
    name = ndb.StringProperty()
    picture_url = ndb.StringProperty()
    response_triggered = ndb.BooleanProperty()
    text = ndb.StringProperty()
    time_sent = ndb.DateTimeProperty()
    settings = ndb.KeyProperty()
    settings_id = ndb.ComputedProperty(lambda self: self.settings.id())

"""Defines a model to store a single prayer request."""

from google.appengine.ext import ndb


class PrayerRequest(ndb.Model):
    """Stores a prayer request."""
    name = ndb.StringProperty()
    request = ndb.StringProperty()
    notices_left = ndb.IntegerProperty(default=3)

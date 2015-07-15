"""Defines a model to store GroupMe data."""

from google.appengine.ext import ndb


class WeatherConf(ndb.Model):
    """Stores GroupMe configuration data."""
    api_key = ndb.StringProperty()
    latitude = ndb.StringProperty()
    longitude = ndb.StringProperty()

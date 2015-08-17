"""Defines a model to store weather data."""

from google.appengine.ext import ndb


class WeatherConf(ndb.Model):
    """Stores weather configuration data."""
    api_key = ndb.StringProperty()
    latitude = ndb.StringProperty()
    longitude = ndb.StringProperty()

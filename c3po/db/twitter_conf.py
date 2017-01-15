"""Defines a model to store Twitter data."""

from google.appengine.ext import ndb


class TwitterConf(ndb.Model):
    """Stores Twitter configuration data."""
    consumer_key = ndb.StringProperty()
    consumer_secret = ndb.StringProperty()
    access_token_key = ndb.StringProperty()
    access_token_secret = ndb.StringProperty()

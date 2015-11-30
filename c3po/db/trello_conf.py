"""Defines a model to store Trello data."""

from google.appengine.ext import ndb


class TrelloConf(ndb.Model):
    """Stores Trello configuration data."""
    app_key = ndb.StringProperty()
    token = ndb.StringProperty()

    nathan_quote_board = ndb.StringProperty()

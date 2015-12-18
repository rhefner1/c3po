"""Defines a model to store results from analytics."""

from google.appengine.ext import ndb


class AnalyticsResults(ndb.Model):
    """Stores results from analytics."""
    most_common_words = ndb.StringProperty(repeated=True)
    word_count_link = ndb.StringProperty()

    finished = ndb.BooleanProperty(default=False)
    settings = ndb.KeyProperty()

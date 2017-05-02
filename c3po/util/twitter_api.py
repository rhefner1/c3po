"""Utility functions for Twitter API interactions"""

from datetime import datetime

import twitter

TWITTER_DATE_FORMAT = "%a %b %d %H:%M:%S +0000 %Y"


def pretty_twitter_date(tweet):
    """Converts a Twitter formatted date to a Python object."""
    py_date = datetime.strptime(tweet.created_at, TWITTER_DATE_FORMAT)
    return pretty_date(py_date)


def get_twitter_client(msg):
    """Returns a Twitter API client."""
    conf = msg.settings.twitter_conf
    return twitter.Api(consumer_key=conf.consumer_key,
                       consumer_secret=conf.consumer_secret,
                       access_token_key=conf.access_token_key,
                       access_token_secret=conf.access_token_secret)


def pretty_date(date):
    """
    Returns a natural language description of a date.
    Adapted from: https://stackoverflow.com/questions/410221
    """
    diff = datetime.utcnow() - date
    seconds = diff.seconds
    if diff.days > 7 or diff.days < 0:
        return date.strftime('%d %b %y')
    elif diff.days == 1:
        return '1 day ago'
    elif diff.days > 1:
        return '{} days ago'.format(diff.days)
    elif seconds <= 1:
        return 'just now'
    elif seconds < 60:
        return '{} seconds ago'.format(seconds)
    elif seconds < 120:
        return '1 minute ago'
    elif seconds < 3600:
        return '{} minutes ago'.format(seconds / 60)
    elif seconds < 7200:
        return '1 hour ago'
    return '{} hours ago'.format(seconds / 3600)

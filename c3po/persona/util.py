"""Utility functions for personas"""
import logging
import random
from datetime import datetime
from datetime import timedelta

import twitter

from c3po.db import stored_message
from google.appengine.api import memcache
from google.appengine.ext import ndb

ONE_DAY = timedelta(days=1)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
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
    else:
        return '{} hours ago'.format(seconds / 3600)


def random_date(start, end):
    """Returns a random date between two given dates."""
    # Courtesy of http://stackoverflow.com/questions/553303
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def random_message(msg):
    """Returns a random StoredMessage from the datastore."""
    memcache_key = "throwback-%s" % msg.settings.key.urlsafe()
    msg_urlsafe = memcache.get(memcache_key)
    if msg_urlsafe:
        memcache.delete(memcache_key)
        return ndb.Key(urlsafe=msg_urlsafe).get()

    # Get a random target date
    random_target_date = random_date(
        msg.settings.throwback_first_date + ONE_DAY,
        datetime.utcnow() - ONE_DAY
    )

    # Run the query finding the first message near the random date
    msg_query = stored_message.StoredMessage.query(
        ndb.AND(
            stored_message.StoredMessage.settings == msg.settings.key,
            stored_message.StoredMessage.time_sent <= random_target_date,
            stored_message.StoredMessage.response_triggered == False  # pylint: disable=singleton-comparison
        )
    ).order(-stored_message.StoredMessage.time_sent)

    return msg_query.fetch(limit=1)[0]


def rate_limit(settings, key, minutes=5):
    """Rate limits a function by a number of minutes."""
    memcache_key = "%s-%s" % (key, settings.key.urlsafe())

    last_use = memcache.get(memcache_key)
    if last_use:
        delta = datetime.now() - datetime.strptime(last_use, DATE_FORMAT)
        min_delta = timedelta(minutes=minutes)
        if delta < min_delta:
            logging.info("Rate Limit: not sending a response.")
            return True

    memcache.set(memcache_key, datetime.now().strftime(DATE_FORMAT))
    return False


def should_mention(should_add_mention):
    """Decorator to add a should_mention return value to contents."""

    def dec(func):
        """Returning the function object."""

        def wrapper(*args, **kwargs):
            """Returning the function value and the should_add_mention var."""
            return func(*args, **kwargs), should_add_mention

        return wrapper

    return dec

"""Utility functions for personas"""

import logging
from datetime import datetime
from datetime import timedelta

from google.appengine.api import memcache

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


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

"""Utility functions for throwbacks"""

import random
from datetime import datetime
from datetime import timedelta

from c3po.db import stored_message
from google.appengine.api import memcache
from google.appengine.ext import ndb

ONE_DAY = timedelta(days=1)


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

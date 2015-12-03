"""Utility functions for personas"""
from datetime import datetime
from datetime import timedelta
import random
from google.appengine.ext import ndb
from c3po.db import stored_message

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
    # Get a random target date
    random_target_date = random_date(msg.settings.throwback_first_date,
                                     datetime.utcnow() - ONE_DAY)

    # Run the query finding the first message near the random date
    msg_query = stored_message.StoredMessage.query(
        ndb.AND(
            stored_message.StoredMessage.settings == msg.settings.key,
            stored_message.StoredMessage.time_sent >= random_target_date
        )
    )

    return msg_query.fetch(limit=1)[0]


def should_mention(should_add_mention):
    """Decorator to add a should_mention return value to contents."""

    def dec(func):
        """Returning the function object."""

        def wrapper(*args, **kwargs):
            """Returning the function value and the should_add_mention var."""
            return func(*args, **kwargs), should_add_mention

        return wrapper

    return dec

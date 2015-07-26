"""Responder specifically for small groups."""

import random

from c3po.db import prayer_request
from c3po.response_mgr import base
from c3po import text_chunks


class SmallGroupResponseManager(base.BaseResponseManager):
    """Adds specific small group functionality to BaseResponder."""

    def __init__(self):
        super(SmallGroupResponseManager, self).__init__()

        self.mentioned_map.update({
            r'gather prayer': self.gather_prayer_requests,
        })

        self.not_mentioned_map.update({
            r'(^)pr (.+)': self.add_prayer_request,
        })

    @staticmethod
    def add_prayer_request(msg):
        """Stores a new prayer request in the database."""
        new_request = prayer_request.PrayerRequest(
            name=msg.name, request=msg.text_chunks[2])
        msg.settings.prayer_requests.append(new_request)
        msg.settings.put()

        return random.choice(text_chunks.ACKNOWLEDGEMENTS)

    @staticmethod
    def gather_prayer_requests(_msg):
        """Sends a note telling people how to submit prayer requests."""
        return "OK everybody. Send a short summary of your request with 'PR' " \
               "at the beginning and then whatever you'd like me to " \
               "remember. You can send multiple and you can do this at any " \
               "time during the week."

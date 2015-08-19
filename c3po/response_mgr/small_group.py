"""Responder specifically for small groups."""

from datetime import datetime
import json
import random

from google.appengine.api import urlfetch
import pytz

from c3po.db import prayer_request
from c3po.response_mgr import base
from c3po import text_chunks

CLARK_OPEN = 8
CLARK_BREAKFAST_END = 11
CLARK_LUNCH_END = 16
CLARK_CLOSE = 21

NCSU_DINING_API = \
    'http://www.ncsudining.com/diningapi/?method=%s&location=%s&format=json'


def get_clark_menu_items(current_meal):
    """Uses the NCSU Dining API to get the current menu at Clark."""
    url = NCSU_DINING_API % ('getMenu', 'clark')
    clark_menu_json = urlfetch.fetch(url)
    clark_menu = json.loads(clark_menu_json.content)
    return clark_menu['Remote']['getMenu']['meals'][current_meal]


def get_current_meal():
    """Gets the current meal based on the time of day."""
    current_time = datetime.now(pytz.timezone('US/Eastern'))

    if current_time.hour < CLARK_BREAKFAST_END:
        return 'breakfast'
    elif current_time.hour < CLARK_LUNCH_END:
        return 'lunch'
    else:
        return 'dinner'


def is_clark_closed():
    """Based on time and the Dining API, determine if Clark is closed."""
    current_time = datetime.now(pytz.timezone('US/Eastern'))

    if current_time.hour < CLARK_OPEN or current_time.hour > CLARK_CLOSE:
        return True

    url = NCSU_DINING_API % ('getHours', 'clark')
    clark_hours_json = urlfetch.fetch(url)
    clark_hours = json.loads(clark_hours_json.content)
    if clark_hours['Remote']['getHours']['closed'] == '1':
        return True

    return False


class SmallGroupResponseManager(base.BaseResponseManager):
    """Adds specific small group functionality to BaseResponder."""

    def __init__(self):
        super(SmallGroupResponseManager, self).__init__()

        self.mentioned_map.update({
            r'gather prayer': self.gather_prayer_requests,
        })

        self.not_mentioned_map.update({
            r'(^)pr (.+)': self.add_prayer_request,
            r'clark\?': self.clark,
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
    def clark(_msg):
        """Clark it up."""
        if is_clark_closed():
            return "Uh oh! Clark is closed right now."

        current_meal = get_current_meal()
        try:
            all_menu_items = get_clark_menu_items(current_meal)
        except KeyError:
            return 'ClarkAlert: Drats, the Clark menu is unavailable.'

        # Filter down some of the options
        entrees = [item['description'] for _, item in all_menu_items.items()
                   if item['type'] == 'Entree'
                   if 'pizza' not in item['description'].lower()]

        return "ClarkAlert for %s: %s." \
               % (current_meal, ', '.join(entrees))

    @staticmethod
    def gather_prayer_requests(_msg):
        """Sends a note telling people how to submit prayer requests."""
        return "OK everybody. Send a short summary of your request with 'PR' " \
               "at the beginning and then whatever you'd like me to " \
               "remember. You can send multiple and you can do this at any " \
               "time during the week."

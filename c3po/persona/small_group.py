"""Responder specifically for small groups."""

from datetime import datetime
import json

from google.appengine.api import urlfetch
import pytz

from c3po.persona import base
from c3po.persona import util

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


class SmallGroupPersona(base.BasePersona):
    """Adds specific small group functionality."""

    def __init__(self):
        super(SmallGroupPersona, self).__init__()

        self.mentioned_map.update({
        })

        self.not_mentioned_map.update({
            r'clark(|.+)\?': self.clark,
        })

    @staticmethod
    @util.should_mention(False)
    def clark(msg):
        """Clark it up."""
        if base.rate_limit(msg.settings, 'clark', minutes=60):
            return

        if is_clark_closed():
            return "Uh oh! Clark is closed right now."

        current_meal = get_current_meal()
        all_menu_items = get_clark_menu_items(current_meal)

        # Filter down some of the options
        entrees = [item['description'] for _, item in all_menu_items.items()
                   if item['type'] == 'Entree'
                   if 'pizza' not in item['description'].lower()]

        return "ClarkAlert for %s: %s." \
               % (current_meal, ', '.join(entrees))

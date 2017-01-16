"""Responder specifically for small groups."""

from datetime import datetime

import pytz

from c3po.persona import base
from c3po.util import api
from c3po.util import message
from c3po.util import variables


def get_current_meal():
    """Gets the current meal based on the time of day."""
    current_time = datetime.now(pytz.timezone('US/Eastern'))

    if current_time.hour < variables.CLARK_BREAKFAST_END:
        return 'breakfast'
    elif current_time.hour < variables.CLARK_LUNCH_END:
        return 'lunch'
    else:
        return 'dinner'


def handle_bible_lookup(msg, version):
    """Handles looking up a Bible passage in a specific version"""
    # Determining what kind of verse we have
    book, chapter, verse1, verse2 = parse_passage(msg.text_chunks)

    # If verse2 is greater than verse1, ignore request
    if int(verse2) < int(verse1):
        return

    # Fetching the verse contents
    passage_text = api.get_bible_passage(msg.settings.bible_api_key, version, book, chapter,
                                         verse1, verse2)

    # Limiting the response length to a constant
    if len(passage_text) > variables.BIBLE_RSP_LENGTH:
        verses_content = passage_text[:variables.BIBLE_RSP_LENGTH]
        verses_content += ' [...]'

    return passage_text


def is_dining_closed(dining_hall):
    """Based on time and the Dining API, determine if Clark is closed."""
    current_time = datetime.now(pytz.timezone('US/Eastern'))

    if dining_hall == 'clark':
        if current_time.hour < variables.CLARK_OPEN or current_time.hour > variables.CLARK_CLOSE:
            return True

    elif dining_hall == 'case':
        if current_time.hour < variables.CASE_OPEN or current_time.hour > variables.CASE_LUNCH_END:
            return True

    else:
        raise ValueError("Dining hall not supported.")

    hours = api.get_dining_hours(dining_hall)
    if hours['closed'] == '1':
        return True

    return False


def parse_passage(text_chunks):
    """Given raw input, return parsed passage."""
    book = text_chunks[1].lower()
    chapter = text_chunks[2]
    verse1 = text_chunks[3]
    verse2 = text_chunks[4] if text_chunks[4] else verse1

    return book, chapter, verse1, verse2


class SmallGroupPersona(base.BasePersona):
    """Adds specific small group functionality."""

    def __init__(self):
        super(SmallGroupPersona, self).__init__()

        self.mentioned_map.update({
        })

        self.not_mentioned_map.update({
            r'hawaiian %s' % variables.REGEX_BIBLE: self.hawaiian_bible,
            variables.REGEX_BIBLE: self.bible,
            r'case(|.+)\?': self.case,
            r'clark(|.+)\?': self.clark,
        })

    @staticmethod
    @message.should_mention(False)
    def hawaiian_bible(msg):
        """If a Bible reference is detected, return it in HWCNT."""
        return handle_bible_lookup(msg, variables.BIBLE_HWCNT)

    @staticmethod
    @message.should_mention(False)
    def bible(msg):
        """If a Bible reference is detected, return it in ESV."""
        return handle_bible_lookup(msg, variables.BIBLE_ESV)

    @staticmethod
    @message.should_mention(False)
    def case(msg):
        """Case it up."""
        if message.rate_limit(msg.settings, 'case', minutes=60):
            return

        if is_dining_closed('case'):
            return "Uh oh! Case is closed right now."

        current_meal = get_current_meal()
        all_menu_items = api.get_dining_menu('case', current_meal)

        # Filter down some of the options
        entrees = [item['description'] for _, item in all_menu_items.items()
                   if item['type'] not in ['Soup', 'Side']
                   if 'pizza' not in item['description'].lower()]

        return "CaseAlert for %s: %s." \
               % (current_meal, ', '.join(entrees))

    @staticmethod
    @message.should_mention(False)
    def clark(msg):
        """Clark it up."""
        if message.rate_limit(msg.settings, 'clark', minutes=60):
            return

        if is_dining_closed('clark'):
            return "Uh oh! Clark is closed right now."

        current_meal = get_current_meal()
        all_menu_items = api.get_dining_menu('clark', current_meal)

        # Filter down some of the options
        entrees = [item['description'] for _, item in all_menu_items.items()
                   if item['type'] not in ['Soup', 'Side']
                   if 'pizza' not in item['description'].lower()]

        return "ClarkAlert for %s: %s." \
               % (current_meal, ', '.join(entrees))

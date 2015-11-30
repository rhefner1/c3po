"""Responder specifically for small groups."""

from datetime import datetime
import json
import urllib
import pytz
from bs4 import BeautifulSoup
from google.appengine.api import urlfetch
from c3po.persona import base
from c3po.persona import util

BIBLE_API = "http://www.esvapi.org/v2/rest/verse?key=IP&passage=%s&include-" \
            "footnotes=false&include-passage-references=false&include-verse-" \
            "numbers=false"
BIBLE_RSP_LENGTH = 750

CLARK_OPEN = 8
CLARK_BREAKFAST_END = 11
CLARK_LUNCH_END = 16
CLARK_CLOSE = 21

CASE_OPEN = 8
CASE_BREAKFAST_END = 11
CASE_LUNCH_END = 16

NCSU_DINING_API = \
    'http://www.ncsudining.com/diningapi/?method=%s&location=%s&format=json'

# Regex matching 1 John 2:2-4:
#  -. any preceding characters
#  -. case insensitivity flag
#  1. a book of the Bible
#  -. whitespace character
#  2. chapter number
#  -. : character
#  3. verse number
#  -. (optional) - character to signify multiple verses
#  4. (optional) second verse number
REGEX_BIBLE = r'(?:.)*(?i)' \
              r'(genesis|exodus|leviticus|numbers|deuteronomy|joshua|' \
              r'judges|ruth|1 samuel|2 samuel|1 kings|2 kings|1 chronicles|' \
              r'2 chronicles|ezra|nehemiah|esther|job|psalms|proverbs|' \
              r'ecclesiastes|song of solomon|isaiah|jeremiah|lamentations|' \
              r'ezekiel|daniel|hosea|joel|amos|obadiah|jonah|micah|nahum|' \
              r'habakkuk|zephaniah|haggai|zechariah|malachi|matthew|mark|' \
              r'luke|john|acts|romans|1 corinthians|2 corinthians|galatians|' \
              r'ephesians|philippians|colossians|1 thessalonians|' \
              r'2 thessalonians|1 timothy|2 timothy|titus|philemon|hebrews|' \
              r'james|1 peter|2 peter|1 john|2 john|3 john|jude|revelation)' \
              r'(?:\s)(\d+)(?::)?(\d+)(?:-)?(\d+)?'


def get_menu_items(dining_hall, current_meal):
    """Uses the NCSU Dining API to get the current menu at Clark."""
    url = NCSU_DINING_API % ('getMenu', dining_hall)
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


def is_dining_closed(dining_hall):
    """Based on time and the Dining API, determine if Clark is closed."""
    current_time = datetime.now(pytz.timezone('US/Eastern'))

    if dining_hall == 'clark':
        if current_time.hour < CLARK_OPEN or current_time.hour > CLARK_CLOSE:
            return True

    elif dining_hall == 'case':
        if current_time.hour < CASE_OPEN or current_time.hour > CASE_LUNCH_END:
            return True

    else:
        raise ValueError("Dining hall not supported.")

    url = NCSU_DINING_API % ('getHours', dining_hall)
    hours_json = urlfetch.fetch(url)
    hours = json.loads(hours_json.content)
    if hours['Remote']['getHours']['closed'] == '1':
        return True

    return False


class SmallGroupPersona(base.BasePersona):
    """Adds specific small group functionality."""

    def __init__(self):
        super(SmallGroupPersona, self).__init__()

        self.mentioned_map.update({
        })

        self.not_mentioned_map.update({
            REGEX_BIBLE: self.bible,
            r'case(|.+)\?': self.case,
            r'clark(|.+)\?': self.clark,
        })

    @staticmethod
    @util.should_mention(False)
    def bible(msg):
        """If a Bible ref is detected, look it up."""
        # Determining what kind of verse we have
        verse = "%s %s:%s" % (msg.text_chunks[1].title(),
                              msg.text_chunks[2],
                              msg.text_chunks[3])

        # Checking if there is a second verse number
        if msg.text_chunks[4]:
            # Making sure the second number is greater than the first
            if int(msg.text_chunks[4]) <= int(msg.text_chunks[3]):
                return
            verse += "-%s" % msg.text_chunks[4]

        # Fetching the verse contents
        verse_html = urlfetch.fetch(BIBLE_API % urllib.quote_plus(verse))

        # Parsing the verse
        soup = BeautifulSoup(verse_html.content, 'html.parser')

        # Removing the span that contains a redundant chapter number
        for tag in soup.findAll('span', {'class': 'chapter-num'}):
            tag.replaceWith('')

        # Extracting verse text
        all_verses = [p.get_text() for p in soup.find_all('p')]
        verses_content = " ".join(all_verses)
        verses_content = verses_content.encode('ascii', 'ignore')

        # Stripping out extra newlines
        verses_content = verses_content.replace('\n', ' ')

        # And limiting the response length to a constant
        if len(verses_content) > BIBLE_RSP_LENGTH:
            verses_content = verses_content[:BIBLE_RSP_LENGTH]
            verses_content += ' [...]'

        return "%s | %s" % (verse, verses_content)

    @staticmethod
    @util.should_mention(False)
    def case(msg):
        """Case it up."""
        if util.rate_limit(msg.settings, 'case', minutes=60):
            return

        if is_dining_closed('case'):
            return "Uh oh! Case is closed right now."

        current_meal = get_current_meal()
        all_menu_items = get_menu_items('case', current_meal)

        # Filter down some of the options
        entrees = [item['description'] for _, item in all_menu_items.items()
                   if item['type'] == 'Entree'
                   if 'pizza' not in item['description'].lower()]

        return "CaseAlert for %s: %s." \
               % (current_meal, ', '.join(entrees))

    @staticmethod
    @util.should_mention(False)
    def clark(msg):
        """Clark it up."""
        if util.rate_limit(msg.settings, 'clark', minutes=60):
            return

        if is_dining_closed('clark'):
            return "Uh oh! Clark is closed right now."

        current_meal = get_current_meal()
        all_menu_items = get_menu_items('clark', current_meal)

        # Filter down some of the options
        entrees = [item['description'] for _, item in all_menu_items.items()
                   if item['type'] == 'Entree'
                   if 'pizza' not in item['description'].lower()]

        return "ClarkAlert for %s: %s." \
               % (current_meal, ', '.join(entrees))

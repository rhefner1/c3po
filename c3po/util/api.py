"""Contains communication logic for all APIs"""

import base64
import json
import urllib
from HTMLParser import HTMLParser

from bs4 import BeautifulSoup

from c3po.util import variables
from google.appengine.api import urlfetch


class MLStripper(HTMLParser):
    """
    Strips markup from a string.
    Taken from https://stackoverflow.com/questions/753052
    """

    def __init__(self):
        HTMLParser.__init__(self)
        self.reset()
        self.fed = []

    def handle_data(self, d):
        """Handles data."""
        self.fed.append(d)

    def get_data(self):
        """Gets data."""
        return ''.join(self.fed)


def clean_bible_text(html):
    """Strips HTML tags from Bible API output."""
    # Stripping unnecessary HTML tags
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup.findAll('h3'):
        tag.replaceWith('')
    for tag in soup.findAll('sup'):
        tag.replaceWith('')

    # Getting verse content
    all_verses = [p.get_text() for p in soup.find_all('p')]
    verses_content = " ".join(all_verses)
    verses_content = verses_content.encode('ascii', 'ignore')

    stripper = MLStripper()
    stripper.feed(verses_content)
    return stripper.get_data()


def get_bible_passage(api_key, version, book, chapter, verse1, verse2):
    """Get a passage from bibles.org API."""
    book_abbr = variables.BIBLE_BOOK_ABBR[book]
    url = variables.BIBLE_ENDPIONT % (version, book_abbr, chapter, verse1, verse2)
    passage_json = urlfetch.fetch(url, headers={
        "Authorization": "Basic %s" % base64.b64encode("%s:X" % api_key)
    })
    verses = json.loads(passage_json.content)['response']['verses']
    passage_text = []
    for verse in verses:
        passage_text.append(verse['text'])

    reference = "%s %s:%s" % (book.title(), chapter, verse1)
    if verse2 != verse1:
        reference += '-%s' % verse2
    stripped_text = clean_bible_text(' '.join(passage_text))
    stripped_version = version.split('-')[1]

    return "%s | %s  (%s)" % (reference, stripped_text, stripped_version)


def get_dining_menu(dining_hall, current_meal):
    """Get the current menu at a dining hall."""
    url = variables.NCSU_DINING_ENDPOINT % ('getMenu', dining_hall)
    clark_menu_json = urlfetch.fetch(url)
    clark_menu = json.loads(clark_menu_json.content)
    return clark_menu['Remote']['getMenu']['meals'][current_meal]


def get_dining_hours(dining_hall):
    """Get current hours of a dining hall"""
    url = variables.NCSU_DINING_ENDPOINT % ('getHours', dining_hall)
    hours_json = urlfetch.fetch(url)
    return json.loads(hours_json.content)['Remote']['getHours']


def get_trello_cards(key, token, board_id):
    """Gets Trello cards from a given board."""
    auth_data = urllib.urlencode(dict(key=key, token=token))
    url = variables.TRELLO_CARD_ENDPOINT % (board_id, auth_data)
    cards_json = urlfetch.fetch(url=url)
    return json.loads(cards_json.content)


def get_weather(api_key, latitude, longitude):
    """Retrieves current get_weather from Forecast.io"""
    url = variables.WEATHER_ENDPOINT % (api_key, latitude, longitude)
    forecast = urlfetch.fetch(url)
    forecast_json = json.loads(forecast.content)

    current = forecast_json['currently']['summary'].lower()
    temp = forecast_json['currently']['temperature']
    apparent_temp = forecast_json['currently']['apparentTemperature']
    hourly = forecast_json['hourly']['summary']
    hourly = hourly[0].lower() + hourly[1:]

    return current, temp, apparent_temp, hourly

"""Responder specifically for for Best Eastside Study."""

import json
import random
import urllib

from c3po.persona import small_group
from c3po.persona import util
from google.appengine.api import urlfetch

TRELLO_CARD_ENDPOINT = 'https://trello.com/1/boards/%s/cards?%s'


def get_trello_cards(key, token, board_id):
    """Gets Trello cards from a given board."""
    auth_data = urllib.urlencode(dict(key=key, token=token))
    url = TRELLO_CARD_ENDPOINT % (board_id, auth_data)
    cards_json = urlfetch.fetch(url=url)
    return json.loads(cards_json.content)


class EastsidePersona(small_group.SmallGroupPersona):
    """Adds specific Best Eastside Study functionality."""

    def __init__(self):
        super(EastsidePersona, self).__init__()

        self.mentioned_map.update({
            r'nathan quote': self.nathan_quote,
        })

        self.not_mentioned_map.update({
        })

    @staticmethod
    @util.should_mention(False)
    def nathan_quote(msg):
        """Returns a quote from a specific Trello board."""
        trello_key = msg.settings.trello_conf.app_key
        trello_token = msg.settings.trello_conf.token
        nathan_board = msg.settings.trello_conf.nathan_quote_board
        if not trello_key or not trello_token or not nathan_board:
            raise ValueError("No Trello credentials found. Can't continue.")

        # Getting Nathan quotes
        all_cards = get_trello_cards(trello_key, trello_token, nathan_board)
        rand_card = random.randrange(0, len(all_cards))

        return "Here's a Nathan quote: %s" % all_cards[rand_card]['name']

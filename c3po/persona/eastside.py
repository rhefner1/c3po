"""Responder specifically for for Best Eastside Study."""

import random

from c3po.persona import small_group
from c3po.util import api
from c3po.util import message


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
    @message.should_mention(False)
    def nathan_quote(msg):
        """Returns a quote from a specific Trello board."""
        key = msg.settings.trello_conf.app_key
        token = msg.settings.trello_conf.token
        board_id = msg.settings.trello_conf.nathan_quote_board

        if not key or not token or not board_id:
            raise ValueError("No Trello credentials found. Can't continue.")

        # Getting Nathan quotes
        all_cards = api.get_trello_cards(key, token, board_id)
        rand_card = random.randrange(0, len(all_cards))

        return "Here's a Nathan quote: %s" % all_cards[rand_card]['name']

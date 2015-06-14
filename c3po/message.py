import logging
import re

from c3po import responders
from settings import Settings

MENTIONED_MAP = {
    "(hi|hello)": responders.hello
}

NOT_MENTIONED_MAP = {

}

REGEX_MENTIONED = '(C-3PO|c3po)'
REGEX_PRE = '(\s+)'
REGEX_POST = '($|\s+|\?+|\.+|\!+)'


class Message:
    """Holds the message contents, processes it and sends a response."""

    def __init__(self, group_id, name, text):
        self.group_id = group_id
        self.name = name
        self.text = text

    @staticmethod
    def _generate_regex(regex):
        return "%s%s%s" % (REGEX_PRE, regex, REGEX_POST)

    def _get_bot_id(self):
        results = Settings.query(Settings.group_id == self.group_id)
        if results.count() == 0:
            raise ValueError("No Settings objects found matching group_id: %s. Cannot continue." % self.group_id)
        elif results.count() > 1:
            raise RuntimeError("Found multiple Settings objects with group_id: %s. Cannot continue." % self.group_id)

        return results.fetch(1)[0]

    def process_message(self):
        # Check for matches where C-3PO is mentioned
        if re.search(REGEX_MENTIONED, self.text):
            self._find_responder(MENTIONED_MAP)

        else:
            # Now checking for the rest of the cases
            self._find_responder(NOT_MENTIONED_MAP)

    def _find_responder(self, responder_map):
        for regex, responder in responder_map.iteritems():
            if re.search(self._generate_regex(regex), self.text):
                logging.info("Responder selected: %s" % str(responder))
                response = responder(self)
                self._send_response(response)

    def _send_response(self, response):
        logging.info("Sending this response: %s" % response)

        bot_id = self._get_bot_id()
        logging.info("Sending to bot_id: %s" % bot_id)
        return

"""Contains the data model for a Message and the actions to process it."""

import abc
import logging
import re

# Regex matching either:
#   1) beginning of string
#   2) one or many whitespace chars
REGEX_PRE = r'(^|\s+)'

# Regex matching either:
#   1) end of string
#   2) any whitespace
#   3) a '?' character
#   4) a '.' character
#   5) a '!' character
REGEX_POST = r'($|\s+|\?+|\.+|\!+)'


class Message(object):
    """Abstract class. Used to hold the message contents, process it and send a
    response. Overridden and extended by a provider to get provider-specific
    send logic."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, name, text):
        self.name = name
        self.persona = None
        self.settings = None
        self.text = text
        self.text_chunks = None

    @abc.abstractmethod
    def _get_settings(self, group_id):
        """Finds the Settings object associated with group_id."""
        return

    def _get_responder(self, responder_map):
        """Returns the responder that is registered for the given text."""
        for regex, responder in responder_map.iteritems():
            full_regex = self._generate_regex(regex)
            if re.search(full_regex, self.text.lower()):
                logging.info("Responder selected: %s", str(responder))
                return regex, responder

        return None, None

    @staticmethod
    def _generate_regex(regex):
        """Generates the regex needed to find the correct responder."""
        return r"%s%s%s" % (REGEX_PRE, regex, REGEX_POST)

    def process_message(self):
        """Finds the responder and uses it to send a response."""
        regex, responder = None, None
        if re.search(self.settings.bot_mentioned_regex, self.text.lower()):
            # Check for matches where C-3PO is mentioned
            regex, responder = self._get_responder(
                self.persona.mentioned_map)

        if not responder:
            # Now checking for the rest of the cases
            regex, responder = self._get_responder(
                self.persona.not_mentioned_map)

        if not regex or not responder:
            logging.info("No responder found for text: '%s'", self.text)
            return

        self.text_chunks = re.split(regex, self.text)
        response = responder(self)
        if response:
            self.send_message(response)

    @abc.abstractmethod
    def send_message(self, response):
        """Sends the given response to the API."""
        return

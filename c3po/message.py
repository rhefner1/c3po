"""Contains the data model for a Message and the actions to process it."""

import abc
from datetime import datetime
import logging
import re

from c3po.db import stored_message

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

    def __init__(self, name, text, time_sent):
        self.name = name
        self.persona = None
        self.settings = None
        self.text = text
        self.text_chunks = None
        self.time_sent = time_sent

    @abc.abstractmethod
    def _add_mention(self, response):
        """When responding back to a person, mention them."""
        return

    @abc.abstractmethod
    def _get_settings(self, bot_id):
        """Finds the Settings object associated with bot_id."""
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

            # Store the message contents
            self.store_message(False)
            return

        self.text_chunks = re.split(regex, self.text)
        response = responder(self)
        if response:
            response = self._add_mention(response)
            self.send_message(response)

        # Store the message contents
        self.store_message(True)

    @abc.abstractmethod
    def send_message(self, response):
        """Sends the given response to the API."""
        return

    def store_message(self, response_triggered):
        """Stores message data in database."""
        new_sm = stored_message.StoredMessage(name=self.name,
                                              response_triggered=response_triggered,
                                              text=self.text,
                                              time_sent=datetime.fromtimestamp(self.time_sent),
                                              settings=self.settings.key)
        new_sm.put()

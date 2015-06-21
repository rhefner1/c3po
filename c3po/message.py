"""Contains the data model for a Message and the actions to process it."""

import logging
import re
import urllib

from google.appengine.api import urlfetch

from c3po import responders
from c3po import settings

GROUPME_API_ENDPOINT = 'https://api.groupme.com'
GROUPME_API_HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
GROUPME_API_PATH = '/v3/bots/post'

MENTIONED_MAP = {
    '(hi|hello)': responders.hello
}

NOT_MENTIONED_MAP = {

}

REGEX_MENTIONED = r'(C-3PO|c3po)'
REGEX_PRE = r'(\s+)'
REGEX_POST = r'($|\s+|\?+|\.+|\!+)'


class Message(object):
    """Holds the message contents, processes it and sends a response."""

    def __init__(self, group_id, name, text):
        self.group_id = group_id
        self.name = name
        self.text = text

    def _generate_api_post_body(self, response):
        """Generates the request body to be sent"""
        bot_id = self._get_bot_id()
        logging.info("Sending to bot_id: %s", bot_id)

        body = {
            'bot_id': bot_id,
            'text': response
        }

        return urllib.urlencode(body)

    @staticmethod
    def _generate_regex(regex):
        """Generates the regex needed to find the correct responder."""
        return "%s%s%s" % (REGEX_PRE, regex, REGEX_POST)

    def _get_bot_id(self):
        """Returns the bot_id corresponding to the given group_id."""
        results = settings.Settings.query(settings.Settings.group_id ==
                                          self.group_id)
        if results.count() == 0:
            raise ValueError(
                "No Settings objects found matching group_id: %s. Cannot"
                "continue." % self.group_id)
        elif results.count() > 1:
            raise RuntimeError(
                "Found multiple Settings objects with group_id: %s. Cannot"
                "continue." % self.group_id)

        return results.fetch(1)[0].bot_id

    def process_message(self):
        """Finds the responder and uses it to send a response."""
        # Check for matches where C-3PO is mentioned
        if re.search(REGEX_MENTIONED, self.text):
            responder = self._find_responder(MENTIONED_MAP)

        else:
            # Now checking for the rest of the cases
            responder = self._find_responder(NOT_MENTIONED_MAP)

        response = responder(self)
        self._send_response(response)

    def _find_responder(self, responder_map):
        """Returns the first responder that is registered for the given
        incoming text."""
        for regex, responder in responder_map.iteritems():
            if re.search(self._generate_regex(regex), self.text):
                logging.info("Responder selected: %s", str(responder))
                return responder

    def _send_response(self, response):
        """Sends the given response to the API."""
        logging.info("Sending this response: %s", response)

        post_body = self._generate_api_post_body(response)
        result = urlfetch.fetch(url=GROUPME_API_ENDPOINT + GROUPME_API_PATH,
                                payload=post_body,
                                method=urlfetch.POST,
                                headers=GROUPME_API_HEADERS)

        if result.status_code != 202:
            logging.debug(
                "GroupMe API was called with body: %s", str(post_body))
            logging.debug("GroupMe API call content: %s", result.content)
            raise RuntimeError(
                "GroupMe API call returned status: %s. Log has more details." %
                str(result.status_code))
        else:
            logging.info('GroupMe API call returned successfully.')

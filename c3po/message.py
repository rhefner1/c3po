"""Contains the data model for a Message and the actions to process it."""

import logging
import re
import urllib

from google.appengine.api import urlfetch

from c3po import settings

GROUPME_API_ENDPOINT = 'https://api.groupme.com'
GROUPME_API_HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
GROUPME_API_PATH = '/v3/bots/post'
GROUPME_API_FULL = "%s%s" % (GROUPME_API_ENDPOINT, GROUPME_API_PATH)

REGEX_MENTIONED = r'(C-3PO|c3po)'
REGEX_PRE = r'(\s+)'
REGEX_POST = r'($|\s+|\?+|\.+|\!+)'


class Message(object):
    """Abstract class. Used to hold the message contents, process it and send a
    response. Overridden and extended by a provider to get provider-specific
    send logic."""

    def __init__(self, group_id, name, text):
        msg_settings = self._get_settings(group_id)

        self.bot_id = msg_settings.bot_id
        self.name = name
        self.response_mgr = msg_settings.get_response_mgr()
        self.text = text

    @staticmethod
    def _get_settings(group_id):
        """Finds the Settings object associated with group_id."""
        results = settings.Settings.query(
            settings.Settings.group_id == group_id)

        if results.count() <= 0:
            raise ValueError(
                "No Settings objects found matching group_id: %s. "
                "Cannot continue." % group_id)
        elif results.count() > 1:
            raise RuntimeError(
                "Found multiple Settings objects with group_id: %s. "
                "Cannot continue." % group_id)

        return results.fetch(1)[0]

    def _get_responder(self, responder_map):
        """Returns the responder that is registered for the given text."""
        for regex, responder in responder_map.iteritems():
            if re.search(self._generate_regex(regex), self.text):
                logging.info("Responder selected: %s", str(responder))
                return responder

        return None

    def _generate_api_post_body(self, response):
        """Generates the request body to be sent"""
        body = {
            'bot_id': self.bot_id,
            'text': response
        }

        return urllib.urlencode(body)

    @staticmethod
    def _generate_regex(regex):
        """Generates the regex needed to find the correct responder."""
        return r"%s%s%s" % (REGEX_PRE, regex, REGEX_POST)

    def process_message(self):
        """Finds the responder and uses it to send a response."""
        responder = None
        if re.search(REGEX_MENTIONED, self.text):
            # Check for matches where C-3PO is mentioned
            responder = self._get_responder(
                self.response_mgr.mentioned_map)

        if not responder:
            # Now checking for the rest of the cases
            responder = self._get_responder(
                self.response_mgr.not_mentioned_map)

        if not responder:
            logging.info("No responder found for text: '%s'", self.text)
            return

        response = responder(self.text)
        self._send_response(response)

    def _send_response(self, response):
        """Sends the given response to the API."""
        logging.info("Sending this response: '%s' to bot_id: '%s'",
                     response, self.bot_id)

        post_body = self._generate_api_post_body(response)
        result = urlfetch.fetch(url=GROUPME_API_FULL,
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

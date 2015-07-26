"""Handles message sending for GroupMe provider."""

import logging
import urllib

from google.appengine.api import urlfetch

from c3po import message
from c3po.db import settings

GROUPME_API_ENDPOINT = 'https://api.groupme.com'
GROUPME_API_HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
GROUPME_API_PATH = '/v3/bots/post'
GROUPME_API_FULL = "%s%s" % (GROUPME_API_ENDPOINT, GROUPME_API_PATH)


class GroupmeMessage(message.Message):
    """Implements Message for the GroupMe provider."""

    def __init__(self, group_id, name, text):
        super(GroupmeMessage, self).__init__(name, text)

        self.settings = self._get_settings(group_id)
        self.bot_id = self.settings.groupme_conf.bot_id
        self.response_mgr = self.settings.get_response_mgr()

    def _get_settings(self, group_id):
        """Finds the Settings object associated with group_id."""
        results = settings.Settings.query(
            settings.Settings.groupme_conf.group_id == group_id)

        if results.count() <= 0:
            raise ValueError(
                "No Settings objects found matching group_id: %s. "
                "Cannot continue." % group_id)
        elif results.count() > 1:
            raise RuntimeError(
                "Found multiple Settings objects with group_id: %s. "
                "Cannot continue." % group_id)

        msg_settings = results.fetch(1)[0]
        self._validate_settings(msg_settings)
        return msg_settings

    def _generate_api_post_body(self, response):
        """Generates the request body to be sent"""
        body = {
            'bot_id': self.bot_id,
            'text': response
        }

        return urllib.urlencode(body)

    def send_message(self, response):
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

    @staticmethod
    def _validate_settings(msg_settings):
        """Validates that the Settings object contains all GroupMe params."""
        required_fields = [
            msg_settings.provider_name,
            msg_settings.response_mgr_name,
            msg_settings.groupme_conf.group_id,
            msg_settings.groupme_conf.bot_id
        ]
        for field in required_fields:
            if not field:
                raise ValueError(
                    "Settings ID '%s' doesn't have required fields."
                    % str(msg_settings.key.id()))

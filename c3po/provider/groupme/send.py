"""Handles message sending for GroupMe provider."""

import logging
import json
import time

from google.appengine.api import urlfetch

from c3po import message
from c3po.db import settings

GROUPME_API_ENDPOINT = 'https://api.groupme.com'
GROUPME_API_PATH = '/v3/bots/post'
GROUPME_API_FULL = "%s%s" % (GROUPME_API_ENDPOINT, GROUPME_API_PATH)

TARGET_SEND_TIME = .4


class GroupmeMessage(message.Message):
    """Implements Message for the GroupMe provider."""

    def __init__(self, start_time, bot_id, name, picture_url, text, time_sent):
        # pylint: disable=too-many-arguments
        super(GroupmeMessage, self).__init__(name, picture_url, text, time_sent)

        self.settings = self._get_settings(bot_id)
        self.groupme_bot_id = self.settings.groupme_conf.bot_id
        self.name = name
        self.persona = self.settings.get_persona()
        self.start_time = start_time

    def _add_mention(self, response):
        """When responding back to a person, mention them."""
        if self.name:
            return "@%s: %s" % (self.name, response)

    def _get_settings(self, bot_id):
        """Finds the Settings object associated with group_id."""
        results = settings.Settings.query(
            settings.Settings.bot_id == bot_id)

        if results.count() <= 0:
            raise ValueError(
                "No Settings objects found matching bot_id: %s. "
                "Cannot continue." % bot_id)
        elif results.count() > 1:
            raise RuntimeError(
                "Found multiple Settings objects with bot_id: %s. "
                "Cannot continue." % bot_id)

        msg_settings = results.fetch(1)[0]
        self._validate_settings(msg_settings)
        return msg_settings

    def _generate_api_post_body(self, response):
        """Generates the request body to be sent"""
        body = {
            'bot_id': self.groupme_bot_id,
            'text': response
        }

        if self.picture_url_to_send:
            body['attachments'] = [
                dict(type='image', url=self.picture_url_to_send)
            ]

        return json.dumps(body)

    def send_message(self, response):
        """Sends the given response to the API."""
        logging.info("Sending this response: '%s' to bot_id: '%s'",
                     response, self.groupme_bot_id)

        elapsed_time = time.time() - self.start_time
        if elapsed_time < TARGET_SEND_TIME:
            time.sleep(TARGET_SEND_TIME - elapsed_time)

        logging.info("WOMBAT elapsed: %s, now: %s", elapsed_time, time.time() - self.start_time)

        post_body = self._generate_api_post_body(response)
        result = urlfetch.fetch(url=GROUPME_API_FULL,
                                payload=post_body,
                                method=urlfetch.POST)

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
            msg_settings.persona_name,
            msg_settings.groupme_conf.group_id,
            msg_settings.groupme_conf.bot_id
        ]
        for field in required_fields:
            if not field:
                raise ValueError(
                    "Settings ID '%s' doesn't have required fields."
                    % str(msg_settings.key.id()))

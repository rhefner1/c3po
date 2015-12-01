"""Handles cron job HTTP handlers."""

import flask
from c3po.provider.groupme import send as groupme_send

APP = flask.Flask(__name__)
APP.config['DEBUG'] = True

SUCCESS = ('', 200)

TEXT_LIMIT = 30


def create_message(settings_obj):
    """Creates a fake message object in which you can call .send_message()."""
    if settings_obj.provider_name == 'groupme':
        return groupme_send.GroupmeMessage(None, settings_obj.bot_id, None,
                                           None, None, None)

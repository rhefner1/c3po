"""Handles message receiving for GroupMe provider."""

import logging
import json
import time

import flask

from c3po.provider.groupme import send

APP = flask.Flask(__name__)
APP.config['DEBUG'] = True

SUCCESS = ('', 200)


@APP.route('/groupme/<bot_id>', methods=['POST'])
def receive_message(bot_id):
    """Processes a message and returns a response."""
    time.sleep(.1)

    msg_data = json.loads(flask.request.data)
    time_sent = float(msg_data['created_at'])
    group_id = msg_data['group_id']
    name = msg_data['name']
    text = msg_data['text']

    if not bot_id or not group_id or not name or not text:
        flask.abort(400)

    logging.info("Group ID: %s", group_id)
    logging.info("Name: %s", name)
    logging.info("Text: %s", text)

    msg = send.GroupmeMessage(bot_id, name, text, time_sent)

    if name == msg.settings.bot_name:
        logging.info("Ignoring request since it's coming from the bot.")
        return SUCCESS

    msg.process_message()

    return SUCCESS

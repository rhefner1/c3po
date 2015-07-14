"""Handles message receiving for GroupMe provider."""

import logging
import json
import time

import flask

from c3po.provider.groupme import send

APP = flask.Flask(__name__)
APP.config['DEBUG'] = True

SUCCESS = ('', 200)


@APP.route('/groupme', methods=['POST'])
def receive_message():
    """Processes a message and returns a response."""
    time.sleep(.1)

    msg_data = json.loads(flask.request.data)
    group_id = msg_data['group_id']
    name = msg_data['name']
    text = msg_data['text']

    if not group_id or not name or not text:
        flask.abort(400)

    logging.info("Group ID: %s", group_id)
    logging.info("Name: %s", name)
    logging.info("Text: %s", text)

    if name == 'C-3PO':
        logging.info("Ignoring request since it's coming from the bot.")
        return SUCCESS

    msg = send.GroupmeMessage(group_id, name, text)

    try:
        msg.process_message()
    except ValueError as error:
        logging.debug("Failed processing message because: %s", error.message)
        flask.abort(500)

    return SUCCESS

"""Handles the web routing for incoming API calls"""

import logging

import flask

from c3po import message

APP = flask.Flask(__name__)
APP.config['DEBUG'] = True

SUCCESS = ('', 200)


@APP.route('/', methods=['POST'])
def handle_message():
    """Processes a message and returns a response."""
    group_id = flask.request.form['group_id']
    name = flask.request.form['name']
    text = flask.request.form['text']

    if not group_id or not name or not text:
        flask.abort(400)

    logging.info("Group ID: %s", group_id)
    logging.info("Name: %s", name)
    logging.info("Text: %s", text)

    msg = message.Message(group_id, name, text)

    try:
        msg.process_message()
    except ValueError as error:
        logging.debug("Failed processing message because: %s", error.message)
        flask.abort(500)

    return SUCCESS


@APP.route('/ping')
def ping():
    """Sample web handler to see if the server is alive."""
    return 'pong'


@APP.errorhandler(404)
def page_not_found(error):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL. Error msg: %s' % error, 404

"""Handles the HTTP routing for the history upload endpoint."""

from datetime import datetime
import flask
import logging

from google.appengine.ext import ndb

from c3po.db import settings
from c3po.db import stored_message


APP = flask.Flask(__name__)
APP.config['DEBUG'] = True

SUCCESS = ('', 200)


@APP.route('/storedata', methods=['POST'])
def receive_message():
    """Processes a message and returns a response."""

    msg_data = flask.request.get_json(silent=True, force=True)

    name = msg_data['name']
    picture_url = msg_data['picture_url']
    text = msg_data['text']
    time_sent = msg_data['time_sent']
    settings_key = ndb.Key(settings.Settings, msg_data['settings'])

    logging.info("Recording entry {name: %s, text: %s, time_sent: %d}",
                 name, text, time_sent)

    new_sm = stored_message.StoredMessage(name=name,
                                          picture_url=picture_url,
                                          response_triggered=False,
                                          text=text,
                                          time_sent=datetime.fromtimestamp(
                                              time_sent),
                                          settings=settings_key)
    new_sm.put()

    return SUCCESS

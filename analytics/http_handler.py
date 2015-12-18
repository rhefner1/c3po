"""Handles the HTTP routing."""

import flask

from analytics import analysis_engine
from c3po.db.settings import Settings
from c3po.provider.groupme.send import GroupmeMessage

APP = flask.Flask(__name__)
APP.config['DEBUG'] = True

SUCCESS = ('', 200)


@APP.route('/analyticsctl/start')
def start():
    """Kicks off the analysis runner."""
    settings_id = int(flask.request.form.get('settings_id'))
    settings = Settings.get_by_id(settings_id)
    analysis_engine.start_analysis(settings)
    return SUCCESS


@APP.route('/analyticsctl/done')
def done():
    """Informs group that analysis is done."""
    # msg = GroupmeMessage(None, settings.bot_id, None, None, None, None)
    # msg.send_message("Here's the link to my analysis: %s")
    return SUCCESS


@APP.errorhandler(404)
def page_not_found(error):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL. Error msg: %s' % error, 404

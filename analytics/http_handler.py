"""Handles the HTTP routing."""

import flask

APP = flask.Flask(__name__)
APP.config['DEBUG'] = True

SUCCESS = ('', 200)


@APP.route('/analytics/hi')
def ping():
    """Sample web handler to see if the server is alive."""
    return 'hello'


@APP.errorhandler(404)
def page_not_found(error):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL. Error msg: %s' % error, 404

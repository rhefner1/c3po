"""Handles the HTTP routing."""

import flask

APP = flask.Flask(__name__)
APP.config['DEBUG'] = True

SUCCESS = ('', 200)


@APP.route('/analytics/<settings_key>')
def analytics(settings_key):
    """Analytics."""
    return flask.render_template('index.html', name='Beasts of the East')


@APP.errorhandler(404)
def page_not_found(error):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL. Error msg: %s' % error, 404

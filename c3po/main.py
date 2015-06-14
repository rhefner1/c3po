from flask import abort, Flask, request
import logging

from c3po.message import Message

SUCCESS = ("", 200)

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/', methods=['POST'])
def message():
    """Processes a message and returns a response."""
    group_id = request.form['group_id']
    name = request.form['name']
    text = request.form['text']

    if not group_id or not name or not text:
        abort(400)

    logging.info("Group ID: %s" % group_id)
    logging.info("Name: %s" % name)
    logging.info("Text: %s" % text)

    msg = Message(group_id, name, text)

    try:
        msg.process_message()
    except ValueError:
        abort(400)

    return SUCCESS


@app.route('/test')
def test():
    """Says hello!"""
    return "Hello!"


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

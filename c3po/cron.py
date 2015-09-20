"""Handles cron job HTTP handlers."""

import flask

from c3po.db import settings
from c3po.provider.groupme import send as groupme_send

APP = flask.Flask(__name__)
APP.config['DEBUG'] = True

SUCCESS = ('', 200)

TEXT_LIMIT = 30


def create_message(settings_obj):
    """Creates a message object to use for sending."""
    if settings_obj.provider_name == 'groupme':
        return groupme_send.GroupmeMessage(settings_obj.bot_id,
                                           None, None, None)


@APP.route('/cron/prayer')
def prayer():
    """Sends out prayer request reminders."""
    all_settings = settings.Settings.query()

    for settings_obj in all_settings:
        if settings_obj.prayer_requests:
            prayer_reminder = "PrayerAlert: remember to pray for: "

            # Need to store all requests here. Doing a `for pr in
            # s.prayer_requests` gets messed up when removing items.
            all_prayer_requests = [p for p in settings_obj.prayer_requests]

            for request in all_prayer_requests:
                prayer_reminder += "[%s] %s, " % (request.name,
                                                  request.request[:TEXT_LIMIT])
                if request.notices_left <= 1:
                    settings_obj.prayer_requests.remove(request)
                else:
                    request.notices_left -= 1

            msg = create_message(settings_obj)
            msg.send_message(prayer_reminder)

            settings_obj.put()

    return SUCCESS

import json
import unittest

import freezegun
import mock

from c3po.provider.groupme import send
from tests import fakes
from c3po.persona import small_group


class TestClarkGetCurrentMeal(unittest.TestCase):
    @freezegun.freeze_time('2015-01-01 10:00:00', tz_offset=+5)
    def test_breakfast(self):
        expected = 'breakfast'
        self.assertEqual(small_group.get_current_meal(), expected)

    @freezegun.freeze_time('2015-01-01 13:00:00', tz_offset=+5)
    def test_lunch(self):
        expected = 'lunch'
        self.assertEqual(small_group.get_current_meal(), expected)

    @freezegun.freeze_time('2015-01-01 19:00:00', tz_offset=+5)
    def test_dinner(self):
        expected = 'dinner'
        self.assertEqual(small_group.get_current_meal(), expected)


class TestClarkClosed(unittest.TestCase):
    @freezegun.freeze_time('2015-01-01 06:00:00', tz_offset=+5)
    def test_closed_early(self):
        expected = True
        self.assertEqual(small_group.is_clark_closed(), expected)

    @freezegun.freeze_time('2015-01-01 23:00:00', tz_offset=+5)
    def test_closed_late(self):
        expected = True
        self.assertEqual(small_group.is_clark_closed(), expected)

    @mock.patch('google.appengine.api.urlfetch.fetch')
    @freezegun.freeze_time('2015-01-01 12:00:00', tz_offset=+5)
    def test_closed_all_day(self, fake_fetch):
        fake_api_return = mock.Mock()
        fake_api_return.content = fakes.CLARK_CLOSED
        fake_fetch.return_value = fake_api_return

        expected = True
        self.assertEqual(small_group.is_clark_closed(), expected)

    @mock.patch('google.appengine.api.urlfetch.fetch')
    @freezegun.freeze_time('2015-01-01 12:00:00', tz_offset=+5)
    def test_open(self, fake_fetch):
        fake_api_return = mock.Mock()
        fake_api_return.content = fakes.CLARK_OPEN
        fake_fetch.return_value = fake_api_return

        expected = False
        self.assertEqual(small_group.is_clark_closed(), expected)


class TestSmallGroupResponders(unittest.TestCase):
    def setUp(self):
        send_patcher = mock.patch(
            'c3po.provider.groupme.send.GroupmeMessage.send_message')
        self.addCleanup(send_patcher.stop)
        self.mock_send = send_patcher.start()

        settings_patcher = mock.patch(
            'c3po.provider.groupme.send.GroupmeMessage._get_settings')
        self.addCleanup(settings_patcher.stop)
        self.mock_settings = settings_patcher.start()
        self.mock_settings.return_value = fakes.FakeSmallGroupResponseMgr()

        self.msg = send.GroupmeMessage(fakes.GROUP_ID, fakes.NAME, '')

    @mock.patch('random.choice')
    def test_add_prayer_request(self, mock_random):
        mock_random.return_value = "Got it."

        self.msg.text = 'pr for my test tomorrow'
        self.msg.process_message()

        self.mock_send.assert_called_with('Got it.')

    @mock.patch('c3po.persona.base.rate_limit')
    @mock.patch('c3po.persona.small_group.get_clark_menu_items')
    @mock.patch('c3po.persona.small_group.get_current_meal')
    @mock.patch('c3po.persona.small_group.is_clark_closed')
    def test_clark(self, fake_clark_closed, fake_current_meal, fake_clark_menu,
                   fake_rate_limit):
        fake_clark_closed.return_value = False
        fake_current_meal.return_value = 'dinner'
        fake_clark_menu.return_value = json.loads(fakes.CLARK_MENU)
        fake_rate_limit.return_value = False

        self.msg.text = 'clark anyone?'
        self.msg.process_message()

        response = "ClarkAlert for dinner: Chicken."
        self.mock_send.assert_called_with(response)

    def test_gather_prayer_requests(self):
        self.msg.text = 'c3po gather prayer requests'
        self.msg.process_message()

        response = \
            "OK everybody. Send a short summary of your request with 'PR' " \
            "at the beginning and then whatever you'd like me to " \
            "remember. You can send multiple and you can do this at any " \
            "time during the week."
        self.mock_send.assert_called_with(response)

    def test_negative(self):
        self.msg.text = 'this is only a test'
        self.msg.process_message()

        self.assertFalse(self.mock_send.called)


if __name__ == '__main__':
    unittest.main()

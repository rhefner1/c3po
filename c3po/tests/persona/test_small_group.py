import json
import unittest
import freezegun
import mock
from c3po.tests import fakes
from c3po.persona import small_group


class TestDiningGetCurrentMeal(unittest.TestCase):
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


class TestDiningClosed(unittest.TestCase):
    @freezegun.freeze_time('2015-01-01 06:00:00', tz_offset=+5)
    def test_closed_early(self):
        expected = True
        self.assertEqual(small_group.is_dining_closed('clark'), expected)

    @freezegun.freeze_time('2015-01-01 23:00:00', tz_offset=+5)
    def test_closed_late(self):
        expected = True
        self.assertEqual(small_group.is_dining_closed('clark'), expected)

    @mock.patch('google.appengine.api.urlfetch.fetch')
    @freezegun.freeze_time('2015-01-01 12:00:00', tz_offset=+5)
    def test_closed_all_day(self, fake_fetch):
        fake_api_return = mock.Mock()
        fake_api_return.content = fakes.DINING_CLOSED
        fake_fetch.return_value = fake_api_return

        expected = True
        self.assertEqual(small_group.is_dining_closed('clark'), expected)

    @mock.patch('google.appengine.api.urlfetch.fetch')
    @freezegun.freeze_time('2015-01-01 12:00:00', tz_offset=+5)
    def test_open(self, fake_fetch):
        fake_api_return = mock.Mock()
        fake_api_return.content = fakes.DINING_OPEN
        fake_fetch.return_value = fake_api_return

        expected = False
        self.assertEqual(small_group.is_dining_closed('clark'), expected)


class TestSmallGroupResponders(unittest.TestCase):
    def setUp(self):
        send_patcher = mock.patch(
            'c3po.tests.fakes.FakeMessage.send_message')
        self.addCleanup(send_patcher.stop)
        self.mock_send = send_patcher.start()

        settings_patcher = mock.patch(
            'c3po.tests.fakes.FakeMessage._get_settings')
        self.addCleanup(settings_patcher.stop)
        self.mock_settings = settings_patcher.start()
        self.mock_settings.return_value = fakes.FakeSmallGroupSettings()

        self.msg = fakes.FakeMessage(fakes.NAME, None, '', fakes.TIME_SENT)

    @mock.patch('c3po.persona.util.rate_limit')
    @mock.patch('c3po.persona.small_group.get_menu_items')
    @mock.patch('c3po.persona.small_group.get_current_meal')
    @mock.patch('c3po.persona.small_group.is_dining_closed')
    def test_case(self, fake_dining_closed, fake_current_meal, fake_dining_menu,
                  fake_rate_limit):
        fake_dining_closed.return_value = False
        fake_current_meal.return_value = 'dinner'
        fake_dining_menu.return_value = json.loads(fakes.DINING_MENU)
        fake_rate_limit.return_value = False

        self.msg.text = 'case anyone?'
        self.msg.process_message()

        response = "CaseAlert for dinner: Chicken."
        self.mock_send.assert_called_with(response)

    @mock.patch('c3po.persona.util.rate_limit')
    @mock.patch('c3po.persona.small_group.get_menu_items')
    @mock.patch('c3po.persona.small_group.get_current_meal')
    @mock.patch('c3po.persona.small_group.is_dining_closed')
    def test_clark(self, fake_dining_closed, fake_current_meal,
                   fake_dining_menu,
                   fake_rate_limit):
        fake_dining_closed.return_value = False
        fake_current_meal.return_value = 'dinner'
        fake_dining_menu.return_value = json.loads(fakes.DINING_MENU)
        fake_rate_limit.return_value = False

        self.msg.text = 'clark anyone?'
        self.msg.process_message()

        response = "ClarkAlert for dinner: Chicken."
        self.mock_send.assert_called_with(response)

    def test_negative(self):
        self.msg.text = 'this is only a test'
        self.msg.process_message()

        self.assertFalse(self.mock_send.called)


if __name__ == '__main__':
    unittest.main()

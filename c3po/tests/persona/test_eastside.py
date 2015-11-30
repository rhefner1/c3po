import unittest

import mock

from c3po.tests import fakes


class TestEastsideResponders(unittest.TestCase):
    def setUp(self):
        send_patcher = mock.patch(
            'c3po.tests.fakes.FakeMessage.send_message')
        self.addCleanup(send_patcher.stop)
        self.mock_send = send_patcher.start()

        settings_patcher = mock.patch(
            'c3po.tests.fakes.FakeMessage._get_settings')
        self.addCleanup(settings_patcher.stop)
        self.mock_settings = settings_patcher.start()
        self.mock_settings.return_value = fakes.FakeEastsideSettings()

        self.msg = fakes.FakeMessage(fakes.NAME, None, '', fakes.TIME_SENT)

    @mock.patch('google.appengine.api.urlfetch.fetch')
    def test_nathan_quote(self, mock_fetch):
        mock_cards = mock.Mock()
        mock_cards.content = fakes.TRELLO_JSON
        mock_fetch.return_value = mock_cards

        self.msg.text = 'c3po nathan quote'
        self.msg.process_message()

        self.mock_send.assert_called_with("Here's a Nathan quote: \"Sin hub.\"")

    def test_negative(self):
        self.msg.text = 'this is only a test'
        self.msg.process_message()

        self.assertFalse(self.mock_send.called)


if __name__ == '__main__':
    unittest.main()

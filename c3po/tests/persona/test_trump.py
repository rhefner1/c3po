import unittest

import mock

from c3po.tests import fakes


class TestTrumpResponders(unittest.TestCase):
    def setUp(self):
        send_patcher = mock.patch(
            'c3po.tests.fakes.FakeMessage.send_message')
        self.addCleanup(send_patcher.stop)
        self.mock_send = send_patcher.start()

        settings_patcher = mock.patch(
            'c3po.tests.fakes.FakeMessage._get_settings')
        self.addCleanup(settings_patcher.stop)
        self.mock_settings = settings_patcher.start()
        self.mock_settings.return_value = fakes.FakeTrumpSettings()

        self.msg = fakes.FakeMessage(fakes.NAME, None, '', fakes.TIME_SENT)

    @mock.patch('c3po.util.twitter_api.pretty_twitter_date')
    @mock.patch('c3po.util.twitter_api.get_twitter_client')
    def test_trump(self, fake_twitter, fake_date):
        fake_twitter.return_value = fakes.FakeTwitter()
        fake_date.return_value = "1 hour ago"

        self.msg.text = 'trump'
        self.msg.process_message()

        self.mock_send.assert_called_with(
            '1 hour ago, I tweeted: "I am Donald Trump."')


if __name__ == '__main__':
    unittest.main()

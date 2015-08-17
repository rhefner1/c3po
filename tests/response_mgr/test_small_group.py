import unittest

import mock

from c3po.provider.groupme import send
from tests import fakes


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

    def test_gather_prayer_requests(self):
        self.msg.text = 'c3po gather prayer requests'
        self.msg.process_message()

        response = \
            "OK everybody. Send a short summary of your request with 'PR' " \
            "at the beginning and then whatever you'd like me to " \
            "remember. You can send multiple and you can do this at any " \
            "time during the week."
        self.mock_send.assert_called_with(response)


if __name__ == '__main__':
    unittest.main()

import unittest

import mock

from c3po.provider.groupme import send
from tests import fakes


class TestEastsideResponders(unittest.TestCase):
    def setUp(self):
        send_patcher = mock.patch(
            'c3po.provider.groupme.send.GroupmeMessage.send_message')
        self.addCleanup(send_patcher.stop)
        self.mock_send = send_patcher.start()

        settings_patcher = mock.patch(
            'c3po.provider.groupme.send.GroupmeMessage._get_settings')
        self.addCleanup(settings_patcher.stop)
        self.mock_settings = settings_patcher.start()
        self.mock_settings.return_value = fakes.FakeEastsideResponseMgr()

        self.msg = send.GroupmeMessage(fakes.GROUP_ID, fakes.NAME, '')

    def test_negative(self):
        self.msg.text = 'this is only a test'
        self.msg.process_message()

        self.assertFalse(self.mock_send.called)


if __name__ == '__main__':
    unittest.main()

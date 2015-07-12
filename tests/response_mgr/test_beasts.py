import unittest

import mock

from c3po.message import Message
from tests import fakes


class TestBeastsResponders(unittest.TestCase):
    def setUp(self):
        send_patcher = mock.patch('c3po.message.Message._send_response')
        self.addCleanup(send_patcher.stop)
        self.mock_send = send_patcher.start()

        settings_patcher = mock.patch('c3po.message.Message._get_settings')
        self.addCleanup(settings_patcher.stop)
        self.mock_settings = settings_patcher.start()
        self.mock_settings.return_value = fakes.FakeBeastsResponseMgr()

        self.msg = Message(fakes.GROUP_ID, fakes.NAME, '')


if __name__ == '__main__':
    unittest.main()

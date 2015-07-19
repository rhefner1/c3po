import unittest

import mock

from c3po.provider.groupme import send
from tests import fakes


class TestBeastsResponders(unittest.TestCase):
    def setUp(self):
        send_patcher = mock.patch(
            'c3po.provider.groupme.send.GroupmeMessage._send_message')
        self.addCleanup(send_patcher.stop)
        self.mock_send = send_patcher.start()

        settings_patcher = mock.patch(
            'c3po.provider.groupme.send.GroupmeMessage._get_settings')
        self.addCleanup(settings_patcher.stop)
        self.mock_settings = settings_patcher.start()
        self.mock_settings.return_value = fakes.FakeBeastsResponseMgr()

        self.msg = send.GroupmeMessage(fakes.GROUP_ID, fakes.NAME, '')

    def test_babe_wait(self):
        self.msg.text = 'babe wait'
        self.msg.process_message()

        self.mock_send.assert_called_with('Babe! Wait! Babe! No!! BABE! NO! '
                                          'BAAAAAAAAABE!!!')


if __name__ == '__main__':
    unittest.main()

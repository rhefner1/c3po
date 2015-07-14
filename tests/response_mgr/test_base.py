import unittest

import mock

from c3po.provider.groupme import send
from tests import fakes


class TestBaseResponders(unittest.TestCase):
    def setUp(self):
        send_patcher = mock.patch(
            'c3po.provider.groupme.send.GroupmeMessage._send_message')
        self.addCleanup(send_patcher.stop)
        self.mock_send = send_patcher.start()

        settings_patcher = mock.patch(
            'c3po.provider.groupme.send.GroupmeMessage._get_settings')
        self.addCleanup(settings_patcher.stop)
        self.mock_settings = settings_patcher.start()
        self.mock_settings.return_value = fakes.FakeBaseResponseMgr()

        self.msg = send.GroupmeMessage(fakes.GROUP_ID, fakes.NAME, '')

    def test_creator(self):
        self.msg.text = 'c3po who created you?'
        self.msg.process_message()

        self.mock_send.assert_called_with(
            'My friend @Hef (and some of his friends) brought me to life!')

    def test_hello(self):
        self.msg.text = 'c3po hello'
        self.msg.process_message()

        self.mock_send.assert_called_with(
            'Greetings. I am C-3PO, human cyborg relations.')

    def test_ping(self):
        self.msg.text = 'c3po ping'
        self.msg.process_message()

        self.mock_send.assert_called_with('pong')


if __name__ == '__main__':
    unittest.main()

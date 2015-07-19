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

    @mock.patch('random.choice')
    def test_motivate(self, mock_random):
        mock_random.return_value = "You're awesome, %s!"

        self.msg.text = 'c3po motivate Henry'
        self.msg.process_message()

        self.mock_send.assert_called_with(
            "You're awesome, Henry!")

    def test_ping(self):
        self.msg.text = 'c3po ping'
        self.msg.process_message()

        self.mock_send.assert_called_with('pong')

    def test_tell_to(self):
        self.msg.text = 'c3po tell Joey to pick up the trash'
        self.msg.process_message()

        self.mock_send.assert_called_with('Joey, pick up the trash!')

    def test_tell_should(self):
        self.msg.text = 'c3po tell Joey that he should behave'
        self.msg.process_message()

        self.mock_send.assert_called_with('Joey, you should behave!')

    @mock.patch('random.choice')
    def test_thanks(self, mock_random):
        mock_random.return_value = "You're welcome"

        self.msg.text = 'c3po thanks!'
        self.msg.process_message()

        self.mock_send.assert_called_with(
            "You're welcome!")

    def test_wolf(self):
        self.msg.text = 'c3po wolf'
        self.msg.process_message()

        self.mock_send.assert_called_with('PACK!')


if __name__ == '__main__':
    unittest.main()

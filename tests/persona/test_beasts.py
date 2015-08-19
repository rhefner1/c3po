import unittest

import mock

from c3po.provider.groupme import send
from tests import fakes


class TestBeastsResponders(unittest.TestCase):
    def setUp(self):
        send_patcher = mock.patch(
            'c3po.provider.groupme.send.GroupmeMessage.send_message')
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

    def test_cool_beans(self):
        self.msg.text = "that's cool beans dude"
        self.msg.process_message()

        self.mock_send.assert_called_with('Cool cool beans beans. Cool '
                                          'be-be-be-beans. Cool beans?')

    def test_gods_of_war(self):
        self.msg.text = 'gods of war'
        self.msg.process_message()

        self.mock_send.assert_called_with('May your hammer be mighty.')

    def test_legit(self):
        self.msg.text = "that's legit"
        self.msg.process_message()

        self.mock_send.assert_called_with("I used to be legit. I was too "
                                          "legit. Too legit to quit. But now, "
                                          "I'm not legit.")

    def test_like_to_party(self):
        self.msg.text = 'i like to party'
        self.msg.process_message()

        self.mock_send.assert_called_with("Billy, I know for a fact you don't "
                                          "party. You do *not* party.")

    def test_negative(self):
        self.msg.text = 'this is only a test'
        self.msg.process_message()

        self.assertFalse(self.mock_send.called)

    def test_safe_word(self):
        self.msg.text = 'safe word'
        self.msg.process_message()

        self.mock_send.assert_called_with('The safe word is: Whhhiskey.')


if __name__ == '__main__':
    unittest.main()

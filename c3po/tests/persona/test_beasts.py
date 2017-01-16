import unittest

import mock

from c3po.tests import fakes


class TestBeastsResponders(unittest.TestCase):
    def setUp(self):
        send_patcher = mock.patch(
            'c3po.tests.fakes.FakeMessage.send_message')
        self.addCleanup(send_patcher.stop)
        self.mock_send = send_patcher.start()

        settings_patcher = mock.patch(
            'c3po.tests.fakes.FakeMessage._get_settings')
        self.addCleanup(settings_patcher.stop)
        self.mock_settings = settings_patcher.start()
        self.mock_settings.return_value = fakes.FakeBeastsSettings()

        self.msg = fakes.FakeMessage(fakes.NAME, None, '', fakes.TIME_SENT)

    @mock.patch('c3po.util.message.rate_limit')
    def test_babe_wait(self, mock_rate):
        mock_rate.return_value = False

        self.msg.text = 'babe wait'
        self.msg.process_message()

        self.mock_send.assert_called_with('Babe! Wait! Babe! No!! BABE! NO! '
                                          'BAAAAAAAAABE!!!')

    @mock.patch('c3po.util.message.rate_limit')
    def test_cool_beans(self, mock_rate):
        mock_rate.return_value = False

        self.msg.text = "that's cool beans dude"
        self.msg.process_message()

        self.mock_send.assert_called_with('Cool cool beans beans. Cool '
                                          'be-be-be-beans. Cool beans?')

    @mock.patch('c3po.util.message.rate_limit')
    def test_gods_of_war(self, mock_rate):
        mock_rate.return_value = False

        self.msg.text = 'gods of war'
        self.msg.process_message()

        self.mock_send.assert_called_with('May your hammer be mighty.')

    @mock.patch('c3po.util.message.rate_limit')
    @mock.patch('random.random')
    def test_knock_knock(self, mock_rnd, mock_rate):
        mock_rnd.return_value = 0.1
        mock_rate.return_value = False

        self.msg.text = 'knock knock'
        self.msg.process_message()

        self.mock_send.assert_called_with("Who's there?")

    @mock.patch('c3po.util.message.rate_limit')
    def test_legit(self, mock_rate):
        mock_rate.return_value = False

        self.msg.text = "that's legit"
        self.msg.process_message()

        self.mock_send.assert_called_with("I used to be legit. I was too "
                                          "legit. Too legit to quit. But now, "
                                          "I'm not legit.")

    @mock.patch('c3po.util.message.rate_limit')
    def test_like_to_party(self, mock_rate):
        mock_rate.return_value = False

        self.msg.text = 'i like to party'
        self.msg.process_message()

        self.mock_send.assert_called_with("Billy, I know for a fact you don't "
                                          "party. You do *not* party.")

    @mock.patch('c3po.util.message.rate_limit')
    def test_negative(self, mock_rate):
        mock_rate.return_value = False

        self.msg.text = 'this is only a test'
        self.msg.process_message()

        self.assertFalse(self.mock_send.called)

    @mock.patch('c3po.util.message.rate_limit')
    def test_safe_word(self, mock_rate):
        mock_rate.return_value = False

        self.msg.text = 'safe word'
        self.msg.process_message()

        self.mock_send.assert_called_with('The safe word is: Whhhiskey.')


if __name__ == '__main__':
    unittest.main()

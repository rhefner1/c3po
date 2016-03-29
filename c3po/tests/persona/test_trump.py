import unittest
import mock
from c3po import text_chunks
from c3po.tests import fakes


def _random_se(*args, **_):
    if args[0] == text_chunks.TRUMP_CLARK:
        return 'Clark is what makes America great.'


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

    def test_america(self):
        self.msg.text = 'america is bad'
        self.msg.process_message()

        self.mock_send.assert_called_with(
            'MAKE AMERICA GREAT AGAIN!')

    @mock.patch('c3po.persona.util.rate_limit')
    @mock.patch('random.choice')
    def test_clark(self, mock_random, fake_rate_limit):
        mock_random.side_effect = _random_se
        fake_rate_limit.return_value = False

        self.msg.text = 'clark?'
        self.msg.process_message()

        self.mock_send.assert_called_with(
            'Clark is what makes America great.')


if __name__ == '__main__':
    unittest.main()

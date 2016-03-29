import unittest
import mock
from c3po import text_chunks
from c3po.tests import fakes


def _random_se(*args, **_):
    if args[0] == text_chunks.TRUMP_CLARK:
        return 'Clark is what makes America great.'
    elif args[0] == text_chunks.TRUMP_MEXICO:
        return "The Mexican government forces many bad people into our " \
               "country. Because they're smart. They're smarter than our leaders."


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

    @mock.patch('random.choice')
    def test_mexico(self, mock_random):
        mock_random.side_effect = _random_se

        self.msg.text = 'mexico is cool'
        self.msg.process_message()

        self.mock_send.assert_called_with(
            "The Mexican government forces many bad people into our country. "
            "Because they're smart. They're smarter than our leaders.")

    def test_women(self):
        self.msg.text = 'I love women'
        self.msg.process_message()

        self.mock_send.assert_called_with(
            "I cherish women. I want to help women. I'm going to be "
            "able to do things for women that no other candidate would "
            "be able to do...")


if __name__ == '__main__':
    unittest.main()

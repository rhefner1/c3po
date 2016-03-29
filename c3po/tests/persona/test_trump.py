import unittest
import mock
from c3po.tests import fakes


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


if __name__ == '__main__':
    unittest.main()
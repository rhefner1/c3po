import unittest

import mock

from c3po.tests import fakes


class TestSaraLaneResponders(unittest.TestCase):
    def setUp(self):
        send_patcher = mock.patch(
            'c3po.tests.fakes.FakeMessage.send_message')
        self.addCleanup(send_patcher.stop)
        self.mock_send = send_patcher.start()

        settings_patcher = mock.patch(
            'c3po.tests.fakes.FakeMessage._get_settings')
        self.addCleanup(settings_patcher.stop)
        self.mock_settings = settings_patcher.start()
        self.mock_settings.return_value = fakes.FakeSaraLaneSettings()

        self.msg = fakes.FakeMessage(fakes.NAME, '', fakes.TIME_SENT)


if __name__ == '__main__':
    unittest.main()

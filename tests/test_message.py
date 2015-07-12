import unittest

import mock
from google.appengine.api import urlfetch

from c3po import message
from tests import fakes


class TestRegex(unittest.TestCase):
    def test_generate_regex(self):
        regex = 'hi'
        self.assertEqual(message.Message._generate_regex(regex),
                         r'(\s+)hi($|\s+|\?+|\.+|\!+)')


class TestGeneratePostBody(unittest.TestCase):
    def setUp(self):
        settings_patcher = mock.patch('c3po.message.Message._get_settings')
        self.addCleanup(settings_patcher.stop)
        self.mock_settings = settings_patcher.start()
        self.mock_settings.return_value = fakes.FakeBaseResponseMgr()

        self.msg = message.Message(fakes.GROUP_ID, fakes.NAME, fakes.TEXT)

    def test_generate_api_post_body(self):
        actual_post_body = self.msg._generate_api_post_body('sample')
        expected_post_body = 'text=sample&bot_id=123'

        self.assertEqual(actual_post_body, expected_post_body)


class TestSendResponse(unittest.TestCase):
    def setUp(self):
        settings_patcher = mock.patch('c3po.message.Message._get_settings')
        self.addCleanup(settings_patcher.stop)
        self.mock_settings = settings_patcher.start()
        self.mock_settings.return_value = fakes.FakeBaseResponseMgr()

        self.msg = message.Message(fakes.GROUP_ID, fakes.NAME, fakes.TEXT)

    @mock.patch('c3po.message.Message._generate_api_post_body')
    @mock.patch('google.appengine.api.urlfetch.fetch')
    def test_send_response(self, mock_urlfetch, mock_gen_api_post_body):
        mock_gen_api_post_body.return_value = 'text=sample&bot_id=123'
        mock_urlfetch.return_value.status_code = 202

        self.msg._send_response('sample')

        mock_urlfetch.assert_called_with(
            url=message.GROUPME_API_ENDPOINT + message.GROUPME_API_PATH,
            payload='text=sample&bot_id=123',
            method=urlfetch.POST,
            headers=message.GROUPME_API_HEADERS
        )

    @mock.patch('c3po.message.Message._generate_api_post_body')
    @mock.patch('google.appengine.api.urlfetch.fetch')
    def test_send_response_500(self, mock_urlfetch, mock_gen_api_post_body):
        mock_gen_api_post_body.return_value = 'text=sample&bot_id=123'
        mock_urlfetch.return_value.status_code = 202

        self.msg._send_response('sample')

        self.assertRaises(RuntimeError)


if __name__ == '__main__':
    unittest.main()

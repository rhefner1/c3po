import unittest

import mock
from google.appengine.api import urlfetch

from c3po import message

GROUP_ID = 'abc'
NAME = 'Billy'
TEXT = ''


class TestRegex(unittest.TestCase):
    def test_generate_regex(self):
        regex = 'hi'
        self.assertEqual(message.Message._generate_regex(regex),
                         r'(\s+)hi($|\s+|\?+|\.+|\!+)')


class TestGeneratePostBody(unittest.TestCase):
    def setUp(self):
        self.msg = message.Message(GROUP_ID, NAME, TEXT)

    @mock.patch('c3po.message.Message._get_bot_id')
    def test_generate_api_post_body(self, mock_get_bot_id):
        mock_get_bot_id.return_value = '123'

        actual_post_body = self.msg._generate_api_post_body('sample')
        expected_post_body = 'text=sample&bot_id=123'

        self.assertEqual(actual_post_body, expected_post_body)


class TestSendResponse(unittest.TestCase):
    def setUp(self):
        self.msg = message.Message(GROUP_ID, NAME, TEXT)

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

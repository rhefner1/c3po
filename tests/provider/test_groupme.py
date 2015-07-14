import unittest

import mock
from google.appengine.api import urlfetch

from c3po import message
from tests import fakes

GROUPME_API_ENDPOINT = 'https://api.groupme.com'
GROUPME_API_HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
GROUPME_API_PATH = '/v3/bots/post'
GROUPME_API_FULL = "%s%s" % (GROUPME_API_ENDPOINT, GROUPME_API_PATH)


class TestGeneratePostBody(unittest.TestCase):
    def setUp(self):
        settings_patcher = mock.patch('c3po.message.Message._get_settings')
        self.addCleanup(settings_patcher.stop)
        self.mock_settings = settings_patcher.start()
        self.mock_settings.return_value = fakes.FakeBaseResponseMgr()

        self.msg = message.Message(fakes.GROUP_ID, fakes.NAME, fakes.TEXT)

    def test_generate_api_post_body(self):
        actual_post_body = self.msg.provider._generate_api_post_body('sample')
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

        self.msg.provider._send_response('sample')

        mock_urlfetch.assert_called_with(
            url=GROUPME_API_ENDPOINT + GROUPME_API_PATH,
            payload='text=sample&bot_id=123',
            method=urlfetch.POST,
            headers=GROUPME_API_HEADERS
        )

    @mock.patch('c3po.message.Message._generate_api_post_body')
    @mock.patch('google.appengine.api.urlfetch.fetch')
    def test_send_response_500(self, mock_urlfetch, mock_gen_api_post_body):
        mock_gen_api_post_body.return_value = 'text=sample&bot_id=123'
        mock_urlfetch.return_value.status_code = 202

        self.msg.provider._send_response('sample')

        self.assertRaises(RuntimeError)

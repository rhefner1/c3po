import mock
import unittest

from c3po.message import Message

GROUP_ID = "abc"
NAME = "Billy"


class TestHello(unittest.TestCase):
    def setUp(self):
        self.msg = Message(GROUP_ID, NAME, "")

    @mock.patch('c3po.message.Message._send_response')
    def test_hello(self, mock_send_response):
        self.msg.text = "c3po hello"
        self.msg.process_message()

        mock_send_response.assert_called_with(
            "Greetings. I am C-3PO, human cyborg relations.")


if __name__ == '__main__':
    unittest.main()

import unittest

from c3po import message


class TestRegex(unittest.TestCase):
    def test_generate_regex(self):
        regex = 'hi'
        self.assertEqual(message.Message._generate_regex(regex),
                         r'(\s+)hi($|\s+|\?+|\.+|\!+)')


if __name__ == '__main__':
    unittest.main()

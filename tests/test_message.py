import unittest

from c3po.message import Message


class TestRegex(unittest.TestCase):
    def test_generate_regex(self):
        regex = "hi"
        self.assertEqual(Message._generate_regex(regex),
                         r'(\s+)hi($|\s+|\?+|\.+|\!+)')


if __name__ == '__main__':
    unittest.main()

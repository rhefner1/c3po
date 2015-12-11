import unittest
from datetime import datetime

import mock

from c3po import text_chunks
from c3po.tests import fakes


def _random_se(*args, **_):
    if args[0] == text_chunks.CHOOSE:
        return 'Hmm... I choose %s.'
    elif args[0] == ['cheddar', 'swiss', 'gouda']:
        return 'gouda'


class TestAddMention(unittest.TestCase):
    def setUp(self):
        send_patcher = mock.patch(
            'c3po.tests.fakes.FakeMessage.send_message')
        self.addCleanup(send_patcher.stop)
        self.mock_send = send_patcher.start()

        settings_patcher = mock.patch(
            'c3po.tests.fakes.FakeMessage._get_settings')
        self.addCleanup(settings_patcher.stop)
        self.mock_settings = settings_patcher.start()
        self.mock_settings.return_value = fakes.FakeBaseSettings()

        self.msg = fakes.FakeMessage(fakes.NAME, None, '', fakes.TIME_SENT)

    @mock.patch('c3po.tests.fakes.FakeMessage._add_mention')
    def test_add_mention(self, fake_add_mention):
        fake_add_mention.return_value = "%s: %s" % (fakes.NAME, 'pong')

        self.msg.text = 'c3po ping'
        self.msg.process_message()

        self.mock_send.assert_called_with('Billy: pong')


class TestBaseResponders(unittest.TestCase):
    def setUp(self):
        send_patcher = mock.patch(
            'c3po.tests.fakes.FakeMessage.send_message')
        self.addCleanup(send_patcher.stop)
        self.mock_send = send_patcher.start()

        settings_patcher = mock.patch(
            'c3po.tests.fakes.FakeMessage._get_settings')
        self.addCleanup(settings_patcher.stop)
        self.mock_settings = settings_patcher.start()
        self.mock_settings.return_value = fakes.FakeBaseSettings()

        self.msg = fakes.FakeMessage(fakes.NAME, None, '', fakes.TIME_SENT)

    def test_choose_0(self):
        self.msg.text = 'c3po choose cheddar'
        self.msg.process_message()

        self.mock_send.assert_called_with(
            'Whoops, you only gave me one item to choose from (cheddar).')

    @mock.patch('random.choice')
    def test_choose_1(self, mock_random):
        mock_random.side_effect = _random_se

        self.msg.text = 'c3po choose cheddar, swiss, gouda'
        self.msg.process_message()

        self.mock_send.assert_called_with(
            'Hmm... I choose gouda.')

    @mock.patch('random.choice')
    def test_choose_2(self, mock_random):
        mock_random.side_effect = _random_se

        self.msg.text = 'c3po choose cheddar, swiss or gouda'
        self.msg.process_message()

        self.mock_send.assert_called_with(
            'Hmm... I choose gouda.')

    @mock.patch('random.choice')
    def test_choose_3(self, mock_random):
        mock_random.side_effect = _random_se

        self.msg.text = 'c3po choose cheddar, swiss, or gouda'
        self.msg.process_message()

        self.mock_send.assert_called_with(
            'Hmm... I choose gouda.')

    @mock.patch('random.choice')
    def test_choose_4(self, mock_random):
        mock_random.side_effect = _random_se

        self.msg.text = 'c3po choose between cheddar, swiss and gouda'
        self.msg.process_message()

        self.mock_send.assert_called_with(
            'Hmm... I choose gouda.')

    @mock.patch('random.choice')
    def test_choose_5(self, mock_random):
        mock_random.side_effect = _random_se

        self.msg.text = 'c3po what cheese? Choose cheddar, swiss or gouda'
        self.msg.process_message()

        self.mock_send.assert_called_with(
            'Hmm... I choose gouda.')

    def test_creator(self):
        self.msg.text = 'c3po who created you?'
        self.msg.process_message()

        self.mock_send.assert_called_with(
            'My friend Hef (and some of his friends) brought me to life!')

    def test_hello(self):
        self.msg.text = 'c3po hello'
        self.msg.process_message()

        self.mock_send.assert_called_with(
            'Greetings. I am C-3PO, human-cyborg relations.')

    @mock.patch('random.choice')
    def test_motivate(self, mock_random):
        mock_random.return_value = "You're awesome, %s!"

        self.msg.text = 'c3po motivate Henry'
        self.msg.process_message()

        self.mock_send.assert_called_with(
            "You're awesome, Henry!")

    def test_negative(self):
        self.msg.text = 'this is only a test'
        self.msg.process_message()

        self.assertFalse(self.mock_send.called)

    def test_ping(self):
        self.msg.text = 'c3po ping'
        self.msg.process_message()

        self.mock_send.assert_called_with('pong')

    def test_tell_to(self):
        self.msg.text = 'c3po tell Joey to pick up the trash'
        self.msg.process_message()

        self.mock_send.assert_called_with('Joey, pick up the trash!')

    def test_tell_should(self):
        self.msg.text = 'c3po tell Joey that he should behave'
        self.msg.process_message()

        self.mock_send.assert_called_with('Joey, you should behave!')

    @mock.patch('random.choice')
    def test_thanks(self, mock_random):
        mock_random.return_value = "You're welcome"

        self.msg.text = 'c3po thanks!'
        self.msg.process_message()

        self.mock_send.assert_called_with(
            "You're welcome!")

    @mock.patch('c3po.db.stored_message.StoredMessage.query')
    @mock.patch('c3po.persona.util.random_date')
    @mock.patch('google.appengine.api.memcache.delete')
    @mock.patch('google.appengine.api.memcache.get')
    def test_throwback_no_picture(self, mock_memcache_get, mock_memcache_del,
                                  mock_rnd_date, mock_query):
        mock_memcache_get.return_value = None
        mock_memcache_del.return_value = True
        mock_rnd_date.return_value = datetime(2015, 9, 19)
        mock_query.return_value = fakes.FakeNDBQuery()

        self.msg.text = 'c3po throwback'
        self.msg.process_message()

        self.mock_send.assert_called_with(
            'Throwback! On 09/20/2015, Billy said, "hi".')

    @mock.patch('c3po.db.stored_message.StoredMessage.query')
    @mock.patch('c3po.persona.util.random_date')
    @mock.patch('google.appengine.api.memcache.delete')
    @mock.patch('google.appengine.api.memcache.get')
    def test_throwback_picture(self, mock_memcache_get, mock_memcache_del,
                               mock_rnd_date, mock_query):
        mock_memcache_get.return_value = None
        mock_memcache_del.return_value = True
        mock_rnd_date.return_value = datetime(2015, 9, 19)
        mock_query.return_value = fakes.FakeNDBQuery(picture=True)

        self.msg.text = 'c3po throwback'
        self.msg.process_message()

        self.mock_send.assert_called_with(
            'Throwback! On 09/20/2015, Billy posted this photo saying, "hi".')

    @mock.patch('google.appengine.api.urlfetch.fetch')
    def test_weather(self, mock_fetch):
        mock_forecast = mock.Mock()
        mock_forecast.content = fakes.WEATHER_JSON
        mock_fetch.return_value = mock_forecast

        self.msg.text = 'c3po weather'
        self.msg.process_message()

        self.mock_send.assert_called_with("It's currently mostly cloudy with a "
                                          "temperature of 84.25 degrees (feels "
                                          "like 92.7). I'm predicting rain "
                                          "tonight and tomorrow afternoon.")

    def test_what_can_you_do(self):
        self.msg.text = 'c3po what can you do?'
        self.msg.process_message()

        response = "Check out this site: " \
                   "https://github.com/rhefner1/c3po/blob/master/README.md"
        self.mock_send.assert_called_with(response)

    def test_wolf(self):
        self.msg.text = 'c3po wolf'
        self.msg.process_message()

        self.mock_send.assert_called_with('PACK!')


if __name__ == '__main__':
    unittest.main()

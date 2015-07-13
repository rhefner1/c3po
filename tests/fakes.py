import mock

from c3po.response_mgr import base
from c3po.response_mgr import beasts

BOT_ID = '123'
GROUP_ID = 'abc'
NAME = 'Billy'
TEXT = ''


class FakeBaseResponseMgr(mock.Mock):
    def __init__(self):
        super(FakeBaseResponseMgr, self).__init__()
        self.groupme_conf = mock.Mock()
        self.groupme_conf.bot_id = BOT_ID

    @staticmethod
    def get_response_mgr():
        return base.BaseResponseManager()


class FakeBeastsResponseMgr(mock.Mock):
    def __init__(self):
        super(FakeBeastsResponseMgr, self).__init__()
        self.groupme_conf.bot_id = BOT_ID

    @staticmethod
    def get_response_mgr():
        return beasts.BeastsResponseManager()

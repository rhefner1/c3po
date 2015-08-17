"""Responder specifically for small groups."""

from c3po.response_mgr import base


class SmallGroupResponseManager(base.BaseResponseManager):
    """Adds specific small group functionality to BaseResponder."""

    def __init__(self):
        super(SmallGroupResponseManager, self).__init__()

        self.mentioned_map.update({
        })

        self.not_mentioned_map.update({
        })

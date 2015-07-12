"""Responder specifically for for Beasts of the East."""

from c3po.response_mgr import base


class BeastsResponseManager(base.BaseResponseManager):
    """Adds specific Beasts of the East functionality to BaseResponder."""

    def __init__(self):
        super(BeastsResponseManager, self).__init__()

        self.mentioned_map.update({
        })

        self.not_mentioned_map.update({
        })

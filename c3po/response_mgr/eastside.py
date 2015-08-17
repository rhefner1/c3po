"""Responder specifically for for Best Eastside Study."""

from c3po.response_mgr import small_group


class EastsideResponseManager(small_group.SmallGroupResponseManager):
    """Adds specific Best Eastside Study functionality to BaseResponder."""

    def __init__(self):
        super(EastsideResponseManager, self).__init__()

        self.mentioned_map.update({
        })

        self.not_mentioned_map.update({
        })

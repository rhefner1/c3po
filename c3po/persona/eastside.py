"""Responder specifically for for Best Eastside Study."""

from c3po.persona import small_group


class EastsidePersona(small_group.SmallGroupPersona):
    """Adds specific Best Eastside Study functionality to BaseResponder."""

    def __init__(self):
        super(EastsidePersona, self).__init__()

        self.mentioned_map.update({
        })

        self.not_mentioned_map.update({
        })

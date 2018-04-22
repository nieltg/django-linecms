from django.db import models
from django.utils.translation import gettext as _

from linecms.apps.reply.models import AbstractAction


class ReplyAction(AbstractAction):

    def handle_event(self, event, line_bot_api):
        bot_obj = self.get_line_bot_object()
        line_bot_api.reply_message(event.reply_token, bot_obj)


class Postback(ReplyAction):
    """Postback message."""

    data = models.TextField(_("Postback data"), max_length=300)

    def __str__(self):
        return self.data


class Message(ReplyAction):
    """Reply message."""

    text = models.CharField(_("Keyword text"), max_length=255)

    def __str__(self):
        return self.text


class InvalidMessage(ReplyAction):
    """Invalid message."""

from django.db import models
from django.utils.translation import gettext as _

from linecms.apps.reply.models import Text


class AbstractAction(models.Model):
    """Reply action."""

    class Meta:
        abstract = True

    REPLY_TEXT = 1
    REPLY_CHOICES = ((REPLY_TEXT, _("Text")), )

    reply = models.IntegerField(choices=REPLY_CHOICES)
    reply_text = models.ForeignKey(Text, on_delete=models.PROTECT)

    def handle_event(self, event, line_bot_api):
        providers = {
            self.REPLY_TEXT: self.reply_text,
        }

        provider = providers[self.reply_text]
        line_bot_api.reply_message(event.reply_token,
                                   provider.get_line_bot_object())


class Postback(AbstractAction):
    """Postback message."""

    data = models.TextField(max_length=300)


class Message(AbstractAction):
    """Reply message."""

    text = models.CharField(max_length=255)

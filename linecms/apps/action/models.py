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

        provider = providers[self.reply]
        line_bot_api.reply_message(event.reply_token,
                                   provider.get_line_bot_object())


class Postback(AbstractAction):
    """Postback message."""

    data = models.TextField(_("Postback data"), max_length=300)

    def __str__(self):
        return self.data


class Message(AbstractAction):
    """Reply message."""

    text = models.CharField(_("Keyword text"), max_length=255)

    def __str__(self):
        return self.text


class InvalidMessage(AbstractAction):
    """Invalid message."""
